# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 21:12:38 2025

@author: liupi
"""

import streamlit as st
import pandas as pd
import random

# ---------- 題庫讀取 ----------
@st.cache_data
def load_questions(path: str = "題庫.xlsx", n_questions: int = 50):
    df = pd.read_excel(path)

    required_cols = {"question", "option1", "option2", "option3", "option4", "answer"}
    if not required_cols.issubset(df.columns):
        st.error(f"❌ 題庫缺少欄位：{required_cols - set(df.columns)}")
        st.stop()

    questions = df.to_dict(orient="records")
    random.shuffle(questions)
    return questions[:min(n_questions, len(questions))]

# ---------- 初始化 ----------
if "initialized" not in st.session_state:
    st.session_state.questions   = load_questions()
    st.session_state.current_q   = 0
    st.session_state.score       = 0
    st.session_state.correct_cnt = 0
    st.session_state.finished    = False
    st.session_state.history     = []
    st.session_state.answered    = False
    st.session_state.initialized = True

# ---------- 重置 ----------
def reset_quiz():
    st.session_state.questions   = load_questions()
    st.session_state.current_q   = 0
    st.session_state.score       = 0
    st.session_state.correct_cnt = 0
    st.session_state.finished    = False
    st.session_state.history     = []
    st.session_state.answered    = False

# ---------- 頁面設定 ----------
st.set_page_config(page_title="測驗系統", page_icon="📝")
st.title("📝 iPAS+AI應用規劃師初級練習題庫")

# ---------- 測驗中 ----------
if not st.session_state.finished:
    q_idx     = st.session_state.current_q
    questions = st.session_state.questions
    total_q   = len(questions)
    q         = questions[q_idx]

    st.markdown(f"### 🖊️ 第 {q_idx + 1} 題 / 共 {total_q} 題")
    st.progress(q_idx / total_q, text=f"進度：{q_idx}/{total_q}")

    # 題目 & 選項
    st.write(q["question"])
    options = [q["option1"], q["option2"], q["option3"], q["option4"]]
    user_choice = st.radio("請選擇答案：", options, index=None, key=f"radio_{q_idx}")

    # 提交答案
    if st.button("提交答案", key=f"submit_{q_idx}") and not st.session_state.answered:
        if user_choice is None:
            st.warning("⚠️ 請先選擇一個選項！")
        else:
            correct_option = str(q["answer"]).strip()
            is_correct = (user_choice.strip() == correct_option)

            # 顯示回饋
            if is_correct:
                st.success("✅ 答對了！")
                st.session_state.score += 4
                st.session_state.correct_cnt += 1
            else:
                st.error(f"❌ 答錯了！正確答案是：{correct_option}")

            # 紀錄歷史
            st.session_state.history.append({
                "題號": q_idx + 1,
                "題目": q["question"],
                "你的答案": user_choice,
                "正確答案": correct_option,
                "是否正確": "✔️" if is_correct else "❌"
            })

            st.session_state.answered = True

    # 下一題按鈕
    if st.session_state.answered:
        if st.button("➡️ 下一題", key=f"next_{q_idx}"):
            st.session_state.current_q += 1
            st.session_state.answered = False

            if st.session_state.current_q >= total_q:
                st.session_state.finished = True

            st.rerun()

# ---------- 結果頁面 ----------
else:
    st.markdown("## 🎉 測驗完成！")
    st.success(f"✅ 答對題數：{st.session_state.correct_cnt} / {len(st.session_state.questions)}")
    st.info(f"🎯 總得分：{st.session_state.score} / {len(st.session_state.questions)*4}")

    st.markdown("---")
    st.markdown("### 📝 作答紀錄")
    result_df = pd.DataFrame(st.session_state.history)
    st.dataframe(result_df, use_container_width=True)

    st.download_button("⬇️ 下載作答紀錄 (CSV)", data=result_df.to_csv(index=False), file_name="quiz_result.csv")

    st.markdown("---")
    st.button("🔄 重新開始測驗", on_click=reset_quiz)

