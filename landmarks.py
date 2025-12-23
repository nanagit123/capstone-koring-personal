"""
-관광 명소 관련 블루프린트
-팀프로젝트 공용 파일
-본 파일 중 '명소 상세 페이지 라우팅' 영역 구현
"""

from flask import Blueprint, render_template, request, current_app
from google.cloud import translate_v2 as translate
import html

# 블루프린트 정의
landmarks_bp = Blueprint("bp", __name__, url_prefix="/koring/landmarks")

# ------------------------------------------------------
# 담당 구현 영역
# - 명소 상세 페이지 라우팅
# - 개별 명소 URL 엔드포인트 정의
# - Kakao Map API 키 템플릿에 전달
# - 공통 렌더링 함수(reder_landmark_page) 재사용


#북촌 한옥 마을
@landmarks_bp.route("/북촌한옥마을", endpoint="bukchon")
def bukchon_page():
    #app.py 설정에 등록된 카카오맵 api 키 사용
    kakao_map_key = current_app.config['KAKAO_MAP_KEY']  
    desc_ko = "북촌한옥마을은 전통 한옥이 모여 있는 서울의 대표적인 역사 문화 공간입니다."
    # 공통 템플릿 렌더링 함수 호출
    return render_landmark_page("landmarks/bukchon.html", desc_ko, kakao_map_key=kakao_map_key)



# 경복궁
@landmarks_bp.route("/경복궁", endpoint="gyeongbokgung")
def gyeongbokgung_page():
    kakao_map_key = current_app.config['KAKAO_MAP_KEY']
    desc_ko = "경복궁은 조선시대의 법궁으로, 아름다운 건축물과 유서 깊은 역사를 자랑합니다."
    return render_landmark_page("landmarks/gyeongbokgung.html", desc_ko, kakao_map_key=kakao_map_key)



# 남산타워
@landmarks_bp.route("/남산타워", endpoint="namsan")
def namsan_page():
    kakao_map_key = current_app.config['KAKAO_MAP_KEY']
    desc_ko = (
        "남산공원은 서울 중심부에 위치한 자연 휴식 공간으로 시민들에게 맑은 공기를 제공합니다. "
        "서울 N타워와 케이블카 등 다양한 관광시설을 갖추고 있습니다."
    )
    return render_landmark_page("landmarks/namsan.html", desc_ko, kakao_map_key=kakao_map_key)



# 이순신 장군 동상
@landmarks_bp.route("/이순신장군동상", endpoint="yisunshin")
def yisunshin_page():
    kakao_map_key = current_app.config['KAKAO_MAP_KEY']
    desc_ko = "광화문 광장에 위치한 이순신 장군 동상은 충무공의 위대한 업적을 기리기 위해 세워졌습니다."
    return render_landmark_page("landmarks/yisunshin.html", desc_ko, kakao_map_key=kakao_map_key)
# ------------------------------------------------------여기까지 구현


# 공통 렌더링 함수 (자동 번역 + 추가 인자 유연 처리)
def render_landmark_page(template_name, desc_ko, **kwargs):
    """
    각 랜드마크 페이지에서 공통적으로 호출됨.
    - lang 파라미터(기본값 'ko')를 읽어서 자동 번역 수행
    - Google Translate API 호출
    - html.unescape()로 특수문자(&#39;) 복원
    - Kakao 지도 키 등 추가 인자는 **kwargs로 받아서 템플릿에 함께 전달
    - 오류 발생 시 원문(desc_ko) 그대로 표시
    """

    # 현재 선택된 언어 파라미터 읽기 (예: ?lang=en)
    lang = request.args.get("lang", "ko")

    # Google 번역 클라이언트 생성 (환경변수는 app.py에서 이미 설정됨)
    translate_client = translate.Client()

    # 번역 처리
    if lang == "ko":
        translated = desc_ko  # 한국어 그대로 표시
    else:
        try:
            result = translate_client.translate(desc_ko, target_language=lang)
            translated = html.unescape(result["translatedText"])  # 특수문자 복원
            print(f"[번역됨] ({lang}) → {translated[:60]}...")  # 콘솔 확인용
        except Exception as e:
            print("[번역 오류]", e)
            translated = desc_ko  # 오류 시 원문 표시

    # 템플릿 렌더링 시 desc, lang, kakao_map_key 등 모두 전달
    #    **kwargs 덕분에 kakao_map_key 이외에도 다른 인자를 쉽게 추가 가능
    return render_template(
        template_name,
        desc=translated,
        lang=lang,
        **kwargs
    )
