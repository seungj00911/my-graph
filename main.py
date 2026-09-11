import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------
# 기본 설정
# ---------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# ---------------------------------------
# 데이터 불러오기
# ---------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str), format="%Y%m%d")

    return df


df = load_data()


# ---------------------------------------
# 데이터 확인
# ---------------------------------------
st.write(
    f"총 {len(df):,}개의 기록을 불러왔습니다."
)


# =======================================
# 그래프 1. 영화별 일관객 변화
# =======================================
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
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
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,"
    }
)

fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
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
# 앞으로 추가할 그래프 영역
# =======================================

st.divider()

st.header("그래프 2. 앞으로 추가할 그래프")
st.info("여기에 두 번째 그래프를 추가할 예정입니다.")


st.divider()

st.header("그래프 3. 앞으로 추가할 그래프")
st.info("여기에 세 번째 그래프를 추가할 예정입니다.")
