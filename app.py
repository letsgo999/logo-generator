import streamlit as st
from openai import OpenAI
import os

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 로고 스타일 상세 설명 딕셔너리
STYLE_DESCRIPTIONS = {
    "미니멀": "단순하고 깔끔한 라인과 기하학적 형태를 사용한 현대적인 미니멀 디자인",
    "모던": "세련되고 현대적인 디자인 요소와 깔끔한 타이포그래피",
    "테크": "기술적이고 미래지향적인 디자인 요소와 기하학적 패턴",
    "클래식": "전통적이고 신뢰감 있는 디자인 요소와 세련된 장식",
}

# 색상 조합 제안
COLOR_COMBINATIONS = {
    "모노크롬": "흑백과 회색 톤",
    "비즈니스": "네이비 블루와 그레이",
    "테크": "일렉트릭 블루와 실버",
    "친환경": "그린과 세이지",
    "현대적": "딥 퍼플과 터콰이즈",
}

def generate_logo_prompt(brand_name, style, color_scheme, icon_type, industry, scale):
    """더 구체적이고 로고에 특화된 프롬프트 생성"""
    base_prompt = f"""디자인 요청: 기업 로고 디자인
브랜드: {brand_name}
스타일: {STYLE_DESCRIPTIONS[style]}

필수 요구사항:
- 벡터 스타일의 {scale}한 로고 디자인
- {color_scheme} 색상 사용
- {industry}산업에 적합한 디자인
- {icon_type} 형태의 심볼마크

추가 지침:
- 로고는 반드시 단순하고 확장 가능한 벡터 형태로 디자인
- 배경은 순수 흰색으로 처리
- 심볼과 로고타입이 조화롭게 배치
- 작은 크기에서도 식별 가능한 디자인
- 전문적이고 현대적인 기업 아이덴티티에 적합한 형태"""
    
    return base_prompt

# Streamlit UI
st.title("전문 로고 생성기 v2.0")
st.write("로고 디자인을 위한 상세 정보를 입력해주세요.")

# 사용자 입력 섹션
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        brand_name = st.text_input("브랜드/회사명", placeholder="예: Techno Labs")
        style = st.selectbox("로고 스타일", list(STYLE_DESCRIPTIONS.keys()))
        color_scheme = st.selectbox("색상 스키마", list(COLOR_COMBINATIONS.keys()))
        
    with col2:
        industry = st.selectbox("산업 분야", 
            ["기술/IT", "금융/투자", "교육", "의료/헬스케어", "환경/에너지", "미디어/엔터테인먼트"])
        icon_type = st.selectbox("아이콘 형태",
            ["기하학적", "추상적", "문자 기반", "심볼릭"])
        scale = st.select_slider("디자인 복잡도",
            options=["미니멀", "중간", "복잡"])

# 고급 설정
with st.expander("고급 설정"):
    use_text = st.checkbox("텍스트 포함", value=True)
    monotone = st.checkbox("모노톤으로 생성", value=False)
    include_variations = st.checkbox("다양한 변형 생성", value=False)

# 생성 버튼
if st.button("로고 생성"):
    if not brand_name:
        st.warning("브랜드/회사명을 입력해주세요.")
    else:
        try:
            with st.spinner('로고 생성 중...'):
                # 프롬프트 생성
                prompt = generate_logo_prompt(
                    brand_name, style, COLOR_COMBINATIONS[color_scheme],
                    icon_type, industry, scale
                )
                
                # 이미지 생성 설정
                response = client.images.generate(
                    model="dall-e-3",  # DALL-E 3 사용
                    prompt=prompt,
                    n=1,
                    quality="hd",  # 고품질 설정
                    size="1024x1024",
                    style="natural"  # 자연스러운 스타일
                )
                
                # 결과 표시
                st.image(response.data[0].url, caption=f"{brand_name} 로고")
                
                # 프롬프트 확인 (디버깅용)
                with st.expander("사용된 프롬프트 확인"):
                    st.text(prompt)
                
        except Exception as e:
            st.error(f"로고 생성 중 오류가 발생했습니다: {str(e)}")
            
# 도움말 섹션
with st.expander("로고 디자인 팁"):
    st.markdown("""
    ### 효과적인 로고 디자인을 위한 팁
    1. **단순함 유지**: 심플할수록 기억하기 쉽고 다양한 크기에서 활용하기 좋습니다.
    2. **확장성 고려**: 작은 명함부터 큰 간판까지 다양한 크기에서 사용될 수 있어야 합니다.
    3. **산업 적합성**: 귀사의 산업에 적합한 이미지를 전달해야 합니다.
    4. **색상 선택**: 브랜드 이미지에 맞는 색상을 선택하되, 흑백으로도 효과적인지 고려하세요.
    """)
