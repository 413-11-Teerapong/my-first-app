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
    </style>
    """,
    unsafe_allow_html=True,
)

TIME_LIMIT = 60  # เวลาทั้งหมดสำหรับ 10 ข้อ (วินาที) ปรับได้

# ============================================================
# ข้อมูลประเทศ แบ่งตามภูมิภาค (รวม 10 ประเทศ)
# ============================================================
COUNTRIES = [
    {"name": "Denmark",  "th": "เดนมาร์ก",  "region": "นอร์ดิก",              "flag": "🇩🇰"},
    {"name": "Sweden",   "th": "สวีเดน",     "region": "นอร์ดิก",              "flag": "🇸🇪"},
    {"name": "Poland",   "th": "โปแลนด์",    "region": "ตะวันออก",             "flag": "🇵🇱"},
    {"name": "Russia",   "th": "รัสเซีย",    "region": "ตะวันออก",             "flag": "🇷🇺"},
    {"name": "Ukraine",  "th": "ยูเครน",     "region": "ตะวันออก",             "flag": "🇺🇦"},
    {"name": "Greece",   "th": "กรีซ",       "region": "ตะวันออกเฉียงใต้",     "flag": "🇬🇷"},
    {"name": "Bulgaria", "th": "บัลแกเรีย",  "region": "ตะวันออกเฉียงใต้",     "flag": "🇧🇬"},
    {"name": "France",   "th": "ฝรั่งเศส",   "region": "ตะวันตก",              "flag": "🇫🇷"},
    {"name": "Germany",  "th": "เยอรมัน",    "region": "ตะวันตก",              "flag": "🇩🇪"},
    {"name": "Italy",    "th": "อิตาลี",     "region": "ใต้",                  "flag": "🇮🇹"},
]
N = len(COUNTRIES)


def blank_word(word: str) -> str:
    """เว้นตัวอักษรตรงกลางเป็น _ เก็บตัวแรก-ตัวสุดท้ายไว้ เช่น Denmark -> D _ _ _ _ _ k"""
    if len(word) <= 2:
        return " ".join(list(word))
    chars = list(word)
    for i in range(1, len(chars) - 1):
        chars[i] = "_"
    return " ".join(chars)


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


# ------------------------------------------------------------
# กล่องแสดงผลลัพธ์ (Dialog)
# ------------------------------------------------------------
@st.dialog("🏆 สรุปผลการแข่งขัน")
def show_result_dialog():
    score = 0
    details = []
    for idx in st.session_state.order:
        country = COUNTRIES[idx]
        user_ans = st.session_state[f"ans{idx}_val"].strip().lower()
        correct_ans = country["name"].lower()
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
    st.divider()

    for country, user_ans, is_correct in details:
        icon = "✅" if is_correct else "❌"
        st.write(
            f"{icon} {country['flag']} **{country['name']}** "
            f"({country['th']} - {country['region']}) "
            f"— คุณตอบ: '{user_ans if user_ans else '(ว่าง)'}'"
        )

    if st.button("🔄 เล่นรอบใหม่"):
        reset_game()
        st.rerun()


# ============================================================
# UI หลัก
# ============================================================
st.title("🌍 เกมทายประเทศในยุโรป (จับเวลา)")
st.caption("เดา ชื่อประเทศ (ภาษาอังกฤษ) จากตัวอักษรที่ให้มา แบ่งตามภูมิภาคของยุโรป")

st.button("🚀 เริ่มเล่นเกม", on_click=reset_game)

# ------------------------------------------------------------
# แถบจับเวลานับถอยหลัง
# ------------------------------------------------------------
if "start" in st.session_state and not st.session_state.get("is_ended", False):
    time_left = int(TIME_LIMIT - (time.time() - st.session_state.start))

    if time_left > 0:
        st.error(f"⏳ เหลือเวลา: {time_left} วินาที")
    else:
        st.session_state.is_ended = True
        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # ช่องรับคำตอบ เรียงตามลำดับที่สุ่มไว้ (order)
    # --------------------------------------------------------
    for n, idx in enumerate(st.session_state.order, start=1):
        country = COUNTRIES[idx]
        hint = blank_word(country["name"])
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
st.write("นักเรียน: __________________ เลขที่ ____ ชั้น ______")
