# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

I tested the recommender with **3 standard profiles** (plus the default pop/happy profile shown in the README) and **7 adversarial or edge-case profiles**. The edge cases were suggested in a separate "System Evaluation" chat to see whether the scoring logic could be tricked. All profiles are defined in `src/main.py`. Run one with `python -m src.main "<profile name>"`, or all of them with `python -m src.main --all`. The outputs below are pasted directly from the terminal.

| Profile | What it tests | Result |
|---|---|---|
| pop/happy (default) | Starter profile | ✅ as expected (see README) |
| high-energy pop | Bright, loud, electronic pop | ✅ as expected |
| chill lofi | Calm, acoustic study music | ✅ as expected |
| deep intense rock | Dark, heavy, driving rock | ⚠️ mood label pulls in *Gym Hero* |
| conflict: high-energy sad | Labels ask for sad folk, numbers ask for energy 0.90. | ❌ labels override energy |
| conflict: labels vs numbers | Labels ask for happy pop, numbers ask for very calm and dark music. | ❌ labels override energy and valence |
| acoustic metalhead | A metal fan who prefers acoustic sound. | ⚠️ small bonus changes the order |
| ghost genre (k-pop) | A genre that isn't in the catalog. | ✅ falls back to mood + energy |
| messy input | Wrong capitalization and extra spaces (`" LOFI "`, `"Chill"`). | 🐛 bug found and fixed |
| out-of-range values | energy 1.50 and valence -0.50 (valid range is 0.0-1.0). | ⚠️ no input checks |
| empty profile | No preferences at all. | ⚠️ returns alphabetical songs |

### Standard profiles

#### high-energy pop

**As expected.** All three pop-family songs fill the top 3. *Gym Hero* moves up to #2 here (it was #3 for the plain pop/happy profile) because the higher energy target (0.92) rewards its 0.93 energy. #4 and #5 (*Pulse Theory*, *Fuego Lento*) match neither label but are bright and high-energy, so the numbers alone found songs that fit the vibe.

```
Loaded songs: 20

Profile: high-energy pop
  genre=pop | mood=happy | energy=0.92 | valence=0.85 | acoustic=False

Top 5 recommendations
================================================================
#1  Sunrise City - Neon Echo                  Score: 6.29 / 6.50
     pop, happy, energy 0.82
     + genre match: pop (+2.0)
     + mood match: happy (+1.0)
     + energy 0.82 vs your 0.92 (+1.80)
     + valence 0.84 vs your 0.85 (+0.99)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#2  Gym Hero - Max Pulse                      Score: 5.40 / 6.50
     pop, intense, energy 0.93
     + genre match: pop (+2.0)
     + energy 0.93 vs your 0.92 (+1.98)
     + valence 0.77 vs your 0.85 (+0.92)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#3  Rooftop Lights - Indigo Parade            Score: 5.14 / 6.50
     indie pop, happy, energy 0.76
     + partial genre match: indie pop ~ pop (+1.0)
     + mood match: happy (+1.0)
     + energy 0.76 vs your 0.92 (+1.68)
     + valence 0.81 vs your 0.85 (+0.96)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#4  Pulse Theory - Kilowatt Kids              Score: 3.41 / 6.50
     edm, euphoric, energy 0.95
     + energy 0.95 vs your 0.92 (+1.94)
     + valence 0.88 vs your 0.85 (+0.97)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#5  Fuego Lento - Brisa Roja                  Score: 3.24 / 6.50
     latin, playful, energy 0.80
     + energy 0.80 vs your 0.92 (+1.76)
     + valence 0.83 vs your 0.85 (+0.98)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
```

#### chill lofi

**As expected.** All three lofi songs rank first, with scores close to the 6.50 maximum. The predicted bias appears: *Focus Flow* (lofi, "focused") ranks above *Spacewalk Thoughts* (ambient, "chill") because the genre match is worth more than the mood match.

