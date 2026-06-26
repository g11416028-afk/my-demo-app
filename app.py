import streamlit as st
import difflib

# 設定網頁標題與圖示
st.set_page_config(page_title="國際處系統優化展示", page_icon="🏫")

st.title("🏫 國際處交換申請：系名智慧辨識系統")
st.markdown("### 💡 現場 Demo 版本 (純前端視覺化)")
st.write("輸入學生手填的各種不規範簡寫，系統會動態解析並與註冊組標準資料庫對齊。")
st.write("---")

# 模擬學校註冊組的官方標準資料庫
official_departments = [
    "資訊科學系/所",
    "體育學系",
    "學習與媒材設計學系",
    "英語教學系",
    "Department of Computer Science"
]

# 在網頁左側邊欄顯示對齊的資料庫，方便承辦人對照
st.sidebar.header("🗄️ 學校官方標準系所清單")
for dept in official_departments:
    st.sidebar.markdown(f"- `{dept}`")

# 核心輸入框（在 GitHub 雲端上跑，這個對話框 100% 會完美出現！）
student_input = st.text_input("請輸入或修改學生填寫的系名：", value="資科系")

if student_input:
    # 進行資料預處理（去空格、轉小寫、統一斜線格式）
    normalized_input = student_input.strip().replace(" ", "").replace("／", "/").lower()
    best_match = None
    highest_score = 0.0

    # 跑模糊比對演算法
    for official_dept in official_departments:
        normalized_official = official_dept.strip().replace(" ", "").replace("／", "/").lower()
        score = difflib.SequenceMatcher(None, normalized_input, normalized_official).ratio()
        if score > highest_score:
            highest_score = score
            best_match = official_dept

    st.write("---")
    st.subheader("🎯 系統即時分析結果：")

    # 根據相似度分數動態渲染漂亮的 UI 狀態框
    if highest_score == 1.0:
        st.success(f"**【✅ 完全匹配】** 官方標準系名：**{best_match}**")
    elif highest_score >= 0.45:
        st.warning(f"**【⚠️ 智慧導正】** 學生填寫：`{student_input}` ➔ 建議修正為：**{best_match}** (相似度：{highest_score*100:.1f}%)")
    else:
        st.error(f"**【❌ 警報】** 無法識別 `{student_input}`，資料庫無匹配系所！")
