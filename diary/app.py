from datetime import datetime
from flask import Flask, render_template, request, jsonify

from data_access import list_diaries, diary_stats

app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.route("/")
@app.route("/index")
def index():
    result = list_diaries()
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    cards = render_template('cardlist.html', diaries=result['diaries'])
    stats_dict = diary_stats()
    stats = 'This book contains {diaries} diaries with {length} characters, covering date range from {from} to {to}. The last change was at {last_changed}.'.format(**stats_dict)
    return render_template('index.html', cards=cards, token=result['token'] if 'token' in result else '', stats=stats)


@app.route("/list-diaries")
def diaries_by_date():
    before_date = request.args.get('before', None)
    max_count = int(request.args.get('max', 20))
    result = list_diaries(max_count, datetime.strptime(before_date, '%Y-%m-%d') if before_date else None)
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    return jsonify({'html': render_template('cardlist.html', diaries=result['diaries']), 'token': result['token'] if 'token' in result else ''})
