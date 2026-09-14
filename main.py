import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("---")

# 데이터 로드 함수 (캐싱 적용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 여덟 자리 숫자 날짜(YYYYMMDD)를 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 수치형 데이터 변환
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

# 데이터 불러오기
try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# 사이드바 안내
st.sidebar.title("📌 안내")
st.sidebar.info(
    "이 앱은 1년치(365일) 일별 박스오피스 10위권 기록 데이터를 기반으로 "
    "시간에 따른 영화 데이터 변화를 시각화합니다."
)

# ==========================================
# 구역 1: 개별 영화 일별 관객수 변화 (선 그래프)
# ==========================================
st.header("1. 개별 영화 일별 관객수 변화")

# 영화 목록 추출 및 드롭다운 선택
movie_list = sorted(df['영화명'].dropna().unique())
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택 영화 데이터 필터링 및 날짜순 정렬
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')
    
    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"'{selected_movie}' 날짜별 일관객수 추이",
        markers=True,
        labels={'날짜': '날짜', '일관객': '일일 관객수(명)'}
    )
    
    # 마우스 오버(Hover) 시 날짜 및 관객수가 깔끔하게 표시되도록 설정
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>관객수:</b> %{y:,}명<extra></extra>"
    )
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )
    
    st.plotly_chart(fig1, use_container_width=True)

# 해석 문구 작성란 (직접 작성하시는 공간)
st.caption("💡 **이 그래프로 알 수 있는 것**")
st.info("작성할 내용을 여기에 입력하세요.")

st.markdown("---")

# ==========================================
# 구역 2: [추가 그래프 영역] (향후 확장용)
# ==========================================
st.header("2. [추가 그래프 구역]")
st.write("앞으로 시간에 따른 추가적인 시각화 그래프가 이 구역에 추가될 예정입니다.")
