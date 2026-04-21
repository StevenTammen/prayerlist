from bs4 import BeautifulSoup
import html5lib
import re
import calendar
import random
import math
from .utility import *
from markdownify import markdownify

def get_ichthys_prayer_list_as_html():
    url = "https://ichthys.com/e-mails.htm"
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "html5lib")
    dir_elements = soup.find_all('dir')
    ichthys_prayer_list_html = get_ichthys_prayer_list_html_from_dir_list(dir_elements)
    ichthys_prayer_list_html = get_rid_of_dir_elements(ichthys_prayer_list_html)
    ichthys_prayer_list_html = get_rid_of_p_elements(ichthys_prayer_list_html)
    ichthys_prayer_list_html = get_rid_of_inline_styles(ichthys_prayer_list_html)
    ichthys_prayer_list_html = clean_up_whitespace(ichthys_prayer_list_html)
    ichthys_prayer_list_html = transform_dates(ichthys_prayer_list_html)
    ichthys_prayer_list_html = get_rid_of_asterisks(ichthys_prayer_list_html)
    return ichthys_prayer_list_html

def add_ichthys_prayer_list_to_prayer_list_dict(prayer_list_dict, pray_through_ichthys_prayer_list_in_x_days):
    prayer_list_dict["# Ichthys prayer list"] = {}
    ichthys_prayer_list_html = get_ichthys_prayer_list_as_html()
    soup = BeautifulSoup(ichthys_prayer_list_html, "html5lib")
    list_items = soup.find_all('li')
    # Get just text
    list_items = [str(li.text) for li in list_items]
    # Get rid of non-breaking spaces
    list_items = [re.sub(r'\xa0', ' ', li) for li in list_items]
    # Get rid of new lines
    list_items = [re.sub(r'\n', ' ', li) for li in list_items]
    ## Get rid of duplicate spaces = only ever have maximum of one space
    list_items = [re.sub(r'  +', ' ', li) for li in list_items]
    # Trim whitespace
    list_items = [li.strip() for li in list_items]

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

# Needed since apparently there is a blank <dir> element on page too
def get_ichthys_prayer_list_html_from_dir_list(dir_elements):
    return find_string_with_substring(dir_elements, "li")

def get_rid_of_dir_elements(ichthys_prayer_list_html):
    ichthys_prayer_list_html = re.sub(r'<dir.+?>', '', ichthys_prayer_list_html)
    return re.sub(r'</dir>', '', ichthys_prayer_list_html)

def get_rid_of_p_elements(ichthys_prayer_list_html):
    ichthys_prayer_list_html = re.sub(r'<p.+?>', '', ichthys_prayer_list_html)
    return re.sub(r'</p>', '', ichthys_prayer_list_html)

def get_rid_of_inline_styles(ichthys_prayer_list_html):
    ichthys_prayer_list_html = re.sub(r'align=".+?"', '', ichthys_prayer_list_html)
    return re.sub(r'style=".+?"', '', ichthys_prayer_list_html)

def clean_up_whitespace(ichthys_prayer_list_html):
    ichthys_prayer_list_html = re.sub(r'<li +?>', '<li>', ichthys_prayer_list_html)
    return re.sub(r"^\s*$\n", "", ichthys_prayer_list_html, flags=re.MULTILINE)

def transform_dates(ichthys_prayer_list_html):
    return re.sub(r'(\d+)\/(\d+)\/(\d+)', convert_date_to_string_version, ichthys_prayer_list_html)

def convert_date_to_string_version(match):
    month = int(match.group(1))
    month_string = calendar.month_name[month]
    day = match.group(2)
    year = match.group(3)
    if(len(year) == 2):
        year = '20' + year
    return f'{month_string} {day}, {year}'

# Just get in the way in TTS
def get_rid_of_asterisks(ichthys_prayer_list_html):
    return re.sub(r'\*', '', ichthys_prayer_list_html)
