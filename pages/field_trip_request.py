import streamlit as st
from app.sidebar_manager import SidebarManager
from streamlit_drawable_canvas import st_canvas
import tempfile
from datetime import date, timedelta
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import datetime
import holidays
import img2pdf
import os
import io
import tempfile
import base64
import pathlib
import sys

# 페이지 설정
st.set_page_config(
    page_title="교외체험학습 신청서",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 렌더링
sidebar = SidebarManager()
sidebar.render_sidebar()

class ResourceManager:
    def __init__(self):
        self.base_dir = self.get_absolute_path()
        self.image_dir = self.base_dir / "images"
        self.font_dir = self.base_dir / "fonts"
        
        # 파일 경로 설정
        self.paths = {
            "신청서 양식": self.image_dir / "studywork001.png",
            "별지 양식": self.image_dir / "studywork002.png",
            "로고": self.image_dir / "logo.png",
            "폰트": self.font_dir / "AppleGothic.ttf"
        }
        
        # 시스템 폰트 백업 경로
        self.system_font_paths = [
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/System/Library/Fonts/AppleGothic.ttf",
            "C:\\Windows\\Fonts\\malgun.ttf"
        ]

    @staticmethod
    def get_absolute_path():
        """Get the absolute path for the application."""
        if os.path.exists("/mount/src/study-work"):
            return pathlib.Path("/mount/src/study-work")
        elif os.path.exists("/workspaces/Study-work"):
            return pathlib.Path("/workspaces/Study-work")
        else:
            return pathlib.Path(__file__).parent.parent.resolve()

    def get_font_path(self):
        """폰트 파일 경로를 찾아 반환"""
        if self.paths["폰트"].exists():
            return str(self.paths["폰트"])
        
        for system_font in self.system_font_paths:
            if os.path.exists(system_font):
                return system_font
        
        st.error("폰트 파일을 찾을 수 없습니다.")
        st.info("나눔고딕 폰트를 설치하거나 fonts 디렉토리에 폰트 파일을 추가해주세요.")
        st.stop()

    def validate_resources(self):
        """리소스 파일 검증"""
        for name, path in self.paths.items():
            if name != "폰트" and not path.exists():
                st.error(f"{name}을(를) 찾을 수 없습니다. 경로: {path}")
                st.stop()
        
        self.font_path = self.get_font_path()

    def print_debug_info(self):
        """디버깅 정보 출력"""
        st.write("현재 경로 정보:")
        st.write(f"BASE_DIR: {self.base_dir}")
        st.write(f"IMAGE_DIR: {self.image_dir}")
        st.write(f"FONT_DIR: {self.font_dir}")
        st.write(f"사용 중인 폰트 경로: {self.font_path}")

# ResourceManager 인스턴스 생성
resources = ResourceManager()

# 디버깅 정보 출력 (필요한 경우)
if os.getenv('STREAMLIT_DEBUG') == 'true':
    resources.print_debug_info()

# 리소스 검증
resources.validate_resources()

# 전역 변수로 경로 설정
BASE_DIR = resources.base_dir
IMAGE_DIR = resources.image_dir
FONT_DIR = resources.font_dir
img_path = resources.paths["신청서 양식"]
extra_img_path = resources.paths["별지 양식"]
logo_path = resources.paths["로고"]
font_path = resources.font_path

# 디버깅을 위한 경로 출력
if os.getenv('STREAMLIT_DEBUG') == 'true':
    st.write(f"""
    현재 설정된 경로:
    - 기본 경로: {BASE_DIR}
    - 이미지 경로: {IMAGE_DIR}
    - 폰트 경로: {FONT_DIR}
    - 신청서 양식: {img_path}
    - 별지 양식: {extra_img_path}
    - 로고: {logo_path}
    - 폰트: {font_path}
    """)

# 1. 세션 상태 초기화 부분 수정
if 'student_canvas_key' not in st.session_state:
    st.session_state.student_canvas_key = 0
    st.session_state.student_canvas_initialized = False  # 새로운 초기화 플래그
if 'guardian_canvas_key' not in st.session_state:
    st.session_state.guardian_canvas_key = 100
    st.session_state.guardian_canvas_initialized = False  # 새로운 초기화 플래그
if 'student_signature_img' not in st.session_state:
    st.session_state.student_signature_img = None
if 'guardian_signature_img' not in st.session_state:
    st.session_state.guardian_signature_img = None

# 현재 스텝 세션 초기화
if 'step' not in st.session_state:
    st.session_state.step = 1

# 교외체험 학습 계획 저장을 위한 초기화
if 'plans' not in st.session_state:
    st.session_state.plans = {}

# 메인 타이틀 표시
st.markdown("<h1 style='text-align: center;'>교외체험학습 신청서</h1>", unsafe_allow_html=True)

# 로고 이미지 처리
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return encoded
    except FileNotFoundError:
        return None

# 로고 표시
logo_base64 = get_base64_image(logo_path) if logo_path.exists() else None

# 로고와 학교명 표시 (서브타이틀로)
if logo_base64:
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center;">
            <img src="data:image/png;base64,{logo_base64}" alt="로고" style="margin-right: 10px; width: 40px; height: 40px;">
            <h3 style="margin: 0;">온양한올고등학교</h3>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h3 style='text-align: center;'>온양한올고등학교</h3>", unsafe_allow_html=True)

# 단일 탭 그룹 생성
tabs = st.tabs([
    "1. 학적 입력", 
    "2. 신청 정보", 
    "3. 학습 계획",  # 엑셀 테이블 입력 부분으로 구성
    "4. 보호자 정보", 
    "5. 서명 입력", 
    "6. 신청서 확인"
])

# 탭 1: 학적 입력
with tabs[0]:
    st.header("학적 입력")
    st.text_input('성명', key='student_name')  # 고유한 key
    st.selectbox('학년', ['학년을 선택하세요', '1학년', '2학년', '3학년'], key='student_grade')
    st.selectbox('반', ['반을 선택하세요'] + [f'{i}반' for i in range(1, 13)], key='student_class')
    st.number_input('번호', min_value=1, max_value=50, step=1, key='student_number')

# 탭 2: 신청 정보 입력
with tabs[1]:
    st.header("교외체험학습 신청 정보 입력")

    # 교외체험학습 시작일과 종료일 입력란 나란히 배치
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('교외체험학습 시작일', min_value=date.today() + timedelta(days=1), key='start_date')
    with col2:
        end_date = st.date_input('교외체험학습 종료일', min_value=start_date + timedelta(days=1), key='end_date')

    # 출석인정 시작일/종료일 설명 텍스트 추가
    st.markdown("""
    **출석인정 기간 입력 안내**
    
    출석인정 기간은 교외체험학습 기간에서 '공휴일'을 빼고 입력하세요.  
    교외체험학습 종료일이 '일요일'이라면 '금요일'까지 출석인정기간으로 입력하세요.
    """)

    # 출석인정 시작일과 종료일 입력란 나란히 배치
    col3, col4 = st.columns(2)
    with col3:
        attendance_start_date = st.date_input('출석인정 시작일', min_value=date.today() + timedelta(days=1), key='attendance_start_date')
    with col4:
        attendance_end_date = st.date_input('출석인정 종료일', min_value=attendance_start_date + timedelta(days=1), key='attendance_end_date')

    # 학습 형태 선택
    st.selectbox(
        '학습 형태 선택', 
        ['학습 형태를 선택하세요', '가족 동반 여행', '친인척 경조사 참석 및 방문', '유적 탐방', '문학 기행', 
         '우리 문화 및 세계 문화 체험', '국토 순례', '자연 탐사', '직업 체험', '기타'], 
        key='learning_type'
    )

    # 목적과 목적지 입력
    st.text_input('목적', key='purpose')
    st.text_input('목적지', key='destination')

# 탭 3: 학습 계획 입력 (폼 기반 동적 추가)
with tabs[2]:
    st.header("교외체험 학습 계획 입력")
    
    # 설명 텍스트 추가
    st.markdown('<p style="color: red; font-size: small;">일정 추가 버튼을 눌러서 시간/장소/활동내용을 구체적으로 작성하세요</p>', unsafe_allow_html=True)

    # 교외체험학습 날짜 계산
    start_date = st.session_state.get('start_date')
    end_date = st.session_state.get('end_date')

    if start_date and end_date:
        total_days = (end_date - start_date).days + 1

        # 일차별 데이터 저장 초기화 및 동기화
        if 'plans' not in st.session_state or not isinstance(st.session_state.plans, dict):
            st.session_state.plans = {f"{day}일차": [] for day in range(1, total_days + 1)}
        else:
            # 기존의 plans에서 누락된 일차 데이터 초기화
            for day in range(1, total_days + 1):
                day_key = f"{day}일차"
                if day_key not in st.session_state.plans:
                    st.session_state.plans[day_key] = []

        # 일차별 입력 폼
        for day in range(1, total_days + 1):
            plan_date = (start_date + timedelta(days=day - 1)).strftime("%m/%d")  # 날짜 계산 및 포맷
            st.subheader(f"{day}일차 계획({plan_date})")
            st.markdown("**시간 / 장소 / 활동내용**")

            # 기본 입력란 보장
            if not st.session_state.plans[f"{day}일차"]:
                st.session_state.plans[f"{day}일차"].append({"시간": "", "장소": "", "활동내용": ""})

            # 각 일차별 기존 데이터 표시 및 추가 기능
            plans_for_day = st.session_state.plans[f"{day}일차"]
            for idx, plan in enumerate(plans_for_day):
                col1, col2, col3 = st.columns(3)
                with col1:
                    plan['시간'] = st.text_input(f"{day}일차 시간 {idx+1}", value=plan.get('시간', ""), key=f"time_{day}_{idx}")
                with col2:
                    plan['장소'] = st.text_input(f"{day}일차 장소 {idx+1}", value=plan.get('장소', ""), key=f"place_{day}_{idx}")
                with col3:
                    plan['활동내용'] = st.text_input(f"{day}일차 활동내용 {idx+1}", value=plan.get('활동내용', ""), key=f"activity_{day}_{idx}")

            # 새로운 일정 추가 버튼
            if st.button(f"{day}일차 일정 추가", key=f"add_{day}"):
                st.session_state.plans[f"{day}일차"].append({"시간": "", "장소": "", "활동내용": ""})
                st.rerun()  # 버튼 클릭 후 즉시 리렌더링

        # 전체 저장 버튼
        if st.button("모든 일정 저장"):
            st.success("모든 학습 계획이 저장되었습니다.")
            # st.write(st.session_state.plans)  # 데이터 출력 제거

    else:
        st.warning("교외체험학습 시작일과 종료일을 설정해주세요.")

# 보호자 정보 입력 탭
with tabs[3]:
    st.header("보호자 정보 입력")

    # 보호자 정보 행
    col1, col2, col3 = st.columns(3)
    with col1:
        guardian_name = st.text_input('보호자명', key='guardian_name')
    with col2:
        guardian_relationship = st.text_input('(보호자와의) 관계', key='guardian_relationship')
    with col3:
        guardian_contact = st.text_input('(보호자) 연락처', key='guardian_contact')

    # 인솔자 정보 행
    col4, col5, col6 = st.columns(3)
    with col4:
        chaperone_name = st.text_input('인솔자명', key='chaperone_name')
    with col5:
        chaperone_relationship = st.text_input('(인솔자와의) 관계', key='chaperone_relationship')
    with col6:
        chaperone_contact = st.text_input('(인솔자) 연락처', key='chaperone_contact')

# 서명 탭 구현
with tabs[4]:
    st.header("최종 서명")

        # 설명 텍스트 추가
    st.markdown('<p style="color: black; font-size: small;">서명 캔버스가 표시되지 않는 경우 [서명란 캔버스 불러오기] 버튼을 눌러주세요</p>', unsafe_allow_html=True)
    
    # 캔버스 리셋 함수들 수정
    def reset_student_canvas():
        st.session_state.student_canvas_key += 1
        st.session_state.student_signature_img = None
        st.session_state.student_canvas_initialized = True
        
    def reset_guardian_canvas():
        st.session_state.guardian_canvas_key += 1
        st.session_state.guardian_signature_img = None
        st.session_state.guardian_canvas_initialized = True

    # 자동 초기화 로직
    if not st.session_state.student_canvas_initialized:
        reset_student_canvas()
        st.rerun()
    
    if not st.session_state.guardian_canvas_initialized:
        reset_guardian_canvas()
        st.rerun()

    # 학생 서명 섹션
    st.markdown("### 학생 서명")
    col1, col2 = st.columns([4, 1])
    
    with col1:
        canvas_key = f"student_signature_canvas_{st.session_state.student_canvas_key}"
        student_canvas = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="rgba(0, 0, 0, 0)",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key=canvas_key
        )
        
        if student_canvas.image_data is not None:
            st.session_state.student_signature_img = student_canvas.image_data
    
    with col2:
        if st.button("서명란 캔버스 불러오기", key=f"reset_student_btn_{st.session_state.student_canvas_key}"):
            reset_student_canvas()
            st.rerun()
    
    if st.session_state.student_signature_img is not None:
        st.markdown("✅ 학생 서명을 입력해 주세요.")
    
    # 구분선 추가
    st.markdown("---")
    
    # 보호자 서명 섹션
    st.markdown("### 보호자 서명")
    col3, col4 = st.columns([4, 1])
    
    with col3:
        # 보호자 캔버스 키도 동일한 방식으로 수정
        guardian_canvas_key = f"guardian_signature_canvas_{st.session_state.guardian_canvas_key}"
        guardian_canvas = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="rgba(0, 0, 0, 0)",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key=guardian_canvas_key
        )
        
        if guardian_canvas.image_data is not None:
            st.session_state.guardian_signature_img = guardian_canvas.image_data
    
    with col4:
        if st.button("서명란 캔버스  불러오기", key=f"reset_guardian_btn_{st.session_state.guardian_canvas_key}"):
            reset_guardian_canvas()
            st.rerun()
    
    if st.session_state.guardian_signature_img is not None:
        st.markdown("✅ 보호자 서명을 입력해 주세요.")
    
    # 서명 완료 확인
    if st.session_state.student_signature_img is not None and st.session_state.guardian_signature_img is not None:
        st.success("✅ 모든 서명을 완료한 후 다음 단계로 진행해주세요.")

