"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from src.recommender import load_songs, recommend_songs  # python -m src.main
except ModuleNotFoundError:
    from recommender import load_songs, recommend_songs  # python src/main.py


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Taste profile: a late-night study listener who wants calm, warm, acoustic music.
    # Keys match the UserProfile fields in recommender.py.
    user_prefs = {
        "favorite_genre": "lofi",   # +2.0 exact match, +1.0 partial match
        "favorite_mood": "chill",   # +1.0 exact match
        "target_energy": 0.38,      # up to +2.0 for closeness (0.0 calm -> 1.0 intense)
        "target_valence": 0.60,     # up to +1.0 for closeness (0.0 dark -> 1.0 happy)
        "likes_acoustic": True,     # +0.5 if the song's acousticness >= 0.5
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
