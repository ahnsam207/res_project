import streamlit as st
import requests
import base64

# GitHub 정보
GITHUB_REPO = "ahnsam207/res"
GITHUB_TOKEN =  st.secrets["git_token"]   # 개인 액세스 토큰 입력
BRANCH = "main"  # 사용할 브랜치

# 파일 업로드
uploaded_file = st.file_uploader(" 계획서 파일을 업로드하세요")

if uploaded_file is not None:
    file_content = uploaded_file.getvalue()
    file_path = f"upload/{uploaded_file.name}"

    # GitHub API URL
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{file_path}"

    # 파일을 base64로 인코딩
    encoded_content = base64.b64encode(file_content).decode("utf-8")

    # API 요청 데이터
    data = {
        "message": f"Upload {uploaded_file.name}",
        "content": encoded_content,
        "branch": BRANCH
    }

    # GitHub API 요청
    response = requests.put(url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})

    if response.status_code == 201:
        st.success(f"✅ 계획서 파일이 정상적으로 업로드되었습니다.\n\n {uploaded_file.name}")
    else:
        st.error("❌ 업로드 실패(파일의 이름을 수정해 주세요.)")
