import calendar
from datetime import datetime

def get_today_str():
    return datetime.now().strftime("%Y-%m-%d")

def generate_month_calender(year, month, contest_data):
    cal = calendar.Calendar(calendar.SUNDAY)
    month_days = cal.monthdatescalendar(year, month)
    
    today_str = get_today_str()
    month_str = f"{year:04d}-{month:02d}"
    
    calendar_grid = []
    for week in month_days:
        week_row = []

        for day in week:
            date_str = day.strftime("%Y-%m-%d")

            day_cell = {
                "date": date_str,
                "day": day.day,
                "is_current_month": date_str.startswith(month_str),
                "is_today": date_str == today_str,
                "contests": contest_data.get(date_str, [])
            }

            week_row.append(day_cell)

        calendar_grid.append(week_row)

    return calendar_grid