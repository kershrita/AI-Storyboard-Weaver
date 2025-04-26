# AI Storyboard Weaver

The **AI Storyboard Weaver** is a Python-based tool that generates film storyboards from user-provided story plots. It leverages the DeepSeek LLM to create detailed scene descriptions and dialogues, and the DALL-E 3 API to generate corresponding images for each scene. The tool features a console-based UI, mood analysis with visualizations, and organizes outputs in story-specific folders. It includes prompt sanitization to comply with Azure’s content policies and displays images in Jupyter Notebook.

## Features
- **Storyboard Generation**: Creates JSON storyboards with scene descriptions, dialogues, and moods using DeepSeek LLM.
- **Image Generation**: Generates images for each scene using DALL-E 3, with support for visual styles (Cinematic, Documentary, Anime, Noir, Experimental).
- **Mood Analysis**: Visualizes scene mood distribution as a bar chart.
- **Content Policy Compliance**: Sanitizes prompts to avoid Azure OpenAI content filter violations.
- **Output Organization**: Saves storyboards, mood charts, and images in story-specific folders.
- **Jupyter Integration**: Displays storyboards and images in Jupyter Notebook using `IPython.display`.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **Jupyter Notebook**: For running `main.ipynb`.
- **Azure API Credentials**:
  - DeepSeek API (for storyboard generation).
  - Azure OpenAI DALL-E 3 API (for image generation).
- **Git**: For cloning the repository.
- **Internet Access**: For API calls and dependency installation.

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/ai-storyboard-weaver.git
   cd ai-storyboard-weaver
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   Install the required Python packages listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the project root with your Azure API credentials:
   ```
   LLM_MODEL_ENDPOINT=your-deepseek-endpoint > .env
   LLM_MODEL_API_KEY=your-deepseek-api-key >> .env
   LLM_MODEL_NAME=your-deepseek-model-name >> .env
   DALLE_MODEL_ENDPOINT=your-dalle-endpoint >> .env
   DALLE_MODEL_API_KEY=your-dalle-api-key >> .env
   ```
   Replace `your-deepseek-endpoint`, `your-deepseek-api-key`, `your-deepseek-model-name`, `your-dalle-endpoint`, and `your-dalle-api-key` with your actual DeepSeek and DALL-E 3 API credentials. Obtain these from your Azure account or API provider.

5. **Verify Setup**:
   Ensure the `.env` file is loaded and dependencies are installed:
   ```python
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.environ['MODEL_ENDPOINT'])"
   ```

## Usage

### Running the Project
The project can be run via Jupyter Notebook (`main.ipynb`) or as a standalone script (`main.py`).

#### Option 1: Jupyter Notebook
1. Start Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Open `main.ipynb` in the browser.
3. Execute the cell to start the console-based UI.
4. Follow the prompts:
   - **Story Plot**: Enter a plot (e.g., "A detective investigates a mysterious incident in a rainy city").
   - **Number of Scenes**: Enter 1–5 scenes.
   - **Visual Style**: Select a style (1–5 for Cinematic, Documentary, Anime, Noir, Experimental).

#### Option 2: Command Line
1. Run the script:
   ```bash
   python main.py
   ```
2. Follow the same prompts as above.

### Example Input
```
=== 🎬 AI Storyboard Weaver ===
✍️ Enter your story parameters below:
Describe your story (e.g., 'A detective discovers aliens in 1920s Chicago'): A detective investigates a mysterious incident in a rainy city
Number of scenes (1-5): 3
Available visual styles:
1. Cinematic
2. Documentary
3. Anime
4. Noir
5. Experimental
Select visual style (1-5): 1
```

### Outputs
The project generates outputs in a story-specific folder (e.g., `outputs/A_detective_investigates_a_mysterious_incident_in_a_rainy_city/`):
- `knowledge_base.json`: Stores plot history and embeddings.
- `storyboard_<plot>.json`: Storyboard with scenes, descriptions, dialogues, moods, and image filenames.
- `mood_distribution.png`: Bar chart of scene moods.
- `scene_<number>.png`: DALL-E 3-generated images for each scene.
- `placeholder_scene_<number>.png`: Placeholder images for scenes where image generation fails (e.g., due to content policy violations).

