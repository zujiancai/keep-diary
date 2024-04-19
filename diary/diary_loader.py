import argparse
from datetime import datetime, timezone
import glob
import json

from common import DIARY_LABEL, get_diary_date
from data_access import upsert_diary


def validate_labels(note: dict, expect_label: str) -> list[str]:
    '''
    Validate the note contains expected label. If it does, return a list of the label names, other return None.
    '''
    if 'labels' in note:
        label_names = [label['name'] for label in note['labels']]
        if expect_label in label_names:
            return label_names


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load Keep notes from takeout folder to diary database.')
    parser.add_argument('source', help='The takeout folder that contains all Keep notes.')
    args = parser.parse_args()

    print('Starting to load notes at {0}.'.format(datetime.now(timezone.utc)))

    # Insert note data to Diaries and Tags tables
    note_count = 0
    insert_count = 0
    update_count = 0
    skip_count = 0
    for note_path in glob.glob(args.source + '/**/*.json', recursive=True):
        with open(note_path, 'r', encoding='utf-8') as f:
            note = json.load(f)
        ntitle, ntext, narchived = note['title'], note['textContent'], note['isArchived']
        if 'createdTimestampUsec' in note:
            inserted = datetime.fromtimestamp(int(note['createdTimestampUsec']) / 1000000, timezone.utc)
        if 'userEditedTimestampUsec' in note:
            updated = datetime.fromtimestamp(int(note['userEditedTimestampUsec']) / 1000000, timezone.utc)
        # Filter out notes without the diary label
        nlabels = validate_labels(note, DIARY_LABEL)
        if not nlabels:
            print('Skipped note for missing label: {}'.format(ntitle))
            skip_count += 1
            continue
        # Filter out notes that are not archived
        if not narchived:
            print('Skipped note for not archived: {}'.format(ntitle))
            skip_count += 1
            continue
        # Filter out notes without the date in title
        diary_date = get_diary_date(ntitle)
        if diary_date is None:
            print('Skipped note for missing date in title: {}'.format(ntitle))
            skip_count += 1
            continue
        # Insert or update the diary
        rs = upsert_diary(ntitle, diary_date, ntext, nlabels, inserted, updated)
        if rs == 3:
            print('Updated diary: {}'.format(ntitle))
            update_count += 1
        elif rs == 1:
            print('Inserted diary: {}'.format(ntitle))
            insert_count += 1
        else: # rs == 2
            print('Skipped diary for no change to existing: {}'.format(ntitle))
            skip_count += 1
        note_count += 1

    print('Finished with {0} notes at {4}: inserted {1}, updated {2} and skipped {3}.'.format(note_count, insert_count, update_count, skip_count, datetime.now(timezone.utc )))
