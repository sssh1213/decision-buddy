import streamlit as st
import pandas as pd

# 網頁標題與設定
st.set_page_config(page_title="終極二選一神器", page_icon="⚖️")
st.title("🤔 終極二選一：決策分析神器")
st.write("陷入選擇障礙？輸入你的選項，設定評估因素與重要性，讓數據幫你做決定！")

# 選項輸入區塊
col1, col2 = st.columns(2)
with col1:
    option_a = st.text_input("輸入選項 A", "例如：買筆電")
with col2:
    option_b = st.text_input("輸入選項 B", "例如：組裝桌機")

st.markdown("---")
st.subheader("⚖️ 評分矩陣")
st.write("請修改下方表格：填入你考量的因素、該因素的重要性（1-5分，5分最重要），以及兩個選項各自的得分（1-5分，5分最好）。你可以隨時在表格最下方新增一列！")

# 建立預設資料表
# 每次選項名稱改變時，更新 DataFrame 的欄位名稱
data = {
    "考量因素": ["價格預算", "外觀設計", "實用程度", "後續維護"],
    "重要性權重 (1-5)": [4, 3, 5, 2],
    f"{option_a} 得分 (1-5)": [3, 4, 4, 3],
    f"{option_b} 得分 (1-5)": [4, 2, 5, 4]
}
df = pd.DataFrame(data)

# 使用 data_editor 讓使用者可以直接在網頁上編輯表格
edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

# 執行分析按鈕
if st.button("📊 產生分析結果", type="primary"):
    # 確保資料為數值型態以進行計算
    try:
        weight = pd.to_numeric(edited_df["重要性權重 (1-5)"])
        score_a_col = pd.to_numeric(edited_df[f"{option_a} 得分 (1-5)"])
        score_b_col = pd.to_numeric(edited_df[f"{option_b} 得分 (1-5)"])
        
        # 計算加權總分
        score_a = sum(weight * score_a_col)
        score_b = sum(weight * score_b_col)

        st.markdown("---")
        st.subheader("🏆 分析結果")
        
        # 顯示分數看板
        res_col1, res_col2 = st.columns(2)
        res_col1.metric(label=f"🔵 {option_a} 加權總分", value=score_a)
        res_col2.metric(label=f"🟢 {option_b} 加權總分", value=score_b)

        # 給出最終結論
        if score_a > score_b:
            st.success(f"🎉 根據你的理性評估，數據強烈建議你選擇：**{option_a}**！")
            st.balloons()
        elif score_b > score_a:
            st.success(f"🎉 根據你的理性評估，數據強烈建議你選擇：**{option_b}**！")
            st.balloons()
        else:
            st.info("⚖️ 勢均力敵！這兩個選擇對你來說一樣好。你可以考慮閉上眼睛，拋個硬幣，或者再新增一個決定性的考量因素。")
            
    except Exception as e:
        st.error("⚠️ 請確保「重要性權重」與「得分」欄位中填寫的都是數字喔！")