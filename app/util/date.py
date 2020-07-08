from datetime import datetime
from pytz import timezone


def current_datetime():
    return datetime.now(
        timezone('America/Sao_Paulo')
    ).replace(tzinfo=None)


def iso_date_to_datetime(date_iso: str):
    return datetime.strptime(date_iso, '%Y-%m-%d')
