# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder suggests 5 songs from a small catalog based on a user's favorite genre, favorite mood, target energy, and whether they like acoustic music. It assumes the user can describe their taste in those four settings.

**Intended use:** classroom exploration of how content-based recommenders work.

**Not intended for:** real users of a music app, decisions about artists or royalties, or any case where fairness to artists matters. The catalog is too small and the profile is too simple.

---

## 3. How the Model Works  

Every song gets points, then the songs are sorted from highest to lowest.

- 2.0 points if the song's genre is the user's favorite genre.
- 1.0 point if the song's mood matches the user's favorite mood.
- Up to 1.5 points for energy. A song exactly at the user's target energy gets all 1.5. The farther away it is, the fewer points it gets.
- Up to 0.5 points for acoustic fit, based on whether the user likes acoustic songs.

The top 5 songs are shown with the reasons for each score. Changes from the starter: the starter did nothing, so I wrote the data loading, scoring, ranking, reasons, and the profiles. I added the acoustic rule on top of the suggested genre + mood + energy recipe.

---

## 4. Data  

The catalog has **20 songs** in `data/songs.csv`. I kept the 10 starter songs and added 10 more to cover genres and moods that were missing: r&b, country, hip hop, edm, classical, indie folk, metal, latin, blues, and a chill indie pop song. Each song has genre, mood, energy, tempo_bpm, valence, danceability, and acousticness.

Limits: most genres have only one song. Lofi has 3 and pop has 2 (plus 2 indie pop), so those are better covered. The data is made up for this project, so it does not reflect real listening. Missing from the data: lyrics, language, artist popularity, release year, and anything about how people actually listen.

---

## 5. Strengths  

- It works well for users whose taste is clear and well covered in the catalog. Chill Lofi returned two lofi/chill songs, then a lofi/focused song, then ambient/chill. That matches how I would describe the "vibe."
- Deep Intense Rock put Storm Runner first by a wide margin (4.93 vs 2.96).
- The reasons make every result easy to check. I can see exactly why a song ranked where it did.
- Energy closeness works as intended: a mid-energy user is not pushed toward the loudest songs.

---

## 6. Limitations and Bias 

The biggest weakness I found is that **genre dominates the ranking**. Genre is worth 2.0 points, which is more than mood (1.0) and more than most of the energy gap. That is why *Gym Hero* (pop, intense) ranks second for the Default Pop/Happy user, even though the user asked for a happy song. It matches the genre and the high energy, so it beats happy songs from other genres. In the weight-shift experiment, when I halved genre and doubled energy, *Rooftop Lights* (a happy indie pop song) moved above Gym Hero, which fit the user better.

Other problems: genre and mood are exact-match only, so "indie pop" gets no credit for being close to "pop." Users whose favorite genre is not in the catalog (like k-pop) get zero genre points, so their lists are decided by mood and energy alone. A user with conflicting taste (sad but high energy) gets one good match and then filler. Because only a few songs exist for most genres, fans of rare genres see weaker lists than fans of lofi or pop, which creates a small filter bubble.

---

## 7. Evaluation  

I tested 4 normal profiles and 3 adversarial profiles, and ran one weight-shift experiment. I checked whether the top results matched my own sense of each "vibe," and whether the reasons made sense.

### Profiles tested

**Normal profiles**

```text
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

```text
================================================================
Profile: High-Energy Pop
Prefs:   {'genre': 'pop', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
----------------------------------------------------------------
1. Gym Hero by Max Pulse  [pop/intense]
   Score: 4.96
     - genre match: pop (+2.0)
     - mood match: intense (+1.0)
     - energy 0.93 vs target 0.92 (+1.48)
     - acoustic fit (+0.47)
2. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.76
     - genre match: pop (+2.0)
     - energy 0.82 vs target 0.92 (+1.35)
     - acoustic fit (+0.41)
3. Storm Runner by Voltline  [rock/intense]
   Score: 2.94
     - mood match: intense (+1.0)
     - energy 0.91 vs target 0.92 (+1.48)
     - acoustic fit (+0.45)
4. Pulse Garden by Helix Union  [edm/euphoric]
   Score: 1.92
     - energy 0.96 vs target 0.92 (+1.44)
     - acoustic fit (+0.48)
5. Iron Tide by Black Harbor  [metal/angry]
   Score: 1.90
     - energy 0.97 vs target 0.92 (+1.43)
     - acoustic fit (+0.47)
```

```text
================================================================
Profile: Chill Lofi
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.38, 'likes_acoustic': True}
----------------------------------------------------------------
1. Library Rain by Paper Lanterns  [lofi/chill]
   Score: 4.88
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.35 vs target 0.38 (+1.46)
     - acoustic fit (+0.43)
