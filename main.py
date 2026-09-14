import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

# 메인 타이틀
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("KOBIS 일별 박스오피스 데이터를 바탕으로 시간 흐름에 따른 영화 관객 수 변화를 시각화합니다.")

# 데이터 로드 (캐싱 사용)
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 날짜 열을 datetime 타입으로 변환 (8자리 숫자 string -> datetime)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

st.divider()

# ===================================================================
# Section 1: 특정 영화의 날짜별 일관객 변화
# ===================================================================
st.header("1. 특정 영화의 날짜별 일관객 변화")

# 데이터 내 unique 영화 목록 (영화명 기준 정렬)
movie_list = sorted(df['영화명'].unique())

selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

if selected_movie:
    # 선택한 영화 데이터 필터링
    movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

    # Plotly 선 그래프 생성
    fig1 = px.line(
        movie_df,
        x='날짜',
        y='일관객',
        title=f"<{selected_movie}> 일별 관객수 추이",
        markers=True,
        labels={'날짜': '날짜', '일관객': '일관객 수(명)'}
    )
    
    fig1.update_traces(
        hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객 수:</b> %{y:,}명<extra></extra>"
    )
    
    fig1.update_layout(
        xaxis_title="날짜",
        yaxis_title="일관객 수 (명)",
        hovermode="x unified",
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 이 그래프로 알 수 있는 것 (사용자 작성 구역)
    st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# ===================================================================
# Section 2: 총 일관객 수가 가장 많은 TOP 5 영화의 날짜별 일관객 비교
# ===================================================================
st.header("2. 기간 내 관객수 상위 5개 영화의 날짜별 일관객 비교")

# 영화별 일관객 합계 계산 후 상위 5개 추출
top5_movies = (
    df.groupby('영화명')['일관객']
    .sum()
    .nlargest(5)
    .index.tolist()
)

# 상위 5개 영화 데이터 필터링
top5_df = df[df['영화명'].isin(top5_movies)].sort_values('날짜')

# Plotly 다중 선 그래프 생성
fig2 = px.line(
        top5_df,
        x='날짜',
        y='일관객',
        color='영화명',
        title="기간 내 총 관객수 TOP 5 영화의 일별 관객수 비교",
        markers=True,
        labels={'날짜': '날짜', '일관객': '일관객 수(명)', '영화명': '영화 제목'}
)

fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객 수:</b> %{y:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수 (명)",
    hovermode="x unified",
    template="plotly_white",
    legend_title_text="영화 제목 (클릭하여 토글)"
)

st.plotly_chart(fig2, use_container_width=True)

# 이 그래프로 알 수 있는 것 (사용자 작성 구역)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# ===================================================================
# Section 3: 추가 그래프 구역 (예정)
# ===================================================================
st.header("3. 추가 그래프 구역 (예정)")
st.caption("앞으로 추가될 시각화 그래프가 이 구역에 들어갈 예정입니다.")
