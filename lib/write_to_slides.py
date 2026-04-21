import re
from datetime import datetime, timedelta
import os
from .utility import *

def get_journal_path(journal_dir_path, file_name):
    today = datetime.now()
    day_of_week_int = today.weekday()
    first_day_of_week = datetime.now() - timedelta(days=day_of_week_int)
    # You add six days to get to the last day of the week, not seven
    last_day_of_week = first_day_of_week + timedelta(days=6)

    first_day_of_week_year = first_day_of_week.year
    first_day_of_week_month = first_day_of_week.month
    first_day_of_week_day = first_day_of_week.day
    first_day_of_week_datestring = f'{first_day_of_week_year}-{first_day_of_week_month:02}-{first_day_of_week_day:02}'
    
    last_day_of_week_year = last_day_of_week.year
    last_day_of_week_month = last_day_of_week.month
    last_day_of_week_day = last_day_of_week.day
    last_day_of_week_datestring = f'{last_day_of_week_year}-{last_day_of_week_month:02}-{last_day_of_week_day:02}'

    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_datestring = f'{today_year}-{today_month:02}-{today_day:02}'

    week_dir = f'{journal_dir_path}/{first_day_of_week_datestring}-through-{last_day_of_week_datestring}'
    journal_path = f'{week_dir}/{today_datestring}/{today_datestring}-{file_name}'

    # As part of generating daily prayer lists, scaffold out weekly journal docs on the
    # first day of the week, if they don't already exist
    if(today_datestring == first_day_of_week_datestring):
        scaffold_empty_file_if_not_exist(f'{week_dir}/{first_day_of_week_datestring}-through-{last_day_of_week_datestring}-tasks.md')
        scaffold_empty_file_if_not_exist(f'{week_dir}/{first_day_of_week_datestring}-through-{last_day_of_week_datestring}-scratch.md')

    return journal_path

def scaffold_empty_file_if_not_exist(path):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "x") as file:
            file.write("")
    except FileExistsError:
        pass

markdown_content_re_pattern = re.compile(r'^markdown-content', re.MULTILINE)
def write_prayer_list_to_slides(
        prayer_list_dict,
        repeat_headers_across_slides_instead_of_only_first_time,
        daily_access_slides_path,
        journal_slides_path,
        template,
        title
    ):

    output = build_slides_markdown_from_nested_dict(prayer_list_dict, repeat_headers_across_slides_instead_of_only_first_time, title)

    # Use raw string to avoid Python writing backslashed apostrophes to file,
    # as a quirk of how Python sometimes stores strings
    new_file_content = fr'{markdown_content_re_pattern.sub(output, template)}'

    with safe_open_w(daily_access_slides_path) as f:
        f.writelines(new_file_content)
    # with safe_open_w(journal_slides_path) as f:
    #     f.writelines(new_file_content)

def build_slides_markdown_from_nested_dict(prayer_list_dict, repeat_headers_across_slides_instead_of_only_first_time, title):
    slides_markdown = f'## {title}'
    prayer_list = list(condense_nested_dict_into_flat_list(prayer_list_dict))
    # Support six levels of header nesting, not that we will probably ever have that much
    headers = ['', '', '', '', '', '']
    for prayer in prayer_list:
        header_portion = ''
        content_portion = ''
        for i in range(len(prayer)):
            if(prayer[i][0] == '#'):
                text = re.sub('#+ ', '', prayer[i])
                if(repeat_headers_across_slides_instead_of_only_first_time):
                    header_portion = ('#### ' + text) if (header_portion == '') else (header_portion + '\n\n#### > ' + text)
                else: # Only have headers when transitioning topics
                    # If header has already been displayed before
                    if(text == headers[i]):
                        pass
                    # Else = header has not yet been displayed
                    else:
                        header_portion = (header_portion + text) if (header_portion == '#### ') else (header_portion + '\n\n#### > ' + text)
                        headers[i] = text
            else:
                content_portion = prayer[i]
            prayer_slide = (header_portion) if (content_portion == '') else (header_portion + '\n\n' + content_portion)
        slides_markdown = slides_markdown + '\n\n---\n\n' + prayer_slide
    return slides_markdown
    
def condense_nested_dict_into_flat_list(tree):
    stack = [(tree, ())]  # (subtree, current_path)
    while stack:
        subtree, cur = stack.pop()
        if not subtree:
            yield cur
        else:
            for n, s in reversed(list(subtree.items())):
                stack.append((s, cur + (n,)))
