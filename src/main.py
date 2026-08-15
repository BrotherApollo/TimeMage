import logging
import os

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord.ext import commands

from src.meme import dadjoke, generate_excuse, get_reacts, random_meme

# Local Imports
from src.timecard import summarize_payperiod, timecard_reminder

TOKEN = os.getenv("DISCORD_TOKEN", "")
APPROVED_CHANNELS = {
        1451552389181214911: {"reminders": False}, # Test Channel
        1349895419513143317: {"reminders": True}, # Studies Timecard Channel
        1430574832436645939: {"reminders": True}, # Lobsters Timecard Channel
        1536524641613643776: {"reminders": False}, # Dad Joke Channel
}

# Scheduler
scheduler = AsyncIOScheduler()

# Setting up logging
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

# Manging discord bot permissions
intents = discord.Intents.default()
allowed_mentions = discord.AllowedMentions(everyone=True)
intents.message_content = True
# intents.members = True

bot = commands.Bot(
    command_prefix="!", intents=intents, allowed_mentions=allowed_mentions
)


# Commands
# !timecard
@bot.command()
async def timecard(ctx):
    """Responds to !timecard messages in the same channel"""
    await ctx.send(summarize_payperiod())


# !meme
@bot.command()
async def meme(ctx):
    filepath = random_meme()
    await ctx.send(file=discord.File(filepath))


# !excuse
@bot.command()
async def excuse(ctx):
    await ctx.send(generate_excuse())


# !joke
@bot.command()
async def joke(ctx):
    await ctx.send(dadjoke())


# Listeners
@bot.event
async def on_message(message: discord.Message):
    # Top level filter to hard limit bot to channels
    if message.channel.id not in APPROVED_CHANNELS:
        return

    # Auto Reacts
    lower_message = message.content.lower()
    reacts = get_reacts(lower_message)
    for emoji in reacts:
        await message.add_reaction(emoji)
    
    # triggers = ["free beer"]
    # target_users = [
    #     int(os.getenv("JIMMY_ID", 0)),
    #     int(os.getenv("CALEB_ID", 0)),
    # ]

    # check if message is from target user
    # from_target = message.author.id in target_users

    # # Call out identified, reply with a meme
    # if message.mentions and from_target and not message.mention_everyone:
    #     await message.reply(file=discord.File(random_meme()))

    # trigger phrases detected
    # active_triggers = [x for x in triggers if x in lower_message]
    # if from_target and active_triggers:
    #     # Mocking Target User
    #     await message.reply(spongify(lower_message))

    # processing regular commands
    await bot.process_commands(message)


# Scheduled Reminders
async def send_start_timecard_reminder():
    for channelid in APPROVED_CHANNELS:
        # only sending to channels with reminder flag
        if not APPROVED_CHANNELS[channelid]["reminders"]:
            continue
        channel = bot.get_channel(channelid)
        await channel.send(
            "If you haven't started a timecard this pay period, please fix that today."
        )


async def send_timecard_reminder():
    """Post timecard reminders in a specific channel"""
    for channelid in APPROVED_CHANNELS:
        # only sending to channels with reminder flag
        if not APPROVED_CHANNELS[channelid]["reminders"]:
            continue
        channel = bot.get_channel(channelid)
        await channel.send(timecard_reminder())


# Test Reminders
async def send_test_reminder():
    channel = bot.get_channel(1451552389181214911)
    await channel.send(timecard_reminder())


@bot.event
async def on_ready():
    """Initilization, includes all schduled jobs"""
    if scheduler.running:
        return

    print(f"Logged in as {bot.user}")

    # Start your timecard reminder
    scheduler.add_job(
        lambda: bot.loop.create_task(send_start_timecard_reminder()),
        CronTrigger(day=2, hour=18, minute=00),
    )
    scheduler.add_job(
        lambda: bot.loop.create_task(send_start_timecard_reminder()),
        CronTrigger(day=17, hour=18, minute=00),
    )

    # End of Month Timecard Reminder
    scheduler.add_job(
        lambda: bot.loop.create_task(send_timecard_reminder()),
        CronTrigger(day="last", hour=18, minute=00),
    )

    # Mid Month Timecard Reminder
    scheduler.add_job(
        lambda: bot.loop.create_task(send_timecard_reminder()),
        CronTrigger(day=15, hour=18, minute=00),
    )

    # Test
    scheduler.add_job(
        lambda: bot.loop.create_task(send_test_reminder()),
        CronTrigger(day=6, hour=3, minute=40)
    )

    scheduler.start()


if __name__ == "__main__":
    bot.run(token=TOKEN, log_handler=handler, log_level=logging.DEBUG)
