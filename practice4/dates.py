#exercise1
from datetime import date, timedelta
# Get today's date
today = date.today()
# Subtract 5 days
five_days_ago = today - timedelta(days=5)
print("Today's date:", today)
print("Date 5 days ago:", five_days_ago)

#exercise2
from datetime import date, timedelta
today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("Today:",today)
print("Yesterday:",yesterday)
print("Tomorrow:",tomorrow)

#exercise3
from datetime import datetime
now = datetime.now()
no_micro = now.replace(microsecond=0)
print("Original time:",now)
print("Time without microseconds:",no_micro)

#exercise4
from datetime import datetime

# Ask user for two dates
date1 = input("Enter the first date (YYYY-MM-DD): ")
date2 = input("Enter the second date (YYYY-MM-DD): ")

# Convert strings to datetime objects
d1 = datetime.strptime(date1, "%Y-%m-%d")
d2 = datetime.strptime(date2, "%Y-%m-%d")

# Calculate difference in seconds
diff_seconds = (d2 - d1).total_seconds()

print("Difference in seconds:", diff_seconds)