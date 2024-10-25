import streamlit as st
import openai
import os
from PIL import Image
from io import BytesIO

# OpenAI API 키를 환경 변수에서 가져오기
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit 웹 애플리케이션 설정
st.title("Custom Logo Generator")
st.write("Provide details below to create a custom logo.")

# 사용자 입력 받기
brand_name = st.text_input("Brand or Company Name", "Ohcom Data")
color = st.text_input("Primary Color (e.g., orange)", "orange")
style = st.selectbox("Logo Style", ["Modern", "Minimal", "Classic", "Tech-Influenced"])
shape = st.selectbox("Logo Shape", ["Rectangular", "Circular", "Abstract", "Shield"])
additional_feature = st.text_area("Additional Feature (e.g., chart, graph, quill)")

# 생성 버튼
if st.button("Generate Logo"):
    # DALL-E 프롬프트 생성
    prompt = (
        f"A {style.lower()} logo for a company named '{brand_name}'. "
        f"The logo should be primarily {color}, with a {shape.lower()} shape. "
        f"Include an abstract representation of {additional_feature.lower()} if possible. "
        f"The design should feel clean, modern, and suitable for technology-related branding."
    )
    
    # DALL-E API 호출
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024",
        )
        # API에서 이미지 URL 가져오기
        image_url = response['data'][0]['url']
        
        # 이미지 표시
        st.image(image_url, caption="Generated Logo")
        st.write(f"Prompt used: {prompt}")
    
    except Exception as e:
        st.error("There was an error generating the image.")
        st.write(e)
