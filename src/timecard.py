"""
Datetime logic for Calculating details about payperiods
"""

import logging
import os
from datetime import date, timedelta

from dotenv import load_dotenv

from src.holiday import USFedHolidays

# Basic configuration
logging.basicConfig(
    level=logging.INFO,  # controls what level of messages to show
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


load_dotenv()
EMAIL_AID = os.getenv("EMAIL_AID", "")


def build_payperiod(today: date | None = None) -> list[date]:
    """
    Takes a optional datetime.date object, defalts to today.

    Returns a list of date objects that make up the pay period
    including the provided date.
    """
    today = today or date.today()

    if today.day <= 15:
        start = date(today.year, today.month, 1)
        end = date(today.year, today.month, 15)
    else:
        start = date(today.year, today.month, 16)
        next_month = today.month + 1
        if next_month <= 12:
            end = date(today.year, next_month, 1) - timedelta(days=1)
        else:
            end = date(today.year + 1, 1, 1) - timedelta(days=1)

    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def calculate_hours(payperiod: list[date]) -> int:
    """
    Returns the number of hours hours required for a payperiod.

    hours = number of week days * 8
    """
    return sum(8 for d in payperiod if d.weekday() < 5)


def count_holidays(payperiod: list[date]) -> list[str]:
    """
    Returns the list of holidays in a given list of dates objects
    """
    years = {d.year for d in payperiod}
    us_holidays = USFedHolidays(years=list(years))
    period_holidays = []
    for d in payperiod:
        if d in us_holidays:
            period_holidays.append(us_holidays.get(d))

    return period_holidays


def summarize_payperiod(today=None) -> str:
    """
    Returns a brief summary of the payperiod that the provided date is in.
    """
    period = build_payperiod(today=today)
    period_holidays = count_holidays(period)
    hours = calculate_hours(period)
    holidays_str = " and ".join(period_holidays)
    if period_holidays:
        return f"This payperiod has {hours} hours and {len(period_holidays)} holiday(s): {holidays_str}."
    else:
        return f"This payperiod has {hours} hours with no holidays."


def timecard_reminder():
    return f"""
@everyone it's timecard day. {summarize_payperiod()} 
If you are having login issues email the following ASAP: {EMAIL_AID}
"""
