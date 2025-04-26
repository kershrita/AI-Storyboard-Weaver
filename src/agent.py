import json
import re
import requests
import os
from typing import Dict, List
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
from PIL import Image, ImageDraw, ImageFont
from IPython.display import display, Markdown
from .config import CONFIG
from .utils import init_knowledge_base

class StoryboardAgent:
    """Main agent class for storyboard generation with DeepSeek API, RAG, and DALL-E 3 images."""

    def __init__(self, endpoint: str, api_key: str, model_name: str, knowledge_base_path: str = None):
        try:
            self.embedding_model = SentenceTransformer(CONFIG["embedding_model"])
        except Exception as e:
            print(f"⚠️ Could not load embedding model: {e}")
            self.embedding_model = None
        
        # Initialize DeepSeek client
        self.client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        self.model_name = model_name
        
        # Initialize Azure OpenAI client for DALL-E 3
        self.image_client = AzureOpenAI(
            api_version="2024-02-01",
            azure_endpoint=os.environ["DALLE_MODEL_ENDPOINT"],
            api_key=os.environ["DALLE_MODEL_API_KEY"]
        )
        
        self.knowledge_base_path = knowledge_base_path or CONFIG["knowledge_base"]
        self.available_functions = {
            "generate_storyboard": self.generate_storyboard,
            "analyze_mood": self.analyze_mood,
            "save_storyboard": self.save_storyboard
        }
        init_knowledge_base(self.knowledge_base_path)

    def execute_function(self, function_name: str, **kwargs):
        """Execute a registered function with error handling."""
        if function_name not in self.available_functions:
            raise ValueError(f"Unknown function: {function_name}")
        try:
            display(Markdown(f"🔧 Executing {function_name.replace('_', ' ')}..."))
            return self.available_functions[function_name](**kwargs)
        except Exception as e:
            display(Markdown(f"⚠️ **Error in {function_name}:** {str(e)}"))
            return None

    def generate_storyboard(self, plot: str, num_scenes: int = 3, visual_style: str = "Cinematic") -> Dict:
        """Generate a storyboard using DeepSeek API with RAG context and DALL-E 3 images."""
        similar_plots = self.retrieve_similar_plots(plot)
        rag_context = "\nSimilar plots:\n" + "\n".join(
            [f"- {p['plot']}" for p in similar_plots[:2]]) if similar_plots else ""
        prompt = self._build_prompt(plot, num_scenes, rag_context, visual_style)
        storyboard = self._call_generation_api(prompt)
        if storyboard:
            # Generate images for each scene
            for scene in storyboard.get("scenes", []):
                image_filename = self._generate_scene_image(scene, plot, visual_style, os.path.dirname(self.knowledge_base_path))
                if image_filename:
                    scene["image_filename"] = image_filename
            self._update_knowledge_base(plot, storyboard)
        return storyboard

    def _build_prompt(self, plot: str, num_scenes: int, rag_context: str = "", visual_style: str = "Cinematic") -> str:
        """Construct the generation prompt for DeepSeek API."""
        genre = self.detect_genre(plot)
        wiki_context = self.fetch_wikipedia_film_data(genre)
        script_example = self.fetch_script_data(genre)
        return f"""Generate a film storyboard in JSON format based on: "{plot}"
Format Requirements:
- Strictly valid JSON output
- Title reflecting plot essence
- {num_scenes} scenes with:
  • scene_number (1-{num_scenes})
  • vivid description
  • natural dialogue
  • mood from: {CONFIG['moods']}
Visual Style: {visual_style}
Genre Context:
{wiki_context[:CONFIG['context_length']]}
{rag_context}
Example Dialogue:
{script_example}
Output:"""

    def _sanitize_prompt(self, prompt: str) -> str:
        """Sanitize the prompt to avoid content policy violations."""
        # Replace sensitive terms
        replacements = {
            r'\bmurder\b': 'mysterious event',
            r'\bkill\b': 'confront',
            r'\bknife\b': 'object',
            r'\bblood\b': 'shadow',
            r'\bviolent\b': 'tense',
            r'\bdeath\b': 'disappearance',
            r'\bwet dress\b': 'rain-soaked clothing',
            r'\bdress adhering to her form\b': 'clothing damp from rain'
        }
        sanitized = prompt.lower()
        for pattern, replacement in replacements.items():
            sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE)
        return sanitized

    def _create_placeholder_image(self, scene_number: int, output_dir: str) -> str:
        """Create a placeholder PNG for failed image generation."""
        try:
            image = Image.new('RGB', (1024, 1024), color='gray')
            draw = ImageDraw.Draw(image)
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            text = f"Scene {scene_number}\nImage Not Generated"
            draw.text((50, 450), text, fill='white', font=font)
            placeholder_filename = os.path.join(output_dir, f"placeholder_scene_{scene_number}.png")
            image.save(placeholder_filename)
            print(f"Created placeholder image: {placeholder_filename}")
            return os.path.basename(placeholder_filename)
        except Exception as e:
            print(f"Error creating placeholder image for scene {scene_number}: {str(e)}")
            return None

    def _generate_scene_image(self, scene: Dict, plot: str, visual_style: str, output_dir: str) -> str:
        """Generate an image for a scene using DALL-E 3 and save it."""
        scene_number = scene.get("scene_number", 1)
        description = scene.get("description", "A generic scene")
        mood = scene.get("mood", "neutral")
        max_retries = 2
        
        for attempt in range(max_retries):
            try:
                # Build and sanitize DALL-E 3 prompt
                raw_prompt = f"""
A {visual_style.lower()} style scene from a film about "{plot}". {description}. 
The mood is {mood}, reflected in lighting, colors, and atmosphere. 
Maintain consistent {visual_style.lower()} art style, color palette, and visual tone across all scenes.
Highly detailed, vivid, and cinematic composition.
"""
                image_prompt = self._sanitize_prompt(raw_prompt)
                print(f"Generating image for scene {scene_number} with prompt: {image_prompt[:100]}...")
                
                # Call DALL-E 3 API
                result = self.image_client.images.generate(
                    model="scene-maker",
                    prompt=image_prompt,
                    n=1,
                    size="1024x1024"
                )
                
                # Get image URL and download
                image_url = json.loads(result.model_dump_json())['data'][0]['url']
                image_filename = os.path.join(output_dir, f"scene_{scene_number}.png")
                
                # Download and save image
                response = requests.get(image_url)
                response.raise_for_status()
                with open(image_filename, 'wb') as f:
                    f.write(response.content)
                
                print(f"Saved image to: {image_filename}")
                return os.path.basename(image_filename)
            
            except Exception as e:
                if 'content_policy_violation' in str(e) and attempt < max_retries - 1:
                    # Retry with a safer fallback prompt
                    print(f"Content policy violation for scene {scene_number}, retrying with safer prompt...")
                    image_prompt = f"""
A {visual_style.lower()} style scene depicting a {mood} moment in a film. 
A generic setting with characters in appropriate attire, focusing on atmosphere and lighting. 
Maintain consistent {visual_style.lower()} art style and color palette.
Highly detailed and cinematic.
"""
                    continue
                print(f"Error generating image for scene {scene_number}: {str(e)}")
                display(Markdown(f"⚠️ **Error generating image for scene {scene_number}:** {str(e)}"))
                # Use placeholder image on final failure
                return self._create_placeholder_image(scene_number, output_dir)
        return self._create_placeholder_image(scene_number, output_dir)

    def _call_generation_api(self, prompt: str) -> Dict:
        """Call DeepSeek API to generate a storyboard."""
        system_prompt = "You are a precise and creative assistant that generates valid JSON output based on the provided instructions."
        for attempt in range(CONFIG["max_retries"]):
            try:
                response = self.client.complete(
                    messages=[
                        SystemMessage(content=system_prompt),
                        UserMessage(content=prompt)
                    ],
                    max_tokens=1024,
                    model=self.model_name
                )
                raw_output = response.choices[0].message.content
                json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                if json_match:
                    storyboard = json.loads(json_match.group(0))
                    if self.validate_storyboard(storyboard):
                        return storyboard
            except Exception as e:
                if attempt == CONFIG["max_retries"] - 1:
                    return self._create_fallback_storyboard(prompt.split('"')[1] if '"' in prompt else prompt)
        return self._create_fallback_storyboard(prompt.split('"')[1] if '"' in prompt else prompt)

    def _create_fallback_storyboard(self, plot: str) -> Dict:
        """Create a fallback storyboard if API fails."""
        return {
            "title": f"Untitled {plot}",
            "scenes": [{
                "scene_number": i+1,
                "description": f"Scene {i+1} of {plot}",
                "dialogue": "...",
                "mood": "neutral"
            } for i in range(3)]
        }

    def detect_genre(self, plot: str) -> str:
        """Detect film genre from plot keywords."""
        plot_lower = plot.lower()
        genre_map = [
            (["heist", "robbery", "steal"], "heist"),
            (["sci-fi", "futuristic", "space", "alien"], "sci-fi"),
            (["romance", "love", "relationship"], "romance"),
            (["thriller", "suspense", "mystery"], "thriller")
        ]
        for keywords, genre in genre_map:
            if any(word in plot_lower for word in keywords):
                return genre
        return CONFIG["default_genre"]

    def fetch_wikipedia_film_data(self, genre: str) -> str:
        """Fetch film context from Wikipedia."""
        url = f"https://en.wikipedia.org/wiki/{genre}_film"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.find('div', {'id': 'mw-content-text'})
            paragraphs = content.find_all('p')[:3] if content else []
            return " ".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])[:CONFIG["context_length"]]
        except Exception as e:
            display(Markdown(f"⚠️ **Wikipedia Unavailable:** Using generic context. (Error: {str(e)})"))
            return f"Standard {genre} film context."

    def fetch_script_data(self, genre: str) -> str:
        """Fetch script snippets from a mock database."""
        mock_scripts = {
            "heist": "INT. BANK VAULT - NIGHT\nThe crew works silently until alarms blare.\n\"We're made!\" shouts the leader.",
            "sci-fi": "EXT. SPACE STATION\nThe captain watches Earth from the viewport.\n\"Initiate hyperdrive,\" she orders.",
            "romance": "EXT. PARIS CAFE - DAY\nThey share coffee as rain falls gently.\n\"I've waited my whole life for this,\" he whispers.",
            "thriller": "INT. ABANDONED HOUSE - NIGHT\nA floorboard creaks. She holds her breath.\n\"I know you're here,\" calls the killer."
        }
        return mock_scripts.get(genre.lower(), "Sample script dialogue.")

    def analyze_mood(self, storyboard: Dict) -> Dict:
        """Analyze mood distribution in the storyboard."""
        moods = [scene.get("mood", "unknown") for scene in storyboard.get("scenes", [])]
        return {mood: moods.count(mood) for mood in set(moods)} if moods else {}

    def validate_storyboard(self, storyboard: Dict) -> bool:
        """Validate the storyboard structure."""
        if not isinstance(storyboard, dict) or "title" not in storyboard or "scenes" not in storyboard:
            return False
        if not isinstance(storyboard["scenes"], list) or not storyboard["scenes"]:
            return False
        for scene in storyboard["scenes"]:
            if not all(key in scene for key in ["scene_number", "description", "dialogue", "mood"]):
                return False
            if scene["mood"] not in CONFIG["moods"]:
                return False
        return True

    def save_storyboard(self, storyboard: Dict, filename: str) -> bool:
        """Save the storyboard to a JSON file."""
        try:
            print(f"Saving storyboard to: {filename}")
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(storyboard, f, indent=2)
            print(f"Successfully saved storyboard to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving storyboard to {filename}: {str(e)}")
            display(Markdown(f"⚠️ **Error saving storyboard:** {str(e)}"))
            return False

    def retrieve_similar_plots(self, plot: str, top_k: int = 3) -> List[Dict]:
        """Retrieve similar plots using vector similarity."""
        if not self.embedding_model:
            return []
        with open(self.knowledge_base_path, "r") as f:
            kb = json.load(f)
        if not kb["plots"]:
            return []
        plot_embedding = self.embedding_model.encode(plot)
        similarities = []
        for stored_plot in kb["plots"]:
            stored_embedding = np.array(stored_plot["embedding"])
            similarity = cosine_similarity([plot_embedding], [stored_embedding])[0][0]
            similarities.append((stored_plot, similarity))
        return [plot for plot, sim in sorted(similarities, key=lambda x: x[1], reverse=True) if sim > CONFIG["rag_threshold"]][:top_k]

    def _update_knowledge_base(self, plot: str, storyboard: Dict):
        """Update the knowledge base with a new plot and storyboard."""
        try:
            with open(self.knowledge_base_path, "r") as f:
                kb = json.load(f)
            plot_embedding = self.embedding_model.encode(plot).tolist() if self.embedding_model else []
            kb["plots"].append({
                "plot": plot,
                "storyboard": storyboard,
                "embedding": plot_embedding,
                "timestamp": str(datetime.now())
            })
            with open(self.knowledge_base_path, "w") as f:
                json.dump(kb, f, indent=2)
        except Exception as e:
            display(Markdown(f"⚠️ Could not update knowledge base: {e}"))