import streamlit as st
import pandas as pd
import plotly.express as px


# =======================================
# 기본 설정
# =======================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")


# =======================================
# 데이터 불러오기
# =======================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    return df


df = load_data()

st.write(f"총 {len(df):,}개의 기록을 불러왔습니다.")


# =======================================
# 그래프 1. 영화별 일관객 변화
# =======================================
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(
    df["영화명"].dropna().unique()
)

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[
    df["영화명"] == selected_movie
].copy()

movie_df = movie_df.sort_values("날짜")


fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}'의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.write(
    "선택한 영화가 날짜에 따라 하루 동안 얼마나 많은 관객을 모았는지와 관객 변화의 흐름을 알 수 있다."
)


# =======================================
# 그래프 2. 일관객 합계 TOP 5 영화 비교
# =======================================
st.divider()

st.header("그래프 2. 일관객 합계 TOP 5 영화")


top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

top5_df = df[
    df["영화명"].isin(top5_movies)
].copy()

top5_df = top5_df.sort_values("날짜")


fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계가 가장 큰 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    }
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}<br>"
        "날짜: %{x|%Y-%m-%d}<br>"
        "관객수: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="closest",
    legend_title_text="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편의 영화가 날짜에 따라 관객 수가 어떻게 변했는지 비교할 수 있다."
)


# =======================================
# 그래프 3. 날짜별 TOP 10 일관객 합계
# =======================================
st.divider()

st.header("그래프 3. 날짜별 TOP 10 일관객 합계")


daily_total = (
    df.groupby("날짜")["일관객"]
    .sum()
    .reset_index()
)

daily_total = daily_total.sort_values("날짜")


top3_days = (
    daily_total
    .nlargest(3, "일관객")
    .sort_values("날짜")
)


fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 박스오피스 TOP 10 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "TOP 10 일관객 합계"
    }
)

fig3.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "TOP 10 관객 합계: %{y:,}명"
        "<extra></extra>"
    )
)


fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    text=[
        f"{date.strftime('%Y-%m-%d')}<br>{total:,}명"
        for date, total in zip(
            top3_days["날짜"],
            top3_days["일관객"]
        )
    ],
    textposition="top center",
    marker=dict(size=10),
    name="TOP 3"
)

fig3.update_layout(
    hovermode="x unified",
    showlegend=True
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

st.subheader("이 그래프로 알 수 있는 것")

st.write(
    "날짜별 박스오피스 TOP 10의 전체 관객 규모와 관객이 가장 많이 몰린 날을 한눈에 확인할 수 있다."
)


# =======================================
# 그래프 4. 영화별 누적 일관객 TOP 10
# =======================================
st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")


# 영화별 일관객 합계
movie_total = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        **{"10위권_등장일수": ("날짜", "count")}
    )
    .reset_index()
)


# 일관객 합계가 가장 큰 TOP 10
top10_movie = (
    movie_total
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .sort_values("일관객합계", ascending=True)
)


# 가로 막대그래프
fig4 = px.bar(
    top10_movie,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "영화명": "영화",
        "일관객합계": "일관객 합계"
    },
    custom_data=["10위권_등장일수"]
)


fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "일관객 합계: %{x:,}명<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    )
)


fig4.update_layout(
    yaxis={
        "categoryorder": "total ascending"
    }
)


st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader("이 그래프로 알 수 있는 것")

st.write(
    "전체 기간 동안 일관객 합계가 가장 많았던 영화 TOP 10과 각 영화가 박스오피스 10위권에 머문 날수를 비교할 수 있다."
)


# =======================================
# 그래프 5. 앞으로 추가할 그래프
# =======================================
st.divider()

st.header("그래프 5. 앞으로 추가할 그래프")

st.info(
    "여기에 다섯 번째 그래프를 추가할 예정입니다."
)
