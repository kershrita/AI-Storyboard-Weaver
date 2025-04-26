from IPython.display import display, Markdown
import matplotlib.pyplot as plt

def visualize_mood(mood_counts: dict):
    """Create and display a mood visualization."""
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
    chart_filename = "mood_distribution.png"
    plt.savefig(chart_filename, bbox_inches='tight')
    plt.close()
    display(Markdown(f"![Mood Distribution Chart]({chart_filename})"))

def display_storyboard(storyboard: dict):
    """Render the storyboard in Markdown format."""
    display(Markdown(f"## 🎬 {storyboard.get('title', 'Untitled Storyboard')}"))
    for scene in storyboard.get("scenes", []):
        mood = scene.get("mood", "neutral").lower()
        display(Markdown(f"""
### 🎥 Scene {scene.get('scene_number', 1)} ({mood.capitalize()})

**Visual Description:**  
{scene.get('description', 'No description available')}

**Dialogue:**  
"{scene.get('dialogue', '...')}"
"""))