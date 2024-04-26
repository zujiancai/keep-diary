from datetime import datetime
from flask import Flask, render_template, request, jsonify

from data_access import get_diary, diary_stats, by_date, by_month

app = Flask(__name__)


def get_stats_text() -> str:
    stats_dict = diary_stats()
    return 'This book contains {diaries} diaries with {length} characters, covering date range from {from} to {to}. The last change was at {last_changed}.'.format(**stats_dict)


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
    result = by_date()
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    cards = render_template('cardlist.html', diaries=result['diaries'])
    return render_template('index.html', cards=cards, token=result['token'] if 'token' in result else '', stats=get_stats_text())


@app.route("/months")
def months():
    syear = request.args.get('year', None)
    smonth = request.args.get('month', None)
    if syear and smonth:
        result = by_month(int(syear), int(smonth))
    else:
        result = by_month()
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    cards = render_template('cardlist.html', diaries=result['diaries'])
    return render_template('months.html', cards=cards, curmonth=result['month'], curyear=result['year'], months=result['months'], stats=get_stats_text())


@app.route("/list-diaries")
def list():
    before_date = request.args.get('before', None)
    max_count = int(request.args.get('max', 20))
    result = by_date(max_count, datetime.strptime(before_date, '%Y-%m-%d') if before_date else None)
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    rbody = {'html': render_template('cardlist.html', diaries=result['diaries']), 'token': result['token'] if 'token' in result else ''}
    return jsonify(rbody)


@app.route("/get-diary")
def diary_details():
    diary_id = request.args.get('id')
    result = get_diary(diary_id)
    if not result:
        return render_template('errors/404.html'), 404
    return render_template('diarymodal.html', diary=result)
