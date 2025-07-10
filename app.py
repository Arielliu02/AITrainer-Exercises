# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 21:12:38 2025

@author: liupi
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="📘 50 題測驗系統", layout="centered")

# ✅ 讀取題庫並隨機抽出 50 題
@st.cache_data
def load_questions():
    df = pd.read_excel("題庫.xlsx").dropna()
    df = df.sample(n=50, random_state=42).reset_index(drop=True)
    questions = []
    for _, row in df.iterrows():
        questions.append({
            "question": row["question"],
            "options": [row["option1"], row["option2"], row["option3"], row["option4"]],
            "answer": row["answer"]
        })
    return questions

# ✅ 初始化 session_state
if "questions" not in st.session_state:
    st.session_state.questions = load_questions()
if "answered" not in st.session_state:
    st.session_state.answered = {}
if "score" not in st.session_state:
    st.session_state.score = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0

# ✅ 顯示一題
def show_question(q_idx):
    q = st.session_state.questions[q_idx]
    st.subheader(f"第 {q_idx + 1} 題：{q['question']}")

    key_choice = f"choice_{q_idx}"
    key_submit = f"submit_{q_idx}"

    if q_idx not in st.session_state.answered:
        choice = st.radio("請選擇你的答案：", q["options"], key=key_choice)
        if st.button("提交答案", key=key_submit):
            st.session_state.answered[q_idx] = choice
            if choice == q["answer"]:
                st.success("✅ 答對了！")
                st.session_state.score += 4
                st.session_state.correct += 1
            else:
                st.error(f"❌ 答錯了！正確答案是：**{q['answer']}**")
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.info("✅ 本題已作答。")
        st.write(f"你的答案：{st.session_state.answered[q_idx]}")
        st.write(f"正確答案：**{q['answer']}**")

# ✅ 測驗結束
def show_result():
    st.success("🎉 測驗完成！")
    st.metric("✅ 答對題數", f"{st.session_state.correct} / 50")
    st.metric("🧮 總得分", f"{st.session_state.score} / 200")
    if st.button("🔁 重新測驗"):
        reset()

# ✅ 重設
def reset():
    st.session_state.questions = load_questions()
    st.session_state.answered = {}
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.current_q = 0
    st.rerun()

# ✅ 主程式
def main():
    st.title("📘 50 題單選練習測驗")
    st.caption("每題 4 分，滿分 200 分，答錯會顯示正確答案")

    q_idx = st.session_state.current_q
    if q_idx >= 50:
        show_result()
    else:
        show_question(q_idx)

if __name__ == "__main__":
    main()