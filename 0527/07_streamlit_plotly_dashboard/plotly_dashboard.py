# pip install streamlit plotly pandas
# 실행 방법: streamlit run plotly_dashboard.py

import streamlit as st          # 웹 화면(버튼, 탭, 차트 등)을 만드는 도구
import pandas as pd             # 표(엑셀 같은) 데이터를 다루는 도구
import plotly.express as px     # 인터랙티브한 그래프(애니메이션, 지도 등)를 그리는 도구
from pathlib import Path        # 파일 경로를 OS와 무관하게 다루는 도구
CSV_PATH = Path(__file__).parent / "gapminder.csv"  # 이 스크립트와 같은 폴더의 CSV (실행 위치와 무관하게 항상 같은 파일을 가리킴)
df = pd.read_csv(CSV_PATH)  # CSV 파일을 표(데이터프레임)로 불러오기. 이후 모든 탭이 이 df를 함께 사용

STUDENT_DATA_PATH = Path(__file__).parent / "student_data.csv"
df_stu = pd.read_csv(STUDENT_DATA_PATH)

st.set_page_config(page_title="통합 대시보드", page_icon="🌍", layout="wide")  # 브라우저 탭 제목/아이콘 + 화면을 넓게 사용
st.title("📊 데이터 통합 대시보드")                                    # 페이지 맨 위 큰 제목
st.caption("Hans Rosling의 TED 강연을 유명하게 만든 데이터 (1952~2007, 142개국)")    # 제목 아래 작은 설명 글씨




tab1, tab2, tab3, tab4 = st.tabs([   # 탭 4개를 한 번에 만들어 각각 tab1~tab4에 담기
    "🫧 애니메이션 버블",            # 첫 번째 탭 이름
    "🗺️ 세계 지도",                  # 두 번째 탭 이름
    "📈 국가 트렌드",                # 세 번째 탭 이름
    "🏆 학생 성취도 분석",            # 네 번째 탭 이름
])


# --- 탭 1: 애니메이션 버블 차트 ---
with tab1:  # 여기 들여쓰기 안에 적은 내용이 첫 번째 탭 화면에 나옴
    st.header("🫧 GDP vs 기대수명 (시간 흐름)")                                       # 탭 안의 소제목
    st.write("▶ 버튼을 눌러 1952년부터 2007년까지 세계가 어떻게 변했는지 확인해보세요.")  # 안내 문장

    fig = px.scatter(           # 점(버블) 그래프를 만들어 fig에 담기
        df,                     # 사용할 데이터(표)
        x="gdpPercap",          # 가로축 = 1인당 GDP
        y="lifeExp",            # 세로축 = 기대수명
        size="pop",             # 버블 크기 = 인구 (인구 많을수록 큰 원)
        color="continent",      # 버블 색 = 대륙별로 다른 색
        hover_name="country",   # 마우스를 올리면 국가명 표시
        animation_frame="year", # 연도별로 화면을 나눠 ▶ 재생(애니메이션) 가능하게
        animation_group="country",  # 애니메이션 중 같은 나라를 계속 추적(부드럽게 이동)
        log_x=True,             # 가로축을 로그 스케일로(GDP 차이가 너무 커서 안 그러면 한쪽에 몰림)
        size_max=60,            # 가장 큰 버블의 최대 크기 제한
        range_x=[200, 100000],  # 가로축 표시 범위 고정(애니메이션 중 축이 안 흔들리게)
        range_y=[25, 90],       # 세로축 표시 범위 고정
        labels={"gdpPercap": "1인당 GDP (달러)", "lifeExp": "기대수명 (세)", "pop": "인구"},  # 영어 컬럼명 → 화면엔 한글로 표시
        title="1인당 GDP vs 기대수명 (버블 크기 = 인구)",  # 그래프 제목
    )
    fig.update_layout(height=580)                  # 그래프 높이를 580픽셀로 조정
    st.plotly_chart(fig, use_container_width=True) # 완성한 그래프를 화면에 표시(가로 폭에 꽉 채움)


