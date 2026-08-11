from bs4 import BeautifulSoup
import html5lib
import re
import calendar
import random
import math
from .utility import *
from markdownify import markdownify

def get_ichthys_prayer_list_as_list_of_strings():
    url = "https://ichthys.com/e-mails.htm"
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "html5lib")

    # First get text of all <li> elements that belong to <dir> elements
    ichthys_prayer_list = [li.get_text(" ", strip=True) for li in soup.select("dir li")]

    ## Then process it in various ways to get it ready for TTS

    # Convert dates to string version, since better for TTS
    ichthys_prayer_list = [re.sub(r'(\d+)\/(\d+)\/(\d+)', convert_date_to_string_version, prayer) for prayer in ichthys_prayer_list]

    # Remove asterisks since they just get in the way in TTS
    ichthys_prayer_list = [re.sub(r'\*', '', prayer) for prayer in ichthys_prayer_list]

    # Turn non-breaking spaces into regular spaces
    ichthys_prayer_list = [re.sub(r'\xa0', ' ', prayer) for prayer in ichthys_prayer_list]

    # Get rid of explicit new lines
    ichthys_prayer_list = [re.sub(r'\n', ' ', prayer) for prayer in ichthys_prayer_list]

    # Get rid of duplicate spaces = only ever have maximum of one space
    ichthys_prayer_list = [re.sub(r'  +', ' ', prayer) for prayer in ichthys_prayer_list]

    # Trim whitespace
    ichthys_prayer_list = [prayer.strip() for prayer in ichthys_prayer_list]

    return ichthys_prayer_list

def add_ichthys_prayer_list_to_prayer_list_dict(prayer_list_dict, pray_through_ichthys_prayer_list_in_x_days):

    list_items = get_ichthys_prayer_list_as_list_of_strings()

    # Randomize list
    random.shuffle(list_items)

    # Only pray through a subset of the list. If pray_through_ichthys_prayer_list_in_x_days = 2,
    # remove 1/2 of the list items, at random. If three, remove 2/3 of the list items at random.
    # If four, remove 3/4 of the list items at random. Etc.
    fraction_to_remove = 1 - 1.0/pray_through_ichthys_prayer_list_in_x_days
    number_of_items_to_remove = math.ceil(len(list_items) * fraction_to_remove)
    for i in range(number_of_items_to_remove):
        random_element = random.choice(list_items)
        list_items.remove(random_element)

    for li in list_items:
        li = markdownify(li)
        prayer_list_dict["# Ichthys prayer list"][li] = {}

def convert_date_to_string_version(match):
    month = int(match.group(1))
    month_string = calendar.month_name[month]
    day = match.group(2)
    year = match.group(3)
    if(len(year) == 2):
        year = '20' + year
    return f'{month_string} {day}, {year}'
