import streamlit as st
import pandas as pd
import difflib

st.set_page_config(page_title="國際處系統優化展示", page_icon="🏫", layout="wide")

st.title("🏫 國際處交換申請：系名智慧批次辨識系統")
st.markdown("### 💡 現場 Demo 版本 (支援 Excel 檔案拖曳上傳)")
st.write("您可以手動輸入測試，或是直接把整份學生申請的 Excel 檔案拉進來批次處理！")
st.write("---")

# 模擬學校註冊組的官方標準資料庫
official_departments = [
    "資訊科學系/所",
    "體育學系",
    "學習與媒材設計學系",
    "英語教學系",
    "Department of Computer Science"
]

st.sidebar.header("🗄️ 學校官方標準系所清單")
for dept in official_departments:
    st.sidebar.markdown(f"- `{dept}`")

# 模糊比對核心函式
def get_best_match(user_input):
    if not user_input or pd.isna(user_input):
        return "無法識別", 0.0
    normalized_input = str(user_input).strip().replace(" ", "").replace("／", "/").lower()
    best_match = None
    highest_score = 0.0
    for official_dept in official_departments:
        normalized_official = official_dept.strip().replace(" ", "").replace("／", "/").lower()
        score = difflib.SequenceMatcher(None, normalized_input, normalized_official).ratio()
        if score > highest_score:
            highest_score = score
            best_match = official_dept
    return best_match, highest_score

# 區塊一：手動測試
st.subheader("✍️ 模式一：單筆手動測試")
student_input = st.text_input("請輸入學生手填的系名進行測試：", value="資科系")
if student_input:
    match, score = get_best_match(student_input)
    if score == 1.0:
        st.success(f"**【✅ 完全匹配】** 官方標準系名：**{match}**")
    elif score >= 0.45:
        st.warning(f"**【⚠️ 智慧導正】** 建議修正為：**{match}** (相似度：{score*100:.1f}%)")
    else:
        st.error(f"**【❌ 警報】** 無法識別，資料庫無匹配系所！")

st.write("---")

# 區塊二：這就是你要的 Excel 上傳區！
st.subheader("📊 模式二：Excel 批次上傳對齊")
uploaded_file = st.file_uploader("請將您的學生申請 Excel 檔 (.xlsx) 拖曳至此處或點擊上傳", type=["xlsx"])

if uploaded_file is not None:
    try:
        # 讀取使用者上傳的 Excel
        df = pd.read_excel(uploaded_file)
        st.info("📂 成功偵測到上傳檔案！原始資料如下：")
        st.dataframe(df) # 顯示原本的髒資料
        
        # 找尋包含「校名」或「系名」的欄位進行自動比對
        target_col = None
        for col in df.columns:
            if "校名" in str(col) or "系名" in str(col) or "院系" in str(col):
                target_col = col
                break
        
        if target_col:
            st.write(f"🤖 系統已自動鎖定比對欄位：`{target_col}`，正在進行智慧對齊...")
            
            # 跑批次比對演算法
            matches = []
            scores = []
            for val in df[target_col]:
                m, s = get_best_match(val)
                matches.append(m)
                scores.append(f"{s*100:.1f}%")
            
            # 將結果塞回 DataFrame
            df["系統智慧導正結果"] = matches
            df["信心指數 (相似度)"] = scores
            
            st.success("✨ 批次智慧對齊完成！處理後的報表如下：")
            st.dataframe(df) # 顯示對齊後的完美表格
            st.balloons() # 噴出慶祝氣球
        else:
            st.error("❌ 在您的 Excel 欄位名稱中找不到包含「校名」或「系名」的欄位，請檢查檔案！")
    except Exception as e:
        st.error(f"讀取檔案時發生錯誤: {e}")
