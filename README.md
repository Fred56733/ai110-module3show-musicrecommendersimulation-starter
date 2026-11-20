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

### Algorithm Recipe

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

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



