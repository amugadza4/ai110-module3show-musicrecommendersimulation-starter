"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs, DEFAULT_WEIGHTS

PROFILES = {
    "Default Pop/Happy": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "High-Energy Pop": {"genre": "pop", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.38, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
}

ADVERSARIAL_PROFILES = {
    "Conflicting (energy 0.9 + sad mood)": {"genre": "blues", "mood": "sad", "energy": 0.9, "likes_acoustic": True},
    "Genre not in catalog (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Middle of the road (energy 0.5)": {"genre": "jazz", "mood": "relaxed", "energy": 0.5, "likes_acoustic": False},
}

# Experiment: double energy, halve genre
SHIFTED_WEIGHTS = {**DEFAULT_WEIGHTS, "genre": 1.0, "energy": 3.0}


def print_recs(name: str, prefs: dict, songs: list, k: int = 5, weights=None) -> None:
    """Print a readable top-k list for one profile."""
    print("=" * 64)
    print(f"Profile: {name}")
    print(f"Prefs:   {prefs}")
    print("-" * 64)
    for rank, (song, score, explanation) in enumerate(recommend_songs(prefs, songs, k, weights), 1):
        print(f"{rank}. {song['title']} by {song['artist']}  [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    print_recs("Default Pop/Happy", PROFILES["Default Pop/Happy"], songs)
    for name in list(PROFILES)[1:]:
        print_recs(name, PROFILES[name], songs)

    print("##### ADVERSARIAL PROFILES #####\n")
    for name, prefs in ADVERSARIAL_PROFILES.items():
        print_recs(name, prefs, songs)

    print("##### EXPERIMENT: genre weight 2.0 -> 1.0, energy weight 1.5 -> 3.0 #####\n")
    for name in ("Default Pop/Happy", "Deep Intense Rock"):
        print_recs(name + " (shifted)", PROFILES[name], songs, weights=SHIFTED_WEIGHTS)


if __name__ == "__main__":
    main()
