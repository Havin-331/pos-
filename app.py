import streamlit as st
from menu_data import DRINK_MENU, generate_drink_report

# 1. 網頁基本設定
st.set_page_config(page_title="手搖飲料點餐系統", page_icon="🥤", layout="centered")

st.title("🥤 手搖飲料智慧點餐系統")

# 2. 初始化 Session State（用來在網頁重新整理時記住購物車資料）
if "cart" not in st.session_state:
    st.session_state.cart = []

# 3. 建立網頁上的分頁（對應原本終端機的 1.開始點餐 2.查看歷史報表）
tab1, tab2 = st.tabs(["🥤 開始點餐", "📜 查看歷史報表"])

# ==================== 分頁一：開始點餐 ====================
with tab1:
    st.subheader("--- 本店菜單 ---")
    
    # 顯示漂亮的菜單表格或列表
    drink_list = list(DRINK_MENU.keys())
    
    # 讓使用者選擇飲料
    selected_drink = st.selectbox("請選擇想喝的飲料品項：", drink_list, key="drink_select")
    current_price = DRINK_MENU[selected_drink]
    st.info(f"💡 **{selected_drink}** 單價：**{current_price} 元**")

    # 數量選擇
    quantity = st.number_input("請輸入數量：", min_value=1, value=1, step=1, key="qty_input")

    # 加入購物車按鈕
    if st.button("🛒 加入購物車", type="primary"):
        subtotal = current_price * quantity
        st.session_state.cart.append((selected_drink, subtotal))
        st.success(f"已成功加入：{selected_drink} x {quantity} (小計 {subtotal} 元)")

    st.markdown("---")
    st.subheader("🛒 目前點餐清單")

    # 如果購物車有東西
    if st.session_state.cart:
        total_amount = 0
        
        # 顯示清單並提供刪除功能
        for i, (drink, subtotal) in enumerate(st.session_state.cart):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{i + 1}. {drink}**")
            with col2:
                st.write(f"小計: {subtotal} 元")
            with col3:
                # 刪除特定品項按鈕
                if st.button("❌ 刪除", key=f"del_{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun() # 重新整理畫面更新購物車
            total_amount += subtotal

        st.markdown(f"### 💰 目前總金額：**{total_amount} 元**")

        # 確認結帳按鈕
        if st.button("✅ 確認結帳並儲存報表"):
            # 呼叫你原本寫好的報表生成函式
            report = generate_drink_report(st.session_state.cart, DRINK_MENU)
            
            # 寫入 sales_report.txt (追加模式 "a")
            with open("sales_report.txt", "a", encoding="utf-8") as f:
                f.write(report + "\n" + "-" * 30 + "\n")
            
            st.success("🎉 訂單已成立！銷售報表已成功寫入 sales_report.txt。")
            
            # 清空購物車
            st.session_state.cart = []
            st.rerun()
    else:
        st.write("目前購物車是空的，快去點幾杯好喝的飲料吧！")

# ==================== 分頁二：查看歷史報表 ====================
with tab2:
    st.subheader("=== 📜 歷史銷售總帳本 ===")
    
    if st.button("🔄 重新整理帳本"):
        st.rerun()

    try:
        with open("sales_report.txt", "r", encoding="utf-8") as file:
            history_content = file.read()
            st.text_area("銷售紀錄內容", history_content, height=400)
    except FileNotFoundError:
        st.warning("⚠️ 目前還沒有任何歷史銷售紀錄喔！趕快去結帳一筆訂單吧！")