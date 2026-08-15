# TimeMage
Discord bot for Timecard reminders

Scheduled Messages:
- Reminder to submit timecards on 15th and last day of the month
- Reminder to start tiem cards on the 2nd and 17th

Commands:
- `!timecard` - Returns a brief summary of the current pay period including
number of hours and holidays in teh pay period
- `!meme` - Sends a random timecard meme from /assets/memes
- `!excuse` - Generates a random excuse
- `!joke` - Sends a random dad joke from [icanhazdadjoke API](https://icanhazdadjoke.com/)

![Time Mage](/assets/TimeMage.jpg)

Running pytest locally:
- Create a venv: `python3 -m venv venv`
- install requirements: `pip install -r requirements.txt`
- run tests: `pytest`

Building:
- Run `docker compose up --build` from project root