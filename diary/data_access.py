import base64
from datetime import datetime, timezone
import hashlib
from pony.orm import *

from common import SQLITE_DATABASE_PATH


def base64_encode(utf8_data: str) -> str:
    return base64.b64encode(utf8_data.encode('utf-8')).decode('ascii')


def diary_digest(title: str, text: str) -> str:
    d = hashlib.sha256()
    d.update(title.encode('utf-8'))
    d.update(text.encode('utf-8'))
    return d.hexdigest()


db = Database()

class Diary(db.Entity):
    id = PrimaryKey(str)
    title = Required(str)
    date = Required(datetime)
    text = Required(str)
    digest = Required(str)
    length = Required(int)
    labels = Required(StrArray)
    inserted_time = Required(datetime, default=datetime.now(timezone.utc))
    updated_time = Optional(datetime)


# Connect to SQLite database
db.bind(provider='sqlite', filename=SQLITE_DATABASE_PATH, create_db=True)

# Create tables in case they don't already exist
db.generate_mapping(create_tables=True)


def output_diaries(raw_diaries, max_count: int) -> dict:
    data = {}
    diaries = raw_diaries[:max_count]
    data['diaries'] = [{ 'title': diary.title, 'date': diary.date, 'text': diary.text.replace('\n', '<br />'), 'length': diary.length, 'labels': list(diary.labels),
            'changed': diary.updated_time if diary.updated_time else diary.inserted_time } for diary in diaries[:max_count]]
    data['token'] = diaries[-1].date.strftime('%Y-%m-%d') if len(raw_diaries) > max_count else ''
    return data


@db_session
def upsert_diary(title: str, date: datetime, text: str, labels: list[str], inserted: datetime, updated: datetime = None) -> int:
    '''
    Upsert a diary entry. It returns an integer with higher bit for existence and lower bit for change: 1 for insert, 2 for no change to existing, 3 for update.
    '''
    target_id = base64_encode(title)
    existing_diary = Diary.get(id=target_id)
    new_digest = diary_digest(title, text)
    new_length = len(text) - text.count('\n')
    change = 1
    if existing_diary:
        if (new_digest != existing_diary.digest or new_length != existing_diary.length) and updated and (existing_diary.updated_time is None or existing_diary.updated_time < updated):
            existing_diary.set(title=title, date=date, text=text, digest=new_digest, length=new_length, labels=labels, inserted_time=inserted, updated_time=updated)
        else:
            change = 0
    else:
        Diary(id=target_id, title=title, date=date, text=text, digest=new_digest, length=new_length, labels=labels, inserted_time=inserted, updated_time=updated)
    return change + (2 if existing_diary else 0)


@db_session
def diary_stats() -> dict: 
    '''
    Summarize the diary entries for count, total length, earliest date, latest date, latest changed time.
    '''
    result = list(select((count(d), sum(d.length), min(d.date), max(d.date), max(d.inserted_time), max(d.updated_time)) for d in Diary).first())
    result[2] = result[2].strftime('%Y-%m-%d')
    result[3] = result[3].strftime('%Y-%m-%d')
    result[4] = max(result[4], result[5]).strftime('%Y-%m-%d %H:%M:%S')
    stats_names = ['diaries', 'length', 'from', 'to', 'last_changed']
    return dict(zip(stats_names, result[:5]))


@db_session
def list_diaries(max_count: int = 20, before_date: datetime = None) -> list:
    '''
    List diaries by date in descending order. If before_date is provided, list diaries up to that date. By default, return the latest 20 diaries.
    '''
    if before_date:
        result = select(d for d in Diary if d.date < before_date).order_by(desc(Diary.date))
    else:
        result = Diary.select().order_by(desc(Diary.date))
    return output_diaries(result, max_count)


@db_session
def simple_search(keyword: str, max_count: int = 20, before_date: datetime = None) -> dict:
    '''
    Search diaries by keyword. If before_date is provided, search entries up to that date. By default, return the latest 20 entries.
    '''
    if before_date:
        results = select(d for d in Diary if (keyword in d.title or keyword in d.text or keyword in d.labels) and d.date < before_date).order_by(desc(Diary.date))
    else:
        results = select(d for d in Diary if keyword in d.title or keyword in d.text or keyword in d.labels).order_by(desc(Diary.date))
    return output_diaries(results, max_count)


@db_session
def by_month(year: int = 0, month: int = 0) -> dict:
    '''
    List diaries by year and month. If year and month are not provided, return the list for latest month with all available months.
    '''
    if year == 0 and month == 0:
        months = select((d.date.year, d.date.month) for d in Diary).distinct()
        if not months:
            return None
        months = sorted(list(months), reverse=True)
        year, month = months[0]
    start_date = datetime(year, month, 1)
    end_date = datetime(year + 1 if month == 12 else year, month + 1 if month < 12 else 1, 1)
    diaries = select(d for d in Diary if d.date >= start_date and d.date < end_date).order_by(desc(Diary.date))
    return output_diaries(diaries, 100).update({'year': year, 'month': month, 'months': months if months else None })


@db_session
def label_stats() -> dict:
    '''
    List all labels with their count.
    '''
    label_stats = {}
    for id, labels in select((d.id, d.labels) for d in Diary):
        for lname in labels:
            label_stats[lname] = label_stats.get(lname, 0) + 1
    return label_stats


@db_session
def by_label(label_name: str, max_count: int = 20, before_date: datetime = None) -> list:
    '''
    List diaries by label. If before_date is provided, list diaries up to that date. By default, return the latest 20 diaries.
    '''
    if before_date:
        result = select(d for d in Diary if label_name in d.labels and d.date < before_date).order_by(desc(Diary.date))
    else:
        result = select(d for d in Diary if label_name in d.labels).order_by(desc(Diary.date))
    return output_diaries(result, max_count)
