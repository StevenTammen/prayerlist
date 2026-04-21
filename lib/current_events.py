from bs4 import BeautifulSoup
import html5lib
from datetime import datetime, timedelta
import calendar
from .utility import *
import re
from markdownify import markdownify


def get_current_events_of_yesterday_as_html():

    url = "https://en.wikipedia.org/wiki/Portal:Current_events"
    html_content = get_html(url)
    soup = BeautifulSoup(html_content, "html5lib")
    current_event_elements = soup.find_all(class_="current-events")

    yesterday = datetime.now() - timedelta(days=1)
    day = yesterday.day
    month = calendar.month_name[yesterday.month]
    year = yesterday.year
    yesterday_id = rf'id="{year}_{month}_{day}"'

    yesterday_current_events_as_html = find_matching_string(
            current_event_elements, yesterday_id
    )

    yesterday_current_events_as_html = clean_up_links(yesterday_current_events_as_html)
    yesterday_current_events_as_html = remove_non_content_elements_from_current_events_html(
            yesterday_current_events_as_html
    )
    yesterday_current_events_as_html = remove_sources(yesterday_current_events_as_html)
    yesterday_current_events_as_html = make_wikipedia_internal_links_work(yesterday_current_events_as_html)

    return yesterday_current_events_as_html

def html_list_to_dict(dict, soup_ul):
    stack = [(soup_ul, dict)]
    while stack:
        current_ul, current_dict = stack.pop()
        for li in current_ul.find_all('li', recursive=False):
            sub_ul = li.find('ul')
            if sub_ul:
                sub_ul.extract()  # Remove it from current li
            text = re.sub(r'<li>', '', str(li))
            text = re.sub(r'</li>', '', text)
            text = markdownify(text)
            if sub_ul:
                text = "# " + text
            current_dict[text] = {}
            if sub_ul:
                stack.append((sub_ul, current_dict[text]))
    return dict

def add_current_events_to_prayer_list_dict(prayer_list_dict, ignored_wikipedia_current_event_sections):
    yesterday_current_events_as_html = get_current_events_of_yesterday_as_html()
    sections = re.split("<p>\s*?<b>(.+?)</b>\s*?</p>", yesterday_current_events_as_html, flags=re.MULTILINE)
    
    # Get rid of initial ''
    sections.pop(0)
    
    prayer_list_dict['# Current events'] = {}

    for i in range(0, len(sections), 2):

        section_heading = sections[i]

        # Short circuit if we are ignoring this section. Like Sports for example.
        # No need to pray about sport results
        if(any(section_heading == ignored_section for ignored_section in ignored_wikipedia_current_event_sections)):
            continue

        prayer_list_dict['# Current events'][f"## {section_heading}"] = {}
        sub_dict = prayer_list_dict['# Current events'][f"## {section_heading}"]
        soup = BeautifulSoup(sections[i+1], "html.parser")
        sub_dict = html_list_to_dict(sub_dict, soup.ul)

def clean_up_links(html):
    # I added this because we don't care about link titles when converting to Markdown
    html = re.sub(r'title=".+?"', '', html)
    # I added this because some Wikipedia link URLs contained parentheses,
    # which was messing with conversion to Markdown
    html = re.sub(r'href="(.+?)"', encode_parens, html)
    return html

def encode_parens(match):
    url = match.group(1)
    url = re.sub(r"\(", "%28", url)
    url = re.sub(r"\)", "%29", url)
    return f'href="{url}"'

def remove_non_content_elements_from_current_events_html(html):
    # First category header will begin with <p>. So first remove all the stuff before there
    html_after_strip_initial_stuff = remove_before_substring(html, "<p>")
    # Remove all the trailing divs
    html_after_remove_trailing_divs = remove_occurrences(
            html_after_strip_initial_stuff, "</div>"
    )
    return html_after_remove_trailing_divs

# Sources are extraneous information when praying through events.
# For our purposes, we are assuming a source is a link whose link text
# is wrapped in parentheses
def remove_sources(html):
    return re.sub(r'<a[^>]*href="[^"]*"[^>]*>\([^<]*\)</a>', '', html)

# Since we are pulling the content off of a Wikipedia page, all links to
# other Wikipedia pages are internal. To make them properly function for
# our purposes, we have to add back the base site.
def make_wikipedia_internal_links_work(html):
    return re.sub(r'href="/wiki/', r'href="https://en.wikipedia.org/wiki/', html)
