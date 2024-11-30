import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

def render():
    st.header("서명 입력")
    
    st.info("서명 캔버스 불러오기 버튼을 눌러 캔버스에 서명을 남겨주세요.")
    
    # 세션 상태 초기화
    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = 0
    
    # 서명 캔버스 초기화 버튼
    if st.button("서명 캔버스 불러오기"):
        st.session_state.canvas_key += 1
        st.session_state.pop("signature_img", None)
        st.rerun()
    
    # 캔버스 생성 (배경 투명)
    canvas_result = st_canvas(
        stroke_width=2,
        stroke_color="#000000",
        background_color="rgba(0, 0, 0, 0)",  # 투명 배경
        height=150,
        width=400,
        drawing_mode="freedraw",
        key=f"canvas_{st.session_state.canvas_key}"
    )
    
    # 서명 데이터 처리
    if canvas_result is not None and canvas_result.image_data is not None:
        if np.any(canvas_result.image_data):
            st.session_state["signature_img"] = canvas_result.image_data
            st.success("서명이 저장되었습니다.")
 