Example `storyboard_<plot>.json`:
```json
{
  "title": "The Rainy City Mystery",
  "scenes": [
    {
      "scene_number": 1,
      "description": "A rainy alleyway with a detective examining a clue...",
      "dialogue": "This case just got a lot darker...",
      "mood": "tense",
      "image_filename": "scene_1.png"
    },
    ...
  ]
}
```

In Jupyter Notebook, the storyboard and images are displayed with embedded images for each scene.

## Project Structure
```
ai_storyboard_weaver/
├── src/
│   ├── __init__.py
│   ├── agent.py          # Core logic for storyboard and image generation
│   ├── visualization.py  # Mood visualization and storyboard display
│   ├── ui.py             # Console-based UI
│   ├── config.py         # Configuration settings
│   ├── utils.py          # Utility functions
├── outputs/
│   ├── <story_folder>/
│   │   ├── knowledge_base.json
│   │   ├── storyboard_<plot>.json
│   │   ├── mood_distribution.png
│   │   ├── scene_1.png
│   │   ├── placeholder_scene_2.png
│   │   ├── ...
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in version control)
├── main.ipynb            # Jupyter Notebook interface
├── main.py               # Command-line interface
├── README.md             # This file
```

## Troubleshooting

### Images Not Displaying in Jupyter Notebook
- **Symptoms**: Images (e.g., `scene_1.png`) don’t appear in the notebook output.
- **Solution**:
  - Verify images exist in `outputs/<story_folder>/`:
    ```bash
    ls outputs/<story_folder>  # Linux/Mac
    dir outputs\<story_folder>  # Windows
    ```
  - Check the notebook’s working directory:
    ```python
    import os
    print(os.getcwd())
    ```
    Ensure it’s the project root. If not, set it:
    ```python
    os.chdir('/path/to/ai-storyboard-weaver')
    ```
  - Test image display:
    ```python
    from IPython.display import Image
    display(Image(filename='outputs/<story_folder>/scene_1.png'))
    ```

### Content Policy Violations
- **Symptoms**: Errors like `Error generating image for scene X: Error code: 400 - {'error': {'code': 'content_policy_violation'...}}`.
- **Solution**:
  - The project sanitizes prompts to avoid terms like "murder" or "knife." Use less sensitive plots (e.g., "A detective investigates a theft").
  - Check console output for specific filters (e.g., `violence`, `sexual`) and adjust the plot or scene descriptions.
  - Placeholder images (`placeholder_scene_X.png`) are generated for failed scenes.

### TensorFlow Warnings
- **Symptoms**: Warnings from TensorFlow during execution.
- **Solution**:
  - The project suppresses these with `os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'`.
  - If warnings persist, reinstall `tf-keras`:
    ```bash
    pip install tf-keras==2.17.0 --force-reinstall
    ```

### API Errors
- **Symptoms**: Errors related to DeepSeek or DALL-E 3 API calls.
- **Solution**:
  - Verify `.env` credentials:
    ```python
    python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.environ['DALLE_API_KEY'])"
    ```
  - Test DALL-E 3 API:
    ```python
    from openai import AzureOpenAI
    import os
    client = AzureOpenAI(
        api_version="2024-02-01",
        azure_endpoint=os.environ["DALLE_ENDPOINT"],
        api_key=os.environ["DALLE_API_KEY"]
    )
    result = client.images.generate(model="scene-maker", prompt="A rainy city street", n=1, size="1024x1024")
    print(json.loads(result.model_dump_json())['data'][0]['url'])
    ```
  - Ensure API quotas are not exceeded.

## Notes
- **Content Filters**: Azure OpenAI’s DALL-E 3 has strict filters for violence, sexual content, and profanity. Use neutral plots to minimize violations.
- **Placeholder Images**: Scenes failing image generation (e.g., due to content policies) use placeholder PNGs created with PIL.
- **Performance**: Image generation takes a few seconds per scene. Ensure sufficient API quota.
- **Environment**: Tested with Python 3.8+ on Windows, Linux, and Mac. Use Anaconda or a virtual environment for dependency management.
- **Jupyter**: Ensure `main.ipynb` is run in a Jupyter environment with `ipython` and `matplotlib` installed.