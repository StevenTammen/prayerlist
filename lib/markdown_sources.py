from .utility import *
import re

def get_prayer_list_markdown(file_name):
    return read_in_file(file_name)

def add_markdown_to_prayer_list_dict(markdown, prayer_list_dict):
    h1_split = re.split("(^# .+$)", markdown, flags=re.MULTILINE)
    
    # Get rid of leading whitespace from split list
    h1_split.pop(0)
    
    h1_dict = {}
    h1_key = ''
    for s in h1_split:
        is_header = s[0] == '#'
        last_thing_was_header = h1_key != ''
        if(is_header):
            if(last_thing_was_header):
                prayer_list_dict[h1_key] = {}
                h1_key = s
            else:
                h1_key = s
        else:
            prayer_list_dict[h1_key] = {}
            h1_dict[h1_key] = s
            h1_key = ''
    if(h1_key != ''):
        prayer_list_dict[h1_key] = {}

    for h1_key, h1_value in h1_dict.items():

        h2_split = re.split("(^## .+$)", h1_value, flags=re.MULTILINE)

        # Get rid of leading whitespace from split list
        h2_split.pop(0)

        # Replace \n with '' at beginning of strings to clean up items
        h2_split = [re.sub('^\n+', '', s) for s in h2_split]

        # Replace \n with '' at end of strings to clean up items
        h2_split = [re.sub('\n+$', '', s) for s in h2_split]

        # Replace '- ' with '' at beginning of strings to clean up items

        # Remove '' items from list
        h2_split = [s for s in h2_split if not s == '']

        h2_dict = {}
        h2_key = ''
        for s in h2_split:
            is_header = s[0] == '#'
            last_thing_was_header = h2_key != ''
            if(is_header):
                if(last_thing_was_header):
                    prayer_list_dict[h1_key][h2_key] = {}
                    h2_key = s
                else:
                    h2_key = s
            else:
                prayer_list_dict[h1_key][h2_key] = {}
                h2_dict[h2_key] = s
                h2_key = ''
        if(h2_key != ''):
            prayer_list_dict[h1_key][h2_key] = {}
        
        for h2_key, h2_value in h2_dict.items():
            ul_split = re.split("\n- ", h2_value, flags=re.MULTILINE)

            # Replace '- ' with '' at beginning of strings to clean up items
            ul_split = [re.sub('^- ', '', s) for s in ul_split]

            for s in ul_split:
                prayer_list_dict[h1_key][h2_key][s] = {}

    # for top_level_section in top_level_sections:
    #     all_content_sections_in_top_level_section = re.split(
    #         "^#.+$", top_level_section, flags=re.MULTILINE
    #     )
        
