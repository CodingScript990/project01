from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb://test:test@localhost', 27017)
# client = MongoClient('localhost', 27017)
db = client.dbsparta_plus_week1

from datetime import datetime

# index.html
@app.route('/')
def home():
    return render_template('index.html')

# Diary GET 방식
@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))
    return jsonify({'all_diary': diaries})

# Diary POST 방식
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    # File Area
    file = request.files["file_give"]

    # File에서 '.'으로 시작하는 것 중에서 맨 마지막 '.'만 들고와라!
    extension = file.filename.split('.')[-1]

    # 현재시각 Data
    today = datetime.now()

    # year/month/day/hour/minute/second
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    # year/month/day
    datatime = today.strftime('%Y.%m.%d')

    # File 이름 구분 짓기
    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    doc = {
        'title' : title_receive,
        'content' : content_receive,
        'file' : f'{filename}.{extension}',
        'data' : datatime
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)