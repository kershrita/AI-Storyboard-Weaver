from IPython.display import display, Markdown, Image
import matplotlib.pyplot as plt
import os

def visualize_mood(mood_counts: dict, story_output_dir: str):
    """Create and display a mood visualization in the story-specific folder."""
    if not mood_counts:
        display(Markdown("⚠️ No mood data available"))
        return
    moods = list(mood_counts.keys())
    counts = list(mood_counts.values())
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    color_map = {
        "joyful": "#FFD700", "romantic": "#FF69B4", "tense": "#8B0000",
        "suspenseful": "#4B0082", "dark": "#000000", "hopeful": "#32CD32",
        "chaotic": "#FF4500"
    }
    colors = [color_map.get(mood, "#888888") for mood in moods]
    bars = ax.bar(moods, counts, color=colors, edgecolor='white', linewidth=1)
    ax.set_title("Scene Mood Distribution", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("Mood Type", fontsize=12)
    ax.set_ylabel("Number of Scenes", fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.spines[['top', 'right']].set_visible(False)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom',
                fontsize=11, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=11)
    plt.tight_layout()
    
    # Ensure story-specific output directory exists
    os.makedirs(story_output_dir, exist_ok=True)
    
    # Save chart in story-specific folder
    chart_filename = os.path.join(story_output_dir, "mood_distribution.png")
    plt.savefig(chart_filename, bbox_inches='tight')
    plt.close()
    display(Markdown(f"![Mood Distribution Chart]({chart_filename})"))

def display_storyboard(storyboard: dict, output_dir: str):
    """Render the storyboard in Markdown format with images."""
    display(Markdown(f"## 🎬 {storyboard.get('title', 'Untitled Storyboard')}"))
    for scene in storyboard.get("scenes", []):
        mood = scene.get("mood", "neutral").lower()
        image_filename = scene.get("image_filename")
        if image_filename and os.path.exists(os.path.join(output_dir, image_filename)):
            # Display image using IPython.display.Image
            image_path = os.path.join(output_dir, image_filename)
            display(Markdown(f"**Image for Scene {scene.get('scene_number', 1)}:**"))
            display(Image(filename=image_path))
        else:
            display(Markdown("⚠️ No image available"))
        display(Markdown(f"""
### 🎥 Scene {scene.get('scene_number', 1)} ({mood.capitalize()})

**Visual Description:**  
{scene.get('description', 'No description available')}

**Dialogue:**  
"{scene.get('dialogue', '...')}"
"""))