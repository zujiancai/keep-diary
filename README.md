# Keep Diary
I use Google Keep to write diaries. Google Keep is very convient to work with but lacks grouping and statistics functionality. To export the diaries and set up a web front end, I can apply my own engineering.

## Install
1. Clone or download this repository.
1. Open a terminal to the repository folder (`keep-diary`).
1. Run `pipenv install -r requirements.txt` to install dependencies.

## Dependencies:
1. `Pony ORM` for accessing database.
1. `Flask` for web front end.

## Run
First we need to download all the Keep files through Google Takeout.
1. Go to [Google Takeout](https://takeout.google.com/settings/takeout).
1. Make sure the 'Keep' checkbox is selected (you can deselect all others).
1. Download and export the archive to a folder (only json type is required). E.g., I use this command with 7zip: 
    ```
    "C:\Program Files\7-Zip\7z.exe" x %Downloads%\takeout-20240410T185002Z-001.zip -oE:\KeepNotes_20240410 *.json -r
    ```
1. Change `diary_config.json` for your own usage. My diaries in Keep all have a label `日记` and their title contain a date string like 2024-03-22.
1. [Optional] Change `data_access.py` to bind with a different database. Currently it uses sqlite with a local file (see `common.py`). 
1. Run diary loader to import diaries from takeout files:
    ```
    python diary_loader.py E:\KeepNotes_20240410
    ```
1. Start Flask server:
    ```
    flask run
    ```
