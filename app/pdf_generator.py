import tempfile
import streamlit as st
from app.helper_functions import render_signature_image

def generate_pdf(form_config):
    try:
        # form_config를 전달하여 올바른 제목과 문구가 포함되도록 함
        preview_image = render_signature_image(
            return_image=True, 
            preview_only=False,
            form_config=form_config  # form_config 전달
        )
        
        # PDF 생성
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            preview_image.save(tmp_pdf.name, "PDF")
            st.download_button(
                label="PDF 다운로드",
                data=open(tmp_pdf.name, "rb").read(),
                file_name=f"{form_config['title']}.pdf",
                mime="application/pdf"
            )
        return True
    except Exception as e:
        st.error(f"PDF 생성 중 오류 발생: {e}")
        return False
