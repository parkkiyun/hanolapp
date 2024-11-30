import tempfile
import streamlit as st
from app.helper_functions import render_signature_image

def generate_pdf(form_config):
    try:
        # preview_only=False로 설정하여 미리보기 표시 없이 이미지만 생성
        preview_image = render_signature_image(return_image=True, preview_only=False)
        
        # PDF 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            preview_image.save(tmp_pdf.name, "PDF")
            st.download_button(
                label="PDF 다운로드",
                data=open(tmp_pdf.name, "rb").read(),
                file_name=f"{form_config['title']}.pdf",
                mime="application/pdf"
            )
        return True  # PDF 생성 성공
    except Exception as e:
        st.error(f"PDF 생성 중 오류 발생: {e}")
        return False  # PDF 생성 실패
