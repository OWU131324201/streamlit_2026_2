import streamlit as st
import pandas as pd
from datetime import date

st.title("🏠 かんたん家計簿")

# 1. データの保存場所を初期化
if "expenses" not in st.session_state:
    st.session_state.expenses = []

# 2. 入力エリア
st.subheader("収支を入力")
col1, col2 = st.columns(2)
with col1:
    expense_date = st.date_input("日付", date.today())
    category = st.selectbox("カテゴリ", ["🍽️ 食費", "🚃 交通費", "🧻 日用品", "🤝 交際費", "🎮 趣味・娯楽", "🏠 固定費", "📦 その他"])
    # フォームの外に出したことで、選択した瞬間に以下の処理が走るようになります
    if category == "📦 その他":
        other_category = st.text_input("カテゴリ名を入力")
    else:
        other_category = ""
with col2:
    item = st.text_input("品目（例：お弁当、電車代など）")
    amount = st.number_input("金額 (円)", min_value=0, step=50)

if st.button("記録する"):
    if item and amount > 0:
        # その他なら入力されたカテゴリ名を使用、未入力なら「その他」とする
        final_category = other_category if category == "📦 その他" and other_category else category
        # 新しいデータを辞書形式で作る
        new_data = {
            "日付": expense_date,
            "カテゴリ": final_category, # 修正: final_categoryを使用するように変更
            "品目": item,
            "金額": amount
        }
        # session_stateのリストに追加
        st.session_state.expenses.append(new_data)
        # フォームの clear_on_submit の代わりに再描画して入力をリセットする
        st.rerun()
    else:
        st.error("品目と金額（1円以上）を入力してください。")

# 3. 履歴の表示と集計
st.markdown("---")
st.subheader("履歴と合計")

if st.session_state.expenses:
    # データをDataFrameに変換して見やすくする
    df = pd.DataFrame(st.session_state.expenses)
    
    # 合計金額を計算して強調表示
    total = df["金額"].sum()
    st.metric("合計支出", f"{total:,} 円")

    # テーブル形式で表示
    st.dataframe(df.sort_values("日付", ascending=True), use_container_width=True)

    if st.button("全ての履歴をリセット"):
        st.session_state.expenses = []
        st.rerun()
else:
    st.info("まだ記録がありません。上のフォームから入力してください。")
