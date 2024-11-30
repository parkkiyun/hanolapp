import pathlib
import streamlit as st
import os

class ResourceManager:
    def __init__(self):
        self.base_dir = pathlib.Path(__file__).parent.parent.absolute()
        self.image_dir = self.base_dir / "images"
        self.font_dir = self.base_dir / "fonts"
        self.paths = {
            "신청서 양식": self.image_dir / "delegation_form.png",
            "폰트": self.font_dir / "HANDotum.ttf",
            "폰트_볼드": self.font_dir / "HANDotumB.ttf"
        }

    def validate_resources(self):
        missing_files = []
        for name, path in self.paths.items():
            if not os.path.exists(path):
                missing_files.append(f"{name}: {path}")
        
        if missing_files:
            error_msg = "다음 파일들을 찾을 수 없습니다:\n" + "\n".join(missing_files)
            st.error(error_msg)
            raise FileNotFoundError(error_msg)

    def get_path(self, resource_name):
        path = self.paths.get(resource_name)
        if not path:
            raise KeyError(f"리소스를 찾을 수 없습니다: {resource_name}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"파일을 찾을 수 없습니다: {path}")
        return path
