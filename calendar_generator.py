import datetime
import math
import calendar

HOLIDAYS = {
    'January 1': ('New Year\'s Day', '🎉'),
    'January 19': ('MLK Jr. Day', '🌟'),
    'February 16': ('Presidents\' Day', '⭐'),
    'April 3': ('Good Friday', '✝️'),
    'May 25': ('Memorial Day', '🇺🇸'),
    'June 19': ('Juneteenth', '🏳️‍🌈'),
    'July 4': ('Independence Day', '🦅'),
    'September 7': ('Labor Day', '💪'),
    'October 12': ('Columbus Day', '🧭'),
    'November 3': ('Election Day', '🗳️'),
    'November 11': ('Veterans Day', '🎖️'),
    'November 26': ('Thanksgiving', '🦃'),
    'December 25': ('Christmas Day', '🎄'),
    'October 31': ('Halloween', '🎃'),
    'April 5': ('Easter', '🐇')
}

class CalendarGenerator:
    def __init__(self, year):
        self.year = year
        self.months = self._initialize_months()

    def _initialize_months(self):
        months = {}
        for month in range(1, 13):
            # Get first day of month and days in month
            first_day = datetime.date(self.year, month, 1)

            # Get days in month using calendar module
            days_in_month = calendar.monthrange(self.year, month)[1]
            
            # Calculate starting weekday for display (Sunday=0, Saturday=6)
            # Python's weekday() returns Monday=0, Tuesday=1, ..., Sunday=6
            # For display we want Sunday=0, Monday=1, ..., Saturday=6
            # Convert using: display_index = (python_weekday + 1) % 7 for Sunday=0, Saturday=6
            # Python's weekday() returns Monday=0, Tuesday=1, ..., Sunday=6
            # Display wants Sunday=0, Monday=1, Saturday=6
            # Conversion: display = (python + 1) % 7
            start_weekday_display = (first_day.weekday() + 1) % 7

            # Calculate how many cells needed for the grid
            total_cells = days_in_month + (7 - start_weekday_display) % 7
            
            # Determine how many weeks we need
            weeks_needed = math.ceil(total_cells / 7)
            
            months[month] = {
                'name': first_day.strftime('%B'),
                'days_in_month': days_in_month,
                'start_weekday': start_weekday_display,
                'weeks_needed': weeks_needed,
                'holidays': self._get_holidays_for_month(month)
            }
        return months

    def _get_holidays_for_month(self, month):
        holidays = []
        for date_str, (name, emoji) in HOLIDAYS.items():
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
    <title>2026 Calendar</title>
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
"""

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

            # Calculate offset days
            offset_days = month_data['start_weekday']

            # Add empty cells for offset
            html += "                <div class='day-cell empty' style='visibility:hidden'></div>\n" * month_data['start_weekday']

            # Calculate starting point for days
            total_days = 0

            # Add days to calendar
            for day in range(1, month_data['days_in_month'] + 1):
                total_days += 1
                html += "                <div class='day-cell'>\n"
                html += f"                    <div class='day-number'>{day}</div>\n"
                html += "                    <div class='day-content'>\n"

                # Check for holidays
                for holiday in month_data['holidays']:
                    if holiday['day'] == day:
                        if holiday['full_date'] in ['October 31', 'March 29']:
                            html += f"                    <div class='holiday-box holiday-{holiday['full_date'].lower().replace(' ', '-')}'>{holiday['emoji']} <span class='holiday-emoji'>{holiday['name']}</span></div>\n"
                        else:
                            html += f"                    <div class='holiday-box'>{holiday['emoji']} <span class='holiday-emoji'>{holiday['name']}</span></div>\n"

                html += "                    </div>\n"
                html += "                </div>\n"

            # Add remaining empty cells to complete the grid
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
    generator = CalendarGenerator(2026)
    html = generator.generate_html()
    
    with open('calendar_2026.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    generate_calendars()