# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world platforms like Spotify and YouTube predict what you'll love next by combining two approaches. **Collaborative filtering** learns from the behavior of millions of users (likes, skips, playlist adds, watch time) and recommends what people with similar taste enjoyed. **Content-based filtering** looks at the attributes of the songs themselves (tempo, energy, mood, genre) and recommends tracks that sound like the ones you already like. Large platforms blend both, then use a ranking step to choose what you actually see. My version is a **content-based** recommender, because the dataset has song attributes but no listening history. It gives each song a score for how well it matches the user's taste: points for a genre match and a mood match, plus points for how *close* the song's energy is to the user's target. It rewards closeness, not just higher values. A ranking rule then sorts the scored songs and returns the top `k`. My version prioritizes **genre** and **energy** most heavily, because in this data energy also tracks tempo, danceability and acousticness. It prioritizes **mood** and **valence** next, and gives each recommendation a plain-language reason so the results are easy to explain.

### `Song` features

| Feature | Type | Role in the simulation |
|---|---|---|
| `id`, `title`, `artist` | int / string | Identify and display the song (not scored) |
| `genre` | string | Scored: +2.0 for an exact match, +1.0 for a partial match (e.g. `pop` in `indie pop`) |
| `mood` | string | Scored: +1.0 for an exact match |
| `energy` | float (0–1) | Scored: up to +2.0 based on closeness to the user's target |
| `valence` | float (0–1) | Scored: up to +1.0 based on closeness (only when the user sets a target) |
| `acousticness` | float (0–1) | Scored: +0.5 if it matches the user's acoustic preference (acoustic = 0.5 or above) |
| `tempo_bpm`, `danceability` | float | Stored but not scored; they closely follow `energy` in this dataset |

### `UserProfile` features

| Feature | Type | What it represents |
|---|---|---|
| `favorite_genre` | string | The genre the user likes most |
| `favorite_mood` | string | The mood the user wants the music to match |
| `target_energy` | float (0–1) | How calm (low) or intense (high) the user wants the music |
| `likes_acoustic` | bool | Whether the user prefers acoustic or electronic-sounding tracks |
| `target_valence` *(optional, planned)* | float (0–1) | How happy (high) or dark (low) the user wants the music |

### Algorithm Recipe (Finalized)

**Scoring rule (one song).** Each song earns points for how well it matches the taste profile. The maximum is **6.5**.

| Rule | Points |
|---|---|
| Genre: exact match | **+2.0** |
| Genre: partial match (e.g. `pop` inside `indie pop`) | +1.0 |
| Mood: exact match | **+1.0** |
| Energy closeness: `2.0 × (1 − abs(song.energy − target_energy))` | 0 – 2.0 |
| Valence closeness: `1.0 × (1 − abs(song.valence − target_valence))` (only if the user sets a target) | 0 – 1.0 |
| Acoustic match: song's `acousticness ≥ 0.5` matches `likes_acoustic` | +0.5 |

If the user leaves out a preference, that rule is skipped. Every rule that awards points also adds a short reason, such as "genre match: lofi (+2.0)". These reasons become the explanation shown with each recommendation.

**Ranking rule (the list).** Score every song, sort from highest to lowest score, break ties by energy closeness and then by title, and return the top `k`.

**Why these weights?**
- **Genre (+2.0) is worth more than mood (+1.0).** Genre describes the overall sound, while mood labels are more subjective. In this dataset, "focused" and "chill" songs have almost identical numbers.
- **Genre is no stronger than energy (max +2.0).** I tested a user who likes *pop* but wants *calm* music (energy 0.4). With genre at +4.0, the system recommended high-energy pop (*Sunrise City*, *Gym Hero*), which ignores the vibe the user asked for. With genre at +2.0, calm songs ranked first and the closest pop song dropped to #4. Keeping genre equal to energy means a genre label can't override how a song feels.
- **Mood isn't raised above genre.** Doubling mood to +2.0 pushed *Gym Hero* (an upbeat pop song labeled "intense") even higher for a rock fan. Exact mood labels are too unreliable to carry more weight.

### Expected Biases

- **Genre can outweigh mood.** A genre match is worth twice as much as a mood match, so the system might rank a same-genre song with the wrong mood above a great song that matches the user's mood. For a chill lofi fan, *Focus Flow* (lofi, "focused") is expected to outrank *Spacewalk Thoughts* (ambient, "chill"), even though Spacewalk is the better mood match.
- **Exact labels miss near-synonyms.** "chill" gets no credit for "relaxed", and "sad" gets none for "melancholic". A label can also be misleading: *Gym Hero* is an upbeat pop song, but its "intense" label could push it near the top for a rock fan.
- **Popular genres get better lists.** Lofi has 3 songs and pop has 2, but 13 genres have only one song. Users who like a rare genre (like metal or jazz) get one genre match, and the rest of their list is filled by energy alone.
- **Everything is reduced to intensity.** Energy is also standing in for tempo, danceability and acousticness, so songs that feel very different but share an energy level (*Pulse Theory*, edm, euphoric; *Iron Cathedral*, metal, angry) can look similar to the system.
- **No variety or discovery.** The system always recommends the closest matches. It has no diversity rule, so it can repeat the same artist (two LoRoom songs for a lofi fan) and keeps users in their current "bubble".
- **Subjective data.** The genre and mood labels and the 0–1 values were assigned by hand, so they reflect one person's judgment of a song's vibe and may not match how other listeners hear it.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

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

