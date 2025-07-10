# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 21:12:38 2025

@author: liupi
"""

import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="出題系統", layout="centered")

# 讀 Excel 題庫 & 隨機抽 50 題
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

# 初始化 session state
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.questions = load_questions()
    st.session_state.finished = False

# 顯示題目與選項
def show_question(q_idx):
    q = st.session_state.questions[q_idx]
    st.subheader(f"第 {q_idx+1} 題：{q['question']}")
    choice = st.radio("請選擇你的答案：", q["options"], key=f"q_{q_idx}")

    if st.button("提交答案", key=f"submit_{q_idx}"):
        if choice == q["answer"]:
            st.success("✅ 答對了！")
            st.session_state.score += 4
            st.session_state.correct += 1
        else:
            st.error(f"❌ 答錯了！正確答案是：**{q['answer']}**")
        st.session_state.current_q += 1
        st.rerun()

# 主程式
def main():
    st.title("📘 50 題單選練習測驗")
    st.caption("每題 4 分，滿分 200 分，題目隨機抽取")

    if st.session_state.finished or st.session_state.current_q >= 50:
        st.session_state.finished = True
        st.success("🎉 測驗完成！")
        st.metric("✅ 答對題數", f"{st.session_state.correct} / 50")
        st.metric("🧮 總得分", f"{st.session_state.score} / 200")
        st.button("🔁 重新測驗", on_click=reset)
    else:
        show_question(st.session_state.current_q)

# 重置測驗
def reset():
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.correct = 0
    st.session_state.questions = load_questions()
    st.session_state.finished = False
    st.rerun()

if __name__ == "__main__":
    main()