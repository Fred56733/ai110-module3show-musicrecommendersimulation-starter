"""
Command line runner for the Music Recommender Simulation.

Usage:
    python -m src.main                 # default "pop/happy" profile
    python -m src.main "chill lofi"    # any profile name from PROFILES
"""

import sys

try:
    from src.recommender import load_songs, recommend_songs, max_possible_score  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs, max_possible_score  # python src/main.py


# Taste profiles. Keys match the UserProfile fields in recommender.py.
PROFILES = {
    # Default starter profile: an upbeat pop listener.
    "pop/happy": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    },
    # A late-night study listener who wants calm, warm, acoustic music.
    "chill lofi": {
        "favorite_genre": "lofi",   # +2.0 exact match, +1.0 partial match
        "favorite_mood": "chill",   # +1.0 exact match
        "target_energy": 0.38,      # up to +2.0 for closeness (0.0 calm -> 1.0 intense)
        "target_valence": 0.60,     # up to +1.0 for closeness (0.0 dark -> 1.0 happy)
        "likes_acoustic": True,     # +0.5 if the song's acousticness >= 0.5
    },
}
DEFAULT_PROFILE = "pop/happy"

WIDTH = 64


def format_profile(user_prefs: dict) -> str:
    """One-line summary of a taste profile, e.g. 'genre=pop | mood=happy | energy=0.80'."""
    labels = {
        "favorite_genre": "genre",
        "favorite_mood": "mood",
        "target_energy": "energy",
        "target_valence": "valence",
        "likes_acoustic": "acoustic",
    }
    parts = []
    for key, label in labels.items():
        if key in user_prefs:
            value = user_prefs[key]
            parts.append(f"{label}={value:.2f}" if isinstance(value, float) else f"{label}={value}")
    return " | ".join(parts)


def print_recommendations(profile_name: str, user_prefs: dict, recommendations: list) -> None:
    """Print recommendations as numbered entries with score and one reason per line."""
    max_score = max_possible_score(user_prefs)

    print()
    print(f"Profile: {profile_name}")
    print(f"  {format_profile(user_prefs)}")
    print()
    print(f"Top {len(recommendations)} recommendations")
    print("=" * WIDTH)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        title = f"#{rank}  {song['title']} - {song['artist']}"
        score_text = f"Score: {score:.2f} / {max_score:.2f}"
        print(f"{title:<{WIDTH - len(score_text)}}{score_text}")
        print(f"     {song['genre']}, {song['mood']}, energy {song['energy']:.2f}")
        for reason in explanation.split("; "):
            print(f"     + {reason}")
        print("-" * WIDTH)


def main() -> None:
    profile_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROFILE
    if profile_name not in PROFILES:
        print(f"Unknown profile '{profile_name}'. Choose one of: {', '.join(PROFILES)}")
        sys.exit(1)
    user_prefs = PROFILES[profile_name]

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print_recommendations(profile_name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
