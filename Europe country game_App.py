import time
import random
import streamlit as st

# ============================================================
# ตั้งค่าหน้าเว็บ
# ============================================================
st.set_page_config(page_title="🌍 เกมทายประเทศยุโรป", page_icon="🌍", layout="centered")

# ------------------------------------------------------------
# พื้นหลัง / สไตล์ (ปรับเปลี่ยนได้ตามใจชอบ)
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
    }
    div[data-testid="stTextInput"] input {
        background-color: #ffffff;
        border-radius: 8px;
    }
    .region-badge {
        display:inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        background-color: #ffd166;
        color: #1e3c72;
        font-weight: bold;
        font-size: 0.8em;
        margin-right: 6px;
    }
    .timer-box {
        background-color: #06d6a0;
        color: #1e3c72;
        font-weight: bold;
        font-size: 1.1em;
        padding: 8px 16px;
        border-radius: 10px;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# ข้อมูลประเทศ แบ่งตามภูมิภาค (รวม 10 ประเทศ) — คำตอบเป็นภาษาไทย
# ============================================================
COUNTRIES = [
    {"th": "เดนมาร์ก",  "region": "นอร์ดิก",              "flag": "🇩🇰"},
    {"th": "สวีเดน",     "region": "นอร์ดิก",              "flag": "🇸🇪"},
    {"th": "โปแลนด์",    "region": "ตะวันออก",             "flag": "🇵🇱"},
    {"th": "รัสเซีย",    "region": "ตะวันออก",             "flag": "🇷🇺"},
    {"th": "ยูเครน",     "region": "ตะวันออก",             "flag": "🇺🇦"},
    {"th": "กรีซ",       "region": "ตะวันออกเฉียงใต้",     "flag": "🇬🇷"},
    {"th": "บัลแกเรีย",  "region": "ตะวันออกเฉียงใต้",     "flag": "🇧🇬"},
    {"th": "ฝรั่งเศส",   "region": "ตะวันตก",              "flag": "🇫🇷"},
    {"th": "เยอรมัน",    "region": "ตะวันตก",              "flag": "🇩🇪"},
    {"th": "อิตาลี",     "region": "ใต้",                  "flag": "🇮🇹"},
]
N = len(COUNTRIES)


def blank_word(word: str) -> str:
    """เว้นตัวอักษรตรงกลางเป็น _ เก็บตัวแรก-ตัวสุดท้ายไว้ เช่น เดนมาร์ก -> เ _ _ _ _ ร์ก"""
    if len(word) <= 2:
        return " ".join(list(word))
    chars = list(word)
    for i in range(1, len(chars) - 1):
        chars[i] = "_"
    return " ".join(chars)


def format_time(seconds: float) -> str:
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


# ============================================================
# ตั้งค่าค่าเริ่มต้นใน session_state
# ============================================================
if "order" not in st.session_state:
    st.session_state.order = list(range(N))
    random.shuffle(st.session_state.order)

if "prev_order" not in st.session_state:
    st.session_state.prev_order = None

for i in range(N):
    key = f"ans{i}_val"
    if key not in st.session_state:
        st.session_state[key] = ""

if "is_ended" not in st.session_state:
    st.session_state.is_ended = False

if "final_time" not in st.session_state:
    st.session_state.final_time = 0


def new_shuffled_order():
    """สุ่มลำดับข้อใหม่ ห้ามซ้ำกับลำดับของรอบที่แล้ว"""
    new_order = list(range(N))
    while True:
        random.shuffle(new_order)
        if new_order != st.session_state.prev_order:
            return new_order


def reset_game():
    st.session_state.prev_order = st.session_state.order[:]
    st.session_state.order = new_shuffled_order()
    for i in range(N):
        st.session_state[f"ans{i}_val"] = ""
    st.session_state.start = time.time()
    st.session_state.is_ended = False
    st.session_state.final_time = 0


# ------------------------------------------------------------
# กล่องแสดงผลลัพธ์ (Dialog)
# ------------------------------------------------------------
@st.dialog("🏆 สรุปผลการแข่งขัน")
def show_result_dialog():
    score = 0
    details = []
    for idx in st.session_state.order:
        country = COUNTRIES[idx]
        user_ans = st.session_state[f"ans{idx}_val"].strip()
        correct_ans = country["th"]
        is_correct = user_ans == correct_ans
        if is_correct:
            score += 1
        details.append((country, user_ans, is_correct))

    if score == N:
        st.balloons()
        st.success("🎉 เก่งมาก! ตอบถูกครบทุกข้อ!")
    elif score == 0:
        st.error("💀 เสียใจด้วย ตอบผิดหมดเลย ลองใหม่อีกครั้งนะ!")
    else:
        st.info("👍 ทำได้ดี ลองอีกครั้งเพื่อคะแนนเต็ม!")

    st.write(f"### ✅ ได้คะแนนรวม: {score} / {N} คะแนน")
    st.write(f"### ⏱️ เวลาที่ใช้: {format_time(st.session_state.final_time)} นาที")
    st.divider()

    for country, user_ans, is_correct in details:
        icon = "✅" if is_correct else "❌"
        st.write(
            f"{icon} {country['flag']} **{country['th']}** "
            f"({country['region']}) "
            f"— คุณตอบ: '{user_ans if user_ans else '(ว่าง)'}'"
        )

    if st.button("🔄 เล่นรอบใหม่"):
        reset_game()
        st.rerun()


# ============================================================
# UI หลัก
# ============================================================
st.title("🌍 เกมทายประเทศในยุโรป")
st.caption("เดา ชื่อประเทศ (ภาษาไทย) จากตัวอักษรที่ให้มา แบ่งตามภูมิภาคของยุโรป — จับเวลาว่าทำได้เร็วแค่ไหน")

st.button("🚀 เริ่มเล่นเกม", on_click=reset_game)

# ------------------------------------------------------------
# แถบจับเวลานับขึ้น (ไม่มีการนับถอยหลัง)
# ------------------------------------------------------------
if "start" in st.session_state and not st.session_state.get("is_ended", False):
    elapsed = time.time() - st.session_state.start
    st.markdown(
        f"<span class='timer-box'>⏱️ เวลาที่ใช้ไป: {format_time(elapsed)}</span>",
        unsafe_allow_html=True,
    )

    st.divider()

    # --------------------------------------------------------
    # ช่องรับคำตอบ เรียงตามลำดับที่สุ่มไว้ (order)
    # --------------------------------------------------------
    for n, idx in enumerate(st.session_state.order, start=1):
        country = COUNTRIES[idx]
        hint = blank_word(country["th"])
        st.markdown(
            f"<span class='region-badge'>{country['region']}</span>"
            f"ข้อ {n}: {country['flag']} **{hint}**",
            unsafe_allow_html=True,
        )
        ans = st.text_input(
            f"คำตอบข้อ {n}",
            value=st.session_state[f"ans{idx}_val"],
            key=f"input_{idx}",
            label_visibility="collapsed",
        )
        st.session_state[f"ans{idx}_val"] = ans
        st.write("")

    # --------------------------------------------------------
    # ปุ่มส่งคำตอบ
    # --------------------------------------------------------
    if st.button("📨 ส่งคำตอบ"):
        st.session_state.final_time = time.time() - st.session_state.start
        st.session_state.is_ended = True
        st.rerun()

    time.sleep(1)
    st.rerun()

# ------------------------------------------------------------
# แสดง Dialog ผลลัพธ์เมื่อจบเกม
# ------------------------------------------------------------
if st.session_state.get("is_ended", False):
    show_result_dialog()

st.divider()
st.write("นักเรียน: นายธีรพงษ์  วิลัยศรี เลขที่   11   ชั้น  4/13 ")
