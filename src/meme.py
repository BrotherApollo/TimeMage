import os
import random

import requests

meme_history = []

def random_meme():
    global meme_history
    memes = os.listdir("assets/memes")
    choice = random.choice(memes)
    while choice in meme_history:
        choice = random.choice(memes)
    
    # adding the meme to history and limiting size
    meme_history.append(choice)
    if len(meme_history) > 5:
        meme_history.pop(0)
    
    return f"assets/memes/{choice}"


def spongify(s):
    return "".join([s[i].upper() if i % 2 else s[i].lower() for i in range(len(s))])


def get_reacts(message) -> list[str]:
    TIME_CARD_REACTS = {
        "📝": ["timecard"],
        "✍️": ["sign"],
        "⚠️": ["error"],
        "💳": ["charge codes", "chargecode"],
        "📧": ["email"],
    }

    reactions = []
    for emoji, keywords in TIME_CARD_REACTS.items():
        if any(trigger in message for trigger in keywords):
            reactions.append(emoji)

    return reactions


def generate_excuse():
    subjects = [
        "I",
        "My dog",
        "The internet",
        "My computer",
        "My coffee machine",
        "My Team Lead",
    ]

    verbs = ["ate", "deleted", "blocked", "misplaced", "forgot", "refused"]

    objects = [
        "my timecard",
        "the VPN connection",
        "the reminder email",
        "my rsa token",
    ]

    modifiers = [
        "because Mercury is in retrograde.",
        "and I couldn't stop crying.",
        "while I was trying to meditate.",
        "and then the Wi-Fi exploded.",
        "and I was trapped in a parallel universe.",
        "and I reported it as phishing.",
    ]
    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)} {random.choice(modifiers)}"

def dadjoke():
    """Get a dad joke from icanhazdadjoke.com"""
    
    response = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"}
    )
    
    if response.status_code == 200:
        joke = response.json()["joke"]
        return joke