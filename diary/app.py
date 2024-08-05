from datetime import datetime
from flask import Flask, render_template, request, jsonify

from data_access import get_diary, diary_stats, by_date, by_month, simple_search

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
    result = by_date()
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return render_template('errors/404.html'), 404
    cards = render_template('cardlist.html', diaries=result['diaries'])
    return render_template('index.html', cards=cards, token=result['token'] if 'token' in result else '', stats=diary_stats())


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
    return render_template('months.html', cards=cards, curmonth=result['month'], curyear=result['year'], months=result['months'])


@app.route("/list-diaries")
def list():
    before_date_str = request.args.get('before', None)
    max_count = int(request.args.get('max', 20))
    search_keyword = request.args.get('find', None)
    before_date = datetime.strptime(before_date_str, '%Y-%m-%d') if before_date_str else None
    result = by_date(max_count, before_date) if not search_keyword else simple_search(search_keyword, max_count, before_date)
    if not result or not 'diaries' in result or len(result['diaries']) == 0:
        return '', 404
    rbody = {'html': render_template('cardlist.html', diaries=result['diaries']), 'token': result['token'] if 'token' in result else ''}
    return jsonify(rbody)


@app.route("/get-diary")
def diary_details():
    diary_id = request.args.get('id')
    result = get_diary(diary_id)
    if not result:
        return render_template('errors/404.html'), 404
    return render_template('diarymodal.html', diary=result)
