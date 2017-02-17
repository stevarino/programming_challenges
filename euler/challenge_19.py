"""https://projecteuler.net/problem=19

You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century
unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth
century (1 Jan 1901 to 31 Dec 2000)?
"""

MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def count_first_sundays(year, end_year):
    """Given a start and end year, returns the number of sundays
    that fall on the first."""
    month = 0
    firsts = 0
    day = 1 # Jan 1 1900 is monday, or 0
    days_in_month = 31
    while month < 12*(end_year-year):
        leap_year = year%400 == 0 or (year%4 == 0 and not year%100 == 0)
        if (month%12) == 1 and leap_year:
            print('leap!')
            days_in_month = 29
        else:
            days_in_month = MONTHS[month%12]
        day += days_in_month
        month += 1
        if day % 7 == 0:
            firsts += 1
    return firsts


if __name__ == '__main__':
    print(count_first_sundays(1900, 2001) - count_first_sundays(1900, 1901))
