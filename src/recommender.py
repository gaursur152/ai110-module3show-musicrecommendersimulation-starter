from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of songs available for recommendation."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs best matching the user's taste profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of song dicts with typed numeric fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences using weighted genre, mood, and audio feature proximity."""
    score = 0.0
    reasons = []

    # Genre match — worth the most (0.35) because genre reflects
    # fundamental differences in sound, instrumentation, and production style
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 0.35
        reasons.append(f"genre match (+0.35)")

    # Mood match — second most important (0.20), meaningful but more fluid
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 0.20
        reasons.append(f"mood match (+0.20)")

    # Energy proximity — rewards closeness to target, not just high/low values
    energy_score = round(1 - abs(song["energy"] - user_prefs["target_energy"]), 3)
    weighted_energy = round(energy_score * 0.20, 3)
    score += weighted_energy
    reasons.append(f"energy proximity {song['energy']} vs target {user_prefs['target_energy']} (+{weighted_energy})")

    # Acousticness proximity — convert likes_acoustic bool to a target float
    acoustic_target = 0.8 if user_prefs["likes_acoustic"] else 0.2
    acoustic_score = round(1 - abs(song["acousticness"] - acoustic_target), 3)
    weighted_acoustic = round(acoustic_score * 0.15, 3)
    score += weighted_acoustic
    reasons.append(f"acousticness proximity {song['acousticness']} vs target {acoustic_target} (+{weighted_acoustic})")

    # Tempo proximity — normalize to 0–1 using 200 BPM as ceiling, then score
    tempo_normalized = song["tempo_bpm"] / 200
    target_tempo_normalized = user_prefs.get("target_tempo_bpm", 100) / 200
    tempo_score = round(1 - abs(tempo_normalized - target_tempo_normalized), 3)
    weighted_tempo = round(tempo_score * 0.10, 3)
    score += weighted_tempo
    reasons.append(f"tempo proximity {song['tempo_bpm']} BPM vs target {user_prefs.get('target_tempo_bpm', 100)} BPM (+{weighted_tempo})")

    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top-k results sorted by descending score."""
    scored = [
        (song, score, "\n  ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return ranked[:k]
