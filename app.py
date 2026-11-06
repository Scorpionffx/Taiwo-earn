import streamlit as st
import random
import time
from datetime import datetime, date

st.set_page_config(page_title="Taiwo Earn V10 - By Taiwo David", page_icon="💰", layout="centered")

FOUNDER = "Taiwo David"
PHONE = "07036325587"
WA = "2347036325587"
EMAIL = "tshollyelectrical@gmail.com"

LINKS = {
    "hilltop": "https://hilltopads.com/?ref=YOUR_ID",
    "adsterra": "https://www.adsterra.com/?ref=YOUR_ID",
    "propeller": "https://propellerads.com/?ref=YOUR_ID",
    "monetag": "https://monetag.com/YOUR_SMARTLINK",
    "cpagrip": "https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=LOCKER",
    "palmpay": "https://palmpay.com/YOUR_REF_CODE",
    "opay_ref": "https://opay.com/YOUR_REF_CODE",
    "youtube": "https://youtube.com/@YOUR_CHANNEL",
    "telegram": "https://t.me/YOUR_GROUP",
}

# ===== SESSION =====
if 'balance' not in st.session_state:
    st.session_state.balance = 0
    st.session_state.ads_watched = 0
    st.session_state.coins = 0
    st.session_state.energy = 100
    st.session_state.is_vip = False
    st.session_state.mining = False
    st.session_state.streak = 1
    st.session_state.last_checkin = ""
    st.session_state.referrals = 0
    st.session_state.spin_used = False
    st.session_state.username = "User"
    st.session_state.level = "Level 1"

# ===== HEADER =====
st.title("💰 Taiwo Earn V10")
st.caption(f"Founder: **{FOUNDER}** | WhatsApp/OPay: **{PHONE}** | Million Apps Features - 50+ Features")
st.divider()

c1,c2,c3,c4 = st.columns(4)
c1.metric("Balance", f"₦{st.session_state.balance}")
c2.metric("Tasks", f"{st.session_state.ads_watched}/30")
c3.metric("Coins", st.session_state.coins)
c4.metric("Energy", f"{st.session_state.energy}%")
c1,c2,c3 = st.columns(3)
c1.metric("Streak 🔥", f"{st.session_state.streak} days")
c2.metric("Referrals 👥", st.session_state.referrals)
c3.metric("Level", st.session_state.level)

st.progress(min(st.session_state.ads_watched/30,1.0), text=f"Beginner Rule: {st.session_state.ads_watched}/30 Tasks - By {FOUNDER}")
if st.session_state.is_vip:
    st.success(f"👑 VIP MEMBER - N100/task - {FOUNDER}")
else:
    st.warning(f"FREE MEMBER - N10/task - Upgrade to VIP N2000 - OPay {PHONE}")
st.divider()

# ===== NEW 1: DAILY CHECK-IN - From Blum/Hamster =====
st.subheader("📅 DAILY CHECK-IN - N100 to N1000")
today = str(date.today())
if st.session_state.last_checkin != today:
    if st.button("CHECK-IN TODAY - Claim Bonus", use_container_width=True, type="primary"):
        bonus = 100 * st.session_state.streak
        st.session_state.balance += bonus
        st.session_state.last_checkin = today
        st.session_state.streak += 1
        st.balloons()
        st.success(f"Day {st.session_state.streak} Check-in! You got N{bonus}!")
else:
    st.info(f"✅ Checked in today! Come back tomorrow for N{100*st.session_state.streak}. Streak: {st.session_state.streak} days")

# ===== NEW 2: REFERRAL SYSTEM - From Pi/TapSwap (Million Maker) =====
st.divider()
st.subheader("👥 REFERRAL - N500 Per Friend - Million Maker")
st.write("Share your link, when friend joins, you earn N500. 100 friends = N50,000")
ref_name = st.text_input("Your Name for Referral Link", value="Taiwo")
st.code(f"https://taiwo-earn.streamlit.app/?ref={ref_name}", language="text")
if st.button("I INVITED 1 FRIEND - Claim N500", use_container_width=True):
    st.session_state.referrals += 1
    st.session_state.balance += 500
    st.success("N500 Referral Bonus Added! Share more!")
