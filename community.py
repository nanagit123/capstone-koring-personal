"""
-게시판 관련 블루프린트
-팀프로젝트 공용 파일
-본 파일의 게시글/댓글 API 연동 디버깅 및 오류 수정 구현
"""

import pymysql
from flask import Blueprint, request, jsonify, session, current_app, render_template
from flask_cors import CORS

community_bp = Blueprint('community', __name__, url_prefix='/koring/community')
CORS(community_bp, supports_credentials=True)  # 세션 유지용

# DB 연결
def get_connection():
    return pymysql.connect(**current_app.config['DB_CONFIG'])

# 권한 체크
def check_ownership(cursor, table, id_col, id_val, userID):
    cursor.execute(f"SELECT userID FROM {table} WHERE {id_col}=%s", (id_val,))
    row = cursor.fetchone()
    return row and row['userID'] == userID

# 게시글 목록 페이지
@community_bp.route('/', methods=['GET'])
def get_posts():
    conn = get_connection()
    posts = []
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
SELECT tpost.postID, tpost.postTitle, tpost.postContent, tpost.postCreatedAt,
       tuser.userLoginID AS username
FROM tpost
LEFT JOIN tuser ON tpost.userID = tuser.userID
ORDER BY tpost.postCreatedAt DESC
"""
            cursor.execute(sql)
            posts = cursor.fetchall()
    finally:
        conn.close()
    return render_template('community.html', posts=posts)

# 게시글 상세보기 (HTML)
@community_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post_detail(post_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
SELECT tpost.postID, tpost.postTitle, tpost.postContent, tpost.postCreatedAt,
       tuser.userLoginID AS username
FROM tpost
LEFT JOIN tuser ON tpost.userID = tuser.userID
WHERE tpost.postID = %s
"""
            cursor.execute(sql, (post_id,))
            post = cursor.fetchone()
            if not post:
                return "게시글이 없습니다.", 404

            return render_template('show.html', post=post)
    finally:
        conn.close()

# 게시글 상세보기 (JSON)
@community_bp.route('/api/post/<int:post_id>', methods=['GET'])
def get_post_detail_api(post_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
SELECT tpost.postID, tpost.postTitle, tpost.postContent, tpost.postCreatedAt,
       tuser.userLoginID AS username
FROM tpost
LEFT JOIN tuser ON tpost.userID = tuser.userID
WHERE tpost.postID = %s
"""
            cursor.execute(sql, (post_id,))
            post = cursor.fetchone()
            if not post:
                return jsonify({'success': False, 'message': '게시글 없음'}), 404

            return jsonify({
                'success': True,
                'post': {
                    'id': post['postID'],
                    'title': post['postTitle'],
                    'content': post['postContent'],
                    'username': post['username'],
                    'date': str(post['postCreatedAt'])
                }
            })
    finally:
        conn.close()

# 글 작성 페이지
@community_bp.route('/create_post', methods=['GET'])
def create_post_page():
    return render_template('c_edit.html')

# 글 작성
@community_bp.route('/posts', methods=['POST'])
def create_post():
    if 'userID' not in session:  
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    data = request.json
    title = data.get('postTitle')
    content = data.get('postContent')
    imageURL = data.get('postImageURL', None)
    userID = session['userID']

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
INSERT INTO tpost(postTitle, postContent, postImageURL, postCreatedAt, userID)
VALUES (%s, %s, %s, NOW(), %s)
"""
            cursor.execute(sql, (title, content, imageURL, userID))
        conn.commit()
        return jsonify({'success': True, 'message': '글 작성 완료'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'DB 오류 발생'}), 500
    finally:
        conn.close()

# 댓글 목록
@community_bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM tcomment WHERE postID=%s ORDER BY commentDate ASC",
                (post_id,)
            )
            comments = cursor.fetchall()
        return jsonify(comments)
    finally:
        conn.close()

# 댓글 작성
@community_bp.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    if 'userID' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    data = request.json
    content = data.get('commentContent')
    userID = session['userID']

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
INSERT INTO tcomment(commentContent, commentDate, postID, userID)
VALUES (%s, NOW(), %s, %s)
"""
            cursor.execute(sql, (content, post_id, userID))
        conn.commit()
        return jsonify({'success': True, 'message': '댓글 작성 완료'})
    finally:
        conn.close()

# 댓글 수정
@community_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    if 'userID' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    data = request.json
    content = data.get('commentContent')
    userID = session['userID']

    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if not check_ownership(cursor, 'tcomment', 'commentID', comment_id, userID):
                return jsonify({'success': False, 'message': '권한이 없습니다.'}), 403

            cursor.execute(
                "UPDATE tcomment SET commentContent=%s WHERE commentID=%s",
                (content, comment_id)
            )
        conn.commit()
        return jsonify({'success': True, 'message': '댓글 수정 완료'})
    finally:
        conn.close()

# 댓글 삭제
@community_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if 'userID' not in session:
        return jsonify({'success': False, 'message': '로그인이 필요합니다.'}), 401

    userID = session['userID']
    conn = get_connection()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            if not check_ownership(cursor, 'tcomment', 'commentID', comment_id, userID):
                return jsonify({'success': False, 'message': '권한이 없습니다.'}), 403

            cursor.execute("DELETE FROM tcomment WHERE commentID=%s", (comment_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '댓글 삭제 완료'})
    
    finally:
        conn.close()
