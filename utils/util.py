import requests
import json
from time import perf_counter
import shutil

is_first_launch = False

try:
    with open("api_key.txt", "r") as f:
        api_key = f.readline()
    
except(FileNotFoundError):
    is_first_launch = True
    api_key = ''

try:
    with open("storage/cards.json", "r") as f:
        cards = json.load(f)["items"]
    
except(FileNotFoundError):
    is_first_launch = True
    cards = []

def performance_logger(func):
    def wrapper():
        start_time = perf_counter()
        print(f"Running {func.__name__}")
        func()
        print(f"Finished operation in {start_time - perf_counter()}")
    
    return wrapper()

        

# Should only need to be run once every season
def fetch_top() -> None:
    seasons_request = "locations/global/seasons"

    seasons_request = requests.get(f"https://api.clashroyale.com/v1/{seasons_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})

    with open("storage/seasons.json", "w") as f:
        f.write(json.dumps(seasons_request.json(), indent=2))

        latest_season = seasons_request.json()["items"][-1]["id"]

    top_request = f"locations/global/pathoflegend/{latest_season}/rankings/players?limit={1000}"
    top_request = requests.get(f"https://api.clashroyale.com/v1/{top_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})

    with open("storage/top_players.json", "w") as f:
        f.write(json.dumps(top_request.json(), indent=2))

# Update list after downloading new
def update_cards_list() -> None:
    global cards

    with open("storage/cards.json", "r") as f:
        cards = json.load(f)["items"]

# Run once every Clash Royale season
def fetch_cards() -> None:
    cards_request = "cards"
    cards_request = requests.get(f"https://api.clashroyale.com/v1/{cards_request}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"})

    with open("storage/cards.json", "w") as f:
        f.write(json.dumps(cards_request.json(), indent=2))
    
    update_cards_list()
    

def fetch_profile(tag: str) -> dict:
    return requests.get(f"https://api.clashroyale.com/v1/players/%23{tag}", headers={"Accept":"application/json", "authorization":f"Bearer {api_key}"}).json()

# Should only need to run once per Clash Royale season
def download_card_images() -> None:
    for card in cards:
        res = requests.get(card["iconUrls"]["medium"], stream=True)

        if res.status_code == 200:
            with open(f"storage/card_images/{card['id']}.png", "wb") as ci:
                shutil.copyfileobj(res.raw, ci)

def get_card_names() -> list:
    card_names = []

    for card in cards:
        card_names.append(card['name'])

    return card_names

def get_id_from_name(name: str) -> int:
    for card in cards:
        if card["name"] == name:
            return card["id"]
    
    return None

def update_api_key(key: str) -> None:
    global api_key

    with open("api_key.txt", "w") as f:
        f.write(key)

    api_key = key

def get_decks(requested_card_id: int, MAX_DECKS=10) -> list:
    applicable_decks = []
    
    with open("storage/top_players.json", "r") as f:
        top_players = json.load(f)["items"]

    for player in top_players:
        tag = player["tag"][1:]
        player_name = player["name"]

        try:
            current_deck = fetch_profile(tag)["currentDeck"]
        
        except(KeyError):
            continue

        deck_contains_card = False
        for card in current_deck:
            if requested_card_id == card["id"]:
                applicable_decks.append(current_deck)
                print(player_name)
                break
        
        if len(applicable_decks) >= MAX_DECKS:
            break

    return applicable_decks

def run_on_first_launch(api_key: str) -> None:
    update_api_key(api_key)
    fetch_cards()
    fetch_top()
    download_card_images()

def refresh_everything() -> None:
    fetch_cards()
    fetch_top()
    download_card_images()


def refresh_leaderboard() -> None:
    fetch_top()

def save_settings(values: dict) -> None:
    with open("settings.json", 'w') as f:
        f.write(json.dumps(values, indent=2))

def load_settings() -> dict:
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            return settings
    
    except(FileNotFoundError):
        return None