2. Midnight Coding by LoRoom  [lofi/chill]
   Score: 4.79
     - genre match: lofi (+2.0)
     - mood match: chill (+1.0)
     - energy 0.42 vs target 0.38 (+1.44)
     - acoustic fit (+0.35)
3. Focus Flow by LoRoom  [lofi/focused]
   Score: 3.86
     - genre match: lofi (+2.0)
     - energy 0.40 vs target 0.38 (+1.47)
     - acoustic fit (+0.39)
4. Spacewalk Thoughts by Orbit Bloom  [ambient/chill]
   Score: 2.81
     - mood match: chill (+1.0)
     - energy 0.28 vs target 0.38 (+1.35)
     - acoustic fit (+0.46)
5. Paper Planes by Indigo Parade  [indie pop/chill]
   Score: 2.58
     - mood match: chill (+1.0)
     - energy 0.48 vs target 0.38 (+1.35)
     - acoustic fit (+0.22)
```

```text
================================================================
Profile: Deep Intense Rock
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
----------------------------------------------------------------
1. Storm Runner by Voltline  [rock/intense]
   Score: 4.93
     - genre match: rock (+2.0)
     - mood match: intense (+1.0)
     - energy 0.91 vs target 0.92 (+1.48)
     - acoustic fit (+0.45)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 2.96
     - mood match: intense (+1.0)
     - energy 0.93 vs target 0.92 (+1.48)
     - acoustic fit (+0.47)
3. Pulse Garden by Helix Union  [edm/euphoric]
   Score: 1.92
     - energy 0.96 vs target 0.92 (+1.44)
     - acoustic fit (+0.48)
4. Iron Tide by Black Harbor  [metal/angry]
   Score: 1.90
     - energy 0.97 vs target 0.92 (+1.43)
     - acoustic fit (+0.47)
5. Concrete Crown by Kid Atlas  [hip hop/confident]
   Score: 1.76
     - energy 0.80 vs target 0.92 (+1.32)
     - acoustic fit (+0.44)
```

**Adversarial profiles**

```text
================================================================
Profile: Conflicting (energy 0.9 + sad mood)
Prefs:   {'genre': 'blues', 'mood': 'sad', 'energy': 0.9, 'likes_acoustic': True}
----------------------------------------------------------------
1. Blue Monday Blues by Delta Slim  [blues/sad]
   Score: 4.12
     - genre match: blues (+2.0)
     - mood match: sad (+1.0)
     - energy 0.45 vs target 0.90 (+0.83)
     - acoustic fit (+0.30)
2. Rainy Window by Soft Meridian  [indie folk/sad]
   Score: 2.04
     - mood match: sad (+1.0)
     - energy 0.30 vs target 0.90 (+0.60)
     - acoustic fit (+0.44)
3. Storm Runner by Voltline  [rock/intense]
   Score: 1.53
     - energy 0.91 vs target 0.90 (+1.48)
     - acoustic fit (+0.05)
4. Gym Hero by Max Pulse  [pop/intense]
   Score: 1.48
     - energy 0.93 vs target 0.90 (+1.46)
     - acoustic fit (+0.03)
5. Sol y Arena by Marisol Vega  [latin/playful]
   Score: 1.47
     - energy 0.78 vs target 0.90 (+1.32)
     - acoustic fit (+0.15)
