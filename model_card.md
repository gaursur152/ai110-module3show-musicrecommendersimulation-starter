# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

A content-based music recommender that matches songs to a user's taste profile using audio features and genre/mood preferences.

---

## 2. Intended Use

VibeFinder is designed to suggest songs from a small catalog based on a user's stated preferences.

- It generates a ranked list of the top 5 most compatible songs for a given user profile.
- It assumes the user knows their preferred genre, mood, energy level, and whether they like acoustic music.
- This is a classroom simulation — not a production app. It is meant to explore how real recommenders like Spotify work, not to replace them.

**Not intended for:** real music discovery at scale, users with complex or shifting tastes, or any catalog larger than a few hundred songs without retuning the weights.

---

## 3. How the Model Works

Every song in the catalog gets a score between 0.0 and 1.0. Higher score = better match.

The score has five parts:

- **Genre match (+0.175):** If the song's genre matches the user's favorite genre, it gets points. No partial credit.
- **Mood match (+0.20):** Same idea — matches get full points, misses get zero.
- **Energy proximity (+0.40):** Uses the formula `1 - |song energy - target energy|`. Closer to the user's target = higher score. A song is not rewarded for being high or low energy — only for being *close* to what the user wants.
- **Acousticness proximity (+0.15):** The user's `likes_acoustic` boolean converts to a target of 0.8 (yes) or 0.2 (no). Same proximity formula applies.
- **Tempo proximity (+0.075):** Tempo is normalized to a 0–1 scale using 200 BPM as the ceiling, then scored by proximity.

The final score is the sum of all five components. Songs are ranked highest to lowest and the top 5 are returned with an explanation of every point awarded.

One key change from the starter: genre weight was reduced from 0.35 to 0.175 and energy was doubled from 0.20 to 0.40, making audio features more competitive against categorical matches.

---

## 4. Data

- **Catalog size:** 18 songs.
- **Original dataset:** 10 starter songs. Added 8 new songs to improve diversity.
- **Genres represented (15):** lofi, pop, rock, ambient, synthwave, jazz, indie pop, hip-hop, classical, electronic, r&b, metal, folk, blues, country.
- **Moods represented (14):** happy, chill, intense, relaxed, focused, moody, energetic, melancholic, romantic, angry, nostalgic, uplifting, sad.
- **Each song has:** id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness.

**Missing from the dataset:**
- No non-English language or international genres (reggae, latin, K-pop, world music).
- Lofi is overrepresented with 3 songs. Most genres have only 1 entry.
- Valence and danceability are tracked on each song but never scored against a user preference.
- No context signals like time of day, activity, or listening session history.

---

## 5. Strengths

- Works well for users whose favorite genre appears multiple times in the catalog (lofi users get meaningful competition between songs).
- The proximity formula correctly rewards "closest match" over "highest value" — a user wanting energy 0.4 gets low-energy songs, not high-energy ones.
- The reasons list makes every score fully transparent — you can see exactly why a song ranked where it did.
- The system degrades gracefully when no genre match exists (Ghost profile) — it still returns 5 results using audio proximity alone without crashing.

---

## 6. Limitations and Bias

- **Catalog is too small for genre weight to be fair.** Most genres have only one song, so a genre match is almost always a guaranteed #1 regardless of audio fit.
- **The Contradiction problem.** A slow, quiet blues song ranked #1 for a user who wanted loud, fast music — because it was the only blues/sad song. Genre + mood combined still outweighed completely wrong audio features even after rebalancing.
- **Mid-range preferences produce a mushy ranking.** When target energy is 0.5, many songs cluster within 0.01 of each other in score. The ranking feels arbitrary below #1 or #2.
- **Valence and danceability are ignored.** A user who wants upbeat, danceable songs has no way to express that through the current UserProfile.
- **No cold-start handling for users.** If a user has never stated preferences, the system has nothing to work with.

---

## 7. Evaluation

**Profiles tested:**
- Three standard profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock.
- Four adversarial profiles: Contradiction (conflicting preferences), Ghost (genre not in catalog), Extremist (everything maxed), Middleman (all mid-range values).

**What I looked for:**
- Whether the #1 result made musical sense for each profile.
- Whether scores spread out meaningfully or clustered too tightly.
- Whether the reasons list correctly explained each component.
- Whether songs with no genre match could still surface via audio proximity.

**What surprised me:**
- Genre dominance was stronger than expected. Even after halving the genre weight, a genre+mood match still almost always won — showing that categorical weights are structurally powerful even when reduced.
- Doubling energy made a visible difference: the gap between #1 and #2 in the Contradiction profile shrank from 0.34 to 0.076, meaning audio-compatible songs became genuinely competitive.

**Weight experiment:**
Ran all profiles twice — once with original weights (genre: 0.35, energy: 0.20) and once with rebalanced weights (genre: 0.175, energy: 0.40, tempo: 0.075). Compared scores and rankings directly.

---

## 8. Future Work

1. **Add valence and danceability to UserProfile.** These are already tracked on every song. Letting users express a preference for "happy-sounding" or "danceable" songs would make the scoring richer and more personal.

2. **Expand the catalog to at least 5 songs per genre.** With only one song per genre in most cases, genre match is winner-takes-all. A larger catalog would let audio features do real separating work within a genre cluster — which is how Spotify's system actually operates.

3. **Add a diversity penalty for repeated artists.** Currently the top 5 can include multiple songs from the same artist (e.g., two LoRoom tracks). A real recommender penalizes this to ensure variety in the results.

---

## 9. Personal Reflection

Building this showed me that recommendation is less about finding the "best" song in the world and more about finding the best song. The scoring formula forces you to make explicit decisions how much does genre matter compared to energy?that streaming apps make invisibly behind the scenes.



---