st.link_button("Share on WhatsApp", f"https://wa.me/?text=Join%20Taiwo%20Earn%20by%20{FOUNDER}%20Earn%20N5000%20daily%20-%20https://taiwo-earn.streamlit.app/?ref={ref_name}")

# ===== NEW 3: SPIN WHEEL - From Lucky Apps =====
st.divider()
st.subheader("🎡 SPIN WHEEL - Free Daily Spin")
if not st.session_state.spin_used:
    if st.button("SPIN NOW - Win up to N1000", use_container_width=True):
        prize = random.choice([50,100,100,200,500,1000,20,50])
        st.session_state.balance += prize
        st.session_state.ads_watched += 1
        st.session_state.spin_used = True
        st.balloons()
        st.success(f"🎉 You won N{prize}!")
else:
    st.info("Spin used today. Watch ad to spin again.")
    if st.button("Watch Ad to Spin Again", use_container_width=True):
        st.session_state.spin_used = False
        st.link_button("Watch Ad", LINKS['hilltop'])

# ===== NEW 4: LEADERBOARD - From TapSwap =====
st.divider()
st.subheader("🏆 LEADERBOARD - Top Earners")
st.table({
    "Rank": ["1 🥇","2 🥈","3 🥉","4","5"],
    "Name": [FOUNDER, "Chinedu P.H", "Amina Lagos", "Emeka", "You"],
    "Balance": ["N85,000","N52,000","N41,000","N30,000", f"N{st.session_state.balance}"]
})
st.caption("Top earner gets N5000 bonus at month end by Founder")

# ===== NEW 5: SOCIAL TASKS - From Blum/Airdrop Apps =====
st.divider()
st.subheader("📱 SOCIAL TASKS - N200 Each - Easy")
t1, t2, t3 = st.columns(3)
with t1:
    if st.button("Follow YouTube N200", use_container_width=True):
        st.link_button("YouTube", LINKS['youtube'])
        st.session_state.balance += 200
        st.session_state.ads_watched += 1
        st.success("N200 Added!")
with t2:
    if st.button("Join Telegram N200", use_container_width=True):
        st.link_button("Telegram", LINKS['telegram'])
        st.session_state.balance += 200
        st.session_state.ads_watched += 1
        st.success("N200 Added!")
with t3:
    if st.button("Share WhatsApp N200", use_container_width=True):
        st.link_button("Share", f"https://wa.me/?text=Taiwo%20Earn%20by%20{FOUNDER}")
        st.session_state.balance += 200
        st.session_state.ads_watched += 1
        st.success("N200 Added!")

# ===== NEW 6: QUIZ - From Quiz Apps =====
st.divider()
st.subheader("🧠 DAILY QUIZ - N300")
st.write("Who is Founder of Taiwo Earn?")
quiz = st.radio("Pick answer", ["Taiwo David", "Elon Musk", "Mark Zuckerberg"], key="quiz")
if st.button("Submit Quiz - Earn N300", use_container_width=True):
    if quiz == "Taiwo David":
        st.session_state.balance += 300
        st.success("Correct! N300 Added!")
    else:
        st.error("Wrong! Try again tomorrow")

# ===== NEW 7: BOOSTERS - From Hamster Kombat =====
st.divider()
st.subheader("🚀 BOOSTERS - Earn 2X Faster")
b1,b2 = st.columns(2)
with b1:
    if st.button("⚡ 2X TAP - Free Ad", use_container_width=True):
        st.session_state.energy = 100
        st.link_button("Activate 2X", LINKS['adsterra'])
        st.success("2X Activated for 1 hour!")
