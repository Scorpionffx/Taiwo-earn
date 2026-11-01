import streamlit as st
import random
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Taiwo-earn by Taiwo David", page_icon="💰")

FOUNDER = "Taiwo David"
PAYPAL = "taiwodavid@gmail.com"
PALMPAY = "08100000000"
WHATSAPP = "2348100000000"

TIMEWALL = "https://timewall.io/offerwall/PUT_YOUR_ID?uid="
ADSCEND = "https://asmwall.com/adwall?hash=PUT_HASH?uid="
BITLABS = "https://web.bitlabs.io/?uid="
PRIME = "https://primeappwall.com/wall/PUT_ID?uid="
ADGATE = "https://wall.adgaterewards.com/PUT_ID?uid="
CPAGRIP = "https://www.cpagrip.com/show.php?l=0&u=PUT_ID&uid="

HILLTOP = "PUT_HILLTOP_ID"
MONETAG = "PUT_MONETAG_ID"
ADCASH = ""

params = st.query_params
if "uid" in params and "amount" in params:
    st.write("OK")
    st.stop()

if 'uid' not in st.session_state:
    st.session_state.uid = random.randint(10000,99999)
if 'balance' not in st.session_state:
    st.session_state.balance = 0

ad = f"<script src='https://hilltopads.net/{HILLTOP}'></script><script src='https://monetag.com/tag/{MONETAG}.js'></script><div>{ADCASH}</div>"
st_html(ad, height=1)

# FIXED - BLACK TEXT - NOT WHITE
st.markdown(f"""
<div style="background:white;padding:15px;border-radius:15px;text-align:center;border-left:6px solid green;color:black !important;">
<b style="color:black;">💰 Taiwo-earn - Founded by {FOUNDER}</b><br>
<span style="color:black;">ID: {st.session_state.uid} | Balance: N{st.session_state.balance}</span><br>
<span style="color:black;">70% Founder / 30% You - PayPal to PalmPay</span><br>
<span style="color:black;">PayPal: {PAYPAL}</span>
</div>
""", unsafe_allow_html=True)

st.write("### ✅ 6 Tasks - Earn Money")

tasks = [("🔥 TimeWall", TIMEWALL), ("💼 Adscend", ADSCEND), ("📝 BitLabs", BITLABS), ("📱 Prime", PRIME), ("🎮 AdGate", ADGATE), ("✉️ CPAGrip", CPAGRIP)]

for name, link in tasks:
    full = f"{link}{st.session_state.uid}"
    st.link_button(f"Open {name}", full, use_container_width=True)
    if st.button(f"Demo +N135 (30%) {name}", key=name):
        st.session_state.balance += 135
        st.success(f"You +N135 (30%) - Founder {FOUNDER} keeps N315 (70%)")
        st.rerun()

st.divider()
st.write(f"### 💳 Withdraw Min N500 - Balance N{st.session_state.balance}")
if st.session_state.balance >= 500:
    num = st.text_input("Your PalmPay Number")
    if st.button("Withdraw to PalmPay"):
        st.success(f"Request sent - {FOUNDER} will pay {num} from {PALMPAY}")
else:
    st.info(f"Need N{500-st.session_state.balance} more to withdraw")

st.markdown(f"<div style='text-align:center;padding:20px;color:black;background:white;border-radius:10px;margin-top:20px;'><b style='color:black;'>Founded by {FOUNDER} - Taiwo-earn</b><br><span style='color:black;'>© 2026 {FOUNDER} - 70/30 PayPal to PalmPay</span></div>", unsafe_allow_html=True)
