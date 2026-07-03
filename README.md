# 🎵 Music Recommender Simulation

## Project Summary

This project is a small music recommender that scores songs from a CSV catalog against a user’s taste profile (genre, mood, energy, acoustic preference). Each song gets a numeric score based on how well it matches; the highest-scoring songs are recommended with short explanations. It’s a hands-on way to explore how rule-based recommenders work and where their limits are.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo

We’re mainly prioritizing mood + energy where the best signal to noise could aligned with user’s profile. Next following would be genre + acousticness where categorical/structural splits in the data. Lastly is valence, tempo_bpm and danceability is where there’s refinements with the lower weight
 
- What information does your `UserProfile` store

User profile stores the following: favorite_genre, favorite_mood, target_energy, and likes_acoustic 
  
- How does your `Recommender` compute a score for each song

  GENRE_WEIGHT   = 2.0          
	MOOD_WEIGHT    = 1.0          
	ENERGY_WEIGHT  = 1.0   
	ACOUSTIC_WEIGHT = 1.0   

Based on the energy score: energy_score = ENERGY_WEIGHT * (1 - abs(song_energy - target_energy))
  
- How do you choose which songs to recommend

  The recommender scores every song in the catalog against the user’s taste profile, ranks them from highest to lowest score, and returns the top 5. Higher scores mean stronger alignment on genre, mood, energy, and acoustic preference.

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


<img width="640" height="127" alt="Screenshot 2026-07-03 at 1 46 42 AM" src="https://github.com/user-attachments/assets/d4102d5b-4c35-44c9-9f5b-5f38776271d9" />



---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

<img width="552" height="633" alt="Screenshot 2026-07-03 at 1 55 53 AM" src="https://github.com/user-attachments/assets/6b4d5cc0-0b8d-47bc-8c35-76bbba039e40" />


---

## TF Reflection
This project provides an insight of how music platforms could predict what users will love next. The objective is to understand the concept of how music recommendation system operates and following up with an execution. AI demonstrated two different approached that was supportive and misleading, AI supported on providing analysis on recommendation system where it indentifies key features, mapping logic, and designing a scoring logic. The part where AI was misleading is over engineering the content based recommender that includes the scoring and ranking structure. It added unnecessary complexity and features that didn't meet the core objectives. One advice I could provdie to support a student is to keep track of the analysis when exploring the music recommendation system and formulate a structure prompt while applying specific analysis that the student took a note of.  


