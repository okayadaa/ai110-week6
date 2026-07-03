import csv
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 1.0


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


EXAMPLE_PROFILES: Dict[str, Dict] = {
    "intense_rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "chill_lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "likes_acoustic": True,
    },
}


def profile_from_dict(profile: Dict) -> UserProfile:
    return UserProfile(
        favorite_genre=profile["favorite_genre"],
        favorite_mood=profile["favorite_mood"],
        target_energy=profile["target_energy"],
        likes_acoustic=profile["likes_acoustic"],
    )


def profile_to_dict(user: UserProfile) -> Dict:
    return asdict(user)


def song_to_dict(song: Song) -> Dict:
    return asdict(song)


def _format_explanation(reasons: List[str]) -> str:
    if not reasons:
        return "No strong matches found for your taste profile."
    return "; ".join(reasons)


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre is {song['genre']} (your favorite)")
    else:
        reasons.append(
            f"genre is {song['genre']}, not your preferred "
            f"{user_prefs['favorite_genre']}"
        )

    if song["mood"] == user_prefs["favorite_mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood is {song['mood']}, matching your preference")
    else:
        reasons.append(
            f"mood is {song['mood']}, not your preferred "
            f"{user_prefs['favorite_mood']}"
        )

    energy_diff = abs(song["energy"] - user_prefs["target_energy"])
    energy_score = ENERGY_WEIGHT * (1 - energy_diff)
    score += energy_score
    if energy_diff < 0.15:
        reasons.append(
            f"energy is {song['energy']:.2f}, close to your target of "
            f"{user_prefs['target_energy']:.2f}"
        )
    else:
        reasons.append(
            f"energy is {song['energy']:.2f}, farther from your target of "
            f"{user_prefs['target_energy']:.2f}"
        )

    is_acoustic = song["acousticness"] > 0.5
    if user_prefs["likes_acoustic"] == is_acoustic:
        score += ACOUSTIC_WEIGHT
        if user_prefs["likes_acoustic"]:
            reasons.append(
                f"acousticness is {song['acousticness']:.2f} "
                f"(you prefer acoustic tracks)"
            )
        else:
            reasons.append(
                f"acousticness is {song['acousticness']:.2f} "
                f"(you prefer produced tracks)"
            )
    elif user_prefs["likes_acoustic"]:
        reasons.append(
            f"acousticness is {song['acousticness']:.2f}, not the acoustic "
            f"sound you prefer"
        )
    else:
        reasons.append(
            f"acousticness is {song['acousticness']:.2f}, not the produced "
            f"sound you prefer"
        )

    return score, reasons


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = profile_to_dict(user)
        scored = sorted(
            (
                (song, score_song(user_prefs, song_to_dict(song))[0])
                for song in self.songs
            ),
            key=lambda item: item[1],
            reverse=True,
        )
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = profile_to_dict(user)
        _, reasons = score_song(user_prefs, song_to_dict(song))
        return _format_explanation(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, List[str]]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
