# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeMatch 1.0**, a content-based music recommender simulation.

---

## 2. Intended Use  

**Goal / task:** VibeMatch predicts which songs a listener will like best. It picks the top 5 songs from a small catalog that match the listener's taste profile and explains why it chose each one.

**Assumptions about the user:** They can describe their taste with one favorite genre, one favorite mood and a target energy level. Optionally, they can also give a target "happiness" level (valence) and say whether they like acoustic music. Their taste is assumed to stay the same in every situation (studying, working out, driving).

**Intended use:**
- Classroom exploration of how recommender systems turn data into predictions
- Experimenting with scoring weights and testing for bias with made-up profiles

**Not intended for:**
- Real users or real music apps. The catalog is only 20 made-up songs.
- Any decision that matters. There are no input checks, no listening history and no way to learn from feedback.
- Judging real artists or genres. All labels and numbers were assigned by hand.

---

## 3. How the Model Works  

Imagine a judge with a checklist who scores every song in the catalog against your profile:

- **Same genre as your favorite?** +2 points (or +1 if it's close, like "indie pop" for a pop fan)
- **Same mood as your favorite?** +1 point
- **Energy close to what you asked for?** Up to +2 points. The closer, the more points. A song isn't rewarded for being louder or quieter, only for being *near* your target.
- **Happiness (valence) close to what you asked for?** Up to +1 point (only if you set a target)
- **Acoustic or electronic, the way you like it?** +0.5 points

The judge adds up the points, sorts the songs from highest to lowest, and shows you the top 5. Each song comes with the list of checklist items it earned points for, so you can see *why* it was picked. If two songs tie, the one with the closer energy wins.

**Changes from the starter:** the starter code returned songs in file order with a placeholder explanation. I designed the point system above, added the valence and acoustic rules, made genre and mood matching ignore capitals and extra spaces (after testing found a bug), and added a reason for every point awarded.

---

## 4. Data  

- **20 songs** in `data/songs.csv`. Each has a genre, a mood, and five numbers from Spotify-style audio features (energy, tempo, valence, danceability, acousticness).
- **17 genres:** lofi (3 songs), pop (2), and one song each of indie pop, rock, metal, edm, hip-hop, r&b, jazz, classical, folk, country, bluegrass, reggae, latin, ambient and synthwave.
- **16 moods**, including happy, chill, intense, sad, angry, romantic, nostalgic and euphoric.
- **I added 10 songs** (ids 11–20) to the original 10. They cover new genres and moods, and fill two gaps: the original data had no sad, low-energy song and no song that was both high-energy and acoustic.
- **What's missing:** lyrics, language, artist popularity, release era, and anything about *when* or *why* someone listens. All songs, labels and numbers are made up and were assigned by hand, so they reflect one person's judgment of each song's vibe. In this data, energy, tempo, danceability and acousticness also move closely together, so the catalog mostly describes songs along a single calm-to-intense scale.

---

## 5. Strengths  

- **Consistent profiles get great results.** When a user's genre, mood and numbers all point the same way, the top song scores near the maximum (*Library Rain* 6.44/6.50 for chill lofi, *Storm Runner* 6.35/6.50 for deep intense rock).
- **It cleanly separates opposite listeners.** Chill lofi and deep intense rock share no songs in their top 5, and the songs that score high for one score low for the other.
- **The chill lofi results matched my own taste.** The top 5 (*Library Rain*, *Midnight Coding*, *Focus Flow*, *Spacewalk Thoughts*, *Coffee Shop Stories*) are all calm, warm, acoustic songs that fit what I'd want while studying.
- **It explains itself.** Every recommendation lists exactly which rules earned points, so it's easy to see *why* a song was chosen, and easy to spot when the reason is a bad one (like *Gym Hero*'s "intense" label).
- **Rewarding closeness works.** Because energy is scored by distance from the target, a calm-music fan gets calm songs, not just the quietest or loudest ones.

---

## 6. Limitations and Bias 

**Weakness: fans of rare genres get worse recommendations, and fans of common genres get stuck in a bubble.** Lofi has 3 songs and pop has 2, but 14 of the 17 genres have only one song. A lofi fan can earn the +2.0 genre bonus three times in their top 5, while a metal or jazz fan earns it once and the other four slots are filled by energy alone. When I tested every genre against every mood and every energy target from 0.0 to 1.0, lofi fans averaged a top-5 score of 2.95 versus 2.22 for metal fans, about 33% higher for the same kind of request. The extra genre matches also create a filter bubble: the chill lofi profile got three lofi songs (two by the same artist, LoRoom) ahead of *Spacewalk Thoughts*, an ambient song that matched its "chill" mood exactly.

---

## 7. Evaluation  

