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

    high_energy_pop = {
        "favorite_genre":   "pop",
        "favorite_mood":    "happy",
        "target_energy":    0.90,
        "likes_acoustic":   False,
        "target_tempo_bpm": 128,
    }

    chill_lofi = {
        "favorite_genre":   "lofi",
        "favorite_mood":    "chill",
        "target_energy":    0.40,
        "likes_acoustic":   True,
        "target_tempo_bpm": 80,
    }

    deep_intense_rock = {
        "favorite_genre":   "rock",
        "favorite_mood":    "intense",
        "target_energy":    0.92,
        "likes_acoustic":   False,
        "target_tempo_bpm": 150,
    }

    contradiction = {
        "favorite_genre":   "blues",
        "favorite_mood":    "sad",
        "target_energy":    0.95,
        "likes_acoustic":   False,
        "target_tempo_bpm": 160,
    }

    ghost = {
        "favorite_genre":   "bossa nova",
        "favorite_mood":    "nostalgic",
        "target_energy":    0.50,
        "likes_acoustic":   True,
        "target_tempo_bpm": 95,
    }

    extremist = {
        "favorite_genre":   "metal",
        "favorite_mood":    "angry",
        "target_energy":    1.0,
        "likes_acoustic":   False,
        "target_tempo_bpm": 200,
    }

    middleman = {
        "favorite_genre":   "indie pop",
        "favorite_mood":    "happy",
        "target_energy":    0.50,
        "likes_acoustic":   True,
        "target_tempo_bpm": 100,
    }

    for label, user_prefs in [
        ("Contradiction",    contradiction),
        ("Ghost",            ghost),
        ("Extremist",        extremist),
        ("Middleman",        middleman),
    ]:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\n" + "=" * 52)
        print(f"  Profile: {label}")
        print("=" * 52)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']}  -  {song['artist']}")
            print(f"    Genre: {song['genre']}  |  Mood: {song['mood']}  |  Score: {score:.4f}")
            print(f"    Why this song:")
            for line in explanation.split("\n"):
                print(f"      - {line.strip()}")

        print("\n" + "=" * 52 + "\n")


if __name__ == "__main__":
    main()
