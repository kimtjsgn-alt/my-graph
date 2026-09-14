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
# Section 3: 날짜별 10위권 일관객 총합 추이 (영역 그래프)
# ===================================================================
st.header("3. 날짜별 박스오피스 10위권 총 일관객수 추이")

# 날짜별 10위권 일관객 합계 구하기
daily_total = df.groupby('날짜')['일관객'].sum().reset_index()
daily_total.columns = ['날짜', '총일관객']

# 영역 그래프 생성
fig3 = px.area(
    daily_total,
    x='날짜',
    y='총일관객',
    title="날짜별 박스오피스 TOP 10 전체 일관객 합계 추이",
    labels={'날짜': '날짜', '총일관객': '10위권 총 관객수(명)'}
)

fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>10위권 총 관객수:</b> %{y:,}명<extra></extra>"
)

# 총 일관객 수가 가장 컸던 날 TOP 3 구하기
top3_days = daily_total.nlargest(3, '총일관객')

# 그래프 위에 상위 3일 어노테이션(마커 및 날짜 텍스트) 추가
for i, row in top3_days.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    total_val = row['총일관객']
    
    fig3.add_annotation(
        x=row['날짜'],
        y=total_val,
        text=f"<b>TOP {top3_days.index.get_loc(i)+1}</b><br>{date_str}<br>({total_val:,}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="red",
        ax=0,
        ay=-45,
        bgcolor="rgba(255, 255, 255, 0.85)",
        bordercolor="red",
        borderwidth=1,
        borderpad=4
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="10위권 총 관객수 (명)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(fig3, use_container_width=True)

# 이 그래프로 알 수 있는 것 (사용자 작성 구역)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# ===================================================================
# Section 4: 기간 내 총 관객수 TOP 10 영화 (가로 막대그래프)
# ===================================================================
st.header("4. 기간 내 총 관객수 TOP 10 영화")

# 영화별 총 관객수 합계 및 10위권 진입 일수 계산
top10_stats = df.groupby('영화명').agg(
    총관객수=('일관객', 'sum'),
    진입일수=('날짜', 'nunique')
).reset_index()

# 총 관객수 기준 TOP 10 추출 및 오름차순 정렬
top10_df = top10_stats.nlargest(10, '총관객수').sort_values('총관객수', ascending=True)

# 가로 막대그래프 생성
fig4 = px.bar(
    top10_df,
    x='총관객수',
    y='영화명',
    orientation='h',
    title="기간 내 총 관객수 TOP 10 영화 (10위권 진입 일수 포함)",
    labels={'총관객수': '총 관객수(명)', '영화명': '영화 제목', '진입일수': '10위권 진입 일수'},
    hover_data={'총관객수': ':,d', '진입일수': True, '영화명': False},
    text='총관객수'
)

fig4.update_traces(
    texttemplate='%{x:,}명',
    textposition='outside',
    hovertemplate="<b>영화명:</b> %{y}<br><b>총 관객수:</b> %{x:,}명<br><b>10위권 진입 일수:</b> %{customdata[0]}일<extra></extra>"
)

fig4.update_layout(
    xaxis_title="총 관객수 (명)",
    yaxis_title="영화 제목",
    template="plotly_white"
)

st.plotly_chart(fig4, use_container_width=True)

# 이 그래프로 알 수 있는 것 (사용자 작성 구역)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# ===================================================================
# Section 5: 월×요일별 일관객 합계 (히트맵)
# ===================================================================
st.header("5. 월×요일별 관객수 분포 히트맵")

# 날짜에서 월과 요일 추출
heatmap_df = df.copy()
heatmap_df['월'] = heatmap_df['날짜'].dt.month.astype(str) + "월"
heatmap_df['요일_num'] = heatmap_df['날짜'].dt.dayofweek  # 월:0, 화:1, ..., 일:6

day_names = {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'}
heatmap_df['요일'] = heatmap_df['요일_num'].map(day_names)

# 월, 요일별 일관객 합계 구하기
monthly_day_sum = heatmap_df.groupby(['월', '요일', '요일_num'])['일관객'].sum().reset_index()

# 월 및 요일 순서 지정
month_order = [f"{m}월" for m in range(1, 13) if f"{m}월" in monthly_day_sum['월'].unique()]
day_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

# 피벗 테이블 생성 (행: 월, 열: 요일)
pivot_df = monthly_day_sum.pivot(index='월', columns='요일', values='일관객')
pivot_df = pivot_df.reindex(index=month_order, columns=day_order)

# 히트맵 생성
fig5 = px.imshow(
    pivot_df,
    labels=dict(x="요일", y="월", color="관객수 합계(명)"),
    x=day_order,
    y=month_order,
    color_continuous_scale="Blues",
    title="월×요일별 관객수 합계 히트맵",
    text_auto=",.0f"
)

fig5.update_traces(
    hovertemplate="<b>%{y} %{x}</b><br><b>총 관객수:</b> %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    template="plotly_white"
)

st.plotly_chart(fig5, use_container_width=True)

# 이 그래프로 알 수 있는 것 (사용자 작성 구역)
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")

st.divider()

# ===================================================================
# Section 6: 추가 그래프 구역 (예정)
# ===================================================================
st.header("6. 추가 그래프 구역 (예정)")
st.caption("앞으로 추가될 시각화 그래프가 이 구역에 들어갈 예정입니다.")
