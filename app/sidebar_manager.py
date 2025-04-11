import streamlit as st
import base64
from pathlib import Path
import os
from PIL import Image

class SidebarManager:
    def __init__(self):
        pass
    
    def get_base64_image(self, image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return None
    
    def render_sidebar(self):
        with st.sidebar:
            # 이미지 추가
            ROOT_DIR = Path(__file__).parent.parent.absolute()
            SIDEBAR_IMAGE_PATH = ROOT_DIR / "images" / "sidebar_logo.png"
            
            if SIDEBAR_IMAGE_PATH.exists():
                image_base64 = self.get_base64_image(SIDEBAR_IMAGE_PATH)
                if image_base64:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="data:image/png;base64,{image_base64}" 
                                 style="width: 180px; margin: auto;">
                        </div>
                    """, unsafe_allow_html=True) 