**How I tested it:**
1. **Profiles:** I ran **4 standard profiles** (pop/happy, chill lofi, high-energy pop, deep intense rock) and **7 adversarial or edge-case profiles**. I asked my AI assistant to suggest the edge cases so I could see whether the scoring could be tricked: conflicting preferences, a genre that isn't in the catalog, messy input, impossible values and an empty profile.
2. **Comparisons:** I compared profiles in pairs to check whether the differences in their top 5 made sense (see "Comparing profiles side by side" below).
3. **Gut check:** I compared the chill lofi results with my own taste.
4. **Experiment:** I doubled the energy weight and halved the genre weight, then compared every profile's top 5 before and after. It fixed the contradictory profiles but let loud songs with the wrong mood into normal lists, so I kept the original weights. (Full details are in the README under "Experiments You Tried".)
5. **Tests:** `python3 -m pytest` checks that the `Recommender` class ranks the matching song first and always returns an explanation.

All profiles are defined in `src/main.py`. Run one with `python3 -m src.main "<profile name>"`, or all of them with `python3 -m src.main --all`. The outputs below are pasted directly from the terminal.

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

### What surprised me

- **One song kept showing up everywhere.** *Gym Hero* appeared in the top 5 for 7 of my 11 profiles, including a dark-rock fan and a fan of "sad" music. I expected each profile to get its own set of songs. (Explained below.)
- **Labels beat the vibe.** "Deep intense rock" and "high-energy sad" ask for the same loud, dark sound, and **4 of their 5 results are the same songs**. But "folk / sad" put a *quiet* folk song (energy 0.26) at #1 for a user who asked for energy 0.90. Two words in the profile outweighed the actual sound.

**Other things I noticed:**
- **A small input mistake changed the results.** Typing `" LOFI "` instead of `"lofi"` quietly cost every lofi song a full point, until it was fixed. It was only caught because we tested messy input on purpose.
- **Big weight changes barely moved normal results.** Doubling the energy weight didn't change the top 3 for any normal profile. The weights mostly matter when a user's preferences contradict each other.
- **Comparing with my own taste:** the **chill lofi** results feel right to me. All five are calm, acoustic songs I'd actually put on while studying.

### Why does *Gym Hero* keep showing up for people who just want "Happy Pop"?

Think of the recommender as a judge holding a checklist rather than someone actually listening to the song. For a "happy pop" fan, the checklist asks: *Is it pop? Is it happy? Is its energy level close to what you asked for?* *Gym Hero* is filed under **pop**, which earns it the biggest prize (2 points). It's also one of the most energetic songs in the catalog (0.93 out of 1.0), so it earns almost full energy points for anyone who wants upbeat music. It only fails one item, because its mood label is "intense" rather than "happy". That's worth just 1 point, which isn't enough to push it out. The judge can't hear that *Gym Hero* is a workout anthem rather than a feel-good song. It only sees "pop + very high energy" and scores it well. The same reasons put it in the rock fan's list: there it matches the "intense" mood label and the high energy, even though it isn't rock. A song with a common genre, a common mood label and extreme energy ends up as a strong second choice for almost every high-energy listener.

### Comparing profiles side by side

**pop/happy vs. high-energy pop**: Same top 3 songs, but *Gym Hero* moves up from #3 to #2. The high-energy profile asks for energy 0.92 instead of 0.80, and *Gym Hero* (0.93) is the closest match. The bright edm song *Pulse Theory* also enters at #4 because this profile also asks for a happy sound (valence 0.85) and non-acoustic music. *This makes sense: turning up the energy dial rewards the loudest pop songs.*

**pop/happy vs. chill lofi**: No songs in common at all. One asks for energy 0.80 and the other for 0.38, which splits the catalog into a loud half and a quiet half. The lofi list is also all acoustic (0.71–0.92 acousticness), while the pop list is all electronic (0.35 or below). *This makes sense: these are opposite listeners, and the system treats them that way.*

**pop/happy vs. deep intense rock**: Both want loud music, so they share two songs (*Gym Hero*, *Concrete Verses*). The rock profile also asks for a dark sound (valence 0.35), so the cheerful songs (*Sunrise City*, *Rooftop Lights*) drop out and darker ones (*Iron Cathedral*, *Night Drive Loop*) come in. *This makes sense: energy decides which half of the catalog you're in, and valence decides happy vs. dark within it.*

**high-energy pop vs. deep intense rock**: These two ask for almost the same energy (0.92 vs. 0.90) and both dislike acoustic music, so only genre, mood and happy-vs-dark separate them. The pop list is bright (*Sunrise City*, *Pulse Theory*, *Fuego Lento*) and the rock list is dark (*Storm Runner*, *Iron Cathedral*, *Night Drive Loop*). *Mostly valid, except that *Gym Hero* is #2 in both lists.* It matches "pop" for one profile and "intense" for the other.

**high-energy pop vs. chill lofi**: Complete opposites with zero overlap, and both #1 songs score almost perfectly (6.29 and 6.44 out of 6.50). *This shows the system serves loud and quiet listeners equally well when their preferences are consistent.*

**chill lofi vs. deep intense rock**: Zero overlap. *Library Rain* scores 6.44 for the lofi fan but only 1.65 for the rock fan, and *Storm Runner* is the reverse (6.35 for the rock fan, 1.82 for the lofi fan). *This is the clearest sign the scoring works: every feature points in opposite directions, so the scores do too.*

