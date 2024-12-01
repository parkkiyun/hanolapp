import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from app.resource_manager import ResourceManager
from datetime import datetime

def validate_required_fields(required_fields):
    """
    필수 필드가 모두 입력되었는지 확인하고, 누락된 필드를 반환합니다.
    """
    missing_fields = []
    for field in required_fields:
        if field not in st.session_state:
            missing_fields.append(field)
        else:
            value = st.session_state[field]
            if value is None:
                missing_fields.append(field)
            elif isinstance(value, (str, list, dict)) and not value:
                missing_fields.append(field)
            # numpy 배열인 경우
            elif isinstance(value, np.ndarray) and value.size == 0:
                missing_fields.append(field)
    return missing_fields

def wrap_text(text, font, max_width):
    """
    주어진 최대 너비에 맞게 텍스트를 줄바꿈합니다.
    """
    result = []
    current_line = ""
    
    for char in text:
        test_line = current_line + char
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            result.append(current_line)
            current_line = char
    
    if current_line:
        result.append(current_line)
    
    return result

def get_adjusted_font_size(text, max_width, font_path, initial_size=70, min_size=50):
    """
    텍스트 길이에 따라 적절한 폰트 크기를 반환합니다.
    """
    current_size = initial_size
    font = ImageFont.truetype(str(font_path), size=current_size)
    
    # 텍스트가 최대 너비를 초과하면 폰트 크기를 줄임
    while font.getlength(text) > max_width and current_size > min_size:
        current_size -= 2
        font = ImageFont.truetype(str(font_path), size=current_size)
    
    return font

def format_date(date_str):
    """
    날짜를 'YYYY년 MM월 DD일' 형식으로 변환합니다.
    """
    if not date_str:
        return ""
    try:
        # 문자열을 datetime 객체로 변환
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # 원하는 형식으로 변환
        return date_obj.strftime('%Y년 %m월 %d일')
    except:
        return date_str

def render_signature_image(preview_only=False, form_config=None, return_image=False):
    """
    신청서 이미지를 생성하고 렌더링하는 함수
    
    Args:
        preview_only (bool): 미리보기 모드 여부
        form_config (dict): 양식 설정
        return_image (bool): 이미지 객체 반환 여부
    """
    # 디버깅을 위한 출력
    print("render_signature_image 호출됨")
    print("받은 form_config:", form_config)
    
    # 기본값 설정
    if form_config is None:
        form_config = {"title": "기본 위임장", "image_texts": []}
        
    try:
        resources = ResourceManager()
        img_path = resources.paths["신청서 양식"]
        font_path = resources.paths["폰트"]

        # 이미지 로드
        image = Image.open(img_path).convert("RGBA")
        draw = ImageDraw.Draw(image)
        
        # 미리보기에만 테두리 추가
        if preview_only:
            width, height = image.size
            draw.rectangle([(0, 0), (width-1, height-1)], outline="black", width=5)

        # 폰트 정의
        font = ImageFont.truetype(str(resources.paths["폰트"]), size=55)  # 일반 폰트
        name_font = ImageFont.truetype(str(resources.paths["폰트_볼드"]), size=60)  # 볼드 폰트로 이름 표시
        

        # 신청서 제목과 동적 텍스트 삽입
        title_text = form_config.get("title", "기본 위임장")
        print("적용할 title_text:", title_text)
        draw.text((1650, 1100), title_text, font=name_font, fill="black")

        additional_texts = form_config.get("image_texts", [])
        print("적용할 additional_texts:", additional_texts)
        y_offset = 2000
        for text in additional_texts:
            draw.text((720, y_offset), text, font=name_font, fill="black")
            y_offset += 100

        # 이름 텍스트 그리기 (큰 폰트 사용)
        draw.text((1900, 3240), f"{st.session_state.get('name', '')}", font=name_font, fill="black")

        # 생년월일과 위임일 형식 변경
        birth_date = format_date(str(st.session_state.get('birth_date', '')))
        delegation_date = format_date(str(st.session_state.get('delegation_date', '')))
        
        # 입력된 데이터 그리기
        draw.text((870, 850), f"{st.session_state.get('name', '')}", font=font, fill="black")
        draw.text((730, 1000), f"{birth_date}", font=font, fill="black")
        draw.text((760, 1380), f"{st.session_state.get('contact', '')}", font=font, fill="black")
        draw.text((1100, 2900), f"{delegation_date}", font=name_font, fill="black")

        # 주소 텍스트 줄리
        address = st.session_state.get('address', '')
        max_width = 750
        
        # 주소 길이에 따라 폰트 크기 조정
        address_font = get_adjusted_font_size(address, max_width, font_path)
        address_lines = wrap_text(address, address_font, max_width)
        
        # 줄바꿈된 주소 표시 (최대 3줄)
        if address_lines:
            # 첫 번째 줄
            draw.text((600, 1150), address_lines[0], font=address_font, fill="black")
            
            # 두 번째 줄
            if len(address_lines) > 1:
                draw.text((600, 1210), address_lines[1], font=address_font, fill="black")
            
            # 세 번째 줄
            if len(address_lines) > 2:
                draw.text((600, 1270), address_lines[2], font=address_font, fill="black")
        
        # 서명 추가
        if "signature_img" in st.session_state and st.session_state["signature_img"] is not None:
            signature_data = st.session_state["signature_img"]
            if isinstance(signature_data, np.ndarray):
                # 이미 RGBA 형식이므로 바로 변환
                signature_img = Image.fromarray(signature_data)
                signature_resized = signature_img.resize((400, 250), Image.Resampling.LANCZOS)
                
                # 서명 위치 조정 (x, y 좌표는 실제 양식에 맞게 조정 필요)
                image.paste(signature_resized, (2200, 3150), signature_resized)

        # preview_only가 True일 때만 미리보기 표시
        if preview_only:
            st.image(image, caption="신청서 미리보기", width=None)  # width=None은 원본 크기 유지
        
        if return_image:
            return image
            
    except Exception as e:
        st.error(f"미리보기 생성 중 오류 발생: {str(e)}")
        if return_image:
            return None
