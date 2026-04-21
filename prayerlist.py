#!/usr/bin/env python3

from lib.current_events import *
from lib.ichthys_prayer_list import *
from lib.markdown_sources import *
from lib.write_to_slides import *
import config

# Read in template just once, then pass it as a variable
template = read_in_file('templates/slides-template.html')

# Morning prayer list
morning_prayer_list = {}
morning_prayer_list_markdown = get_prayer_list_markdown(f'{config.prayer_lists_markdown_source_path}/morning-prayer-list.md')
add_markdown_to_prayer_list_dict(morning_prayer_list_markdown, morning_prayer_list)
write_prayer_list_to_slides(
    morning_prayer_list,
    config.repeat_headers_across_slides_instead_of_only_first_time,
    f'{config.daily_access_dir_path}/morning-prayer-list.html',
    get_journal_path(config.journal_dir_path, "morning-prayer-list.html"),
    template,
    'Morning prayer list'
)

# Afternoon prayer list
afternoon_prayer_list = {}
add_ichthys_prayer_list_to_prayer_list_dict(afternoon_prayer_list, config.pray_through_ichthys_prayer_list_in_x_days)
write_prayer_list_to_slides(
    afternoon_prayer_list,
    config.repeat_headers_across_slides_instead_of_only_first_time,
    f'{config.daily_access_dir_path}/afternoon-prayer-list.html',
    get_journal_path(config.journal_dir_path, "afternoon-prayer-list.html"),
    template,
    'Afternoon prayer list'
)

# Evening prayer list
evening_prayer_list = {}
evening_prayer_list_markdown = get_prayer_list_markdown(f'{config.prayer_lists_markdown_source_path}/evening-prayer-list.md')
add_markdown_to_prayer_list_dict(evening_prayer_list_markdown, evening_prayer_list)
add_current_events_to_prayer_list_dict(evening_prayer_list, config.ignored_wikipedia_current_event_sections)
write_prayer_list_to_slides(
    evening_prayer_list,
    config.repeat_headers_across_slides_instead_of_only_first_time,
    f'{config.daily_access_dir_path}/evening-prayer-list.html',
    get_journal_path(config.journal_dir_path, "evening-prayer-list.html"),
    template,
    'Evening prayer list'
)
