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
    
    #Extraction
    archive_url = f"https://api.chess.com/pub/player/{USERNAME}/games/archives"
    response = requests.get(archive_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"Error fetching archives: {response.status_code}")
        return
    archives = response.json().get("archives", [])
    if not archives:
        print("No game history archives found for this user.")
        return

    recent_archives = archives[-10:]
    all_games = []

    for url in recent_archives:
        month_response = requests.get(url, headers=HEADERS)
        if month_response.status_code == 200:
            games = month_response.json().get("games", [])
            all_games.extend(games)

    print(f"Successfully retrieved {len(all_games)} games. Parsing strategic insights...")

    #Transformation
    processed_games = []
    for game in all_games:
        is_white = game["white"]["username"].lower() == USERNAME.lower()
        my_player_data = game['white'] if is_white else game['black']
        opponent_data = game['black'] if is_white else game['white']

        raw_opening_url = game.get("opening", "https://www.chess.com/openings/Unknown-Opening")
        opening_name = raw_opening_url.split("/openings/")[-1].replace("-", " ").split("?")[0]
        opening_short = " ".join(opening_name.split()[:3])

        processed_games.append ({
            "date": game.get("end_time"),
            "time_class": game.get("time_class"),
            "my_rating": my_player_data.get("rating"),
            "result": my_player_data.get("result"),
            "opening": opening_short
        })

    df = pd.DataFrame(processed_games)
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df = df.sort_values('date')

    total_games_count = len(df)
    wins_count = int(df['result'].isin(['win']).sum())
    draw_strings = ['agreed', 'repetition', 'stalemate', 'insufficient', '50move']
    draws_count = int(df['result'].isin(draw_strings).sum())
    losses_count = int(total_games_count - wins_count - draws_count)
    
    opening_stats = []
    if not df.empty:
        top_openings = df['opening'].value_counts().head(4).index.tolist()
        for op in top_openings:
           op_df = df[df['opening'] == op]
           op_total = len(op_df)
           op_wins= len(op_df[op_df['result'] == 'win'])
           opening_stats.append({
               "opening": op,
                "total_games": op_total,
                "win_rate_percentage": round((op_wins / op_total) * 100, 1) if op_total > 0 else 0

            })
    df.set_index('date', inplace=True)
    trend_df = df.groupby('time_class').resample('W')['my_rating'].last().ffill().reset_index()

    main_format = 'rapid' if len(df[df['time_class'] == 'rapid']) > len(df[df['time_class'] == 'blitz']) > 0 else 'bullet'
    history_points = []
    for _, row in trend_df[trend_df['time_class'] == main_format].iterrows():
        history_points.append({
            "week": row['date'].strftime('%d %b'),
            "rating": int(row['my_rating'])
        })
    
    summary_stats = {
        "metadata": {
            "username": USERNAME,
            "total_games": total_games_count,
            "wins": wins_count,
            "losses": losses_count,
            "draws": draws_count,
            "win_rate_percentage": round((wins_count / total_games_count) * 100, 1) if total_games_count > 0 else 0,
            "main_format": main_format
        },
        "ratings": {
            "blitz_avg": int(pd.Series(df[df['time_class'] == 'blitz']['my_rating'].mean()).fillna(0).iloc[0]),
            "rapid_avg": int(pd.Series(df[df['time_class'] == 'rapid']['my_rating'].mean()).fillna(0).iloc[0]),
            "bullet_avg": int(pd.Series(df[df['time_class'] == 'bullet']['my_rating'].mean()).fillna(0).iloc[0]),
        },
        "openings": opening_stats,
        "history": history_points
    }

    output_dir = "../frontend/public"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "stats.json")

    with open(output_file, 'w') as f:
        json.dump(summary_stats, f, indent=4)
        
    print(f"Compiled statistics written to: {output_file}")

if __name__ == "__main__":
    fetch_and_clean_data()