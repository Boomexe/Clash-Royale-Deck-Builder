import requests
import json

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjUyY2NkZDAwLTcyZjQtNDZkNC1iYjNjLTYyMTc2MWYyMDQzOCIsImlhdCI6MTY5ODEwMDQzMSwic3ViIjoiZGV2ZWxvcGVyL2RjOTU2ODg0LTk3NDgtNTlkOC0wZDFhLTBlZDY3YWQ0ZDM3ZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyMDYuMTEwLjIzNS4yMSJdLCJ0eXBlIjoiY2xpZW50In1dfQ.MEU2wVBRoHzYo6BCJ6ClzrU3Ii9QYtvKV4wDWLx5G_4CXY5QfKeZfRANbde4nJYE4Lr6SnpdfKD9R12mMQs9ag"

cards_request = "cards"
seasons_request = "locations/global/seasons"

cards_request = requests.get(f"https://api.clashroyale.com/v1/{cards_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})
seasons_request = requests.get(f"https://api.clashroyale.com/v1/{seasons_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})

with open("cards.json", "w") as f:
    f.write(json.dumps(cards_request.json(), indent=2))

with open("seasons.json", "w") as f:
    f.write(json.dumps(seasons_request.json(), indent=2))

    latest_season = seasons_request.json()["items"][-1]["id"]
    
top_request = f"locations/global/pathoflegend/{latest_season}/rankings/players?limit=100"
top_request = requests.get(f"https://api.clashroyale.com/v1/{top_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})

with open("top_players.json", "w") as f:
    f.write(json.dumps(top_request.json(), indent=2))