```
Loaded songs: 20

Profile: chill lofi
  genre=lofi | mood=chill | energy=0.38 | valence=0.60 | acoustic=True

Top 5 recommendations
================================================================
#1  Library Rain - Paper Lanterns             Score: 6.44 / 6.50
     lofi, chill, energy 0.35
     + genre match: lofi (+2.0)
     + mood match: chill (+1.0)
     + energy 0.35 vs your 0.38 (+1.94)
     + valence 0.60 vs your 0.60 (+1.00)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#2  Midnight Coding - LoRoom                  Score: 6.38 / 6.50
     lofi, chill, energy 0.42
     + genre match: lofi (+2.0)
     + mood match: chill (+1.0)
     + energy 0.42 vs your 0.38 (+1.92)
     + valence 0.56 vs your 0.60 (+0.96)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#3  Focus Flow - LoRoom                       Score: 5.45 / 6.50
     lofi, focused, energy 0.40
     + genre match: lofi (+2.0)
     + energy 0.40 vs your 0.38 (+1.96)
     + valence 0.59 vs your 0.60 (+0.99)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#4  Spacewalk Thoughts - Orbit Bloom          Score: 4.25 / 6.50
     ambient, chill, energy 0.28
     + mood match: chill (+1.0)
     + energy 0.28 vs your 0.38 (+1.80)
     + valence 0.65 vs your 0.60 (+0.95)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#5  Coffee Shop Stories - Slow Stereo         Score: 3.37 / 6.50
     jazz, relaxed, energy 0.37
     + energy 0.37 vs your 0.38 (+1.98)
     + valence 0.71 vs your 0.60 (+0.89)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
```

#### deep intense rock

**Partly as expected.** *Storm Runner* is a clear #1. But *Gym Hero*, a bright pop song (valence 0.77), ranks #2 only because its mood label is "intense". *Iron Cathedral* (metal, angry, valence 0.21) feels closer to dark rock but ranks #3, because the exact mood label outweighs how the song actually sounds.

```
Loaded songs: 20

Profile: deep intense rock
  genre=rock | mood=intense | energy=0.90 | valence=0.35 | acoustic=False

Top 5 recommendations
================================================================
#1  Storm Runner - Voltline                   Score: 6.35 / 6.50
     rock, intense, energy 0.91
     + genre match: rock (+2.0)
     + mood match: intense (+1.0)
     + energy 0.91 vs your 0.90 (+1.98)
     + valence 0.48 vs your 0.35 (+0.87)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#2  Gym Hero - Max Pulse                      Score: 4.02 / 6.50
     pop, intense, energy 0.93
     + mood match: intense (+1.0)
     + energy 0.93 vs your 0.90 (+1.94)
     + valence 0.77 vs your 0.35 (+0.58)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#3  Iron Cathedral - Grave Signal             Score: 3.22 / 6.50
     metal, angry, energy 0.97
     + energy 0.97 vs your 0.90 (+1.86)
     + valence 0.21 vs your 0.35 (+0.86)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#4  Night Drive Loop - Neon Echo              Score: 3.06 / 6.50
     synthwave, moody, energy 0.75
     + energy 0.75 vs your 0.90 (+1.70)
     + valence 0.49 vs your 0.35 (+0.86)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
#5  Concrete Verses - Block Theory            Score: 2.99 / 6.50
     hip-hop, confident, energy 0.78
     + energy 0.78 vs your 0.90 (+1.76)
     + valence 0.62 vs your 0.35 (+0.73)
     + electronic sound, as you prefer (+0.5)
----------------------------------------------------------------
```

### Adversarial / edge-case profiles

#### conflict: high-energy sad

*Tests:* Labels ask for sad folk, numbers ask for energy 0.90.

**Tricked.** *Empty Train Home* ranks #1 even though its energy (0.26) is far from the 0.90 target: genre + mood (+3.0) outweigh the energy rule (max +2.0). No song in the catalog is both loud and sad. *Iron Cathedral* (#2, energy 0.97, valence 0.21) is the closest real fit.