# 신청서 확인 탭
with tabs[5]:
    st.header("신청서 확인")

    # 이미지 파일 경로 설정
    img_path = IMAGE_DIR / "studywork001.png"
    extra_img_path = IMAGE_DIR / "studywork002.png"  # 별지 이미지

    # 필수 데이터 유효성 검사
    required_fields = [
        "student_name", "student_grade", "student_class", "student_number", 
        "start_date", "end_date", "attendance_start_date", "attendance_end_date", "plans"
    ]
    missing_fields = [field for field in required_fields if field not in st.session_state or not st.session_state[field]]
    
    if missing_fields:
        st.error(f"다음 필수 항목이 누락되었습니다: {', '.join(missing_fields)}")
    else:
        try:
            # 이미지 파일 존재 확인
            if not img_path.exists():
                st.error("신청서 양식 이미지를 찾을 수 없습니다.")
                st.stop()

            # 이미지 로드 및 설정
            image = Image.open(img_path).convert("RGBA")
            draw = ImageDraw.Draw(image)
            
            # 폰트 파일 경로 설정 및 폴백 처리
            font_paths = [
                pathlib.Path("/Library/Fonts/AppleGothic.ttf"),  # Mac AppleGothic
                pathlib.Path("/System/Library/Fonts/AppleGothic.ttf"),  # Mac AppleGothic 대체 경로
                FONT_DIR / "AppleGothic.ttf",  # 프로젝트 내 폰트
                pathlib.Path("/usr/share/fonts/truetype/nanum/NanumGothic.ttf"),  # Linux
                pathlib.Path("C:\\Windows\\Fonts\\malgun.ttf"),  # Windows
            ]
            
            font_path = None
            for path in font_paths:
                if path.exists():
                    font_path = path
                    break
            
            if font_path is None:
                st.error("""
                폰트 파일을 찾을 수 없습니다. 
                다음 중 하나의 방법으로 해결할 수 있습니다:
                1. Mac OS에 AppleGothic 폰트 설치
                2. 프로젝트의 fonts 폴더에 AppleGothic.ttf 파일을 추가
                """)
                st.stop()
            
            font = ImageFont.truetype(str(font_path), size=55)

            # 날짜 계산 로직 (교외체험학습)
            start_date = st.session_state.get("start_date")
            end_date = st.session_state.get("end_date")

            today = date.today()  # 제출일
            submit_date_formatted = today.strftime("%Y년 %m월 %d일")
            
            try:
                if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
                    duration = (end_date - start_date).days + 1  # 시작일과 종료일 포함
                    start_date_formatted = start_date.strftime("%Y년 %m월 %d일")
                    end_date_formatted = end_date.strftime("%Y년 %m월 %d일")
                else:
                    raise ValueError("시작일과 종료일이 올바른 날짜 형식이 아닙니다.")
            except Exception as e:
                st.error(f"날짜 계산 중 오류 발생: {e}")
                st.stop()

            # 출석인정 기간 계산 (공휴일 제외)
            attendance_start_date = st.session_state.get("attendance_start_date")
            attendance_end_date = st.session_state.get("attendance_end_date")
            
            try:
                kr_holidays = holidays.KR(years=attendance_start_date.year)  # 해당 연도의 대한민국 공휴일
                attendance_days = [
                    attendance_start_date + timedelta(days=i)
                    for i in range((attendance_end_date - attendance_start_date).days + 1)
                    if (attendance_start_date + timedelta(days=i)) not in kr_holidays
                    and (attendance_start_date + timedelta(days=i)).weekday() < 5  # 주말 제외
                ]
                attendance_duration = len(attendance_days)
                attendance_start_formatted = attendance_start_date.strftime("%Y년 %m월 %d일")
                attendance_end_formatted = attendance_end_date.strftime("%Y년 %m월 %d일")
            except Exception as e:
                st.error(f"출석인정 기간 계산 중 오류 발생: {e}")
                st.stop()

            # 기본 정보 그리기
            draw.text((770, 590), st.session_state.get("student_name", ""), fill="black", font=font)
            draw.text((1860, 590), st.session_state.get("student_grade", "").replace('학년', ''), fill="black", font=font)
            draw.text((2050, 590), st.session_state.get("student_class", "").replace('반', ''), fill="black", font=font)
            draw.text((2200, 590), str(st.session_state.get("student_number", "")), fill="black", font=font)

            # 교외체험학습 기간 그리기
            draw.text((1250, 690), start_date_formatted, fill="black", font=font)
            draw.text((1840, 690), end_date_formatted, fill="black", font=font)
            draw.text((2400, 690), f"{duration}", fill="black", font=font)

            # 출석인정 기간 그리기
            draw.text((1250, 800), attendance_start_formatted, fill="black", font=font)
            draw.text((1850, 800), attendance_end_formatted, fill="black", font=font)
            draw.text((2400, 800), f"{attendance_duration}", fill="black", font=font)
            draw.text((1250, 3270), submit_date_formatted, fill="black", font=font)  # 제출일 추가

            # 학습 형태에 따라 '0'의 위치 조정
            learning_type = st.session_state.get("learning_type", "")
            if learning_type == "가족 동반 여행":
                draw.text((940, 875), "0", fill="black", font=font)
            elif learning_type == "친인척 경조사 참석 및 방문":
                draw.text((1700, 875), "0", fill="black", font=font)
            elif learning_type == "유적 탐방":
                draw.text((2075, 875), "0", fill="black", font=font)
            elif learning_type == "문학 기행":
                draw.text((2450, 875), "0", fill="black", font=font)
            elif learning_type == "우리 문화 및 세계 문화 체험":
                draw.text((1225, 945), "0", fill="black", font=font)
            elif learning_type == "국토 순례":
                draw.text((1580, 945), "0", fill="black", font=font)
            elif learning_type == "자연 탐사":
                draw.text((1970, 945), "0", fill="black", font=font)
            elif learning_type == "직업 체험":
                draw.text((2340, 945), "0", fill="black", font=font)
            elif learning_type == "기타":
                draw.text((2600, 945), "0", fill="black", font=font)
            else:
                draw.text((300, 460), "학습 형태를 선택하세요", fill="red", font=font)

            draw.text((580, 1050), st.session_state.get("purpose", ""), fill="black", font=font)
            draw.text((580, 1200), st.session_state.get("destination", ""), fill="black", font=font)
            draw.text((710, 1330), st.session_state.get("guardian_name", ""), fill="black", font=font)
            draw.text((2150, 1330), st.session_state.get("guardian_contact", ""), fill="black", font=font)
            draw.text((710, 1470), st.session_state.get("chaperone_name", ""), fill="black", font=font)
            draw.text((2150, 1470), st.session_state.get("chaperone_contact", ""), fill="black", font=font)
            draw.text((1540, 1330), st.session_state.get("guardian_relationship", ""), fill="black", font=font)
            draw.text((1540, 1470), st.session_state.get("chaperone_relationship", ""), fill="black", font=font)
            draw.text((2250, 3400), st.session_state.get("student_name", ""), fill="black", font=font)
            draw.text((2250, 3530), st.session_state.get("guardian_name", ""), fill="black", font=font)

            def add_signatures(image):
                """서명 이미지를 신청서에 추가하는 헬퍼 함수"""
                if 'student_signature_img' in st.session_state:
                    student_signature_img = Image.fromarray(np.array(st.session_state['student_signature_img']).astype('uint8')).convert("RGBA")
                    new_size = (int(student_signature_img.width), int(student_signature_img.height))
                    student_signature_img = student_signature_img.resize(new_size, Image.Resampling.LANCZOS)
                    image.paste(student_signature_img, (2400, 3350), student_signature_img)

                if 'guardian_signature_img' in st.session_state:
                    guardian_signature_img = Image.fromarray(np.array(st.session_state['guardian_signature_img']).astype('uint8')).convert("RGBA")
                    new_size = (int(guardian_signature_img.width), int(guardian_signature_img.height))
                    guardian_signature_img = guardian_signature_img.resize(new_size, Image.Resampling.LANCZOS)
                    image.paste(guardian_signature_img, (2400, 3500), guardian_signature_img)

            # 학습 계획 데이터 처리를 위한 변수 초기화
            x_start, y_start = 580, 1570  # 첫 번째 칸 시작 치
            max_y = 2900
            font_size = 50
            min_font_size = 30
            extra_needed = False
            first_section_plans = ""  # 첫 번째 칸 계획
            second_section_plans = ""  # 두 번째 칸 계획
            remaining_plans = ""  # 남은 계획 (폰트 축소 후에도 넘치는 경우)

            def get_text_height(text, font):
                """텍스트의 높이를 계산하는 헬퍼 함수"""
                bbox = font.getbbox(text)
                return bbox[3] - bbox[1]

            if 'plans' in st.session_state and isinstance(st.session_state.plans, dict):
                # 전체 계획 텍스트 생성
                full_plans = ""
                start_date = st.session_state.start_date
                sorted_days = sorted(
                    [(day_key, (start_date + timedelta(days=int(''.join(filter(str.isdigit, day_key))) - 1))) for day_key in st.session_state.plans.keys()],
                    key=lambda x: x[1]
                ) 

                # 첫 번째 칸과 두 번째 칸에 나눠 담기 위한 높이 계산
                current_y = y_start
                first_section = []
                second_section = []
                second_section_y = y_start

                for day_key, date in sorted_days:
                    plans = st.session_state.plans.get(day_key, [])
                    day_plans = f"{day_key} 계획 ({date.strftime('%m/%d')}):\n"
                    for plan in plans:
                        day_plans += f"{plan.get('시간', '')} | {plan.get('장소', '')} | {plan.get('활동내용', '')}\n"
                    
                    # 현재 계획을 추가했을 때 y축 위치 계산
                    test_font = ImageFont.truetype(font_path, size=font_size)
                    line_height = get_text_height("test", test_font) + 5  # 줄 간격 포함
                    plan_height = len(day_plans.split('\n')) * line_height
                    
                    # 첫 번째 칸에 들어갈 수 있는지 확인
                    if current_y + plan_height <= max_y:
                        first_section.append(day_plans)
                        current_y += plan_height
                    # 두 번째 칸에 들어갈 수 있는지 확인
                    elif second_section_y + plan_height <= max_y:
                        second_section.append(day_plans)
                        second_section_y += plan_height
                    else:
                        # 두 번째 칸도 다 찼을 경우
                        extra_needed = True
                        remaining_plans += day_plans

                # 첫 번째 칸과 두 번째 칸의 텍스트 생성
                first_section_plans = "".join(first_section)
                second_section_plans = "".join(second_section)

                # 계획 텍스트 그리기
                if extra_needed:
                    # 기본 신청서에는 첫 번째 칸과 두 번째 칸의 내용만 표시
                    draw.text((580, 1570), first_section_plans, fill="black", 
                            font=ImageFont.truetype(font_path, size=font_size))
                    draw.text((1700, 1570), second_section_plans, fill="black", 
                            font=ImageFont.truetype(font_path, size=font_size))
                    draw.text((1800, max_y - 30), "※ 나머지 일정은 별지 참조", fill="black", font=font)
                    
                    # 별지에 나머지 계획 작성
                    try:
                        extra_image = Image.open(extra_img_path).convert("RGBA")
                        extra_draw = ImageDraw.Draw(extra_image)
                        extra_draw.text((100, 100), remaining_plans, fill="black", 
                                      font=ImageFont.truetype(font_path, size=12))
                        
                        # 서명 추가 후 이미지 출력
                        add_signatures(image)
                        st.image(image, caption='신청서', use_container_width=True)
                        st.image(extra_image, caption='학습계획 상세내용', use_container_width=True)
                    except FileNotFoundError:
                        st.error(f"별지 이미지를 찾을 수 없습니다: {extra_img_path}")
                        st.stop()
                else:
                    # 기본 신청서에 모든 내용 표시
                    draw.text((580, 1570), first_section_plans, fill="black", 
                            font=ImageFont.truetype(font_path, size=font_size))
                    if second_section_plans:
                        draw.text((1700, 1570), second_section_plans, fill="black", 
                                font=ImageFont.truetype(font_path, size=font_size))

                    # 서명 추가 후 이미지 출력
                    add_signatures(image)
                    st.image(image, caption='교외체험학습 신청서', use_container_width=True)

        except Exception as e:
            st.error(f"이미지 또는 폰트 로드 중 오류 발생: {e}")
            st.stop()

    def generate_pdf():
        try:
            # 임시 디렉토리 사용
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = pathlib.Path(temp_dir)
                
                # 임시 파일 경로 설정
                main_image_path = temp_dir_path / "studywork_main.png"
                extra_image_path = temp_dir_path / "studywork_extra.png"

                # 이미지 파일 저장
                image.save(main_image_path)
                if extra_needed:
                    extra_image.save(extra_image_path)

                # PDF 생성할 이미지 파 목록
                image_list = [str(main_image_path)]
                if extra_needed:
                    image_list.append(str(extra_image_path))

                # PDF 파일을 메모리에 생성
                pdf_bytes = img2pdf.convert(image_list)

                # 생성된 PDF 파일 다운로드 버튼 추가
                st.download_button(
                    label="신청서 PDF 다운로드",
                    data=pdf_bytes,
                    file_name="교외체험학습_신청서.pdf",
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"PDF 생성 중 오류 발생: {e}")

    if st.button("PDF 파일 생성  다운로드", key="pdf_download_button"):
        generate_pdf()

# HTML과 CSS로 푸터 추가
footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        제작자: 박기윤
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)