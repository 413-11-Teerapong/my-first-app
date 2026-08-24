import time
import streamlit as st

st.set_page_config(page_title="เกมทายศัพท์จับเวลา", page_icon="⏱️")
st.title("⏱️ เกมทายศัพท์จับเวลา")

# ---------------------------------------------------------
# 1. กำหนดค่าเริ่มต้นใน session_state ถ้ายังไม่มี
# ---------------------------------------------------------
if "ans1_val" not in st.session_state:
    st.session_state.ans1_val = ""
if "ans2_val" not in st.session_state:
    st.session_state.ans2_val = ""
if "ans3_val" not in st.session_state:
    st.session_state.ans3_val = ""
if "ans4_val" not in st.session_state:
    st.session_state.ans4_val = ""
if "start" not in st.session_state:
    st.session_state.start = time.time()
if "is_ended" not in st.session_state:
    st.session_state.is_ended = False


# ---------------------------------------------------------
# ฟังก์ชันเคลียร์ค่าเมื่อกดปุ่มเริ่มใหม่
# ---------------------------------------------------------
def reset_game():
    st.session_state.ans1_val = ""     # เคลียร์ค่าช่องข้อ 1
    st.session_state.ans2_val = ""     # เคลียร์ค่าช่องข้อ 2
    st.session_state.ans3_val = ""     # เคลียร์ค่าช่องข้อ 3
    st.session_state.ans4_val = ""     # เคลียร์ค่าช่องข้อ 4
    st.session_state.start = time.time()  # เริ่มเวลาใหม่
    st.session_state.is_ended = False  # ปิด Dialog


# ---------------------------------------------------------
# ฟังก์ชัน MessageBox (Dialog) แสดงผลสรุป
# ---------------------------------------------------------
@st.dialog("สรุปผลการเล่นเกม")
def show_result_dialog(ans1, ans2, ans3, ans4, elapsed):
    st.balloons()
    score = 0
    u_ans1 = ans1.strip().lower()
    u_ans2 = ans2.strip().lower()
    u_ans3 = ans3.strip().lower()
    u_ans4 = ans4.strip().lower()

    # ตรวจข้อ 1
    if u_ans1 == "apple":
        st.success("ข้อ 1: ถูกต้อง")
        score += 1
    else:
        st.error(f"ข้อ 1: ยังไม่ถูกต้อง (คุณตอบ '{u_ans1}')")

    # ตรวจข้อ 2
    if u_ans2 == "fish":
        st.success("ข้อ 2: ถูกต้อง")
        score += 1
    else:
        st.error(f"ข้อ 2: ยังไม่ถูกต้อง (คุณตอบ '{u_ans2}')")

    # ตรวจข้อ 3
    if u_ans3 == "dog":
        st.success("ข้อ 3: ถูกต้อง")
        score += 1
    else:
        st.error(f"ข้อ 3: ยังไม่ถูกต้อง (คุณตอบ '{u_ans3}')")

    # ตรวจข้อ 4
    if u_ans4 == "bird":
        st.success("ข้อ 4: ถูกต้อง")
        score += 1
    else:
        st.error(f"ข้อ 4: ยังไม่ถูกต้อง (คุณตอบ '{u_ans4}')")

    st.info(f"คุณได้คะแนนรวม {score} / 4 คะแนน")
    st.caption(f"ใช้เวลาไปทั้งหมด {elapsed:.1f} วินาที")

    if st.button("เริ่มเล่นใหม่", use_container_width=True):
        reset_game()
        st.rerun()


# ---------------------------------------------------------
# หน้าเกมหลัก
# ---------------------------------------------------------
st.write("แปลคำศัพท์ภาษาอังกฤษต่อไปนี้เป็นภาษาไทย แล้วกด **ส่งคำตอบ** ก่อนเวลาหมด")

elapsed_now = time.time() - st.session_state.start
st.metric("เวลาที่ผ่านไป (วินาที)", f"{elapsed_now:.1f}")

with st.form("quiz_form"):
    ans1 = st.text_input("1. Apple = ?", key="ans1_val")
    ans2 = st.text_input("2. Fish = ?", key="ans2_val")
    ans3 = st.text_input("3. Dog = ?", key="ans3_val")
    ans4 = st.text_input("4. Bird = ?", key="ans4_val")
    submitted = st.form_submit_button("ส่งคำตอบ")

if submitted:
    st.session_state.is_ended = True
    total_time = time.time() - st.session_state.start
    show_result_dialog(ans1, ans2, ans3, ans4, total_time)

st.divider()
if st.button("🔄 เริ่มเกมใหม่"):
    reset_game()
    st.rerun()

# 5. แสดง Dialog ผลลัพธ์
if st.session_state.get("is_ended", False):
    show_result_dialog(ans1, ans2)

st.divider()
st.write("นายธีรพงษ์ วิลัยศรี เลขที่ 11 ม.4/13")