with b2:
    if st.button("🔋 Full Energy - N50", use_container_width=True):
        st.session_state.energy = 100
        st.success("Energy Full!")

# ===== OLD FEATURES: TAP / COMBO / CIPHER / MINING / CHEST =====
st.divider()
st.subheader("👆 TAP TO EARN - TapSwap Style")
if st.button("💰 TAP COIN - N5 per Tap", use_container_width=True):
    if st.session_state.energy > 0:
        earn = 100 if st.session_state.is_vip else 5
        st.session_state.balance += earn
        st.session_state.coins += 1
        st.session_state.energy -= 5
        st.toast(f"N{earn} earned!")
    else:
        st.warning("No Energy! Watch ad to refill")

st.divider()
st.subheader("🎯 DAILY COMBO - N500")
combo = st.multiselect("Combo Hint: Hilltop + Adsterra + Propeller", ["Hilltop","Adsterra","Propeller","AdMaven"])
if st.button("CHECK COMBO - N500", use_container_width=True):
    if set(combo) == set(["Hilltop","Adsterra","Propeller"]):
        st.session_state.balance += 500
        st.balloons()
        st.success("COMBO CORRECT! N500!")
    else:
        st.error("Wrong combo!")

st.divider()
st.subheader("🔐 DAILY CIPHER - N1000 - Code: TAIWO")
cipher = st.text_input("Enter Cipher")
if st.button("DECODE - N1000", use_container_width=True):
    if cipher.upper() == "TAIWO":
        st.session_state.balance += 1000
        st.success("Cipher Correct! N1000!")
    else:
        st.error("Wrong code!")

st.divider()
st.subheader("⛏️ MINING")
if not st.session_state.mining:
    if st.button("START MINING", use_container_width=True):
        st.session_state.mining = True
        st.success("Mining Started!")
else:
    if st.button("CLAIM MINING N50 - Watch Ad", use_container_width=True):
        st.session_state.balance += 50
        st.session_state.ads_watched += 1
        st.session_state.mining = False
        st.link_button("Claim Ad", LINKS['adsterra'])

st.divider()
st.subheader("📦 LUCKY CHEST")
ch1,ch2,ch3 = st.columns(3)
for i, col in enumerate([ch1,ch2,ch3]):
    if col.button(f"🎁 Chest {i+1}", key=f"chest{i}", use_container_width=True):
        reward = random.choice([20,50,100,500])
        st.session_state.balance += reward
        st.session_state.ads_watched += 1
        col.success(f"N{reward}!")

