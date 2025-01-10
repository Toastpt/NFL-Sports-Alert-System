import os
import json
import urllib.request
import boto3
from datetime import date, datetime, timedelta, timezone

def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayScore', 'N/A')}-{game.get('HomeScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")
    
    # Format stadium details
    stadium = game.get("StadiumDetails", {})
    stadium_name = stadium.get("Name", "Unknown")
    stadium_city = stadium.get("City", "Unknown")
    stadium_state = stadium.get("State", "Unknown")

    if status == "Final":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Final Score: {final_score}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
            f"Stadium: {stadium_name}, {stadium_city}, {stadium_state}\n"
        )

    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Current Score: {final_score}\n"
            f"Last Play: {last_play}\n"
            f"Channel: {channel}\n"
            f"Stadium: {stadium_name}, {stadium_city}, {stadium_state}\n"
        )

    elif status == "Scheduled":
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Start Time: {start_time}\n"
            f"Channel: {channel}\n"
        )

    else:
        return (
            f"Game Status: {status}\n"
            f"{away_team} vs {home_team}\n"
            f"Details are unavailable at the moment.\n"
        )

def lambda_handler(event, context):
    # Get environment variables
    api_key = os.getenv("NFL_API_KEY")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    sns_client = boto3.client("sns")

    # Validate environment variables
    if not api_key:
        print("Error: NFL_API_KEY environment variable is missing.")
        return {"statusCode": 500, "body": "NFL API Key is missing"}
    if not sns_topic_arn:
        print("Error: SNS_TOPIC_ARN environment variable is missing.")
        return {"statusCode": 500, "body": "SNS Topic ARN is missing"}
    
    # Adjust for Central Time (UTC-6)
    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)  # Central Time is UTC-6
    today_date = central_time.strftime("%Y-%m-%d")
    specific_date = date(2025, 1, 5).strftime("%Y-%m-%d")  # Correct format for "YYYY-MM-DD"

    print(f"Fetching games for date: {specific_date}")
    
    # Fetch data from the API
    api_url = f"https://api.sportsdata.io/v3/nfl/scores/json/ScoresByDate/{specific_date}?key={api_key}"
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            print(f"Fetched data for {specific_date}: {len(data)} games")
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        return {"statusCode": e.code, "body": f"Error fetching data from API: {e.reason}"}
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
        return {"statusCode": 500, "body": f"Network error: {e.reason}"}
    except Exception as e:
        print(f"Unexpected error fetching data: {e}")
        return {"statusCode": 500, "body": "Error fetching data"}

    # Include all games (final, in-progress, and scheduled)
    try:
        messages = [format_game_data(game) for game in data]
        final_message = "\n---\n".join(messages) if messages else "No games available for today."
    except Exception as e:
        print(f"Error formatting game data: {e}")
        return {"statusCode": 500, "body": "Error formatting game data"}
    
    # Publish to SNS
    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=final_message,
            Subject="NFL Game Updates"
        )
        print("Message published to SNS successfully.")
    except sns_client.exceptions.InvalidParameterException as e:
        print(f"InvalidParameterException: {e}")
        return {"statusCode": 400, "body": "Invalid parameter in SNS request"}
    except sns_client.exceptions.InternalErrorException as e:
        print(f"InternalErrorException: {e}")
        return {"statusCode": 500, "body": "SNS internal error"}
    except Exception as e:
        print(f"Unexpected error publishing to SNS: {e}")
        return {"statusCode": 500, "body": "Error publishing to SNS"}
    
    return {"statusCode": 200, "body": "Data processed and sent to SNS"}
