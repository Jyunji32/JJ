import streamlit as st
import pandas as pd
import os

st.title("🔥 筋トレ自己ベスト・チェッカー")

# データの読み込み
if os.path.exists("workout_log.csv"):
    df = pd.read_csv("workout_log.csv")
    
    # 種目選択
    menus = df["種目"].unique()
    target = st.selectbox("種目を選んでください", menus)
    
    # その種目のデータだけを抽出
    target_df = df[df["種目"] == target]
    
    if not target_df.empty:
        # 1. 自己ベスト（最大重量）を取得
        best_weight = target_df["重量"].max()
        
        # 2. 前回の重量を取得（比較用）
        last_weight = target_df.iloc[-1]["重量"]
        
        # 3. カッコよく表示 (st.metric)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"{target} の自己ベスト", value=f"{best_weight} kg")
        with col2:
            delta = best_weight - last_weight
            st.metric(label="前回との差", value=f"{last_weight} kg", delta=f"{delta} kg")

        # 4. 成長グラフ
        st.line_chart(target_df.set_index("日付")["重量"])
else:
    st.info("まだ記録がありません。まずはデータを入力しましょう！")

# 入力フォーム（前回のコードと同じ）
with st.expander("新しい記録を追加する"):
    with st.form("input_form"):
        new_menu = st.selectbox("種目", ["ベンチプレス", "スクワット", "デッドリフト"])
        new_weight = st.number_input("重量(kg)", step=2.5)
        new_reps = st.number_input("回数", step=1)
        submitted = st.form_submit_button("保存")
        
        if submitted:
            # ここに保存処理を書く（前回のロジックと同じ）
            st.success("保存しました！画面を更新してください。")