```

```text
================================================================
Profile: Genre not in catalog (k-pop)
Prefs:   {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
----------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 2.88
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.80 (+1.47)
     - acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 2.77
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.80 (+1.44)
     - acoustic fit (+0.33)
3. Concrete Crown by Kid Atlas  [hip hop/confident]
   Score: 1.94
     - energy 0.80 vs target 0.80 (+1.50)
     - acoustic fit (+0.44)
4. Sol y Arena by Marisol Vega  [latin/playful]
   Score: 1.82
     - energy 0.78 vs target 0.80 (+1.47)
     - acoustic fit (+0.35)
5. Night Drive Loop by Neon Echo  [synthwave/moody]
   Score: 1.81
     - energy 0.75 vs target 0.80 (+1.42)
     - acoustic fit (+0.39)
```

```text
================================================================
Profile: Middle of the road (energy 0.5)
Prefs:   {'genre': 'jazz', 'mood': 'relaxed', 'energy': 0.5, 'likes_acoustic': False}
----------------------------------------------------------------
1. Coffee Shop Stories by Slow Stereo  [jazz/relaxed]
   Score: 4.36
     - genre match: jazz (+2.0)
     - mood match: relaxed (+1.0)
     - energy 0.37 vs target 0.50 (+1.30)
     - acoustic fit (+0.05)
2. Paper Planes by Indigo Parade  [indie pop/chill]
   Score: 1.75
     - energy 0.48 vs target 0.50 (+1.47)
     - acoustic fit (+0.28)
3. Velvet Hours by Luna Marsh  [r&b/romantic]
   Score: 1.72
     - energy 0.55 vs target 0.50 (+1.42)
     - acoustic fit (+0.30)
4. Dust Road Home by Cedar Hollow  [country/nostalgic]
   Score: 1.68
     - energy 0.50 vs target 0.50 (+1.50)
     - acoustic fit (+0.17)
5. Blue Monday Blues by Delta Slim  [blues/sad]
   Score: 1.62
     - energy 0.45 vs target 0.50 (+1.42)
     - acoustic fit (+0.20)
```

**Experiment: genre 2.0 -> 1.0, energy 1.5 -> 3.0**

```text
================================================================
Profile: Default Pop/Happy (shifted)
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'likes_acoustic': False}
----------------------------------------------------------------
1. Sunrise City by Neon Echo  [pop/happy]
   Score: 5.35
     - genre match: pop (+1.0)
     - mood match: happy (+1.0)
     - energy 0.82 vs target 0.80 (+2.94)
     - acoustic fit (+0.41)
2. Rooftop Lights by Indigo Parade  [indie pop/happy]
   Score: 4.21
     - mood match: happy (+1.0)
     - energy 0.76 vs target 0.80 (+2.88)
     - acoustic fit (+0.33)
3. Gym Hero by Max Pulse  [pop/intense]
   Score: 4.08
     - genre match: pop (+1.0)
     - energy 0.93 vs target 0.80 (+2.61)
     - acoustic fit (+0.47)
4. Concrete Crown by Kid Atlas  [hip hop/confident]
   Score: 3.44
     - energy 0.80 vs target 0.80 (+3.00)
     - acoustic fit (+0.44)
5. Sol y Arena by Marisol Vega  [latin/playful]
   Score: 3.29
     - energy 0.78 vs target 0.80 (+2.94)
     - acoustic fit (+0.35)
```

```text
================================================================
Profile: Deep Intense Rock (shifted)
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 0.92, 'likes_acoustic': False}
----------------------------------------------------------------
1. Storm Runner by Voltline  [rock/intense]
   Score: 5.42
     - genre match: rock (+1.0)
     - mood match: intense (+1.0)
     - energy 0.91 vs target 0.92 (+2.97)
     - acoustic fit (+0.45)
2. Gym Hero by Max Pulse  [pop/intense]
   Score: 4.44
     - mood match: intense (+1.0)
     - energy 0.93 vs target 0.92 (+2.97)
     - acoustic fit (+0.47)
