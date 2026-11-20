import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Columns that must be converted from CSV text to numbers so we can do math with them.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

# Algorithm Recipe weights (see README "Algorithm Recipe"). Max total = 6.5.
GENRE_WEIGHT = 2.0          # exact genre match
PARTIAL_GENRE_WEIGHT = 1.0  # shared word, e.g. "pop" vs "indie pop"
MOOD_WEIGHT = 1.0           # exact mood match
ENERGY_WEIGHT = 2.0         # max points for energy closeness
VALENCE_WEIGHT = 1.0        # max points for valence closeness
ACOUSTIC_WEIGHT = 0.5       # acoustic preference matches
ACOUSTIC_THRESHOLD = 0.5    # acousticness >= this counts as "acoustic"


def closeness(value: float, target: float, value_range: float = 1.0) -> float:
    """Return 1.0 for a perfect match, falling linearly to 0.0 as value moves away from target."""
    return max(0.0, 1.0 - abs(value - target) / value_range)

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None  # optional: skipped in scoring when None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of Song objects to recommend from."""
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        """Convert a UserProfile into the user_prefs dict used by score_song (drops unset fields)."""
        return {key: value for key, value in asdict(user).items() if value is not None}

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, using the same ranking rule as recommend_songs."""
        by_id = {song.id: song for song in self.songs}
        ranked = recommend_songs(self._prefs(user), [asdict(song) for song in self.songs], k)
        return [by_id[song_dict["id"]] for song_dict, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation listing the score and each rule that awarded points."""
        score, reasons = score_song(self._prefs(user), asdict(song))
        if not reasons:
            return f"Score {score:.2f}: no preferences matched this song."
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting id to int and audio features to float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            song = {key: value.strip() for key, value in row.items()}
            for field in INT_FIELDS:
                song[field] = int(song[field])
            for field in FLOAT_FIELDS:
                song[field] = float(song[field])
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user_prefs and return (score, reasons) listing each rule's points."""
    score = 0.0
    reasons: List[str] = []

    # Rule 1: genre (+2.0 exact, +1.0 partial such as "pop" vs "indie pop")
    # Normalize text preferences so " LOFI " matches "lofi".
    favorite_genre = (user_prefs.get("favorite_genre") or "").strip().lower()
    if favorite_genre:
        song_genre = song["genre"].lower()
        if song_genre == favorite_genre:
            score += GENRE_WEIGHT
            reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")
        elif set(song_genre.split()) & set(favorite_genre.split()):
            score += PARTIAL_GENRE_WEIGHT
            reasons.append(
                f"partial genre match: {song['genre']} ~ {favorite_genre} "
                f"(+{PARTIAL_GENRE_WEIGHT:.1f})"
            )

    # Rule 2: mood (+1.0 exact)
    favorite_mood = (user_prefs.get("favorite_mood") or "").strip().lower()
    if favorite_mood and song["mood"].lower() == favorite_mood:
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Rule 3: energy closeness (0 to +2.0), rewards being near the target, not just high or low
    target_energy = user_prefs.get("target_energy")
    if target_energy is not None:
        points = ENERGY_WEIGHT * closeness(song["energy"], target_energy)
        score += points
        reasons.append(f"energy {song['energy']:.2f} vs your {target_energy:.2f} (+{points:.2f})")

    # Rule 4: valence closeness (0 to +1.0), only if the user set a target
    target_valence = user_prefs.get("target_valence")
    if target_valence is not None:
        points = VALENCE_WEIGHT * closeness(song["valence"], target_valence)
        score += points
        reasons.append(f"valence {song['valence']:.2f} vs your {target_valence:.2f} (+{points:.2f})")

    # Rule 5: acoustic preference (+0.5 if the song's sound matches likes_acoustic)
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        is_acoustic = song["acousticness"] >= ACOUSTIC_THRESHOLD
        if is_acoustic == likes_acoustic:
            score += ACOUSTIC_WEIGHT
            sound = "acoustic" if is_acoustic else "electronic"
            reasons.append(f"{sound} sound, as you prefer (+{ACOUSTIC_WEIGHT:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score (ties: energy closeness, then title) and return the top k with explanations."""
    target_energy = user_prefs.get("target_energy")

    def energy_tiebreak(song: Dict) -> float:
        """Energy closeness used to break score ties (0.0 if the user set no energy target)."""
        return closeness(song["energy"], target_energy) if target_energy is not None else 0.0

    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    scored.sort(key=lambda item: (-item[1], -energy_tiebreak(item[0]), item[0]["title"]))
    return scored[:k]


def max_possible_score(user_prefs: Dict) -> float:
    """Highest score a song could earn for these preferences (only rules the user set count)."""
    total = 0.0
    if user_prefs.get("favorite_genre"):
        total += GENRE_WEIGHT
    if user_prefs.get("favorite_mood"):
        total += MOOD_WEIGHT
    if user_prefs.get("target_energy") is not None:
        total += ENERGY_WEIGHT
    if user_prefs.get("target_valence") is not None:
        total += VALENCE_WEIGHT
    if user_prefs.get("likes_acoustic") is not None:
        total += ACOUSTIC_WEIGHT
    return total
