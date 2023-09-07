from datetime import datetime, timezone, timedelta


def get_now():
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    return datetime.fromisoformat(now)
