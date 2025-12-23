import pymysql
from flask import Flask, jsonify, current_app
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# DB 연결 함수
def get_connection():
    return pymysql.connect(**current_app.config['DB_CONFIG'])


# 메인 페이지
@app.route('/')
def mainpage():
    return jsonify({"message": "홈 페이지입니다."})


# 이 달의 추천 명소
@app.route("/recommend-spots")
def recommend_spots():
    sql = """
        SELECT spotID AS id, spotName AS name, imagePath AS image 
        FROM tSpot 
        ORDER BY createdAt DESC 
        LIMIT 5
    """
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            spots = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({"status": "ok", "data": spots})


# 공지사항
@app.route("/notices/preview")
def notices_preview():
    notices = [
        {"id": 1, "title": "11월 이벤트 안내"},
        {"id": 2, "title": "서버 점검 공지"},
        {"id": 3, "title": "새로운 기능 업데이트"},
    ]
    return jsonify({"status": "ok", "data": notices})


# 커뮤니티 미리보기
@app.route("/community/preview")
def community_preview():
    sql = """
        SELECT p.postID AS id, p.postTitle AS title, p.postCreatedAt AS createdAt, 
               u.userLoginID AS author
        FROM tPost p
        JOIN tUser u ON u.userID = p.userID
        ORDER BY p.postID DESC
        LIMIT 3
    """
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            posts = cursor.fetchall()
    finally:
        conn.close()

    return jsonify({"status": "ok", "data": posts})


# Flask 실행
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