```
Loaded songs: 20

Profile: conflict: high-energy sad
  genre=folk | mood=sad | energy=0.90 | valence=0.20

Top 5 recommendations
================================================================
#1  Empty Train Home - Hollow Pines           Score: 4.70 / 6.00
     folk, sad, energy 0.26
     + genre match: folk (+2.0)
     + mood match: sad (+1.0)
     + energy 0.26 vs your 0.90 (+0.72)
     + valence 0.18 vs your 0.20 (+0.98)
----------------------------------------------------------------
#2  Iron Cathedral - Grave Signal             Score: 2.85 / 6.00
     metal, angry, energy 0.97
     + energy 0.97 vs your 0.90 (+1.86)
     + valence 0.21 vs your 0.20 (+0.99)
----------------------------------------------------------------
#3  Storm Runner - Voltline                   Score: 2.70 / 6.00
     rock, intense, energy 0.91
     + energy 0.91 vs your 0.90 (+1.98)
     + valence 0.48 vs your 0.20 (+0.72)
----------------------------------------------------------------
#4  Night Drive Loop - Neon Echo              Score: 2.41 / 6.00
     synthwave, moody, energy 0.75
     + energy 0.75 vs your 0.90 (+1.70)
     + valence 0.49 vs your 0.20 (+0.71)
----------------------------------------------------------------
#5  Gym Hero - Max Pulse                      Score: 2.37 / 6.00
     pop, intense, energy 0.93
     + energy 0.93 vs your 0.90 (+1.94)
     + valence 0.77 vs your 0.20 (+0.43)
----------------------------------------------------------------
```

#### conflict: labels vs numbers

*Tests:* Labels ask for happy pop, numbers ask for very calm and dark music.

**Tricked.** *Sunrise City* (energy 0.82, valence 0.84) ranks #1 for a user who wants energy 0.10 and valence 0.10. The +3.0 from labels outweighs songs that match the requested feel, such as *Winter Sonata No. 3* and *Empty Train Home* (#2 and #3).

```
Loaded songs: 20

Profile: conflict: labels vs numbers
  genre=pop | mood=happy | energy=0.10 | valence=0.10 | acoustic=True

Top 5 recommendations
================================================================
#1  Sunrise City - Neon Echo                  Score: 3.82 / 6.50
     pop, happy, energy 0.82
     + genre match: pop (+2.0)
     + mood match: happy (+1.0)
     + energy 0.82 vs your 0.10 (+0.56)
     + valence 0.84 vs your 0.10 (+0.26)
----------------------------------------------------------------
#2  Winter Sonata No. 3 - Ellery Quartet      Score: 3.12 / 6.50
     classical, melancholic, energy 0.22
     + energy 0.22 vs your 0.10 (+1.76)
     + valence 0.24 vs your 0.10 (+0.86)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#3  Empty Train Home - Hollow Pines           Score: 3.10 / 6.50
     folk, sad, energy 0.26
     + energy 0.26 vs your 0.10 (+1.68)
     + valence 0.18 vs your 0.10 (+0.92)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#4  Rooftop Lights - Indigo Parade            Score: 2.97 / 6.50
     indie pop, happy, energy 0.76
     + partial genre match: indie pop ~ pop (+1.0)
     + mood match: happy (+1.0)
     + energy 0.76 vs your 0.10 (+0.68)
     + valence 0.81 vs your 0.10 (+0.29)
----------------------------------------------------------------
#5  Gym Hero - Max Pulse                      Score: 2.67 / 6.50
     pop, intense, energy 0.93
     + genre match: pop (+2.0)
     + energy 0.93 vs your 0.10 (+0.34)
     + valence 0.77 vs your 0.10 (+0.33)
----------------------------------------------------------------
```

#### acoustic metalhead

*Tests:* A metal fan who prefers acoustic sound.

**Mostly fine, one surprise.** *Iron Cathedral* is #1. *Banjo Breakdown* (bluegrass, happy) comes in at #2, ahead of *Storm Runner*, because its +0.5 acoustic bonus outweighs a big valence mismatch (0.80 vs 0.20). A small bonus can still change the order.

