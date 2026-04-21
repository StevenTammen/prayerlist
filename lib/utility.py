#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import calendar
import re
import os

def get_html(url):
		"""
		Retrieves the HTML content of a webpage.

		Args:
			url: The URL of the webpage.

		Returns:
			The HTML content as a string, or None if the request fails.
		"""
		try:
				headers = {
					'User-Agent': 'Prayerlist/1.0 (steven@steventammen.com)'
				}
				response = requests.get(url, headers=headers)
				response.raise_for_status()	# Raise HTTPError for bad responses (4xx or 5xx)
				return response.text
		except requests.exceptions.RequestException as e:
				print(f"Error fetching URL: {e}")
				return None

def find_matching_string(string_list, regex):
		"""
		Returns the first string in the list that matches the regex, or None if no match is found.
		"""
		for string in string_list:
				if re.search(regex, str(string)):
						return str(string)
		return None

def remove_before_substring(text, substring):
		index = text.find(substring)
		if index == -1:
				return text	# Substring not found, return original string
		return text[index:]

def remove_occurrences(s: str, part: str) -> str:
		# Continue removing occurrences of 'part' as long as it exists in 's'
		while part in s:
				# Find the index of the leftmost occurrence of 'part'
				part_start_index = s.find(part)

				# Remove the substring 'part' by concatenating segments before and after 'part'
				s = s[:part_start_index] + s[part_start_index + len(part) :]

		# Return the updated string after all occurrences are removed
		return s

def find_string_with_substring(soup_string_list, substring):
	"""
	Returns the first string in the list that contains the substring, or None if no string contains the substring.

	Args:
		string_list: A list of strings.
		substring: The substring to search for.

	Returns:
		The first string in the list that contains the substring, or None if no string contains the substring.
	"""
	return next((str(s.prettify()) for s in soup_string_list if substring in str(s)), None)\
	
# https://stackoverflow.com/questions/49640513/
def read_in_file(file_path):
	with open(file_path, "r", encoding="utf8") as f:
		return f.read()
	
def safe_open_w(path):
  '''
  Open "path" for writing, creating any parent directories as needed.

  https://stackoverflow.com/a/23794010
  '''
  os.makedirs(os.path.dirname(path), exist_ok=True)
  return open(path, 'w', encoding="utf8")