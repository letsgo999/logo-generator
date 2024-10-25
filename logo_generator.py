import streamlit as st
import openai
import os
from PIL import Image
from io import BytesIO
import requests

# OpenAI API 키를 환경 변수에서 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit 웹 애플리케이션 설정
st.title("맞춤형 로고 생성기")
st.write("아래 정보를 입력하여 맞춤형 로고를 생성하세요.")

# 사용자 입력 받기 (플레이스홀더 사용)
brand_name = st.text_input("회사 또는 브랜드 이름", placeholder="예시: 오컴 데이터")
color = st.text_input("주요 색상 (예: 주황색)", placeholder="예시: 주황색")
style = st.selectbox("로고 스타일", ["모던", "미니멀", "클래식", "기술 기반"])
shape = st.selectbox("로고 형태", ["사각형", "원형", "추상적", "방패 모양"])
additional_feature = st.text_area("추가 요소 (예: 차트, 그래프, 깃펜)", placeholder="예시: 차트")

# 생성 버튼
if st.button("로고 생성"):
    # DALL-E 프롬프트 생성
    prompt = (
        f"{style.lower()} 스타일의 '{brand_name}'라는 회사 또는 브랜드의 로고. "
        f"주요 색상은 {color}, 형태는 {shape.lower()}입니다. "
        f"가능하다면 {additional_feature.lower()}을(를) 추상적으로 표현하세요. "
        f"로고는 깨끗하고 현대적이며, 기술과 관련된 느낌을 주어야 합니다."
    )
    
    # GPT-4 모델을 사용하여 이미지 생성
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="url"
        )
        # 생성된 이미지의 URL 가져오기
        image_url = response['data'][0]['url']

        # 이미지 다운로드 및 표시
        st.image(image_url, caption="생성된 로고")
        st.write(f"사용된 프롬프트: {prompt}")

    except Exception as e:
        st.error("이미지를 생성하는 동안 오류가 발생했습니다.")
        st.write(e)
