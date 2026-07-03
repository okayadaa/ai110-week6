"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List, Tuple

from .recommender import EXAMPLE_PROFILES, load_songs, recommend_songs

LINE_WIDTH = 60


def _format_profile_label(profile_name: str, user_prefs: Dict) -> str:
    genre = user_prefs["favorite_genre"]
    mood = user_prefs["favorite_mood"]
    energy = user_prefs["target_energy"]
    acoustic = "yes" if user_prefs["likes_acoustic"] else "no"
    return (
        f"{profile_name}  "
        f"(genre={genre}, mood={mood}, energy={energy:.2f}, acoustic={acoustic})"
    )


def print_recommendations(
    recommendations: List[Tuple[Dict, float, List[str]]],
    profile_name: str,
    user_prefs: Dict,
) -> None:
    print()
    print("=" * LINE_WIDTH)
    print("  MUSIC RECOMMENDATIONS")
    print(f"  Profile: {_format_profile_label(profile_name, user_prefs)}")
    print("=" * LINE_WIDTH)
    print()

    if not recommendations:
        print("  No recommendations found.")
        print()
        return

    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"  #{rank}  {song['title']}")
        print(f"      Score: {score:.2f}")

        if reasons:
            print("      Reasons:")
            for reason in reasons:
                print(f"        - {reason}")
        else:
            print("      Reasons:")
            print("        - No strong matches found for your taste profile.")

        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    profile_name = "chill_lofi"
    user_prefs = EXAMPLE_PROFILES[profile_name]

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(recommendations, profile_name, user_prefs)


if __name__ == "__main__":
    main()
