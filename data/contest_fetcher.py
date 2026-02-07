import requests
from datetime import datetime, timedelta, timezone

# detect DIV info from codeforces
def detetc_cf_div(contest_name):
    name = contest_name.lower()
    if "div. 1" in name or "division 1" in name:
        return "Div 1"
    if "div. 2" in name or "division 2" in name:
        return "Div 2"
    if "div. 3" in name or "division 3" in name:
        return "Div 3"
    if "div. 4" in name or "division 4" in name:
        return "Div 4"
    return "unkown"


def utc_to_ist(timestamp):
    utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    ist_dt = utc_dt + timedelta(hours=5, minutes=30)
    
    date_str = ist_dt.strftime("%Y-%m-%d")
    time_str = ist_dt.strftime("%H:%M")
    
    return date_str, time_str

def fetch_cf_contests():
    url = "https://codeforces.com/api/contest.list"
    response = requests.get(url)
    data = response.json()
    
    contest_by_date = {}
    if data['status'] != "OK":
        return contest_by_date

    #  we skipping past and current contest
    for contest in data["result"]:
        if contest["phase"] != "BEFORE":
            continue
        
        date, time  = utc_to_ist(contest["startTimeSeconds"])
        div = detetc_cf_div(contest["name"])
        
        contest_info = {
            "platform": "Codeforces",
            "name": contest["name"],
            "type": div,
            "time": time,
            "duration": f'{contest["durationSeconds"] // 3600}h'
        }
        
        if date not in contest_by_date:
            contest_by_date[date] = []
        contest_by_date[date].append(contest_info)
    return contest_by_date

def detect_lc_type(contest_title):
    title = contest_title.lower()

    if "weekly" in title:
        return "Weekly Contest"
    if "biweekly" in title:
        return "Biweekly Contest"

    return "Contest"

def fetch_leetcode_contests(weeks=8):
    """
    Generate LeetCode Weekly & Biweekly contests
    """
    contests_by_date = {}

    today = datetime.now(timezone.utc)

    for i in range(weeks * 7):
        day = today + timedelta(days=i)
        weekday = day.weekday()  # Monday=0, Sunday=6

        # Weekly Contest → Sunday 8:00 AM IST
        if weekday == 6:  # Sunday
            ist_dt = day + timedelta(hours=5, minutes=30)
            date = ist_dt.strftime("%Y-%m-%d")

            contests_by_date.setdefault(date, []).append({
                "platform": "LeetCode",
                "name": "LeetCode Weekly Contest",
                "type": "Weekly Contest",
                "time": "08:00",
                "duration": "1.5h"
            })

        # Biweekly Contest → Saturday 8:00 PM IST (alternate weeks)
        if weekday == 5 and i % 14 == 0:  # Saturday
            ist_dt = day + timedelta(hours=5, minutes=30)
            date = ist_dt.strftime("%Y-%m-%d")

            contests_by_date.setdefault(date, []).append({
                "platform": "LeetCode",
                "name": "LeetCode Biweekly Contest",
                "type": "Biweekly Contest",
                "time": "20:00",
                "duration": "1.5h"
            })

    return contests_by_date


def fetch_all_contests():
    all_contests = {}

    cf = fetch_cf_contests()
    lc = fetch_leetcode_contests()

    for source in (cf, lc):
        for date, events in source.items():
            if date not in all_contests:
                all_contests[date] = []
            all_contests[date].extend(events)

    return all_contests
