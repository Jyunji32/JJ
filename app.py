import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("💪 筋トレ記録")

# 接続
conn = st.connection("gsheets", type=GSheetsConnection)

# 読み込み
df = conn.read(ttl=0)

# 入力フォーム
with st.form("my_form"):
    menu = st.selectbox("種目", ["ベンチプレス", "スクワット", "デッドリフト"])
    weight = st.number_input("重量", step=2.5)
    reps = st.number_input("回数", step=1)
    submit = st.form_submit_button("保存")

    if submit:
        new_data = pd.DataFrame([{
            "日付": pd.Timestamp.now().strftime("%Y-%m-%d"),
            "種目": menu,
            "重量": weight,
            "回数": reps
        }])
        # 既存のデータと合体
        updated_df = pd.concat([df, new_data], ignore_index=True)
        
        # 【修正ポイント】書き込みを実行
        try:
            conn.update(data=updated_df)
            st.success("保存完了！")
            st.balloons()
        except Exception as e:
            st.error(f"保存に失敗しました。エラー内容: {e}")
            st.info("スプレッドシートの『共有』が『編集者』になっているか再度確認してください。")
