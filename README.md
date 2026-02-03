# 2026 Calendar Generator

A Python web application that generates a comprehensive HTML calendar for the year 2026 with all major US holidays, proper weekday display, and printing support.

## Features

- **Full Year Display**: Shows all 12 months from January to December in a vertically scrolling layout
- **Traditional Layout**: Sunday is displayed on the left, Saturday on the right
- **Uniform Day Cells**: Each day's cell is sized appropriately (100px minimum, 180px when printed) for writing notes
- **Holiday Markers**: Top 15 US holidays are highlighted with emojis and italicized names in their respective day cells
- **Special Styling**: Halloween and Easter have special background colors to distinguish them
- **Print Optimized**: Includes CSS for automatic page breaks and blue borders on printed days
- **Responsive Design**: Works on various screen sizes while maintaining the calendar's visual integrity

## Supported Holidays

1. New Year's Day (January 1) - 🎉
2. MLK Day (January 20) - 🌟
3. Presidents' Day (February 16) - ⭐
4. Good Friday (April 3) - ✝️
5. Memorial Day (May 25) - 🇺🇸
6. Juneteenth (June 19) - 🏳️‍🌈
7. Independence Day (July 4) - 🦅
8. Labor Day (September 7) - 💪
9. Columbus Day (October 12) - 🧭
10. Election Day (November 3) - 🗳️
11. Veterans Day (November 11) - 🎖️
12. Thanksgiving (November 26) - 🦃
13. Christmas Day (December 25) - 🎄
14. Halloween (October 31) - 🎃
15. Easter (March 29) - 🐇

## Requirements

- Python 3.x
- No external dependencies (uses only Python standard library modules: `datetime`, `calendar`, `math`)

## Installation

1. Navigate to the project directory:
```bash
cd basic_calendar
```

## Usage

1. Run the calendar generator:
```bash
python3 calendar_generator.py
```

2. Open the generated HTML file in a web browser:
```bash
open calendar_2026.html
```

Or simply double-click `calendar_2026.html` in your file manager.

## How It Works

### Weekday Layout Logic

The calendar uses a Sunday-first display format where:
- Sunday = 0 (leftmost position)
- Monday = 1
- Tuesday = 2
- Wednesday = 3
- Thursday = 4
- Friday = 5
- Saturday = 6 (rightmost position)

Python's `datetime.weekday()` returns values from Monday=0 to Sunday=6. The script converts these values using the formula:
```python
start_weekday_display = (first_day.weekday() + 1) % 7
```

This ensures each month starts on the correct day with the appropriate number of empty cells before the first day.

### Calendar Generation

1. The script calculates the first day of each month and the total number of days in each month
2. It determines how many weeks are needed to display all days in proper grid format
3. It identifies which days in each month are US holidays
4. It generates HTML with embedded CSS for styling and print optimizations
5. The output is a single, self-contained HTML file

## Calendar Grid Structure

Each month section includes:
- Large, centered month title
- Weekday headers (Sun-Sat)
- Day cells arranged in a 7-column grid
- Empty cells to account for offset days where needed
- Holiday markers in special colored boxes when applicable

## Printing

To print the calendar:
1. Open the `calendar_2026.html` file in your web browser
2. Press Ctrl+P (or Command+P on Mac) to open the print dialog
3. The calendar is optimized with:
   - Blue borders around each day cell for easy identification
   - Automatic page breaks between months
   - Proper margins and formatting

## File Structure

```
basic_calendar/
├── calendar_generator.py   # Main Python script that generates the calendar
├── calendar_2026.html      # Generated HTML calendar file
└── README.md               # This documentation file
```

## Customization

You can customize the calendar by modifying the `HOLIDAYS` dictionary in `calendar_generator.py`:

```python
HOLIDAYS = {
    'Month Day': ('Holiday Name', 'Emoji'),
    # Add or modify holiday entries as needed
}
```

## License

This project is provided as-is for personal and educational use.