**pop/happy vs. conflict: labels vs. numbers**: Same labels (pop, happy), but the second profile asks for very calm, dark music. *Sunrise City* stays #1 because of its labels. Then quiet, sad songs (*Winter Sonata No. 3*, *Empty Train Home*) take #2–3, followed by more upbeat pop. *The result is half one list and half the other, and it doesn't serve either listener well. It shows that labels (+3.0) outweigh the energy rule (max +2.0).*

**deep intense rock vs. conflict: high-energy sad**: Both ask for loud, dark music, and 4 of their 5 songs are the same (*Iron Cathedral*, *Storm Runner*, *Night Drive Loop*, *Gym Hero*). The only difference is #1: "folk / sad" puts *Empty Train Home* on top, a quiet song with energy 0.26 when the user asked for 0.90. *Mathematically correct, but musically wrong: two text labels beat the actual sound.*

**deep intense rock vs. acoustic metalhead**: Both are loud and dark. The metalhead gets *Iron Cathedral* at #1 (metal + angry). The only new song is *Banjo Breakdown* at #2, the one song in the catalog that is both high-energy and acoustic. *This makes sense for "loud but acoustic", even though the banjo song's cheerful mood doesn't fit a metal fan.*

**pop/happy vs. ghost genre (k-pop)**: Same mood and energy, but "k-pop" isn't in the catalog. The top 2 are the same songs in the same order, but lower: *Sunrise City* loses its full 2-point genre bonus (4.96 → 2.96) and *Rooftop Lights* loses its 1-point partial bonus (3.92 → 2.92). *Gym Hero* drops out because without the pop bonus it has nothing left except energy. *This makes sense: with no genre to match, mood and energy decide.*

**chill lofi vs. messy input**: The messy profile types `" LOFI "` and `"Chill"` and leaves out valence and acoustic preference. After the bug fix, it gives the same top 5 in the same order, just with a lower maximum (5.0 instead of 6.5). *This shows the fix works: capitals and extra spaces no longer change the results.*

**high-energy pop vs. out-of-range values**: Both want loud, electronic music, but the out-of-range profile asks for impossible values (energy 1.5, valence −0.5). Its #1 (*Pulse Theory*, an edm/euphoric match) still makes sense, but scores collapse to 0.68–1.23 for #2–5 because no song can be close to an impossible target. *The system doesn't crash or warn. It just quietly gives weaker results, which a real app should catch.*

**any profile vs. empty profile**: With no preferences, every song scores 0, so the list is simply alphabetical (*Banjo Breakdown*, *Coffee Shop Stories*, …). *This confirms that every ranking in the other profiles comes entirely from the user's preferences. With no preferences, the system has nothing to go on, so it shouldn't present this list as a recommendation.*

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

- **Group related moods** (e.g. chill/relaxed/focused = "calm", intense/angry = "aggressive") and give partial credit, so near-synonyms count and misleading labels like *Gym Hero*'s "intense" matter less.
- **Let users list more than one favorite genre and mood**, so someone who likes lofi *and* jazz can say so.
- **Add a diversity rule** to the ranking step, e.g. at most one song per artist in the top 5, to break the filter bubble.
- **Check inputs.** Reject values outside 0–1, and return a "tell me more about your taste" message for empty profiles instead of an alphabetical list.
- **Balance labels against sound.** Lower the genre weight or raise energy and valence when they conflict with the labels. My experiment showed this fixes contradictory profiles but needs care so normal lists don't fill up with loud songs that have the wrong mood.
- **Grow the catalog** so every genre has several songs, and eventually add listening history to combine content-based and collaborative filtering, the way real platforms do.

---

## 9. Personal Reflection  

**Biggest learning moment:** I asked for loud, sad music and got a quiet folk song at #1. That's when I understood that a recommender doesn't "hear" anything. It's mostly a scoring rule plus a ranking rule, and small choices, like giving genre 2 points instead of 1, decide what a user actually sees. Two words in my profile ("folk" and "sad") outweighed the energy level I asked for. *Gym Hero* showing up for very different listeners came from the same problem.

**How AI helped, and when I had to double-check:** I did every step in one chat with an AI coding assistant. It was most useful for explaining concepts before any code was written, like collaborative vs. content-based filtering and why scoring by closeness works better than "higher is better." Testing with strange and contradictory profiles it suggested is how most of the problems were found, including a bug where extra spaces in "LOFI" cost songs a full point. I still had to run things myself to check them. The test command didn't work on my Mac until I used `python3 -m pytest`, and a set of commands it gave me failed because the `#` comments broke them in my terminal.

**How simple algorithms can still "feel" like recommendations:** The whole system is just adding up a few points per song, but the chill lofi list still felt right to me, like something a real app would give me. It surprised me that something so simple could feel personal. It also made me realize that the "same stuff repeating" I notice in my own recommendations is probably what happens when a system keeps rewarding matches to what I already like. Before this project, I had never thought about how apps like Spotify pick songs.

**What I'd try next:** I'd group similar moods (like chill, relaxed and focused) so near-matches get partial credit, and I'd add a rule that allows only one song per artist in the top 5 to break the filter bubble. I'd also add more songs so every genre has more than one option.
