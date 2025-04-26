import os
import ipywidgets as widgets
from IPython.display import display, Markdown, HTML
from .agent import StoryboardAgent
from .visualization import display_storyboard, visualize_mood
from .config import CONFIG

def create_ui():
    """Create and display the UI for the Storyboard Weaver."""
    plot_input = widgets.Textarea(
        placeholder='Describe your story (e.g., "A detective discovers aliens in 1920s Chicago")',
        description='Plot:',
        layout=widgets.Layout(width='80%', height='100px'),
        style={'description_width': 'initial'}
    )
    scenes_slider = widgets.IntSlider(
        value=3, min=1, max=CONFIG["max_scenes"], step=1,
        description='Number of Scenes:',
        continuous_update=False,
        style={'description_width': 'initial'}
    )
    style_selector = widgets.Dropdown(
        options=['Cinematic', 'Documentary', 'Anime', 'Noir', 'Experimental'],
        value='Cinematic',
        description='Visual Style:',
        style={'description_width': 'initial'}
    )
    generate_btn = widgets.Button(
        description='Generate Storyboard',
        button_style='success',
        layout=widgets.Layout(width='200px', height='40px'),
        icon='film'
    )
    output_area = widgets.Output()

    def on_generate_click(b):
        with output_area:
            output_area.clear_output()
            steps = widgets.HBox([
                widgets.Label(value="Progress:"),
                widgets.IntProgress(value=0, min=0, max=4, description='', bar_style='info')
            ])
            display(steps)
            agent = StoryboardAgent(
                endpoint=os.environ["MODEL_ENDPOINT"],
                api_key=os.environ["MODEL_API_KEY"],
                model_name=os.environ["MODEL_NAME"]
            )
            try:
                steps.children[1].value = 1
                display(Markdown("### 🔍 Analyzing your plot..."))
                steps.children[1].value = 2
                display(Markdown("### 🎥 Generating storyboard..."))
                storyboard = agent.execute_function(
                    "generate_storyboard",
                    plot=plot_input.value,
                    num_scenes=scenes_slider.value
                )
                if not storyboard:
                    raise ValueError("Generation failed")
                steps.children[1].value = 3
                display(Markdown("### 📊 Analyzing story structure..."))
                mood_analysis = agent.execute_function("analyze_mood", storyboard=storyboard)
                steps.children[1].value = 4
                display(Markdown(f"## 🎬 {storyboard.get('title', 'Your Storyboard')}"))
                display_storyboard(storyboard)
                visualize_mood(mood_analysis)
                filename = f"storyboard_{plot_input.value[:20].replace(' ', '_')}.json"
                if agent.execute_function("save_storyboard", storyboard=storyboard, filename=filename):
                    display(Markdown("### 💾 Download Options"))
                    display(HTML(f"""
                    <a href="{filename}" download>
                        <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; border-radius:6px; font-size:14px; margin:5px">
                            Download JSON
                        </button>
                    </a>
                    """))
                steps.children[1].bar_style = 'success'
            except Exception as e:
                steps.children[1].bar_style = 'danger'
                display(Markdown(f"## ❌ Error: {str(e)}"))
                display(Markdown("Please try again with a different plot description."))

    generate_btn.on_click(on_generate_click)
    display(Markdown("### ✍️ Your Story Parameters"))
    display(widgets.VBox([
        plot_input,
        widgets.HBox([scenes_slider, style_selector]),
        generate_btn
    ]))
    display(output_area)