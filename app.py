import streamlit as st
import random, datetime
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="EarnNG by Taiwo David", page_icon="💰")

# --- FOUNDER ---
FOUNDER = "Taiwo David"
PAYPAL = "taiwodavid@gmail.com"  # CHANGE TO YOUR PAYPAL
PALMPAY = "08100000000"  # CHANGE TO YOUR PALMPAY
WHATSAPP = "2348100000000"  # CHANGE TO YOUR WHATSAPP

# --- YOUR 6 TASK LINKS - PASTE HERE WHEN YOU GET THEM ---
TIMEWALL = "https://timewall.io/offerwall/PUT_YOUR_ID_HERE?uid="
ADSCEND = "https://asmwall.com/adwall?hash=PUT_YOUR_HASH_HERE&uid="
BITLABS = "https://web.bitlabs.io/?uid="
PRIME = "https://primeappwall.com/wall/PUT_YOUR_ID_HERE?uid="
ADGATE = "https://wall.adgaterewards.com/PUT_YOUR_ID_HERE?uid="
CPAGRIP = "https://www.cpagrip.com/show.php?l=0&u=PUT_YOUR_ID_HERE&uid="

# --- YOUR 3 ADS LINKS - PASTE HERE WHEN YOU GET THEM ---
HILLTOP = "PUT_HILLTOP_ID"
MONETAG = "PUT_MONETAG_ID"
ADCASH = "<!-- PUT ADCASH CODE -->"

# --- AUTO POSTBACK - DO NOT TOUCH ---
params = st.query_params
if "uid" in params and "amount" in params:
    st.write("OK")
    st.stop()

# --- USER BALANCE ---
if 'uid' not in st.session_state:
    st.session_state.uid = random.randint(10000,99999)
if 'balance' not in st.session_state:
    st.session_state.balance = 0

# --- ADS SPACE ---
ad = f"<script src='https://hilltopads.net/{HILLTOP}'></script><script src='https://monetag.com/tag/{MONETAG}.js'></script><div>{ADCASH}</div>"
st_html(ad, height=1)

# --- HEADER ---
st.markdown(f"""
<div style="background:white;padding:15px;border-radius:15px;text-align:center;border-left:6px solid green;">
<b>💰 EarnNG - Founded by {FOUNDER}</b><br>
ID: {st.session_state.uid} | Balance: N{st.session_state.balance} | You 70% / User 30%<br>
PayPal: {PAYPAL} | PalmPay: {PALMPAY}
</div>
""", unsafe_allow_html=True)

# --- TASKS ---
st.write("### ✅ 6 Tasks - Earn Money")
tasks = [
    (f"🔥 TimeWall", TIMEWALL),
    (f"💼 Adscend", ADSCEND),
    (f"📝 BitLabs", BITLABS),
    (f"📱 Prime", PRIME),
    (f"🎮 AdGate", ADGATE),
    (f"✉️ CPAGrip", CPAGRIP),
]

for name, link in tasks:
    full = f"{link}{st.session_state.uid}"
    st.link_button(f"Open {name}", full, use_container_width=True)
    if st.button(f"Demo +N135 (30%) {name}", key=name):
        st.session_state.balance += 135  # 30% of $0.30 = N135 to user, you keep N315
        st.success(f"You (Taiwo) keep N315 (70%) - User gets N135 (30%)")
        st.rerun()

# --- WITHDRAW ---
st.divider()
st.write(f"### 💳 Withdraw - Min N500 to PalmPay")
st.write(f"Your Balance: N{st.session_state.balance}")

if st.session_state.balance >= 500:
    palmpay_num = st.text_input("Your PalmPay Number")
    if st.button("Withdraw to PalmPay"):
        st.success(f"Send N{st.session_state.balance} to {palmpay_num} - Founder {FOUNDER} will pay from {PALMPAY}")
        st.write(f"How {FOUNDER} gets money: PayPal {PAYPAL} -> Bybit P2P -> PalmPay {PALMPAY}")

# --- FOOTER ---
st.markdown(f"<div style='text-align:center;padding:20px;'>Founded by {FOUNDER} - 2026<br>70% {FOUNDER} / 30% User - PayPal to PalmPay</div>", unsafe_allow_html=True)