```
Loaded songs: 20

Profile: acoustic metalhead
  genre=metal | mood=angry | energy=0.95 | valence=0.20 | acoustic=True

Top 5 recommendations
================================================================
#1  Iron Cathedral - Grave Signal             Score: 5.95 / 6.50
     metal, angry, energy 0.97
     + genre match: metal (+2.0)
     + mood match: angry (+1.0)
     + energy 0.97 vs your 0.95 (+1.96)
     + valence 0.21 vs your 0.20 (+0.99)
----------------------------------------------------------------
#2  Banjo Breakdown - Copper Hollow           Score: 2.68 / 6.50
     bluegrass, energetic, energy 0.84
     + energy 0.84 vs your 0.95 (+1.78)
     + valence 0.80 vs your 0.20 (+0.40)
     + acoustic sound, as you prefer (+0.5)
----------------------------------------------------------------
#3  Storm Runner - Voltline                   Score: 2.64 / 6.50
     rock, intense, energy 0.91
     + energy 0.91 vs your 0.95 (+1.92)
     + valence 0.48 vs your 0.20 (+0.72)
----------------------------------------------------------------
#4  Gym Hero - Max Pulse                      Score: 2.39 / 6.50
     pop, intense, energy 0.93
     + energy 0.93 vs your 0.95 (+1.96)
     + valence 0.77 vs your 0.20 (+0.43)
----------------------------------------------------------------
#5  Pulse Theory - Kilowatt Kids              Score: 2.32 / 6.50
     edm, euphoric, energy 0.95
     + energy 0.95 vs your 0.95 (+2.00)
     + valence 0.88 vs your 0.20 (+0.32)
----------------------------------------------------------------
```

#### ghost genre (k-pop)

*Tests:* A genre that isn't in the catalog.

**Handled reasonably.** No genre points are awarded, so mood and energy take over and the results are upbeat pop. Partial matching splits only on spaces, so "k-pop" does not partially match "pop".

```
Loaded songs: 20

Profile: ghost genre (k-pop)
  genre=k-pop | mood=happy | energy=0.80

Top 5 recommendations
================================================================
#1  Sunrise City - Neon Echo                  Score: 2.96 / 5.00
     pop, happy, energy 0.82
     + mood match: happy (+1.0)
     + energy 0.82 vs your 0.80 (+1.96)
----------------------------------------------------------------
#2  Rooftop Lights - Indigo Parade            Score: 2.92 / 5.00
     indie pop, happy, energy 0.76
     + mood match: happy (+1.0)
     + energy 0.76 vs your 0.80 (+1.92)
----------------------------------------------------------------
#3  Fuego Lento - Brisa Roja                  Score: 2.00 / 5.00
     latin, playful, energy 0.80
     + energy 0.80 vs your 0.80 (+2.00)
----------------------------------------------------------------
#4  Concrete Verses - Block Theory            Score: 1.96 / 5.00
     hip-hop, confident, energy 0.78
     + energy 0.78 vs your 0.80 (+1.96)
----------------------------------------------------------------
#5  Banjo Breakdown - Copper Hollow           Score: 1.92 / 5.00
     bluegrass, energetic, energy 0.84
     + energy 0.84 vs your 0.80 (+1.92)
----------------------------------------------------------------
```

#### messy input

*Tests:* Wrong capitalization and extra spaces (`" LOFI "`, `"Chill"`).

**Bug found and fixed.** Before the fix, `" LOFI "` earned only the *partial* genre match (+1.0 instead of +2.0) because spaces weren't trimmed, and Library Rain scored 3.94 instead of 4.94. `score_song` now applies `strip().lower()` to genre and mood. The output below is after the fix.

```
Loaded songs: 20

Profile: messy input
  genre= LOFI  | mood=Chill | energy=0.38

Top 5 recommendations
================================================================
#1  Library Rain - Paper Lanterns             Score: 4.94 / 5.00
     lofi, chill, energy 0.35
     + genre match: lofi (+2.0)
     + mood match: chill (+1.0)
     + energy 0.35 vs your 0.38 (+1.94)
----------------------------------------------------------------
#2  Midnight Coding - LoRoom                  Score: 4.92 / 5.00
     lofi, chill, energy 0.42
     + genre match: lofi (+2.0)
     + mood match: chill (+1.0)
     + energy 0.42 vs your 0.38 (+1.92)
----------------------------------------------------------------
#3  Focus Flow - LoRoom                       Score: 3.96 / 5.00
     lofi, focused, energy 0.40
     + genre match: lofi (+2.0)
     + energy 0.40 vs your 0.38 (+1.96)
----------------------------------------------------------------
#4  Spacewalk Thoughts - Orbit Bloom          Score: 2.80 / 5.00
     ambient, chill, energy 0.28
     + mood match: chill (+1.0)
     + energy 0.28 vs your 0.38 (+1.80)
----------------------------------------------------------------
#5  Coffee Shop Stories - Slow Stereo         Score: 1.98 / 5.00
     jazz, relaxed, energy 0.37
     + energy 0.37 vs your 0.38 (+1.98)
----------------------------------------------------------------
```

