import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 타이틀 및 안내 문구
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 변화를 시각화합니다.")

# 데이터 불러오기 및 캐싱
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    # 8자리 숫자로 되어있는 날짜 열을 실제 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.divider()

# -------------------------------------------------------------------
# 구역 1: 특정 영화의 날짜별 일관객 변화
# -------------------------------------------------------------------
st.header("1. 특정 영화의 날짜별 일관객 변화")

# 데이터에 존재하는 영화 목록 가져오기
movie_list = sorted(df['영화명'].unique())
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택한 영화 데이터 필터링 및 날짜순 정렬
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

    # Plotly 선 그래프 작성
    fig = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"<{selected_movie}> 일별 관객수 추이",
        markers=True,
        labels={'날짜': '날짜', '일관객': '일관객 수(명)'}
    )
    
    # 마우스 오버(Hover) 시 날짜 및 관객수 포맷 설정
    fig.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객 수:</b> %{y:,}명<extra></extra>"
    )
    
    fig.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객 수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )

    # 그래프 출력
    st.plotly_chart(fig, use_container_width=True)

    # 이 그래프로 알 수 있는 것 (사용자 작성 구역)
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# -------------------------------------------------------------------
# 구역 2: 향후 추가 그래프를 위한 예시 구역
# -------------------------------------------------------------------
st.header("2. 추가 그래프 구역 (예정)")
st.caption("앞으로 추가될 시각화 그래프가 이 구역에 들어갈 예정입니다.")
