"""
-지도(카카오맵) 관련 블루프린트
-팀프로젝트 공용 파일
-본 파일 중 '랜드마크 상세 페이지 라우팅' 영역 구현
"""

import pymysql
from flask import Flask, Blueprint, request, jsonify, session, current_app, render_template
from flask_cors import CORS

map_bp = Blueprint('map', __name__, url_prefix='/koring')
CORS(map_bp, supports_credentials=True)  # 세션 유지용 CORS

# DB 연결
def get_connection():
    return pymysql.connect(**current_app.config['DB_CONFIG'])

#사이드바 연결
@map_bp.route('/search_spot')
def search_spot():
    dev = request.args.get('dev', '')
    return render_template('map.html', dev=dev)

# 방문 기록 저장
@map_bp.route("/visit", methods=['POST'])
def add_visit():
    if 'userID' not in session:
        return jsonify({"status": "error", "message": "로그인이 필요합니다."}), 401

    data = request.get_json(silent=True) or {}
    spot_id = data.get("spotID")
    user_id = session['userID']  # 로그인 세션에서 가져오기

    if not spot_id:
        return jsonify({"status": "error", "message": "spotID 필수"}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO tVisit(visitDate, userID, spotID) VALUES (NOW(), %s, %s)"
            cursor.execute(sql, (user_id, spot_id))
            conn.commit()
            visit_id = cursor.lastrowid
    finally:
        conn.close()

    return jsonify({"status": "ok", "data": {"visitID": visit_id}}), 201

# ------------------------------------------------------
# 담당 구현 영역
# - 주요 관광지 개별 페이지 라우팅
# - Kakao Map API Key 전달
# - 랜드마크 상세 페이지 렌더링
@map_bp.route("/이순신장군동상")
def yisunshin():
    kakao_map_key = map_bp.config['KAKAO_MAP_KEY']
    return render_template("landmarks/yisunshin.html", kakao_map_key=kakao_map_key)

@map_bp.route("/남산타워")
def namsan():
    kakao_map_key = map_bp.config['KAKAO_MAP_KEY']
    return render_template("landmarks/namsan.html", kakao_map_key=kakao_map_key)

@map_bp.route("/북촌한옥마을")
def bukchon():
    kakao_map_key = map_bp.config['KAKAO_MAP_KEY']
    return render_template("landmarks/bukchon.html", kakao_map_key=kakao_map_key)

@map_bp.route("/경복궁")
def gyeongbokgung():
    kakao_map_key = map_bp.config['KAKAO_MAP_KEY']
    return render_template("landmarks/gyeongbokgung.html", kakao_map_key=kakao_map_key)

# ------------------------------------------------------