import streamlit as st, json, os, random, time
from datetime import datetime

# --- YOUR LINKS ---
LINK_A = "YOUR_MONETAG_LINK"
LINK_B = "YOUR_ADSTERRA_LINK"
LINK_C = "YOUR_MONETAG_SPIN_LINK"
ADSCEND_ID = "YOUR_ADSCEND_ID"
BITLABS_ID = "YOUR_BITLABS_ID"
LOOTABLY_ID = "YOUR_LOOTABLY_ID"
PUSH_LINK = "YOUR_MONETAG_PUSH_LINK"
TELEGRAM_LINK = "https://t.me/YOUR_CHANNEL"
REWARD = 150
ADMIN_PASS = "taiwo123" # Change this!

st.set_page_config(page_title="Taiwo-Earn Unlimited", page_icon="💸")

# --- FOREVER DB ---
DB_FILE = "leaderboard.json"
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}
def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

db = load_db()

if "user" not in st.session_state:
    st.session_state.user = f"User_{random.randint(1000,9999)}"
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "ads" not in st.session_state:
    st.session_state.ads = 0
if "tasks" not in st.session_state:
    st.session_state.tasks = 0
if "spins" not in st.session_state:
    st.session_state.spins = 0

# --- CHECK IF ADMIN ---
query_params = st.query_params
is_admin = query_params.get("admin", "") == "1"

if is_admin:
    st.title("🔐 ADMIN DASHBOARD - Taiwo")
    pwd = st.text_input("Admin Password", type="password")
    if pwd == ADMIN_PASS:
        st.success("Welcome Admin!")
        total_users = len(db)
        total_tasks_all = sum([v.get('total',0) for v in db.values()])
        estimated_profit = total_tasks_all * 450
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Users", total_users)
        c2.metric("Total Tasks+Ads", total_tasks_all)
        c3.metric("Your Profit", f"N{estimated_profit}")
        c4.metric("Phone Goal", f"N{estimated_profit}/N150k")
        
        st.progress(min(estimated_profit/150000, 1.0))
        if estimated_profit >= 150000:
            st.balloons()
            st.success("🎉 YOU CAN BUY YOUR PHONE! N150k REACHED!")
        
        st.subheader("All Users Forever Stats")
        st.json(db)
        
        if st.button("Delete Fake User"):
            user_del = st.selectbox("Select user to delete", list(db.keys()))
            if st.button(f"Confirm Delete {user_del}"):
                del db[user_del]
                save_db(db)
                st.success("Deleted!")
                st.rerun()
    else:
        st.warning("Enter password")
    st.stop()

# --- NORMAL USER VIEW ---
st.title("💸 Taiwo-Earn UNLIMITED")
st.caption(f"Goal: Help Taiwo buy new phone N150k | Earn N{REWARD} per task UNLIMITED")

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Balance", f"N{st.session_state.balance}")
c2.metric("📺 Ads", st.session_state.ads)
c3.metric("📋 Tasks", st.session_state.tasks)
c4.metric("Total", st.session_state.ads + st.session_state.tasks)

ref = query_params.get("ref", None)
username_input = st.text_input("Create username to save forever", value=st.session_state.user)
if username_input:
    st.session_state.user = username_input
    your_link = f"https://YOUR-APP-NAME.streamlit.app/?ref={username_input}"
    st.code(your_link)
    if ref:
        st.info(f"Invited by {ref} - Both get bonus after 1st task")

def unlimited_task(name, link, type_name):
    st.link_button(f"Open {name} 🔥", link)
    if st.button(f"Claim N{REWARD} - {name}", key=f"{name}_{st.session_state.ads}_{st.session_state.tasks}_{random.randint(1,9999999)}"):
        st.session_state.balance += REWARD
        if type_name == "ads":
            st.session_state.ads += 1
        else:
            st.session_state.tasks += 1
        
        db[st.session_state.user] = {
            "balance": st.session_state.balance,
            "ads": st.session_state.ads,
            "tasks": st.session_state.tasks,
            "spins": st.session_state.spins,
            "total": st.session_state.ads + st.session_state.tasks,
            "last_seen": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "ref": ref
        }
        save_db(db)
        st.balloons()
        st.success(f"N{REWARD} Added! Total Actions: {st.session_state.ads + st.session_state.tasks}")
        time.sleep(0.3)
        st.rerun()

col1, col2 = st.columns(2)
with col1:
    unlimited_task("Watch Ad A", LINK_A, "ads")
with col2:
    unlimited_task("Watch Ad B", LINK_B, "ads")

st.divider()
st.subheader(f"📋 Unlimited Tasks - N{REWARD} Each")
unlimited_task("Adscend Unlimited", f"https://adscendmedia.com/{ADSCEND_ID}", "tasks")
unlimited_task("BitLabs Unlimited", f"https://bitlabs.io/{BITLABS_ID}", "tasks")
unlimited_task("Lootably Unlimited", f"https://lootably.com/{LOOTABLY_ID}", "tasks")

st.divider()
st.subheader("🎰 Daily Spin + Push")
st.link_button("Spin Now (Ad)", LINK_C)
if st.button("Claim Spin N50-N500"):
    win = random.choice([50, 100, 150, 300, 500])
    st.session_state.balance += win
    st.session_state.spins += 1
    st.success(f"Won N{win}! Spins: {st.session_state.spins}")

st.link_button("Enable Push - Bonus N100", PUSH_LINK)
if st.button("I Enabled Push (+N100)"):
    st.session_state.balance += 100
    st.success("N100 Added!")

st.link_button("Join Telegram - Bonus N200", TELEGRAM_LINK)
if st.button("I Joined (+N200)"):
    st.session_state.balance += 200
    st.success("N200 Added!")

# Leaderboard
st.divider()
st.subheader("🏆 Forever Leaderboard")
if db:
    sorted_users = sorted(db.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
    st.table([{"Rank": f"#{i}", "User": n, "Ads": d.get("ads",0), "Tasks": d.get("tasks",0), "Total": d.get("total",0)} for i,(n,d) in enumerate(sorted_users,1)])
else:
    st.info("Be first!")

if st.button("💸 Withdraw Min N2000"):
    if st.session_state.balance >= 2000:
        st.success(f"N{st.session_state.balance} Withdrawal Sent!")
    else:
        st.warning(f"Need N2000, you have N{st.session_state.balance}")

st.caption("Admin? Add ?admin=1 to your link - Example: YOUR-APP-NAME.streamlit.app/?admin=1")