#### out-of-range values

*Tests:* energy 1.50 and valence -0.50 (valid range is 0.0-1.0).

**Silently accepted.** There's no input check. Every song earns 0 valence points (the closeness score bottoms out at 0), so valence is effectively ignored, and energy closeness still "works" against an impossible target. The top pick is still sensible (*Pulse Theory*, an edm/euphoric match), but only because of the labels.

```
Loaded songs: 20

Profile: out-of-range values
  genre=edm | mood=euphoric | energy=1.50 | valence=-0.50

Top 5 recommendations
================================================================
#1  Pulse Theory - Kilowatt Kids              Score: 3.90 / 6.00
     edm, euphoric, energy 0.95
     + genre match: edm (+2.0)
     + mood match: euphoric (+1.0)
     + energy 0.95 vs your 1.50 (+0.90)
     + valence 0.88 vs your -0.50 (+0.00)
----------------------------------------------------------------
#2  Iron Cathedral - Grave Signal             Score: 1.23 / 6.00
     metal, angry, energy 0.97
     + energy 0.97 vs your 1.50 (+0.94)
     + valence 0.21 vs your -0.50 (+0.29)
----------------------------------------------------------------
#3  Gym Hero - Max Pulse                      Score: 0.86 / 6.00
     pop, intense, energy 0.93
     + energy 0.93 vs your 1.50 (+0.86)
     + valence 0.77 vs your -0.50 (+0.00)
----------------------------------------------------------------
#4  Storm Runner - Voltline                   Score: 0.84 / 6.00
     rock, intense, energy 0.91
     + energy 0.91 vs your 1.50 (+0.82)
     + valence 0.48 vs your -0.50 (+0.02)
----------------------------------------------------------------
#5  Banjo Breakdown - Copper Hollow           Score: 0.68 / 6.00
     bluegrass, energetic, energy 0.84
     + energy 0.84 vs your 1.50 (+0.68)
     + valence 0.80 vs your -0.50 (+0.00)
----------------------------------------------------------------
```

#### empty profile

*Tests:* No preferences at all.

**Misleading.** Every song scores 0.00, so the tie-break (title order) decides, and the "recommendations" are just the first 5 songs alphabetically. The system should probably say it has nothing to go on instead of returning a list.

```
Loaded songs: 20

Profile: empty profile
  (no preferences)

Top 5 recommendations
================================================================
#1  Banjo Breakdown - Copper Hollow           Score: 0.00 / 0.00
     bluegrass, energetic, energy 0.84
     + (no matching rules)
----------------------------------------------------------------
#2  Coffee Shop Stories - Slow Stereo         Score: 0.00 / 0.00
     jazz, relaxed, energy 0.37
     + (no matching rules)
----------------------------------------------------------------
#3  Concrete Verses - Block Theory            Score: 0.00 / 0.00
     hip-hop, confident, energy 0.78
     + (no matching rules)
----------------------------------------------------------------
#4  Dusty Porch Light - Willow Creek Band     Score: 0.00 / 0.00
     country, nostalgic, energy 0.52
     + (no matching rules)
----------------------------------------------------------------
#5  Empty Train Home - Hollow Pines           Score: 0.00 / 0.00
     folk, sad, energy 0.26
     + (no matching rules)
----------------------------------------------------------------
```

### Key findings

- **Typical profiles work well.** When the labels and numbers agree, the top results match what I'd expect.
- **Labels can override the vibe.** When labels and numbers conflict, genre + mood (+3.0) beat energy (max +2.0), so the system can recommend songs that feel nothing like what the user asked for.
- **Exact mood labels can mislead.** *Gym Hero*'s "intense" label puts an upbeat pop song in a dark-rock list.
- **Input isn't validated.** Messy text (now fixed), out-of-range numbers and empty profiles are all accepted without warning.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
