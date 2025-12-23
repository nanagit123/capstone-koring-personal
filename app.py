import os
from flask import Flask, render_template, request, url_for, current_app, g   
from flask_cors import CORS
from config import Config
from google.cloud import translate_v2 as translate
from landmarks import landmarks_bp
from login import login_bp
from signup import signup_bp
from community import community_bp
from album import album_bp
from map import map_bp
from reservation import reservation_bp
from restaurant import restaurant_bp
from translate import translate_bp  

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
app.config['DB_CONFIG'] = Config.DB_CONFIG
app.config.from_object(Config)

CORS(app, supports_credentials=True, origins=Config.CORS_ORIGINS)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_CREDENTIALS_PATH")
translate_client = translate.Client()

@app.before_request
def set_lang():
    g.lang = request.args.get('lang', 'ko')  
    print(f"[before_request] 현재 언어 설정됨 → {g.lang}")

def tr(text, lang=None):
    if lang is None:
        lang = getattr(g, 'lang', None) or request.args.get('lang', 'ko')
    if lang == 'ko':
        return text
    try:
        result = translate_client.translate(text, target_language=lang)
        print(f"[번역됨] {text} → {result['translatedText']} ({lang})")
        return result['translatedText']
    except Exception as e:
        print("[번역 오류]", e)
        return text  
app.register_blueprint(landmarks_bp)
app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(album_bp)
app.register_blueprint(community_bp)
app.register_blueprint(map_bp)
app.register_blueprint(reservation_bp)
app.register_blueprint(restaurant_bp)
app.register_blueprint(translate_bp) 

from translate import tr  
app.jinja_env.globals['tr'] = tr

@app.route('/')
@app.route('/mainpage')
def mainpage():
    lang = g.lang
    print("현재 페이지 언어:", lang)
    texts = {
        'title': "한국의 대표 관광지",
        'description': "Koring은 관광지 길찾기, 번역, 커뮤니티 기능을 제공합니다."
    }
    translated = {key: tr(value) for key, value in texts.items()}

    return render_template(
        "mainpage.html",
        lang=lang,
        title=translated['title'],
        description=translated['description']
    )
@app.route("/koring/restaurant")
def restaurant_page():
    return render_template("restaurant.html")

@app.route("/restaurant/result")
def restaurant_result_page():
    return render_template("recommend.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)