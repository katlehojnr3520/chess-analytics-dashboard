import os
import requests
import json
import pandas as pd

USERNAME = "modisee"
EMAIL = "katlehojnr3520@gmail.com"

HEADERS = {
    "User-Agent":f"ChessPortfolioDashboard/1.0 ({EMAIL}; GitHub portfolio project)"
}

def fetch_and_clean_data():
    print(f"Starting ETL Pipeline for chess user:{USERNAME}")

    archive_url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
    response = requests.get(archive_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching archives: {response.status_code}")
        return
    archives = response.json().get("archives", [])

    if not archives:
        print("No game history archives found for this user.")
        return

    print(f"Found {len(archives)} monthly game logs. Fetching recent games...")

    recent_archives = archives[-10:]
    all_games = []

    for url in recent_archives:
        month_response = requests.get(url, headers=HEADERS)
        if month_response.status_code == 200:
            games = month_response.json().get("games", [])
            all_games.extend(games)

    print(f"Successfully retrieved {len(all_games)} total raw games.")

    processed_games = []
    for game in all_games:
        is_white = game["white"]["username"].lower() == USERNAME.lower()
        my_player_data = game['white'] if is_white else game['black']
        opponent_data = game['black'] if is_white else game['white']
        processed_games.append ({
            "time_class": game.get("time_class"),
            "my_rating": my_player_data.get("rating"),
            "opp_rating": opponent_data.get("rating"),
            "result": my_player_data.get("result"),
        })

    df = pd.DataFrame(processed_games)

    total_games_count = len(df)
    wins_count = int(df['result'].isin(['win']).sum())
    draw_strings = ['agreed', 'repetition', 'stalemate', 'insufficient', '50move']
    draws_count = int(df['result'].isin(draw_strings).sum())
    losses_count = int(total_games_count - wins_count - draws_count)
    
    summary_stats = {
        "metadata": {
            "username": USERNAME,
            "total_games": total_games_count,
            "wins": wins_count,
            "losses": losses_count,
            "draws": draws_count,
            "win_rate_percentage": round((wins_count / total_games_count) * 100, 1) if total_games_count > 0 else 0
        },
        "ratings": {
            "blitz_avg": int(pd.Series(df[df['time_class'] == 'blitz']['my_rating'].mean()).fillna(0).iloc[0]),
            "rapid_avg": int(pd.Series(df[df['time_class'] == 'rapid']['my_rating'].mean()).fillna(0).iloc[0]),
            "bullet_avg": int(pd.Series(df[df['time_class'] == 'bullet']['my_rating'].mean()).fillna(0).iloc[0]),
        }
    }

    output_dir = "../frontend/public"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "stats.json")

    with open(output_file, 'w') as f:
        json.dump(summary_stats, f, indent=4)
        
    print(f"Compiled statistics written to: {output_file}")

if __name__ == "__main__":
    fetch_and_clean_data()