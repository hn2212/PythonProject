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
#st.caption("Hans Rosling의 TED 강연을 유명하게 만든 데이터 (1952~2007, 142개국)")    # 제목 아래 작은 설명 글씨




tab1, tab2, = st.tabs([   # 탭 2개를 한 번에 만들어 각각 tab1~tab2에 담기

    "🏆 학생 성취도 분석",            # 첫 번째 탭 이름
    "📈 성취도 변화 궤적"             # 두 번째 탭 이름
])



#  탭 1: 학생 성취도 분석 적용
with tab1:
    st.header("🎓 학생 성취도 상세 분석")

    st.subheader("1. 학생별 월별 출석률과 학습량 비교")
    fig1 = px.scatter(
        df_stu,
        x="출석률", y="학습량(시간)",
        size="성취도",  # 성취도는 버블 크기
        color="학생명",  # 학생별 고유 색상(이전 스타일)
        symbol_sequence=['circle'],  # 아이콘을 원형으로 통일
        text="월",  # 아이콘 옆에 월 표기
        title="전체 학생 종합 활동 분포 (색상=학생, 숫자=월, 성취도=크기)",
        template="plotly_white"
    )

    # 텍스트와 마커 가독성 조정
    fig1.update_traces(
        mode='markers+text',
        textposition='top center',
        marker=dict(line=dict(width=1, color='DarkSlateGrey'))
    )

    # sizeref 값을 작게 할수록 전체적인 버블 크기가 커지며 상대적 차이가 잘 보임
    # sizemode='area'는 성취도 수치와 버블 면적을 비례하게 함
    fig1.update_traces(
        mode='markers+text',
        textposition='top center',
        marker=dict(sizemode='area', sizeref=0.1, line=dict(width=1, color='DarkSlateGrey'))
    )

    # 축 레이블 한 번만 설정
    fig1.update_layout(
        xaxis_title="출석률 (%)",
        yaxis_title="학습량 (시간)",
        showlegend=True
    )

    st.plotly_chart(fig1, use_container_width=True)


    st.subheader("2. 월별 학생 성취도 순위 (행 배치)")
    # 행(row)을 기준으로 월을 구분하여 1월과 2월을 위아래로 배치
    fig2 = px.bar(
        df_stu.sort_values(["월", "성취도"], ascending=[True, False]),
        x="성취도", y="학생명",  # x와 y를 바꾸어 가로 막대 그래프로 변경
        facet_row="월",        # 월별로 행을 나누어 배치
        text="성취도",
        color="성취도",
        orientation='h',       # 가로 방향 막대
        height=600,            # 행 배치를 위해 높이 확장
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("3. 학생별 상세 데이터")
    st.dataframe(df_stu, use_container_width=True)



#  탭 2: 성취도 변화 궤적
with tab2:  # 탭 목록에 "🚀 성취 변화 궤적"을 추가하세요
    st.header("🚀 학생별 성취도 변화 궤적")
    st.write("1월에서 2월로 이동하는 화살표를 통해 성취 변화를 확인하세요.")

    # 덤벨/궤적 차트 생성
    df_pivot = df_stu.pivot(index='학생명', columns='월', values='성취도').reset_index()
    df_pivot.columns = ['학생명', '1월_성취도', '2월_성취도']

    fig = px.scatter(
        df_pivot,
        x=['1월_성취도', '2월_성취도'], y='학생명',
        color_discrete_sequence=['#ff9999', '#66b3ff'],
        title="1월(분홍) → 2월(파랑) 성취도 이동",
        labels={'value': '성취도 점수', 'variable': '기준 월'}
    )

    # 1. 아이콘(마커) 크기를 조절 (10)
    fig.update_traces(marker=dict(size=10))

    # 1월에서 2월을 잇는 화살표 궤적 추가
    for i, row in df_pivot.iterrows():
        fig.add_annotation(
            dict(
                ax=row['1월_성취도'], ay=row['학생명'],
                x=row['2월_성취도'], y=row['학생명'],
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=1,
                arrowsize=1,
                arrowwidth=2,  # 2. 화살표 굵기를 키움 (2 → 3)
                arrowcolor="gray",  # 3. 화살표 색상을 더 진하게 변경 (gray → black)
                standoff=5,  # 마커가 작아졌으므로 standoff도 살짝 조정
                opacity=1.0  # 4. 투명도를 제거하여 더 선명하게 표시
            )
        )

    fig.update_layout(height=500, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)