# --- 탭 2: 세계 지도 ---
with tab2:  # 두 번째 탭 화면
    st.header("🗺️ 세계 지도로 보기")  # 소제목

    col1, col2 = st.columns(2)  # 화면을 좌우 2칸으로 나누기
    with col1:                  # 왼쪽 칸
        metric = st.selectbox(                      # 드롭다운에서 한 개 선택 → 고른 값이 metric에 담김
            "표시할 지표",                            # 드롭다운 위 라벨
            ["gdpPercap", "lifeExp", "pop"],         # 선택지(실제 컬럼명)
            format_func=lambda x: {"gdpPercap": "1인당 GDP", "lifeExp": "기대수명", "pop": "인구"}[x],  # 화면엔 한글로 보이게 변환
        )
    with col2:                  # 오른쪽 칸
        animate = st.checkbox("연도별 애니메이션", value=True)  # 체크박스(기본은 켜짐) → True/False가 animate에 담김

    label_map = {"gdpPercap": "1인당 GDP (달러)", "lifeExp": "기대수명 (세)", "pop": "인구"}  # 컬럼명 → 한글 라벨 사전

    # px.choropleth: iso_alpha(국가 코드)로 세계 지도를 자동 생성
    fig = px.choropleth(        # 나라별로 색칠하는 세계 지도 그래프
        df,                     # 사용할 데이터
        locations="iso_alpha",  # 나라를 알아보는 기준 = 국가 코드 컬럼(예: KOR, JPN)
        color=metric,           # 색칠 기준 = 위에서 고른 지표
        hover_name="country",   # 마우스 올리면 국가명 표시
        animation_frame="year" if animate else None,  # 체크박스 켜졌으면 연도 애니메이션, 아니면 정지
        color_continuous_scale="Viridis",  # 색 팔레트(낮음→높음 그라데이션)
        labels={metric: label_map[metric]},  # 범례 라벨을 한글로
        title=f"세계 {label_map[metric]} 분포",  # 고른 지표에 맞춰 제목 자동 변경
    )
    fig.update_layout(height=520)                  # 지도 높이 조정
    st.plotly_chart(fig, use_container_width=True) # 화면에 표시

# --- 탭 3: 국가 트렌드 ---
with tab3:  # 세 번째 탭 화면
    st.header("📈 국가별 시간 흐름")  # 소제목

    default_countries = ["Korea, Rep.", "Japan", "China", "United States", "Germany"]  # 처음에 미리 골라둘 나라들
    all_countries = sorted(df["country"].unique())  # 데이터에 있는 모든 나라 목록
    selected = st.multiselect(
        "국가 선택 (여러 개 가능)",
        all_countries,
        default=[c for c in default_countries if c in all_countries],
    )

    if not selected:
        st.info("국가를 하나 이상 선택하세요.")
        st.stop()

    metric2 = st.radio(
        "지표 선택",
        ["lifeExp", "gdpPercap", "pop"],
        format_func=lambda x: {"lifeExp": "기대수명", "gdpPercap": "1인당 GDP", "pop": "인구"}[x],
        horizontal=True,
    )

    filtered = df[df["country"].isin(selected)]
    label_map2 = {"lifeExp": "기대수명 (세)", "gdpPercap": "1인당 GDP (달러)", "pop": "인구"}

    # --- 추가된 부분: 선 그래프가 자라나는 애니메이션을 위한 누적 데이터 생성 ---
    frames = []
    years = sorted(filtered["year"].unique())  # 존재하는 모든 연도 가져오기 (1952, 1957...)
    for y in years:
        temp_df = filtered[filtered["year"] <= y].copy()  # 현재 연도(y)와 같거나 과거인 데이터만 복사
        temp_df["frame_year"] = y  # 애니메이션 재생 기준이 될 프레임 연도 기록
        frames.append(temp_df)
    cumulative_df = pd.concat(frames)  # 생성된 모든 누적 데이터를 하나로 합치기

    # 애니메이션 중 그래프 축이 위아래로 흔들리지 않도록 Y축 고정 범위 계산
    y_min, y_max = filtered[metric2].min(), filtered[metric2].max()
    y_margin = (y_max - y_min) * 0.1  # 위아래 10% 여백

    fig = px.line(
        cumulative_df,  # 원본 대신 새로 만든 누적 데이터 사용
        x="year", y=metric2,
        color="country",
        markers=True,
        animation_frame="frame_year",  # 동영상처럼 재생할 기준 (frame_year)
        range_x=[1952, 2007],  # 가로축 범위 고정
        range_y=[y_min - y_margin, y_max + y_margin],  # 세로축 범위 고정
        labels={"year": "연도", metric2: label_map2[metric2]},
        title=f"선택 국가 {label_map2[metric2]} 변화 (1952~2007)",
    )

    # 애니메이션 재생 속도 조절 (프레임당 500ms 딜레이)
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500

    fig.update_layout(height=480)
    st.plotly_chart(fig, use_container_width=True)



# [수정] 탭 4: 학생 성취도 분석 적용
with tab4:
    st.header("🎓 학생 성취도 상세 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("출석률과 학습량의 관계")
        fig1 = px.scatter(
            df_stu, x="출석률", y="학습량(시간)",
            size="성취도점수", color="학생명",
            title="학생별 출석/학습량 분포"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("성취도 순위")
        fig2 = px.bar(
            df_stu.sort_values("성취도점수", ascending=False),
            x="학생명", y="성취도점수",
            text="성취도점수", color="성취도점수",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("학생별 상세 데이터")
    st.dataframe(df_stu, use_container_width=True)