# =======================================
# 그래프 2. 일관객 합계 TOP 5 영화
# =======================================

st.divider()

st.header("그래프 2. 일관객 합계 TOP 5 영화")

# 영화별 일관객 합계 계산
top5_movies = (
    df.groupby("영화명")["일관객"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

# TOP 5 영화만 추출
top5_df = df[df["영화명"].isin(top5_movies)].copy()

# 날짜순 정렬
top5_df = top5_df.sort_values(["날짜", "영화명"])


# 선 그래프 생성
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 TOP 5 영화의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "영화명": True,
        "일관객": ":,"
    }
)

fig2.update_traces(
    hovertemplate="영화: %{fullData.name}<br>"
                  "날짜: %{x|%Y-%m-%d}<br>"
                  "관객수: %{y:,}명<extra></extra>"
)

fig2.update_layout(
    hovermode="x unified",
    legend_title="영화"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


st.subheader("이 그래프로 알 수 있는 것")
st.write(
    "전체 기간 동안 일관객 합계가 가장 큰 5편의 영화가 날짜에 따라 어떤 관객 변화 추이를 보였는지 비교할 수 있다."
)
