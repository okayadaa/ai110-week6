from src.recommender import (
    EXAMPLE_PROFILES,
    Song,
    UserProfile,
    Recommender,
    profile_from_dict,
)

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def make_catalog_recommender() -> Recommender:
    songs = [
        Song(
            id=2,
            title="Midnight Coding",
            artist="LoRoom",
            genre="lofi",
            mood="chill",
            energy=0.42,
            tempo_bpm=78,
            valence=0.56,
            danceability=0.62,
            acousticness=0.71,
        ),
        Song(
            id=3,
            title="Storm Runner",
            artist="Voltline",
            genre="rock",
            mood="intense",
            energy=0.91,
            tempo_bpm=152,
            valence=0.48,
            danceability=0.66,
            acousticness=0.10,
        ),
        Song(
            id=5,
            title="Gym Hero",
            artist="Max Pulse",
            genre="pop",
            mood="intense",
            energy=0.93,
            tempo_bpm=132,
            valence=0.77,
            danceability=0.88,
            acousticness=0.05,
        ),
        Song(
            id=4,
            title="Library Rain",
            artist="Paper Lanterns",
            genre="lofi",
            mood="chill",
            energy=0.35,
            tempo_bpm=72,
            valence=0.60,
            danceability=0.58,
            acousticness=0.86,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_intense_rock_vs_chill_lofi_profiles_rank_differently():
    rec = make_catalog_recommender()

    rock_user = profile_from_dict(EXAMPLE_PROFILES["intense_rock"])
    lofi_user = profile_from_dict(EXAMPLE_PROFILES["chill_lofi"])

    rock_results = rec.recommend(rock_user, k=1)
    lofi_results = rec.recommend(lofi_user, k=1)

    assert rock_results[0].genre == "rock"
    assert rock_results[0].mood == "intense"
    assert lofi_results[0].genre == "lofi"
    assert lofi_results[0].mood == "chill"
