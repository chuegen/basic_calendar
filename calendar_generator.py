import datetime
import math
import calendar
import sys

def get_holidays_for_year(year):
    """Calculate all holidays for a given year"""
    holidays = {}

    # New Year's Day
    holidays['January 1'] = ('New Year\'s Day', '🎉')

    # MLK Jr. Day - Third Monday in January
    jan1 = datetime.date(year, 1, 1)
    for day in range(1, 32):
        if jan1.replace(day=day).weekday() == 0:  # Monday
            holidays[f'January {day}'] = ('MLK Jr. Day', '🌟')
            break

    # Presidents' Day - Third Monday in February
    feb1 = datetime.date(year, 2, 1)
    for day in range(1, 30):
        if feb1.replace(day=day).weekday() == 0:  # Monday
            holidays[f'February {day}'] = ('Presidents\' Day', '⭐')
            break

    # Good Friday - Friday before Easter
    easter = calculate_easter(year)
    good_friday = easter - datetime.timedelta(days=2)
    holidays[good_friday.strftime('%B %d')] = ('Good Friday', '✝️')

    # Memorial Day - Last Monday in May
    may31 = datetime.date(year, 5, 31)
    for day in reversed(range(25, 32)):
        if may31.replace(day=day).weekday() == 0:  # Monday
            holidays[f'May {day}'] = ('Memorial Day', '🇺🇸')
            break

    # Juneteenth
    holidays['June 19'] = ('Juneteenth', '🏳️‍🌈')

    # Independence Day
    holidays['July 4'] = ('Independence Day', '🦅')

    # Labor Day - First Monday in September
    sep1 = datetime.date(year, 9, 1)
    for day in range(1, 30):
        if sep1.replace(day=day).weekday() == 0:  # Monday
            holidays[f'September {day}'] = ('Labor Day', '💪')
            break

    # Columbus Day - Second Monday in October
    oct1 = datetime.date(year, 10, 1)
    for day in range(1, 32):
        if oct1.replace(day=day).weekday() == 0:  # Monday
            holidays[f'October {day}'] = ('Columbus Day', '🧭')
            # Skip if after the proper Columbus Day
            if day > 8:
                del holidays[f'October {day}']
                break

    # Election Day - Tuesday after first Monday in November
    nov1 = datetime.date(year, 11, 1)
    for day in range(3, 30):
        if nov1.replace(day=day).weekday() == 1:  # Tuesday
            holidays[f'November {day}'] = ('Election Day', '🗳️')
            break

    # Veterans Day
    holidays['November 11'] = ('Veterans Day', '🎖️')

    # Thanksgiving - Fourth Thursday of November
    for day in range(1, 31):
        if datetime.date(year, 11, day).weekday() == 3:  # Thursday
            thanksgiving_count = sum(1 for d in range(1, day+1) if datetime.date(year, 11, d).weekday() == 3)
            if thanksgiving_count == 4:
                holidays[f'November {day}'] = ('Thanksgiving', '🦃')
                break

    # Christmas Day
    holidays['December 25'] = ('Christmas Day', '🎄')

    # Halloween
    holidays['October 31'] = ('Halloween', '🎃')

    # Easter
    easter = calculate_easter(year)
    holidays[easter.strftime('%B %d')] = ('Easter', '🐇')

    return holidays

def calculate_easter(year):
    """Calculates the date of Easter for a given year using the Anonymous Gregorian algorithm"""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime.date(year, month, day)

