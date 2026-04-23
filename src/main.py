"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "favorite_genre":  "lofi",
        "favorite_mood":   "chill",
        "target_energy":   0.4,
        "likes_acoustic":  True,
        "target_tempo_bpm": 80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 48)
    print("  Top 5 Recommendations For You")
    print("=" * 48)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  -  {song['artist']}")
        print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.4f}")
        print(f"    Why this song:")
        for line in explanation.split("\n"):
            print(f"      - {line.strip()}")

    print("\n" + "=" * 48 + "\n")


if __name__ == "__main__":
    main()
