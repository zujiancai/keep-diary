from datetime import datetime
import json
import re


SQLITE_DATABASE_PATH = '..\\..\\keep-diary.db'

DIARY_CONFIG_PATH = 'diary_config.json'

with open(DIARY_CONFIG_PATH, 'r', encoding='utf-8') as f:
    settings = json.load(f)

DIARY_LABEL = settings['diary_label']


def get_diary_date(title: str) -> datetime:
    '''
    Extract the date from the diary title with configured regex and date format. If the date is not found, return None.
    '''
    search_date = re.search(settings['title_date_regex'], title)
    if search_date:
        return datetime.strptime(search_date.group(), settings['title_date_format'])