class CalendarGenerator:
    def __init__(self, year):
        self.year = year
        self.months = self._initialize_months()
        self.holidays = get_holidays_for_year(year)
    def _initialize_months(self):
        months = {}
        for month in range(1, 13):
            first_day = datetime.date(self.year, month, 1)

            days_in_month = calendar.monthrange(self.year, month)[1]

            start_weekday_display = (first_day.weekday() + 1) % 7

            total_cells = days_in_month + (7 - start_weekday_display) % 7

            weeks_needed = math.ceil(total_cells / 7)

            months[month] = {
                'name': first_day.strftime('%B'),
                'days_in_month': days_in_month,
                'start_weekday': start_weekday_display,
                'weeks_needed': weeks_needed
            }
        return months

    def get_holidays_for_month(self, month):
        holidays = []
        for date_str, (name, emoji) in self.holidays.items():
            month_name, day_str = date_str.rsplit(' ', 1)
            month_num = datetime.datetime.strptime(month_name, '%B').month
            day_num = int(day_str)
            date_obj = datetime.date(self.year, month_num, day_num)
            if date_obj.month == month and date_obj.year == self.year:
                holidays.append({
                    'day': date_obj.day,
                    'name': name,
                    'emoji': emoji,
                    'full_date': date_str
                })
        return holidays

    def generate_html(self):
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>%s Calendar</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .month-section {
            background-color: white;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .month-title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }

        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 2px;
        }

        .weekday-label {
            background-color: #e0e0e0;
            padding: 8px 4px;
            text-align: center;
            font-weight: bold;
            font-size: 14px;
            color: #555;
        }

        .day-cell {
            background-color: white;
            border: 1px solid #ddd;
            min-height: 100px;
            padding: 4px;
            position: relative;
            display: flex;
            flex-direction: column;
        }

        .day-number {
            font-size: 12px;
            font-weight: bold;
            color: #666;
            margin-bottom: 4px;
        }

        .day-content {
            flex: 1;
            font-size: 10px;
        }

        .holiday-box {
            margin: 4px 0;
            padding: 4px;
            background-color: #fff3e0;
            border-radius: 2px;
            font-style: italic;
            font-size: 10px;
            overflow: hidden;
        }

        .halloween-box {
            background-color: #ffcdd2;
        }

        .easter-box {
            background-color: #c8e6c9;
        }

        .holiday-emoji {
            margin-right: 4px;
        }

        @media print {
            body {
                padding: 0;
                background-color: white;
            }

            .container {
                max-width: none;
            }

            .month-section {
                page-break-before: always;
                box-shadow: none;
            }

            .calendar-grid {
                display: grid;
            }

            .day-cell {
                min-height: 180px;
                border: 1px solid #00f;
            }
        }
    </style>
</head>
<body>
    <div class="container'>
""" % self.year

        for month_num, month_data in self.months.items():
            html += f"""
        <div class="month-section">
            <h2 class="month-title">{month_data['name']} {self.year}</h2>
            <div class="calendar-grid">
                <div class="weekday-label">Sun</div>
                <div class="weekday-label">Mon</div>
                <div class="weekday-label">Tue</div>
                <div class="weekday-label">Wed</div>
                <div class="weekday-label">Thu</div>
                <div class="weekday-label">Fri</div>
                <div class="weekday-label">Sat</div>
"""

            offset_days = month_data['start_weekday']

            html += "                <div class='day-cell empty' style='visibility:hidden'></div>\n" * month_data['start_weekday']

            total_days = 0

            for day in range(1, month_data['days_in_month'] + 1):
                total_days += 1
                html += "                <div class='day-cell'>\n"
                html += f"                    <div class='day-number'>{day}</div>\n"
                html += "                    <div class='day-content'>\n"
                html += "                    </div>\n"

                for holiday in self.get_holidays_for_month(month_num):
                    if holiday['day'] == day:
                        if holiday['full_date'] in ['October 31', 'April 5', 'March 29']:
                            html += f"                    <div class='holiday-box holiday-{holiday['full_date'].lower().replace(' ', '-')}'>{holiday['emoji']} <span class='holiday-emoji'>{holiday['name']}</span></div>\n"
                        else:
                            html += f"                    <div class='holiday-box'>{holiday['emoji']} <span class='holiday-emoji'>{holiday['name']}</span></div>\n"

                html += "                </div>\n"

            remaining_cells = (7 * month_data['weeks_needed']) - total_days
            html += "                <div class='day-cell empty' style='visibility:hidden'></div>\n" * remaining_cells

            html += """            </div>
        </div>
"""

        html += """    </div>
</body>
</html>
"""

        return html

def generate_calendars():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 calendar_generator.py [year]")
        print("Example: python3 calendar_generator.py 2026")
        sys.exit(1)

    try:
        year = int(sys.argv[1])
        if year < 1 or year > 9999:
            print("Year must be between 1 and 9999")
            sys.exit(1)
    except ValueError:
        print("Please provide a valid year number")
        sys.exit(1)

    generator = CalendarGenerator(year)
    filename = f"calendar_{year}.html"
    html = generator.generate_html()
    
    with open(filename, 'w') as f:
        f.write(html)

    print(f"Calendar generated successfully: {filename}")

if __name__ == '__main__':
    generate_calendars()
