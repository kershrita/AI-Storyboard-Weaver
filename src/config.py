import matplotlib.colors as mcolors

CONFIG = {
    "max_scenes": 5,
    "moods": ["tense", "joyful", "romantic", "suspenseful", "chaotic", "dark", "hopeful"],
    "context_length": 300,
    "colors": list(mcolors.TABLEAU_COLORS.values()),
    "max_retries": 3,
    "rag_threshold": 0.7,
    "knowledge_base": "knowledge_base.json",
    "embedding_model": "all-MiniLM-L6-v2",
    "default_genre": "drama",
    "output_dir": "outputs" 
}