3. Pulse Garden by Helix Union  [edm/euphoric]
   Score: 3.36
     - energy 0.96 vs target 0.92 (+2.88)
     - acoustic fit (+0.48)
4. Iron Tide by Black Harbor  [metal/angry]
   Score: 3.32
     - energy 0.97 vs target 0.92 (+2.85)
     - acoustic fit (+0.47)
5. Sunrise City by Neon Echo  [pop/happy]
   Score: 3.11
     - energy 0.82 vs target 0.92 (+2.70)
     - acoustic fit (+0.41)
```

### What surprised me

- **Gym Hero keeps showing up for people who just want Happy Pop.** In plain words: Gym Hero is a pop song, and it is very high energy, and the user asked for pop with high energy. The system only checks if the words match and how close the energy is. It does not know that "intense" and "happy" feel different. Sunrise City still wins because it matches the mood too.
- Songs from other genres appear when they have the right energy, like Storm Runner for High-Energy Pop. That makes sense, but it also shows the system uses energy as a stand-in for vibe.
- The k-pop profile had no genre match at all, so the system quietly fell back to mood and energy and still gave a confident-looking list.

### Comparing pairs of profiles

- **Default Pop/Happy vs High-Energy Pop:** Both put a pop song first. Pop/Happy picks Sunrise City (happy) and High-Energy Pop picks Gym Hero (intense, energy 0.93). The mood setting is what flipped them, which is correct.
- **High-Energy Pop vs Deep Intense Rock:** Both want intense, high-energy songs, so Gym Hero and Storm Runner swap places. Genre decides which one wins, which makes sense.
- **Chill Lofi vs Deep Intense Rock:** These are opposites. Lofi returns quiet, acoustic songs (energy 0.35-0.42) and Rock returns loud ones (0.91+). There is no overlap in the top 5, so the energy rule clearly works.
- **Chill Lofi vs Middle of the road (jazz/relaxed):** Lofi has several close matches, but the jazz user has only one (Coffee Shop Stories), then a big score drop (4.36 to 1.75). That shows how a one-song genre leaves a user with weak results after the first pick.
- **Conflicting (sad + 0.9 energy) vs Deep Intense Rock:** Both ask for high energy, but the sad profile puts a slow blues song first because genre + mood points (3.0) outweigh the energy miss. The high-energy songs only show up in spots 3-4. This is a case where the system "works" by its rules but not by the user's real intent.
- **Experiment (shifted weights):** Making energy matter more made the lists feel more about vibe and less about genre labels. For Pop/Happy it was more accurate (the happy song rose). For Rock it was only different: a happy pop song entered the top 5 just for its energy.

---

## 8. Future Work  

- Add partial credit for similar genres and moods (for example, "indie pop" is close to "pop"; "sad" is close to "melancholy").
- Use tempo, valence, and danceability in the score, and let the user set a target for each.
- Add a diversity step so the top 5 do not all come from the same genre or artist.
- Show a warning when no song matches the user's genre, instead of quietly falling back.
- Add a bigger catalog so rare genres have more than one song.

---

## 9. Personal Reflection  

**Biggest learning moment:** seeing that the weights are the whole opinion of the system. When I cut the genre weight in half and doubled the energy weight, the same data gave different lists. The "right" answer depends on choices I made.

**How AI helped, and what I double-checked:** An AI assistant (Claude) helped me design the scoring recipe, expand the dataset, write the code, and run the profiles. I still checked the pieces myself: that numbers were converted from text to floats, that the energy formula rewards closeness and not just high values, that the two starter tests pass, and that the ranked lists matched what I would expect by ear. I also had to check explanations like "why does Gym Hero rank second" against the actual score breakdown instead of just trusting the first answer.

**What surprised me:** A few additions and a sort already feel like a real recommendation. The reasons list helps a lot, because "genre match (+2.0)" makes a simple score feel like it understands me, even though it only compares labels.

**What I would try next:** add partial matches for genres and moods, use more audio features, add a diversity step, and let the profile change when a user skips or likes a song.
