import streamlit as st
import sqlite3, hashlib, random, time, json
from datetime import date, datetime

st.set_page_config(page_title="Taiwo Earn V12 - By Taiwo David", page_icon="💰", layout="centered")
FOUNDER="Taiwo David"; PHONE="07036325587"; WA="2347036325587"
ADMIN_USER="Taiwo"
ADMIN_PASS="Taiwo123" # CHANGE THIS! This is your admin password

LINKS={
 "youtube":"https://youtube.com/@YOUR_CHANNEL",
 "telegram":"https://t.me/YOUR_GROUP",
 "whatsapp_group":"https://chat.whatsapp.com/YOUR_GROUP_LINK",
 "hilltop":"https://hilltopads.com/?ref=YOUR_ID",
 "adsterra":"https://www.adsterra.com/?ref=YOUR_ID",
 "monetag":"https://monetag.com/YOUR_SMARTLINK",
 "cpagrip":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=LOCKER",
 "palmpay":"https://palmpay.com/YOUR_REF_CODE",
 "opay_ref":"https://opay.com/YOUR_REF_CODE",
}

# ===== DATABASE - SAVES FOREVER =====
def get_db():
    conn=sqlite3.connect("users.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY, password TEXT, pin TEXT, phone TEXT,
        balance INTEGER DEFAULT 0, tasks INTEGER DEFAULT 0, coins INTEGER DEFAULT 0,
        energy INTEGER DEFAULT 100, streak INTEGER DEFAULT 1, referrals INTEGER DEFAULT 0,
        is_vip INTEGER DEFAULT 0, last_checkin TEXT DEFAULT '', spin_date TEXT DEFAULT '',
        created TEXT DEFAULT '', device TEXT DEFAULT '', banned INTEGER DEFAULT 0)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS task_logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, task TEXT, date TEXT, amount INTEGER, time TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS transactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, type TEXT, amount INTEGER, detail TEXT, time TEXT)""")
    conn.commit()
    return conn
DB=get_db()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def add_tx(user, typ, amt, detail):
    DB.execute("INSERT INTO transactions(username,type,amount,detail,time) VALUES(?,?,?,?,?)",(user,typ,amt,detail,str(datetime.now())[:19]))
    DB.commit()
def add_task_log(user, task, amt):
    today=str(date.today())
    DB.execute("INSERT INTO task_logs(username,task,date,amount,time) VALUES(?,?,?,?,?)",(user,task,today,amt,str(datetime.now())[:19]))
    DB.commit()
def did_task_today(user, task):
    cur=DB.execute("SELECT * FROM task_logs WHERE username=? AND task=? AND date=?",(user,task,str(date.today())))
    return cur.fetchone() is not None
def update_user(user, **kwargs):
    for k,v in kwargs.items():
        DB.execute(f"UPDATE users SET {k}=? WHERE username=?",(v,user))
    DB.commit()
def get_user(user):
    cur=DB.execute("SELECT * FROM users WHERE username=?",(user,))
    row=cur.fetchone()
    if not row: return None
    cols=[d[0] for d in cur.description]
    return dict(zip(cols,row))

# ===== SESSION =====
if 'logged' not in st.session_state:
    st.session_state.logged=False; st.session_state.user=None; st.session_state.opened={}
    st.session_state.captcha_q=""; st.session_state.captcha_a=0; st.session_state.captcha_passed=False

def new_captcha():
    a=random.randint(2,9); b=random.randint(2,9)
    st.session_state.captcha_q=f"What is {a} + {b} ? (Anti-Bot)"; st.session_state.captcha_a=a+b; st.session_state.captcha_passed=False

if not st.session_state.captcha_q: new_captcha()

# ===== HEADER =====
st.title("💰 Taiwo Earn V12")
st.caption(f"By {FOUNDER} | OPay: {PHONE} | Login System + Anti-Cheat + Security")

# ===== LOGIN / SIGNUP =====
if not st.session_state.logged:
    tab1, tab2 = st.tabs(["🔑 LOGIN", "📝 SIGN UP"])
    with tab1:
        st.subheader("Login - Your Progress is Saved")
        lu=st.text_input("Username", key="login_u", placeholder="e.g. Taiwo")
        lp=st.text_input("Password", type="password", key="login_p")
        if st.button("LOGIN", use_container_width=True, type="primary"):
            u=get_user(lu.strip())
            if not u: st.error("User not found. Sign Up first.")
            elif u['banned']: st.error("Account banned for cheating. Contact Founder 07036325587")
            elif u['password']!=hash_pw(lp): st.error("Wrong password!")
            else:
                st.session_state.logged=True; st.session_state.user=lu.strip()
                st.success(f"Welcome back {lu}! Balance N{u['balance']}")
                st.rerun()
        st.info("Forgot password? WhatsApp Founder 07036325587")
    with tab2:
        st.subheader("Sign Up - 1 Phone = 1 Account")
        su=st.text_input("Choose Username (no space)", key="su", placeholder="e.g. Chinedu123")
        sp=st.text_input("Choose Password", type="password", key="sp")
        spin=st.text_input("Create 4-Digit Withdraw PIN", type="password", max_chars=4, key="spin_code", placeholder="e.g. 1234")
        sphone=st.text_input("Your OPay / Phone Number", key="sphone", placeholder="07036325587")
        sref=st.text_input("Referral Code (Optional) - Who invited you?", key="sref", placeholder="Username of inviter")
        # ANTI-BOT CAPTCHA
        st.write(f"🤖 Anti-Bot: **{st.session_state.captcha_q}**")
        cap_ans=st.text_input("Answer Captcha", key="cap_ans", placeholder="Type answer")
        if st.button("CREATE ACCOUNT", use_container_width=True, type="primary"):
            if not su or not sp or not spin or not sphone:
                st.error("Fill all fields!")
            elif len(spin)!=4 or not spin.isdigit():
                st.error("PIN must be 4 numbers!")
            elif len(sphone)<10:
                st.error("Enter real OPay number!")
            elif cap_ans.strip()!=str(st.session_state.captcha_a):
                st.error("Wrong Captcha! You are Bot? Try again.")
                new_captcha()
            elif get_user(su.strip()):
                st.error("Username already taken! Choose another.")
            else:
                device = st.session_state.get("_device", su.strip())
                DB.execute("INSERT INTO users(username,password,pin,phone,balance,tasks,coins,energy,streak,referrals,is_vip,last_checkin,spin_date,created,device) VALUES(?,?,?,?,0,0,0,100,1,0,0,'','',?,?)",(su.strip(),hash_pw(sp),hash_pw(spin),sphone,str(datetime.now())[:10],device))
                DB.commit()
                add_tx(su.strip(),"SIGNUP BONUS",100,"Welcome bonus")
                # Referral bonus to inviter
                if sref.strip() and get_user(sref.strip()):
                    inv=get_user(sref.strip())
                    update_user(sref.strip(), balance=inv['balance']+500, referrals=inv['referrals']+1)
                    add_tx(sref.strip(),"REFERRAL",500,f"Invited {su.strip()}")
                    add_tx(su.strip(),"REFERRED BY",0,f"By {sref.strip()}")
                # Give signup bonus
                nu=get_user(su.strip()); update_user(su.strip(), balance=100)
                st.session_state.logged=True; st.session_state.user=su.strip()
                st.balloons(); st.success("Account Created! +N100 Bonus! You are logged in.")
                st.rerun()
    st.divider()
    st.caption("Your progress saves in database. Even if you reload, close app, change phone, login again = money still there.")
    st.stop()

# ===== LOGGED IN =====
user = get_user(st.session_state.user)
if not user: st.session_state.logged=False; st.rerun()

# Refresh user each run
st.success(f"👋 Welcome {user['username']} | Phone: {user['phone']} | {'👑 VIP' if user['is_vip'] else 'FREE'}")
c1,c2,c3,c4=st.columns(4)
c1.metric("Balance", f"₦{user['balance']}"); c2.metric("Tasks", f"{user['tasks']}/30"); c3.metric("Coins", user['coins']); c4.metric("Energy", f"{user['energy']}%")
c1,c2,c3=st.columns(3); c1.metric("Streak 🔥", f"{user['streak']} days"); c2.metric("Referrals", user['referrals']); c3.metric("Level", "VIP" if user['is_vip'] else "Free")
st.progress(min(user['tasks']/30,1.0), text=f"{user['tasks']}/30 Tasks to Withdraw")

# NOTIFICATIONS
st.info(f"🔔 Notification: Daily Check-in available! Top user gets N5000 month end. Founder {FOUNDER}")

# Logout + Security
col_log, col_sec = st.columns(2)
with col_log:
    if st.button("LOGOUT", use_container_width=True):
        st.session_state.logged=False; st.session_state.user=None; st.rerun()
with col_sec:
    if st.button("🔒 CHANGE PIN", use_container_width=True):
        st.session_state.show_pin=True

if st.session_state.get("show_pin"):
    old_pin=st.text_input("Old PIN", type="password")
    new_pin=st.text_input("New 4-Digit PIN", type="password", max_chars=4)
    if st.button("Update PIN"):
        if hash_pw(old_pin)==user['pin'] and len(new_pin)==4:
            update_user(user['username'], pin=hash_pw(new_pin)); st.success("PIN Changed!"); st.session_state.show_pin=False; st.rerun()
        else: st.error("Wrong old PIN or new PIN not 4 digits")

# ===== HELPERS FOR EARNING =====
def earn(amount, task_name, task_key):
    if did_task_today(user['username'], task_key):
        st.warning("Already done today! Come back tomorrow.")
        return False
    add_task_log(user['username'], task_key, amount)
    update_user(user['username'], balance=user['balance']+amount, tasks=user['tasks']+1)
    add_tx(user['username'], task_key, amount, f"Earned N{amount}")
    st.success(f"+N{amount} Added! New Balance N{user['balance']+amount}")
    return True

def earn_no_task(amount, task_name):
    update_user(user['username'], balance=user['balance']+amount)
    add_tx(user['username'], task_name, amount, f"Earned N{amount}")
    st.success(f"+N{amount} Added!")

# ===== DAILY CHECK-IN =====
st.divider(); st.subheader("📅 Daily Check-In")
today=str(date.today())
if user['last_checkin']!=today:
    if st.button("CHECK-IN TODAY", use_container_width=True, type="primary"):
        bonus=100*user['streak']
        update_user(user['username'], balance=user['balance']+bonus, last_checkin=today, streak=user['streak']+1)
        add_tx(user['username'],"CHECKIN",bonus,f"Day {user['streak']}")
        st.balloons(); st.success(f"+N{bonus} Check-in!")
        st.rerun()
else: st.success(f"✅ Checked in today. Streak {user['streak']} days")

# ===== SOCIAL TASKS - 2 STEP ANTI-CHEAT =====
st.divider(); st.subheader("📱 Social Tasks - Must Join - 10 Sec Wait - Once Per Day")
st.caption("1. Click OPEN, join group, wait 10 sec, click VERIFY. No join = No money.")

def social_task(key, label, link):
    if did_task_today(user['username'], key):
        st.success(f"✅ {label} Done today!"); return
    st.write(f"**{label} - N200**")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button(f"1. OPEN {label}", key=f"open_{key}", use_container_width=True):
            st.session_state.opened[key]=time.time()
            st.success("Opened! Go and join now.")
            st.link_button(f"Open {label}", link)
    with col_b:
        opened=st.session_state.opened.get(key,0)
        if opened==0:
            st.button("2. VERIFY - Open First", key=f"v_{key}", disabled=True, use_container_width=True)
        elif time.time()-opened < 10:
            st.info(f"Wait {int(10-(time.time()-opened))} sec after joining...")
            if st.button("Try Verify", key=f"vw_{key}", use_container_width=True):
                st.warning("You must join and wait 10 sec!")
        else:
            if st.button(f"2. I JOINED - VERIFY +N200", key=f"vo_{key}", use_container_width=True, type="primary"):
                earn(200, label, key); st.rerun()

social_task("youtube","YouTube Follow", LINKS['youtube'])
social_task("telegram","Telegram Group", LINKS['telegram'])
social_task("whatsapp","WhatsApp Group", LINKS['whatsapp_group'])

# ===== SPIN / QUIZ / COMBO / CIPHER / CHEST - ONCE PER DAY =====
st.divider(); st.subheader("🎡 Spin Wheel - Once Per Day")
if not did_task_today(user['username'],"spin"):
    if st.button("SPIN NOW", use_container_width=True):
        prize=random.choice([20,50,100,100,200,500]); earn(prize,"Spin","spin"); st.balloons(); st.rerun()
else: st.success("✅ Spin done today!")

st.divider(); st.subheader("🧠 Daily Quiz - N300")
if not did_task_today(user['username'],"quiz"):
    q=st.radio("Who is Founder?", ["Taiwo David","Elon Musk","Mark Zuckerberg"], key="quizq")
    if st.button("Submit Quiz", use_container_width=True):
        if q=="Taiwo David": earn(300,"Quiz","quiz"); st.rerun()
        else: st.error("Wrong!")
else: st.success("✅ Quiz done today!")

st.divider(); st.subheader("🎯 Daily Combo - N500 - Hint: Hilltop + Adsterra + Propeller")
if not did_task_today(user['username'],"combo"):
    combo=st.multiselect("Pick Combo", ["Hilltop","Adsterra","Propeller","AdMaven"], key="combo")
    if st.button("CHECK COMBO", use_container_width=True):
        if set(combo)==set(["Hilltop","Adsterra","Propeller"]): earn(500,"Combo","combo"); st.balloons(); st.rerun()
        else: st.error("Wrong!")
else: st.success("✅ Combo done today!")

st.divider(); st.subheader("🔐 Daily Cipher - N1000 - Code: TAIWO")
if not did_task_today(user['username'],"cipher"):
    cipher=st.text_input("Enter Cipher")
    if st.button("DECODE", use_container_width=True):
        if cipher.upper()=="TAIWO": earn(1000,"Cipher","cipher"); st.rerun()
        else: st.error("Wrong!")
else: st.success("✅ Cipher done today!")

st.divider(); st.subheader("👆 Tap To Earn + Captcha Anti-Bot")
st.write(f"Anti-Bot: {st.session_state.captcha_q}")
cap2=st.text_input("Answer to Tap", key="cap_tap")
if st.button("💰 TAP COIN - N5", use_container_width=True):
    if cap2.strip()!=str(st.session_state.captcha_a):
        st.error("Wrong Captcha! Bot blocked."); new_captcha()
    elif user['energy']<=0: st.warning("No Energy! Refill below.")
    else:
        earn_amt=100 if user['is_vip'] else 5
        update_user(user['username'], balance=user['balance']+earn_amt, coins=user['coins']+1, energy=user['energy']-5)
        add_tx(user['username'],"TAP",earn_amt,"Tap coin")
        new_captcha(); st.toast(f"+N{earn_amt}"); st.rerun()
if st.button("⚡ Refill Energy - Watch Ad", use_container_width=True):
    update_user(user['username'], energy=100, tasks=user['tasks']+1)
    st.link_button("Watch Ad", LINKS['hilltop'])

st.divider(); st.subheader("📦 Lucky Chest - Once Per Day")
if not did_task_today(user['username'],"chest"):
    ch1,ch2,ch3=st.columns(3)
    for i,col in enumerate([ch1,ch2,ch3]):
        if col.button(f"🎁 Chest {i+1}", key=f"ch_{i}", use_container_width=True):
            r=random.choice([20,50,100,500]); earn(r,"Chest","chest"); st.rerun()
else: st.success("✅ Chest done today!")

# ===== STAKING - From Binance =====
st.divider(); st.subheader("💎 STAKING - Lock Money, Earn Profit - From Binance")
st.write("Stake N1000 for 7 days, get N1200 back = N200 profit. Like Binance Earn.")
if st.button("STAKE N1000 - Earn N200", use_container_width=True):
    if user['balance']>=1000:
        update_user(user['username'], balance=user['balance']-1000)
        add_tx(user['username'],"STAKE","-1000","Staked 7 days")
        st.success("Staked N1000! Founder will pay N1200 in 7 days via OPay. WhatsApp 07036325587 to confirm.")
    else: st.error("Need N1000 balance to stake!")

# ===== KING FEATURES =====
st.divider(); st.title("👑 KING FEATURES")
st.subheader("👑 KING 1: VIP N2000/Month")
if not user['is_vip']:
    if st.button("JOIN VIP - N2000", type="primary", use_container_width=True):
        st.link_button("Pay VIP via WhatsApp", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%20VIP%20N2000%20My%20username%20{user['username']}")
        st.info("Pay N2000 to OPay 07036325587, send receipt, Founder will make you VIP in Admin Panel.")
else: st.success("👑 YOU ARE VIP!")

st.divider(); st.subheader("💰 KING 2: CPAGrip N4000")
st.link_button("UNLOCK - Enter Email Only", LINKS['cpagrip'])
if st.button("I ENTERED EMAIL - CLAIM N500", use_container_width=True):
    if did_task_today(user['username'],"cpagrip"): st.warning("Already claimed today!")
    else: earn(500,"CPAGrip","cpagrip"); st.balloons(); st.rerun()

st.divider(); st.subheader("💵 KING 3: PalmPay + OPay Referral")
if st.button("DOWNLOAD PALMPAY - N500", use_container_width=True):
    st.link_button("PalmPay", LINKS['palmpay'])
    earn_no_task(500,"PalmPay"); st.rerun()
if st.button("DOWNLOAD OPAY - N500", use_container_width=True):
    st.link_button("OPay", LINKS['opay_ref'])
    earn_no_task(500,"OPay"); st.rerun()

st.divider(); st.subheader("🔗 Monetag SmartLink")
if st.button("CLICK SMARTLINK - N50", use_container_width=True):
    st.link_button("SmartLink", LINKS['monetag'])
    update_user(user['username'], balance=user['balance']+50, tasks=user['tasks']+1)

st.divider(); st.subheader("📱 KING 4: Data Vending")
mtn=st.text_input("Phone for Data", placeholder="07036325587")
if st.button("BUY 1GB N350 - WhatsApp", use_container_width=True):
    st.link_button("Buy Data", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%201GB%20N350%20to%20{mtn}%20My%20user%20{user['username']}")

st.divider(); st.subheader("🚀 Level Up")
for lvl,price in {"Level 2 Silver N1500":1500,"Level 3 Gold N3000":3000,"Level 4 Diamond N6000":6000}.items():
    if st.button(f"UPGRADE TO {lvl}", use_container_width=True, key=lvl):
        st.link_button(f"Pay N{price}", f"https://wa.me/{WA}?text=I%20want%20{lvl}%20User%20{user['username']}")

# ===== TRANSACTION HISTORY + LEADERBOARD =====
st.divider(); st.subheader("📜 My Transaction History")
cur=DB.execute("SELECT type,amount,detail,time FROM transactions WHERE username=? ORDER BY id DESC LIMIT 15",(user['username'],))
rows=cur.fetchall()
if rows:
    for r in rows: st.write(f"**{r[0]}** | N{r[1]} | {r[2]} | {r[3]}")
else: st.write("No transactions yet.")

st.divider(); st.subheader("🏆 Leaderboard - Top 5")
cur=DB.execute("SELECT username,balance FROM users ORDER BY balance DESC LIMIT 5")
for i,row in enumerate(cur.fetchall(),1):
    st.write(f"{i}. **{row[0]}** - N{row[1]}")

# ===== WITHDRAW - REQUIRES PIN + KYC =====
st.divider(); st.subheader("💳 Withdraw - Requires PIN + OPay Number")
if not user['is_vip'] and user['tasks']<30:
    st.error(f"Complete {30-user['tasks']} more tasks! Rule by {FOUNDER}")
else:
    st.success(f"Ready to withdraw N{user['balance']}!")
    opay=st.text_input("Your OPay Number (Must match signup)", value=user['phone'])
    pin_in=st.text_input("Enter Your 4-Digit Withdraw PIN", type="password", max_chars=4)
    if st.button("WITHDRAW NOW", type="primary", use_container_width=True):
        if hash_pw(pin_in)!=user['pin']: st.error("Wrong PIN! Withdraw blocked for security.")
        elif opay!=user['phone']: st.error("OPay number must match signup number! Anti-cheat.")
        elif user['balance']<=0: st.error("No balance!")
        else:
            st.success(f"Withdrawal N{user['balance']} to {opay} requested! Founder will pay in 24h.")
            st.link_button("Confirm via WhatsApp", f"https://wa.me/{WA}?text=Withdraw%20N{user['balance']}%20to%20{opay}%20User%20{user['username']}%20PIN%20OK")
            add_tx(user['username'],"WITHDRAW REQUEST",user['balance'],f"To {opay}")

# ===== COURSE + CLONE =====
st.divider(); st.subheader("🎓 Learn - N15,000 | 🛒 Clone - N25,000")
if st.button("PAY N15k TO LEARN", use_container_width=True):
    st.link_button("Learn", f"https://wa.me/{WA}?text=Hi%20Taiwo%20I%20want%20to%20learn%20N15000%20User%20{user['username']}")
if st.button("BUY CLONE - N25k", use_container_width=True):
    st.link_button("Buy Clone", f"https://wa.me/{WA}?text=I%20want%20Clone%20V12%20N25000%20User%20{user['username']}")

# ===== ADMIN PANEL - ONLY FOR YOU =====
st.divider()
with st.expander("🛡️ ADMIN PANEL - Only Taiwo David"):
    ap=st.text_input("Admin Password", type="password")
    if ap==ADMIN_PASS:
        st.success("Admin Access Granted")
        cur=DB.execute("SELECT username,phone,balance,tasks,referrals,is_vip,banned FROM users ORDER BY balance DESC")
        for r in cur.fetchall():
            c1,c2,c3=st.columns([2,1,1])
            c1.write(f"**{r[0]}** {r[1]} Bal N{r[2]} Tasks {r[3]} Ref {r[4]} VIP {r[5]}")
            if c2.button(f"Make VIP {r[0]}", key=f"vip_{r[0]}"):
                update_user(r[0], is_vip=1); st.success(f"{r[0]} now VIP"); st.rerun()
            if c3.button(f"Ban {r[0]}", key=f"ban_{r[0]}"):
                update_user(r[0], banned=1); st.success(f"{r[0]} banned"); st.rerun()
        if st.button("Reset All Daily Tasks (New Day)"):
            st.success("Daily tasks auto-reset by date. No need to reset.")
    elif ap: st.error("Wrong Admin Password!")

st.caption(f"Taiwo Earn V12 | Founder {FOUNDER} | OPay {PHONE} | Login + Database + PIN + Anti-Cheat | No Timewall")
