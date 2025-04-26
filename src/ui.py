import os
from .agent import StoryboardAgent
from .visualization import display_storyboard, visualize_mood
from .config import CONFIG
from .utils import sanitize_filename

def create_ui():
    """Create a console-based UI for the Storyboard Weaver."""
    print("=== 🎬 AI Storyboard Weaver ===")
    print("✍️ Enter your story parameters below:")
    
    # Get plot input
    plot = input("Describe your story (e.g., 'A detective discovers aliens in 1920s Chicago'): ").strip()
    if not plot:
        print("❌ Error: Plot cannot be empty.")
        return
    
    # Get number of scenes
    while True:
        try:
            num_scenes = int(input(f"Number of scenes (1-{CONFIG['max_scenes']}): ").strip())
            if 1 <= num_scenes <= CONFIG["max_scenes"]:
                break
            print(f"❌ Error: Number of scenes must be between 1 and {CONFIG['max_scenes']}.")
        except ValueError:
            print("❌ Error: Please enter a valid number.")
    
    # Get visual style with numbered selection
    style_options = ['Cinematic', 'Documentary', 'Anime', 'Noir', 'Experimental']
    print("Available visual styles:")
    for i, style in enumerate(style_options, 1):
        print(f"{i}. {style}")
    while True:
        try:
            style_choice = int(input("Select visual style (1-5): ").strip())
            if 1 <= style_choice <= len(style_options):
                style = style_options[style_choice - 1]
                break
            print(f"❌ Error: Please enter a number between 1 and {len(style_options)}.")
        except ValueError:
            print("❌ Error: Please enter a valid number.")
    print(f"Selected style: {style}")
    
    # Create story-specific output folder
    story_folder_name = sanitize_filename(plot)
    story_output_dir = os.path.join(CONFIG["output_dir"], story_folder_name)
    print(f"Creating output directory: {story_output_dir}")
    os.makedirs(story_output_dir, exist_ok=True)
    
    # Set knowledge base path for this story
    knowledge_base_path = os.path.join(story_output_dir, CONFIG["knowledge_base"])
    
    # Initialize agent with story-specific knowledge base
    agent = StoryboardAgent(
        endpoint=os.environ["MODEL_ENDPOINT"],
        api_key=os.environ["MODEL_API_KEY"],
        model_name=os.environ["MODEL_NAME"],
        knowledge_base_path=knowledge_base_path
    )
    
    # Generate and display storyboard
    try:
        print("\n🔍 Analyzing your plot...")
        storyboard = agent.execute_function("generate_storyboard", plot=plot, num_scenes=num_scenes)
        if not storyboard:
            raise ValueError("Storyboard generation failed.")
        
        print("📊 Analyzing story structure...")
        mood_analysis = agent.execute_function("analyze_mood", storyboard=storyboard)
        
        print(f"\n🎬 {storyboard.get('title', 'Your Storyboard')}")
        display_storyboard(storyboard)
        visualize_mood(mood_analysis, story_output_dir)
        
        # Save storyboard in story-specific folder
        filename = os.path.join(story_output_dir, f"storyboard_{story_folder_name}.json")
        print(f"Attempting to save storyboard to: {filename}")
        if agent.execute_function("save_storyboard", storyboard=storyboard, filename=filename):
            print(f"💾 Storyboard saved to {filename}")
        else:
            print(f"❌ Failed to save storyboard to {filename}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Please try again with different parameters.")