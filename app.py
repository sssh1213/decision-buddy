import streamlit as st

# 1. 頁面基本設定
st.set_page_config(page_title="DecisionSS", page_icon="⚖️", layout="centered")

# 2. 燕麥白、純白與莫蘭迪 CSS 注入
morandi_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #F4F1ED; 
        color: #5C5855; 
        max-width: 600px; 
        margin: 0 auto;
    }
    
    h2, h4, h5, p, span, label {
        color: #5C5855 !important; 
    }
    
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        border: 1px solid #D5CABD !important;
        border-radius: 8px !important;
        color: #5C5855 !important;
    }
    
    hr {
        border-top: 1px dashed #D5CABD !important; 
        margin: 1.5em 0;
    }
    
    /* 按鈕顏色改造 */
    div.stButton > button:first-child {
        background-color: #A48A7A !important; 
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #8D7464 !important; 
        color: #FFFFFF !important;
    }

    /* 讓滑桿視覺變輕盈 */
    div[data-baseweb="slider"] > div > div > div:nth-child(1) {
        background-color: #E8E3DF !important; 
    }
    div[data-baseweb="slider"] > div > div > div:nth-child(2) {
        background-color: #A48A7A !important; 
    }
    div[data-baseweb="slider"] > div > div > div[role="slider"] {
        background-color: #8D7464 !important; 
        box-shadow: 0 0 5px rgba(0,0,0,0.1) !important;
    }

    /* 讓單選按鈕 (Radio) 水平置中排列 */
    div[role="radiogroup"] {
        justify-content: center !important;
    }
    </style>
