# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a small content-based music recommender. It loads a 20-song catalog from `data/songs.csv`, compares every song to a user "taste profile" (favorite genre, favorite mood, target energy, acoustic taste), and prints the top 5 matches with a plain-language reason for each score. It runs entirely in the terminal with `python -m src.main`.

---

## How The System Works

Real platforms like Spotify and YouTube mix two ideas. **Collaborative filtering** learns from other users' behavior (likes, skips, playlists, listening time): if people who like what you like also love a song, it gets recommended to you. **Content-based filtering** looks at the songs themselves (genre, tempo, mood, energy) and finds songs similar to ones you already like. At scale, platforms blend both with large models trained on billions of interactions. My version is content-based only. It prioritizes **genre first, then mood, then how close a song's energy is to what the user wants**.

**Song features:** `id, title, artist, genre, mood, energy (0-1), tempo_bpm, valence, danceability, acousticness`

**UserProfile / preference dict:** `favorite_genre, favorite_mood, target_energy, likes_acoustic`

### Algorithm Recipe

Scoring Rule (one song): add up points.

- +2.0 if the song's genre matches the user's favorite genre
- +1.0 if the song's mood matches the user's favorite mood
- Up to +1.5 for energy: `1.5 * (1 - |song energy - target energy|)`. A song right on target gets the full 1.5; the further away, the fewer points. This rewards *closeness*, not just "higher" or "lower".
- Up to +0.5 for acoustic fit: `0.5 * (1 - |song acousticness - target|)`, where the target is 1.0 for acoustic fans and 0.0 otherwise
- Every rule also adds a "reason" string, such as `genre match: pop (+2.0)`, so each score is explainable.

Ranking Rule (whole catalog): run the scoring rule on every song, sort by score from highest to lowest, and return the top k. Scoring answers "how good is this song for this user?"; ranking answers "which songs should I show first?" You need both, because a score by itself doesn't produce a list.

Data flow: `User prefs -> loop over every song in CSV -> score_song() -> sort by score -> Top K with reasons`

### Expected biases

- Genre is worth the most, so the system may bury a great mood-and-energy match that is in a different genre.
- Exact-match genre and mood are all-or-nothing: "indie pop" gets no credit for being close to "pop".
- Pop and lofi have several songs in the catalog, so their fans get more good options than fans of one-song genres.
- It never learns from skips or likes, so a user's profile never changes.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output for the default pop/happy profile (`python -m src.main`; the full run covers every profile and is in `model_card.md`):

```text
Loaded songs: 20

================================================================
Profile: Default Pop/Happy
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
----------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 4.88
     - genre match: pop (+2.0)
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.80 (+1.47)
     - acoustic fit (+0.41)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 3.78
     - genre match: pop (+2.0)
     - energy 0.93 vs target 0.80 (+1.30)
     - acoustic fit (+0.47)
3. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 2.77
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.80 (+1.44)
     - acoustic fit (+0.33)
4. Concrete Crown by Kid Atlas  [hip hop/confident]
   Score: 1.94
     - energy 0.80 vs target 0.80 (+1.50)
     - acoustic fit (+0.44)
5. Sol y Arena by Marisol Vega  [latin/playful]
   Score: 1.82
     - energy 0.78 vs target 0.80 (+1.47)
     - acoustic fit (+0.35)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

**Experiment: weight shift.** I halved the genre weight (2.0 -> 1.0) and doubled the energy weight (1.5 -> 3.0), then re-ran the Default Pop/Happy and Deep Intense Rock profiles.

- **Pop/Happy:** the top song stayed Sunrise City, but indie pop *Rooftop Lights* (a happy song) moved above *Gym Hero*. Mood and energy now count for more relative to genre, so an off-genre happy song beats an on-genre intense one. This felt more accurate for someone who just wants happy music.
- **Deep Intense Rock:** Storm Runner stayed first, but *Sunrise City* (a pop/happy song) appeared in the top 5 only because its energy is high. That is "different," not better, because a rock fan would probably not want it.

Other things I tried: three adversarial profiles (conflicting sad + high energy, a genre missing from the catalog, and a middle-of-the-road user). Details are in `model_card.md`.

---

## Limitations and Risks

- The catalog is only 20 songs, so most genres have a single song and the top 5 quickly fills with weak matches.
- It matches genre and mood by exact text, so it can't tell that "indie pop" is close to "pop" or that "sad" is close to "melancholy".
- It ignores lyrics, language, artist, tempo, and valence when scoring.
- Because genre is worth the most, a song in the user's genre can outrank a song that matches their mood and energy much better.
- A user who wants something unusual (like high energy but a sad mood) gets one good match and then filler.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me that a recommender is just two steps: score each item, then sort. The "intelligence" is really my choices about weights. When I changed one number, the lists changed, which made it clear that a recommender's idea of taste is a design decision, not a fact. Bias shows up in the same places: which songs are in the catalog, which features get counted, and how heavily each one is weighted. In this project, genre fans of well-represented genres get better results than fans of rare genres, and nobody can discover music outside the genre they typed in.

See the full reflection in [model_card.md](model_card.md).