# ===== KING FEATURES =====
st.divider()
st.title("👑 KING FEATURES - Money Makers")
st.subheader("👑 KING 1: VIP N2000/Month")
if not st.session_state.is_vip:
    if st.button("JOIN VIP - N2000 - OPay 07036325587", type="primary", use_container_width=True):
        st.link_button("Pay VIP via WhatsApp", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%20VIP%20N2000")
else:
    st.success("👑 YOU ARE VIP!")

st.divider()
st.subheader("💰 KING 2: CPAGrip N4000 - Enter Email Only")
if st.button("UNLOCK N5000 BONUS - Enter Email", type="primary", use_container_width=True):
    st.link_button("Unlock - Email Only", LINKS['cpagrip'])
    if st.button("I ENTERED EMAIL - CLAIM N500", use_container_width=True, key="cpa"):
        st.session_state.balance += 500
        st.balloons()
        st.success("N500 Claimed! Founder earns N4000!")

st.divider()
st.subheader("💵 KING 3 NEW: PalmPay + OPay Referral - No Timewall")
st.info("Download PalmPay/OPay, I earn N1500, you earn N500!")
cr1, cr2 = st.columns(2)
with cr1:
    if st.button("DOWNLOAD PALMPAY - N500", use_container_width=True):
        st.link_button("PalmPay Link", LINKS['palmpay'])
        st.session_state.balance += 500
        st.success("N500 Added!")
with cr2:
    if st.button("DOWNLOAD OPAY - N500", use_container_width=True):
        st.link_button("OPay Link", LINKS['opay_ref'])
        st.session_state.balance += 500
        st.success("N500 Added!")

st.divider()
st.subheader("🔗 MONETAG SMARTLINK - Every Click Pays")
if st.button("CLICK SMARTLINK - N50", use_container_width=True):
    st.link_button("SmartLink", LINKS['monetag'])
    st.session_state.ads_watched += 1
    st.session_state.balance += 50

st.divider()
st.subheader("📱 KING 4: DATA VENDING - N100 Profit")
mtn = st.text_input("Phone for Data", placeholder="07036325587")
if st.button("BUY 1GB N350 - WhatsApp Founder", use_container_width=True):
    st.link_button("Buy Data", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%201GB%20N350%20to%20{mtn}")

st.divider()
st.subheader("🚀 LEVEL UP")
for lvl, price in {"Level 2 Silver N1500":1500,"Level 3 Gold N3000":3000,"Level 4 Diamond N6000":6000}.items():
    if st.button(f"UPGRADE TO {lvl}", use_container_width=True, key=lvl):
        st.link_button(f"Pay N{price} - OPay {PHONE}", f"https://wa.me/{WA}?text=I%20want%20{lvl}%20N{price}")

# ===== NEW 8: AI CHAT / SUPPORT - From Million Apps =====
st.divider()
st.subheader("🤖 ASK FOUNDER - AI Support")
q = st.text_input("Ask anything about earning", placeholder="How do I withdraw?")
if st.button("Ask Taiwo", use_container_width=True):
    st.info(f"Hi! I am {FOUNDER}. To withdraw, do 30 tasks, then enter your OPay number. For VIP, pay N2000 to OPay {PHONE} and WhatsApp me. Good luck!")

# ===== COURSE + CLONE =====
st.divider()
st.subheader("🎓 LEARN TO BUILD THIS - N15,000")
if st.button("PAY N15k TO LEARN", type="primary", use_container_width=True):
    st.link_button(f"Chat {FOUNDER}", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%20to%20learn%20N15000")
st.divider()
st.subheader("🛒 APPS FOR SALE")
c1,c2 = st.columns(2)
with c1:
    if st.button("Buy Clone - N25k", use_container_width=True):
        st.link_button("Buy Clone", f"https://wa.me/{WA}?text=I%20want%20Clone%20V10%20N25000")
with c2:
    if st.button("Custom App - N100k", use_container_width=True):
        st.link_button("Custom", f"https://wa.me/{WA}?text=I%20need%20custom%20app%20N100k")

# ===== WITHDRAW =====
st.divider()
st.subheader("💳 Withdraw")
if not st.session_state.is_vip and st.session_state.ads_watched < 30:
    st.error(f"Complete {30 - st.session_state.ads_watched} more tasks! Rule by {FOUNDER}")
else:
    st.success(f"Ready to withdraw N{st.session_state.balance}!")
    opay = st.text_input("Your OPay/PalmPay Number", placeholder="07036325587", key="wd")
    if st.button("WITHDRAW NOW", type="primary", use_container_width=True):
        st.success(f"Withdrawal to {opay} requested! {FOUNDER} will pay in 24h via OPay {PHONE}")
        st.link_button("Confirm via WhatsApp", f"https://wa.me/{WA}?text=Withdraw%20N{st.session_state.balance}%20to%20{opay}")

st.divider()
st.markdown(f"""
<center>
<b>Taiwo Earn V10 Millionaire</b><br>
Founder & CEO: <b>{FOUNDER}</b><br>
WhatsApp/OPay: <b>{PHONE}</b><br>
Email: {EMAIL}<br>
Port Harcourt, Rivers State<br>
© 2026 {FOUNDER} - 50+ Features - No Timewall
</center>
""", unsafe_allow_html=True)
