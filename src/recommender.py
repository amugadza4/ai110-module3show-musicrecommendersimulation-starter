import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Algorithm Recipe: points available for each rule. Kept in one place so the
# weight-shift experiment only has to change these numbers.
DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre": 2.0,       # exact genre match
    "mood": 1.0,        # exact mood match
    "energy": 1.5,      # max points for energy; shrinks as the gap grows
    "acoustic": 0.5,    # max points for matching acoustic taste
}


@dataclass
class Song:
    """A song and its attributes, as loaded from data/songs.csv."""
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
    """A user's taste profile: favorite genre/mood, target energy, acoustic taste."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def _song_to_dict(song: Song) -> Dict:
    """Convert a Song dataclass to the dict shape used by the functional API."""
    return {
        "id": song.id, "title": song.title, "artist": song.artist,
        "genre": song.genre, "mood": song.mood, "energy": song.energy,
        "tempo_bpm": song.tempo_bpm, "valence": song.valence,
        "danceability": song.danceability, "acousticness": song.acousticness,
    }


def _profile_to_prefs(user: UserProfile) -> Dict:
    """Convert a UserProfile dataclass to the preference dict used by score_song."""
    return {
        "genre": user.favorite_genre,
        "mood": user.favorite_mood,
        "energy": user.target_energy,
        "likes_acoustic": user.likes_acoustic,
    }


class Recommender:
    """OOP wrapper around the scoring and ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects for a user, best first."""
        prefs = _profile_to_prefs(user)
        ranked = sorted(
            self.songs,
            key=lambda s: score_song(prefs, _song_to_dict(s))[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song scored as it did."""
        score, reasons = score_song(_profile_to_prefs(user), _song_to_dict(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to numbers."""
    int_fields = ("id",)
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for key in int_fields:
                row[key] = int(row[key])
            for key in float_fields:
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score, list of reasons)."""
    w = weights or DEFAULT_WEIGHTS
    score = 0.0
    reasons: List[str] = []

    if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
        score += w["genre"]
        reasons.append(f"genre match: {song['genre']} (+{w['genre']:.1f})")

    if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
        score += w["mood"]
        reasons.append(f"mood match: {song['mood']} (+{w['mood']:.1f})")

    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        points = w["energy"] * (1.0 - gap)  # closer to target = more points
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{points:.2f})")

    if "likes_acoustic" in user_prefs:
        target = 1.0 if user_prefs["likes_acoustic"] else 0.0
        points = w["acoustic"] * (1.0 - abs(song["acousticness"] - target))
        score += points
        reasons.append(f"acoustic fit (+{points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    weights: Optional[Dict[str, float]] = None,
) -> List[Tuple[Dict, float, str]]:
    """Score every song, then return the top-k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    # sorted() returns a new list and leaves the catalog untouched (.sort() would reorder in place)
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