Output of `python -m src.main` with the default **pop/happy** profile:

```
Loaded songs: 20

Profile: pop/happy
  genre=pop | mood=happy | energy=0.80

Top 5 recommendations
================================================================
#1  Sunrise City - Neon Echo                  Score: 4.96 / 5.00
     pop, happy, energy 0.82
     + genre match: pop (+2.0)
     + mood match: happy (+1.0)
     + energy 0.82 vs your 0.80 (+1.96)
----------------------------------------------------------------
#2  Rooftop Lights - Indigo Parade            Score: 3.92 / 5.00
     indie pop, happy, energy 0.76
     + partial genre match: indie pop ~ pop (+1.0)
     + mood match: happy (+1.0)
     + energy 0.76 vs your 0.80 (+1.92)
----------------------------------------------------------------
#3  Gym Hero - Max Pulse                      Score: 3.74 / 5.00
     pop, intense, energy 0.93
     + genre match: pop (+2.0)
     + energy 0.93 vs your 0.80 (+1.74)
----------------------------------------------------------------
#4  Fuego Lento - Brisa Roja                  Score: 2.00 / 5.00
     latin, playful, energy 0.80
     + energy 0.80 vs your 0.80 (+2.00)
----------------------------------------------------------------
#5  Concrete Verses - Block Theory            Score: 1.96 / 5.00
     hip-hop, confident, energy 0.78
     + energy 0.78 vs your 0.80 (+1.96)
----------------------------------------------------------------
```

**Does this match expectations?** Yes. *Sunrise City* is the only song that matches pop, happy and the target energy, so it ranks first with nearly a perfect score. *Rooftop Lights* (indie pop, happy) edges out *Gym Hero* (pop, but "intense") because both earn +2.0 from labels (partial genre + mood vs. exact genre), so energy decides: 0.76 is closer to the 0.80 target than 0.93. Positions #4 and #5 have no genre or mood match and are chosen only for energy, which shows the "rare genre" bias noted above: after the 3 pop-like songs, the catalog has nothing else pop or happy to offer.

Another profile can be run by name, e.g. `python -m src.main "chill lofi"`.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Experiment 1: Weight shift (double energy, halve genre)

**Change:** `ENERGY_WEIGHT` 2.0 → **4.0**, `GENRE_WEIGHT` 2.0 → **1.0** (and partial genre 1.0 → 0.5). The maximum score rises from 6.5 to 7.5.

**Checking the math:** `closeness()` still returns values from 0 to 1, and `max_possible_score()` reads the weight constants, so it updated automatically. I checked that every song's score for all 11 profiles stays between 0 and the maximum, that a perfect match scores exactly 7.5, and that the "+points" in each reason still add up to the total score.

**Results** (top 5 before → after, from `python -m src.main --all`):

| Profile | Before (baseline) | After (experiment) | Verdict |
|---|---|---|---|
| pop/happy, chill lofi, messy input, ghost genre, out-of-range, empty | — | **Identical top 5** | No change |
| conflict: labels vs numbers (pop/happy labels, energy 0.10, valence 0.10) | #1 *Sunrise City* (upbeat pop) | #1 *Winter Sonata No. 3*, then *Empty Train Home*, *Spacewalk Thoughts*: all calm and dark | **More accurate** |
| conflict: high-energy sad (folk/sad labels, energy 0.90) | #1 *Empty Train Home* (energy 0.26) | #1 *Iron Cathedral* (energy 0.97, valence 0.21) | **More accurate** |
| acoustic metalhead | #2 *Banjo Breakdown* (happy bluegrass) | #2 *Storm Runner* | **More accurate** |
| high-energy pop | #5 *Fuego Lento* (latin, playful, valence 0.83) | #5 *Storm Runner* (rock, intense, valence 0.48) | **Less accurate**: a dark rock song in a happy pop list |
| deep intense rock | #4 *Night Drive Loop* (moody) | #4 *Pulse Theory* (edm, euphoric, valence 0.88) | **Less accurate**: a euphoric edm song in a dark rock list |

**More accurate or just different?** Both, depending on the profile:
- **Conflicting profiles improved.** When labels and numbers disagree, the songs that *feel* like what the user asked for now win, instead of songs that only share a label.
- **Normal profiles mostly stayed the same.** The top 3 didn't change for any standard profile, because the right songs win on labels *and* energy.
- **The bottom of normal lists got worse.** With energy worth more than half the maximum score, any loud song can fill an empty slot, whatever its mood. A dark rock song now appears for a happy pop fan, and a euphoric edm song for a dark rock fan.
- **Scores bunch together.** For "high-energy sad", the top 5 scores now span only 0.55 points (4.16–4.71) instead of 2.33. The system becomes less decisive because most loud songs look alike to it.
- **It doesn't fix *Gym Hero*.** It is still #2 for deep intense rock, because that problem comes from its "intense" **mood** label, not the genre weight.

**Decision:** I reverted to the baseline weights (genre 2.0, energy 2.0). The shift fixed the edge cases but made normal recommendations a bit worse. Real users more often have consistent preferences than conflicting ones. A better fix would be to use valence or mood families so that "loud" doesn't automatically mean "good match".

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



