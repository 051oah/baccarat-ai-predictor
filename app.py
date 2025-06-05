import streamlit as st
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="百家樂 AI 預測", layout="centered")
st.title("🎲 百家樂 AI 預測器 v1.1")
st.markdown("透過 AI 預測下一局是「莊」還是「閒」，點選下方按鈕開始輸入：")

# 儲存歷史資料
if "history" not in st.session_state:
    st.session_state.history = []

# 操作按鈕
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟥 莊 (B)"):
        st.session_state.history.append("B")
with col2:
    if st.button("🟦 閒 (P)"):
        st.session_state.history.append("P")
with col3:
    if st.button("🔄 清除"):
        st.session_state.history = []

# 顯示目前輸入資料
history = st.session_state.history
st.markdown(f"### 🎯 當前紀錄：{' → '.join(history) if history else '尚未輸入'}")

# AI 模型預測
LOOKBACK = 8
if st.button("🔍 預測下一局") and len(history) >= LOOKBACK + 1:
    X, y = [], []
    for i in range(LOOKBACK, len(history)):
        feature = [1 if x == 'B' else 0 for x in history[i - LOOKBACK:i]]
        label = 1 if history[i] == 'B' else 0
        X.append(feature)
        y.append(label)

    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    latest = history[-LOOKBACK:]
    latest_feature = [1 if x == 'B' else 0 for x in latest]
    prediction = model.predict([latest_feature])[0]
    prob = model.predict_proba([latest_feature])[0]

    result = "🟥 莊 (B)" if prediction == 1 else "🟦 閒 (P)"
    st.success(f"✅ 預測下一局為：**{result}**")
    st.markdown(f"📊 機率：莊 `{prob[1]:.2f}`，閒 `{prob[0]:.2f}`")

elif len(history) < LOOKBACK + 1:
    st.info(f"請至少輸入 {LOOKBACK + 1} 局資料。")
