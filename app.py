# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 21:12:38 2025

@author: liupi
"""

import streamlit as st
import random

def load_questions():
    return [
        {
            "question": "Python 中用於數據分析的套件是？",
            "options": ["NumPy", "Flask", "Django", "TensorFlow"],
            "answer": "NumPy"
        },
        {
            "question": "R 中畫出直方圖使用哪個函數？",
            "options": ["barplot()", "hist()", "plot()", "curve()"],
            "answer": "hist()"
        },
        {
            "question": "SAS 中使用哪個語法讀取資料？",
            "options": ["DATA", "PROC SQL", "RUN", "LIBNAME"],
            "answer": "DATA"
        }
    ]

def show_question(q):
    st.subheader(q["question"])
    choice = st.radio("請選擇你的答案：", q["options"], key=q["question"])
    if st.button("提交答案", key=q["question"] + "_submit"):
        if choice == q["answer"]:
            st.success("恭喜答對了！")
        else:
            st.error(f"答錯了，正確答案是：{q['answer']}")

def main():
    st.title("練習題隨機出題系統")
    st.markdown("從內建題庫中隨機出題，選擇答案進行練習")
    questions = load_questions()
    q = random.choice(questions)
    show_question(q)
    st.button("再出一題", on_click=st.rerun)

if __name__ == "__main__":
    main()