"""
st.markdown(morandi_style, unsafe_allow_html=True)

# 3. 極簡風格標題
st.markdown("<h2 style='text-align: center; font-weight: 600; margin-bottom: 0;'>DecisionSS</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px; letter-spacing: 1px;'>放下執念，讓數據打醒你</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. 選項輸入
col1, col2 = st.columns(2)
with col1:
    option_a = st.text_input("選項 A", placeholder="例如：買新手機", label_visibility="collapsed")
with col2:
    option_b = st.text_input("選項 B", placeholder="例如：出國旅遊", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 初始化 Session State
if 'criteria' not in st.session_state:
    st.session_state.criteria = [
        {"name": "價格與荷包的痛楚", "weight": 4, "score_a": 3, "score_b": 3},
        {"name": "心靈滿足感", "weight": 5, "score_a": 3, "score_b": 3}
    ]

def add_criterion():
    st.session_state.criteria.append({"name": "新考量因素", "weight": 3, "score_a": 3, "score_b": 3})

# 6. 渲染評估區塊
st.markdown("<h5 style='text-align: center; font-weight: 500;'>— 評估維度 —</h5>", unsafe_allow_html=True)

for i, c in enumerate(st.session_state.criteria):
    with st.container():
        # 因素名稱
        c["name"] = st.text_input("因素名稱", c["name"], key=f"name_{i}", label_visibility="collapsed")
        
        # 【修改區塊】字體放大 (16px)、增加底部邊距 (15px)、並置中對齊
        st.markdown("<p style='text-align: center; font-size: 16px; font-weight: 600; margin-top: 15px; margin-bottom: 15px;'>💡 此因素的致命程度 (1=還好, 5=絕對關鍵)</p>", unsafe_allow_html=True)
        
        # 單選按鈕 (透過上方的 CSS 已經達成置中)
        c["weight"] = st.radio(
            "致命程度", 
            options=[1, 2, 3, 4, 5], 
            index=c["weight"] - 1, 
            key=f"w_{i}", 
            horizontal=True, 
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True) # 增加與下方滑桿的呼吸空間
        
        # 選項 A 與 B 的滑桿
        col_a, col_b = st.columns(2)
        with col_a:
            c["score_a"] = st.slider(f"🤎 {option_a if option_a else 'A'} 的表現", 1, 5, c["score_a"], key=f"a_{i}")
        with col_b:
            c["score_b"] = st.slider(f"🩶 {option_b if option_b else 'B'} 的表現", 1, 5, c["score_b"], key=f"b_{i}")
        
        st.markdown("<hr>", unsafe_allow_html=True)

st.button("＋ 覺得還不夠？再加一個條件", on_click=add_criterion, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. 計算與【靈魂深度分析】結果呈現
if st.button("🔮 揭曉殘酷真相", type="primary", use_container_width=True):
    name_a = option_a if option_a else "選項 A"
    name_b = option_b if option_b else "選項 B"

    score_a = sum(c["weight"] * c["score_a"] for c in st.session_state.criteria)
    score_b = sum(c["weight"] * c["score_b"] for c in st.session_state.criteria)
    max_possible = sum(c["weight"] * 5 for c in st.session_state.criteria)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; font-weight: 500;'>— 分析結論 —</h4>", unsafe_allow_html=True)
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label=f"🤎 {name_a}", value=score_a)
        st.progress(score_a / max_possible if max_possible > 0 else 0)
    with res_col2:
        st.metric(label=f"🩶 {name_b}", value=score_b)
        st.progress(score_b / max_possible if max_possible > 0 else 0)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- 深度數據分析邏輯 ---
    if score_a == score_b:
        highest_weight_item = max(st.session_state.criteria, key=lambda x: x["weight"])["name"]
        st.warning(f"⚖️ **平分秋色！宇宙級的糾結！**\n\n醒醒吧！數據顯示這兩個選項對你來說根本一樣好（或一樣糟）。你明明在「**{highest_weight_item}**」給了那麼高的權重，結果兩邊表現居然差不多？建議拋個硬幣，或者去給自己沖杯 Espresso 醒醒腦。再糾結下去只是浪費生命！")
    else:
        winner = name_a if score_a > score_b else name_b
        loser = name_b if score_a > score_b else name_a
        diff = abs(score_a - score_b)
        
        adv_list = []
        for c in st.session_state.criteria:
            val_a = c["weight"] * c["score_a"]
            val_b = c["weight"] * c["score_b"]
            if score_a > score_b:
                adv = val_a - val_b
            else:
                adv = val_b - val_a
            adv_list.append({"name": c["name"], "adv": adv})
        
        adv_list.sort(key=lambda x: x["adv"], reverse=True)
        killer_factor = adv_list[0]["name"] 
        
        pity_factor = None 
        for item in reversed(adv_list):
            if item["adv"] < 0:
                pity_factor = item["name"]
                break
                
        if diff >= (max_possible * 0.2): 
            text = f"🎉 **毫無懸念，【{winner}】徹底碾壓了【{loser}】！**\n\n光是在「**{killer_factor}**」這個項目上，【{winner}】就已經把對手按在地上摩擦了。分數懸殊成這樣，你到底還在猶豫什麼？"
            if pity_factor:
                text += f"\n\n雖然【{loser}】在「**{pity_factor}**」試圖挽回一點顏面，但根本是螳臂擋車。聽數據的，果斷投入【{winner}】的懷抱吧！"
            else:
                text += f"\n\n可憐的【{loser}】連一個能打的項目都沒有。選它完全是拿石頭砸自己的腳！"
            st.success(text)
            
        elif diff >= (max_possible * 0.1): 
            text = f"✨ **【{winner}】穩穩勝出！**\n\n綜合你的『貪心程度』與『現實考量』，【{winner}】才是那個對的選擇。它在「**{killer_factor}**」上的亮眼表現是這次獲勝的關鍵。"
            if pity_factor:
                text += f" 別再看【{loser}】了，就算它在「**{pity_factor}**」有小優勢，但「大人全都要」是不可能的。不甘心是不會有好結果的！"
            st.info(text)
            
        else: 
            text = f"🤏 **【{winner}】以微弱優勢險勝！**\n\n這分數黏得比麥芽糖還緊！【{winner}】只不過是靠著在「**{killer_factor}**」上多拿了一點分數苟延殘喘贏了這局。"
            if pity_factor:
                text += f" 而且別忘了，【{loser}】在「**{pity_factor}**」可是贏過它的！"
            text += f"\n\n老實說，分數咬這麼緊，你心裡是不是本來就比較偏袒【{winner}】？這個測驗只是給你一個冠冕堂皇的藉口罷了。去吧，就順從你的直覺選它！"
            st.info(text)
