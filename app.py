import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("💪 筋トレ自己ベスト チェッカー")

# 1. スプレッドシートへの接続設定（Secretsの設定を使う）
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. データの読み込み
df = conn.read(ttl=0)

if not df.empty:
    # 種目選択
    menus = df["種目"].unique()
    target = st.selectbox("種目を選んでください", menus)
    
    # 選んだ種目のデータだけを抽出
    target_df = df[df["種目"] == target]
    
    if not target_df.empty:
        # 自己ベストの計算
        best_weight = target_df["重量"].max()
        last_weight = target_df.iloc[-1]["重量"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label=f"{target} の自己ベスト", value=f"{best_weight} kg")
        with col2:
            delta = float(last_weight) - float(target_df.iloc[-2]["重量"]) if len(target_df) > 1 else 0
            st.metric(label="今回の記録", value=f"{last_weight} kg", delta=f"{delta} kg")

        # 成長グラフ
        st.line_chart(target_df.set_index("日付")["重量"])
else:
    st.info("まだ記録がありません。下のフォームから最初の記録を追加しましょう！")

# 3. 入力フォーム
with st.expander("新しい記録を追加する"):
    with st.form("input_form"):
        new_menu = st.selectbox("種目", ["ベンチプレス", "スクワット", "デッドリフト"])
        new_weight = st.number_input("重量(kg)", min_value=0.0, step=2.5)
        new_reps = st.number_input("回数", min_value=0, step=1)
        submitted = st.form_submit_button("保存")
        
        if submitted:
            # 新しい行を作成
            new_row = pd.DataFrame([{
                "日付": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "種目": new_menu,
                "重量": new_weight,
                "回数": new_reps
            }])
            # 既存のデータに合体させてスプレッドシートを更新
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("スプレッドシートに保存しました！画面を更新してください。")
            st.balloons()
