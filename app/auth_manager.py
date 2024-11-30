import streamlit as st
import json
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.config_path = Path("config/page_access.json")
        self.load_access_config()
    
    def load_access_config(self):
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.access_config = json.load(f)
    
    def is_teacher_page(self, page_name):
        page_mapping = {
            "dashboard": "대시보드",
            "delegation_login": "위임장로그인",
            "write_delegation": "위임장작성",
            "absence": "결석신고서"
        }
        korean_name = page_mapping.get(page_name, page_name)
        return korean_name in self.access_config["teacher_only"]
    
    def is_guest_allowed_page(self, page_name):
        page_mapping = {
            "dashboard": "대시보드",
            "delegation_login": "위임장로그인",
            "write_delegation": "위임장작성",
            "field_trip_request": "교외체험학습신청서",
            "field_trip_report": "교외체험학습결과보고서"
        }
        korean_name = page_mapping.get(page_name, page_name)
        return korean_name in self.access_config["guest_allowed"]
    
    def check_page_access(self, page_name):
        if self.is_teacher_page(page_name) and not st.session_state.get("authenticated", False):
            st.error("이 페이지는 교사 로그인이 필요합니다.")
            st.switch_page("pages/dashboard.py")
            st.stop()
    