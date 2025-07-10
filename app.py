# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 21:12:38 2025

@author: liupi
"""

import streamlit as st
import pandas as pd
import random

# ====== 載入題庫 ======
@st.cache_data
def load_questions():
    df = pd.read_excel("題庫.xlsx")
    questions = df.to_dict(orient="records")
    random.shuffle(questions)
    return questions[:50]  # 選前50題

# ====== 初始化 Session State ======
if "questions" not in st.session_state:
    st.session_state.questions = load_questions()
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.finished = False

# ====== 重置測驗 ======
def reset():
    st.session_state.questions = load_questions()
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.finished = False

st.title("🧠 隨機出題測驗系統")

# ====== 測驗進行中 ======
if not st.session_state.finished:
    total_questions = len(st.session_state.questions)
    current_q = st.session_state.current_q
    q = st.session_state.questions[current_q]

    st.markdown(f"### 第 {current_q + 1} 題 / 共 {total_questions} 題")
    st.progress(current_q / total_questions)  # ✅ 進度條

    st.markdown(f"**{q['question']}**")
    options = [q['A'], q['B'], q['C'], q['D']]
    user_answer = st.radio("請選擇答案：", options, key=current_q)

    if st.button("提交答案"):
        correct_option = q[q['answer']]  # 正確選項的文字
        if user_answer == correct_option:
            st.success("✅ 答對了！")
            st.session_state.score += 4
            st.session_state.correct += 1
        else:
            st.error(f"❌ 答錯了！正確答案是：{correct_option}")

        st.session_state.current_q += 1

        if st.session_state.current_q >= total_questions:
            st.session_state.finished = True

        st.experimental_rerun()  # 手動刷新畫面

# ====== 測驗結束 ======
else:
    st.markdown("## 🎉 測驗完成！")
    st.markdown(f"✅ 答對題數：{st.session_state.correct} / 50")
    st.markdown(f"🎯 得分：{st.session_state.score} / 200")

    st.button("🔄 重新開始測驗", on_click=reset)
