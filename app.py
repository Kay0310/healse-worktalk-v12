
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="WORK TALK", layout="wide")

# 큰 로고 중앙 정렬
st.markdown("<div style='text-align: center;'><img src='WORK_TALK_small.png' width='340'></div>", unsafe_allow_html=True)

st.markdown("사진 1장 업로드 → 질문 4개 응답 → 저장 → 다음 사진 순서대로 진행해 주세요.")

# 세션 초기화
if "responses" not in st.session_state:
    st.session_state.responses = []

def clear_inputs():
    st.session_state.name = ""
    st.session_state.dept = ""
    st.session_state.photo = None
    st.session_state.q1 = ""
    st.session_state.q2 = ""
    st.session_state.q3 = ""
    st.session_state.q4 = ""

# 입력 폼
with st.form("survey_form", clear_on_submit=False):
    st.text_input("👤 이름", key="name")
    st.text_input("🏢 부서", key="dept")
    uploaded_file = st.file_uploader("📸 작업 사진 업로드", type=["jpg", "jpeg", "png"], key="photo")

    show_questions = uploaded_file is not None
    if show_questions:
        st.image(uploaded_file, width=300)
        st.text_input("1️⃣ 어떤 작업을 하고 있는 건가요?", key="q1")
        st.text_input("2️⃣ 이 작업은 왜 위험하다고 생각하나요?", key="q2")
        st.radio("3️⃣ 이 작업은 얼마나 자주 하나요?", ["연 1-2회", "반기 1-2회", "월 2-3회", "주 1회 이상", "매일"], key="q3")
        st.radio("4️⃣ 이 작업은 얼마나 위험하다고 생각하나요?", [
            "약간의 위험: 일회용 밴드 치료 필요 가능성 있음",
            "조금 위험: 병원 치료 필요. 1-2일 치료 및 휴식",
            "위험: 보름 이상의 휴식이 필요한 중상 가능성 있음",
            "매우 위험: 불가역적 장애 또는 사망 가능성 있음"
        ], key="q4")

    submitted = st.form_submit_button("📥 저장하기")
    if submitted and all([
        st.session_state.get("name"),
        st.session_state.get("dept"),
        uploaded_file,
        st.session_state.get("q1"),
        st.session_state.get("q2"),
        st.session_state.get("q3"),
        st.session_state.get("q4")
    ]):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.responses.append({
            "작성일시": now,
            "이름": st.session_state.name,
            "부서": st.session_state.dept,
            "사진": uploaded_file.name,
            "질문1": st.session_state.q1,
            "질문2": st.session_state.q2,
            "질문3": st.session_state.q3,
            "질문4": st.session_state.q4
        })
        st.success("✅ 저장 완료! 다음 사진을 입력해 주세요.")
        clear_inputs()

# 응답 누적표시
if st.session_state.responses:
    st.markdown("---")
    st.markdown("### 📊 입력된 응답 모음 (WORK TALK 대화방)")
    df = pd.DataFrame(st.session_state.responses)
    st.dataframe(df)
