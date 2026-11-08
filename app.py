import streamlit as st
import sqlite3, hashlib, random, time
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Taiwo Earn V16 - By Taiwo David", page_icon="💰", layout="centered")
FOUNDER="Taiwo David"; PHONE="07036325587"; WA="2347036325587"
ADMIN_PASS="TaiwoV16Secure2026"  # NEW ADMIN PASS - Change after paste
FOUNDER_SHARE=0.80; USER_SHARE=0.20
PRICES={"survey":4000,"game":7500,"cpagrip":20000,"palmpay":7500,"opay":5000,"video":1000,"social":1000,"combo":2500,"cipher":5000,"quiz":1500,"spin":1000,"chest":1000,"checkin":500,"referral":2500,"mission":2500,"luckybox":2000}
def user_get(t): return int(PRICES[t]*USER_SHARE)
def founder_get(t): return int(PRICES[t]*FOUNDER_SHARE)
LINKS={
 "youtube":"https://youtube.com/@YOUR_CHANNEL","telegram":"https://t.me/YOUR_GROUP","whatsapp_group":"https://chat.whatsapp.com/YOUR_GROUP_LINK",
 "hilltop":"https://hilltopads.com/?ref=YOUR_ID","adsterra":"https://www.adsterra.com/?ref=YOUR_ID","monetag":"https://monetag.com/YOUR_SMARTLINK",
 "cpagrip":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=LOCKER","palmpay":"https://palmpay.com/YOUR_REF_CODE","opay_ref":"https://opay.com/YOUR_REF_CODE",
 "survey1":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=SURVEY","game_offer":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=GAME","honeygain":"https://r.honeygain.me/YOUR_CODE",
}

# ===== DATABASE WITH AUTO-MIGRATION - FIXES KeyError =====
def get_db():
    conn=sqlite3.connect("users.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY, password TEXT, pin TEXT, phone TEXT, balance INTEGER DEFAULT 0, tasks INTEGER DEFAULT 0,
        coins INTEGER DEFAULT 0, energy INTEGER DEFAULT 100, streak INTEGER DEFAULT 1, referrals INTEGER DEFAULT 0,
        is_vip INTEGER DEFAULT 0, vip_level TEXT DEFAULT 'FREE', last_checkin TEXT DEFAULT '', created TEXT DEFAULT '', banned INTEGER DEFAULT 0,
        total_earned INTEGER DEFAULT 0, videos_watched INTEGER DEFAULT 0, tickets INTEGER DEFAULT 0, badge TEXT DEFAULT 'Newbie', referrer TEXT DEFAULT '')""")
    # AUTO-ADD MISSING COLUMNS - THIS FIXES OLD DB CRASH
    existing=[r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
    needed={"last_task_time":"TEXT DEFAULT ''","tasks_last_hour":"INTEGER DEFAULT 0","pin_attempts":"INTEGER DEFAULT 0","pin_locked_until":"TEXT DEFAULT ''","staked":"INTEGER DEFAULT 0","stake_until":"TEXT DEFAULT ''","last_luckybox":"TEXT DEFAULT ''","social_open_time":"TEXT DEFAULT ''","login_token":"TEXT DEFAULT ''"}
    for col, typ in needed.items():
        if col not in existing:
            try: conn.execute(f"ALTER TABLE users ADD COLUMN {col} {typ}")
            except: pass
    conn.execute("""CREATE TABLE IF NOT EXISTS task_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, task TEXT, date TEXT, amount INTEGER, time TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, type TEXT, amount INTEGER, detail TEXT, time TEXT)""")
    conn.commit(); return conn
DB=get_db()
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()
def make_token(username, password_hash): return hashlib.sha256(f"{username}:{password_hash}:TaiwoV16".encode()).hexdigest()[:20]
def add_tx(u,t,a,d): DB.execute("INSERT INTO transactions(username,type,amount,detail,time) VALUES(?,?,?,?,?)",(u,t,a,d,str(datetime.now())[:19])); DB.commit()
def add_log(u,t,a): DB.execute("INSERT INTO task_logs(username,task,date,amount,time) VALUES(?,?,?,?,?)",(u,t,str(date.today()),a,str(datetime.now())[:19])); DB.commit()
def did_today(u,t): return DB.execute("SELECT * FROM task_logs WHERE username=? AND task=? AND date=?",(u,t,str(date.today()))).fetchone() is not None
def did_ever(u,t): return DB.execute("SELECT * FROM task_logs WHERE username=? AND task=?",(u,t)).fetchone() is not None
def upd(u,**kw):
    for k,v in kw.items(): DB.execute(f"UPDATE users SET {k}=? WHERE username=?",(v,u))
    DB.commit()
def get_user(u):
    if not u: return None
    cur=DB.execute("SELECT * FROM users WHERE username=?",(u,)); r=cur.fetchone()
    if not r: return None
    d=dict(zip([x[0] for x in cur.description],r))
    # SAFE DEFAULTS - Prevents KeyError even if DB is old
    for k,v in {"pin_locked_until":"","staked":0,"stake_until":"","last_luckybox":"","social_open_time":"","last_task_time":"","pin_attempts":0,"videos_watched":0,"tickets":0,"badge":"Newbie","referrer":"","total_earned":0,"vip_level":"FREE","is_vip":0,"streak":1,"balance":0,"tasks":0}.items():
        if k not in d or d[k] is None: d[k]=v
    return d
def get_user_by_phone(p):
    cur=DB.execute("SELECT * FROM users WHERE phone=?",(p,)); r=cur.fetchone()
    return dict(zip([x[0] for x in cur.description],r)) if r else None
def new_cap():
    a=random.randint(2,9); b=random.randint(2,9); st.session_state.captcha_q=f"What is {a} + {b} ?"; st.session_state.captcha_a=a+b

if 'logged' not in st.session_state: st.session_state.logged=False; st.session_state.user=None; st.session_state.captcha_q=""; st.session_state.captcha_a=0; st.session_state.tap_count=0
if not st.session_state.captcha_q: new_cap()

# ===== ALWAYS SIGNED IN - CHECK LINK TOKEN =====
# If user has ?user=Taiwo&token=xxx in link, auto-login without password
try:
    qp=st.query_params
    q_user=qp.get("user","")
    q_token=qp.get("token","")
    if q_user and q_token and not st.session_state.logged:
        u=get_user(q_user)
        if u and not u.get("banned",0):
            expected=make_token(u["username"], u["password"])
            if q_token==expected:
                st.session_state.logged=True; st.session_state.user=q_user
except: pass

def do_login(username):
    u=get_user(username)
    token=make_token(u["username"], u["password"])
    st.session_state.logged=True; st.session_state.user=username
    # SAVE IN LINK - So reload keeps you logged in
    try: st.query_params["user"]=username; st.query_params["token"]=token
    except: pass
    st.rerun()

def do_logout():
    st.session_state.logged=False; st.session_state.user=None
    try: st.query_params.clear()
    except: pass
    st.rerun()

st.title("💰 Taiwo Earn V16")
st.caption(f"By {FOUNDER} | OPay {PHONE} | 80% Founder / 20% User | ALWAYS SIGNED IN | NO KeyError")

# ===== LOGIN / SIGNUP =====
if not st.session_state.logged:
    t1,t2=st.tabs(["🔑 LOGIN","📝 SIGN UP"])
    with t1:
        lu=st.text_input("Username",key="lu", value="Taiwo"); lp=st.text_input("Password",type="password",key="lp", value="1234")
        st.caption("✅ Stay signed in: After login, bookmark the link. It will keep you logged in even after you close app.")
        if st.button("LOGIN",use_container_width=True,type="primary"):
            u=get_user(lu.strip())
            if not u: st.error("User not found. Sign Up first.")
            elif u.get("banned",0): st.error("BANNED. Contact Founder.")
            elif u.get("pin_locked_until","") and u.get("pin_locked_until","")>str(datetime.now()): st.error(f"Locked until {u.get('pin_locked_until')}")
            elif u["password"]!=hash_pw(lp): st.error("Wrong password!")
            else: do_login(lu.strip())
    with t2:
        su=st.text_input("Username",key="su"); sp=st.text_input("Password (min 6)",type="password",key="sp")
        spin=st.text_input("4-Digit PIN",type="password",max_chars=4,key="spn"); sphone=st.text_input("OPay Number - 11 Digits",key="sph", placeholder="07036325587"); sref=st.text_input("Who Invited You?",key="sref")
        st.write(f"🤖 {st.session_state.captcha_q}"); cap=st.text_input("Answer",key="cap")
        if st.button("CREATE ACCOUNT",use_container_width=True,type="primary"):
            if not su or not sp or not spin or not sphone: st.error("Fill all!")
            elif len(sp)<6: st.error("Password 6+ chars!")
            elif len(spin)!=4 or not spin.isdigit(): st.error("PIN must be 4 numbers!")
            elif len(sphone)!=11 or not sphone.isdigit(): st.error("Phone must be 11 digits!")
            elif cap.strip()!=str(st.session_state.captcha_a): st.error("Wrong Captcha!"); new_cap()
            elif get_user(su.strip()): st.error("Username taken!")
            elif get_user_by_phone(sphone.strip()): st.error("This phone already has account! 1 Phone = 1 Account.")
            else:
                DB.execute("INSERT INTO users(username,password,pin,phone,balance,tasks,coins,energy,streak,referrals,is_vip,vip_level,last_checkin,created,total_earned,videos_watched,tickets,badge,referrer,login_token) VALUES(?,?,?,?,500,0,0,100,1,0,0,'FREE','',?,500,0,0,'Newbie',?,'')",(su.strip(),hash_pw(sp),hash_pw(spin),sphone.strip(),str(datetime.now())[:10],sref.strip())); DB.commit()
                if sref.strip() and get_user(sref.strip()):
                    l1=get_user(sref.strip()); upd(sref.strip(), balance=l1['balance']+500, referrals=l1['referrals']+1); add_tx(sref.strip(),"REFERRAL L1",500,f"Invited {su.strip()}")
                    if l1.get("referrer") and get_user(l1.get("referrer")):
                        l2=get_user(l1.get("referrer")); upd(l1.get("referrer"), balance=l2['balance']+200); add_tx(l1.get("referrer"),"REFERRAL L2",200,f"Friend of {su.strip()}")
                do_login(su.strip())
    st.info("🔒 80/20 Rule: You 20% | Founder 80% | 1 Phone = 1 Account | Stay Signed In")
    st.stop()

user=get_user(st.session_state.user)
if not user: do_logout()

# Auto-ban check
hour_ago=str(datetime.now()-timedelta(hours=1))
recent=DB.execute("SELECT COUNT(*) FROM task_logs WHERE username=? AND time>=?",(user['username'],hour_ago[:19])).fetchone()[0]
if recent>=20 and not user.get("banned",0):
    upd(user['username'], banned=1); st.error("AUTO-BANNED: 20 tasks in 1 hour = Bot."); do_logout()
if user.get("banned",0): st.error("BANNED. Contact Founder."); st.stop()

multiplier=1.0
if user.get("streak",1)>=30: multiplier=3.0
elif user.get("streak",1)>=7: multiplier=2.0
elif user.get("streak",1)>=3: multiplier=1.5
vip_mult={"FREE":1.0,"BRONZE":1.5,"SILVER":2.0,"GOLD":2.5}.get(user.get("vip_level","FREE"),1.0)
total_mult=multiplier*vip_mult
available_balance=user.get("balance",0)-user.get("staked",0)

st.success(f"👋 {user['username']} | {user.get('vip_level')} VIP | Streak {user.get('streak')}d = {multiplier}X | Total {total_mult}X | ✅ Always Signed In")
c1,c2,c3,c4=st.columns(4); c1.metric("Balance",f"₦{user.get('balance',0)}"); c2.metric("Available",f"₦{available_balance}"); c3.metric("Tickets 🎟️",user.get("tickets",0)); c4.metric("Tasks",f"{user.get('tasks',0)}/30")
st.progress(min(user.get("tasks",0)/30,1.0))
st.info(f"💡 80/20: You 20% | Founder 80% | Multiplier {total_mult}X | Staked Locked: N{user.get('staked',0)} | This hour: {recent}/20")
if st.button("LOGOUT - Sign Out", use_container_width=True): do_logout()
st.caption("🔗 Your login link is saved. If you close app and open same link, you stay logged in. Don't share link, it has your token.")

def earn(task, label):
    if did_today(user['username'], task): st.warning("⛔ Already claimed today! DB blocked."); return False
    last=user.get("last_task_time","")
    if last:
        try:
            if (datetime.now()-datetime.strptime(last,"%Y-%m-%d %H:%M:%S")).total_seconds()<5: st.warning("Wait 5 sec between tasks! Anti-Bot."); return False
        except: pass
    base=user_get(task); amount=int(base*total_mult); f_amount=founder_get(task)
    add_log(user['username'], task, amount)
    fresh=get_user(user['username'])
    upd(user['username'], balance=fresh['balance']+amount, tasks=fresh['tasks']+1, total_earned=fresh.get("total_earned",0)+amount, tickets=fresh.get("tickets",0)+1, last_task_time=str(datetime.now())[:19])
    add_tx(user['username'], label, amount, f"You 20% N{amount} | Founder 80% N{f_amount} | Total N{PRICES[task]}")
    st.success(f"+N{amount} (20% of N{PRICES[task]}). Founder N{f_amount}. +1 Ticket 🎟️")
    return True

# DAILY MISSIONS
st.divider(); st.subheader("🎯 Daily Missions - Do 5 = N500, Do 10 = N1000")
today_tasks=DB.execute("SELECT COUNT(*) FROM task_logs WHERE username=? AND date=?",(user['username'],str(date.today()))).fetchone()[0]
st.write(f"Today: **{today_tasks} / 10** tasks")
if today_tasks>=5 and not did_today(user['username'],"mission5"):
    if st.button("CLAIM MISSION 5 - N500",use_container_width=True,type="primary"): earn("mission","MISSION 5"); st.rerun()
elif today_tasks>=5: st.success("✅ Mission 5 claimed!")
if today_tasks>=10 and not did_today(user['username'],"mission10"):
    if st.button("CLAIM MISSION 10 - N1000",use_container_width=True,type="primary"):
        add_log(user['username'],"mission10",1000); upd(user['username'], balance=get_user(user['username'])['balance']+1000); add_tx(user['username'],"MISSION 10",1000,"10 tasks"); st.success("+N1000!"); st.rerun()
elif today_tasks>=10: st.success("✅ Mission 10 claimed!")

# LUCKY BOX
st.divider(); st.subheader("📦 Lucky Box - Every 1 Hour")
last_box=user.get("last_luckybox","")
can_open=True
if last_box:
    try:
        diff=(datetime.now()-datetime.strptime(last_box,"%Y-%m-%d %H:%M:%S")).total_seconds()
        if diff<3600: can_open=False; st.info(f"Next in {int((3600-diff)//60)} mins")
    except: pass
if can_open:
    if st.button("OPEN LUCKY BOX",use_container_width=True):
        prize=random.choice([200,200,500,500,1000]); upd(user['username'], balance=get_user(user['username'])['balance']+prize, last_luckybox=str(datetime.now())[:19]); add_tx(user['username'],"LUCKY BOX",prize,"Hourly"); st.balloons(); st.success(f"Won N{prize}!"); st.rerun()

# CHECK-IN
st.divider(); st.subheader("📅 Daily Check-In")
if user.get("last_checkin","")!=str(date.today()):
    if st.button(f"CHECK-IN - N{int(user_get('checkin')*total_mult)}",use_container_width=True,type="primary"):
        amt=int(user_get('checkin')*total_mult); upd(user['username'], balance=get_user(user['username'])['balance']+amt, last_checkin=str(date.today()), streak=user.get("streak",1)+1, total_earned=get_user(user['username']).get("total_earned",0)+amt); add_tx(user['username'],"CHECKIN",amt,f"Streak"); st.balloons(); st.success(f"+N{amt}!"); st.rerun()
else: st.success(f"✅ Checked in! Streak {user.get('streak')} days")

# HIGH PAY
st.divider(); st.subheader(f"📝 SURVEY - You N{user_get('survey')} (20%) | Founder N{founder_get('survey')} (80%)")
if not did_today(user['username'],"survey"):
    if st.button("START SURVEY",use_container_width=True,type="primary"): st.link_button("Open Survey",LINKS['survey1']); st.session_state.survey_open=True
    if st.session_state.get("survey_open"):
        if st.button("I FINISHED SURVEY - CLAIM",use_container_width=True): earn("survey","SURVEY"); st.rerun()
else: st.success("✅ Survey done!")
st.divider(); st.subheader(f"🎮 GAME - You N{user_get('game')} (20%) | Founder N{founder_get('game')} (80%)")
if not did_today(user['username'],"game"):
    if st.button("INSTALL GAME",use_container_width=True,type="primary"): st.link_button("Install Game",LINKS['game_offer']); st.session_state.game_open=True
    if st.session_state.get("game_open"):
        if st.button("I PLAYED - CLAIM",use_container_width=True): earn("game","GAME"); st.balloons(); st.rerun()
else: st.success("✅ Game done!")
st.divider(); st.subheader(f"💰 CPAGrip - You N{user_get('cpagrip')} (20%) | Founder N{founder_get('cpagrip')} (80%)")
st.link_button("UNLOCK - Enter Email Only",LINKS['cpagrip'])
if st.button("I ENTERED EMAIL - CLAIM",use_container_width=True):
    if not did_today(user['username'],"cpagrip"): earn("cpagrip","CPAGRIP"); st.balloons(); st.rerun()
    else: st.warning("Already claimed!")

# PALMPAY ONCE EVER
st.divider(); st.subheader("💵 PalmPay / OPay - ONCE EVER - Screenshot + Code TAIWO")
if not did_ever(user['username'],"palmpay"):
    if st.button("DOWNLOAD PALMPAY",use_container_width=True): st.link_button("PalmPay",LINKS['palmpay'])
    code_in=st.text_input("Enter Code from Founder after screenshot (TAIWO)", key="palm_code")
    if st.button("I SENT SCREENSHOT - CLAIM PALMPAY",use_container_width=True):
        if code_in.strip().upper()=="TAIWO": earn("palmpay","PALMPAY"); st.rerun()
        else: st.error("Wrong code! Send screenshot to WhatsApp 07036325587 first.")
else: st.success("✅ PalmPay already claimed once.")
if not did_ever(user['username'],"opay"):
    if st.button("DOWNLOAD OPAY",use_container_width=True): st.link_button("OPay",LINKS['opay_ref'])
    code2=st.text_input("Enter Code for OPay", key="opay_code")
    if st.button("I SENT SCREENSHOT - CLAIM OPAY",use_container_width=True):
        if code2.strip().upper()=="TAIWO": earn("opay","OPAY"); st.rerun()
        else: st.error("Wrong code!")
else: st.success("✅ OPay already claimed once.")

# TEMU + FUND + HONEYGAIN + FREELANCE
st.divider(); st.subheader("🎁 Temu Referral + Creator Fund")
st.write(f"Referrals: {user.get('referrals')} | Tickets: {user.get('tickets')} | Code: {user['username']}")
st.code(f"Join Taiwo Earn with code {user['username']}")
if user.get("tickets",0)>=100:
    if st.button("🎟️ ENTER LUCKY DRAW N10,000",use_container_width=True,type="primary"): upd(user['username'], tickets=0); add_tx(user['username'],"LUCKY DRAW",0,"Entered"); st.success("Entered Draw! Winner Sunday!")
st.write("🏆 Top 3 Sunday:")
for i,row in enumerate(DB.execute("SELECT username,balance FROM users ORDER BY balance DESC LIMIT 3").fetchall(),1): st.write(f"{i}. {row[0]} - N{row[1]}")
st.divider(); st.subheader("🌐 Honeygain - Passive")
if st.button("INSTALL HONEYGAIN",use_container_width=True): st.link_button("Honeygain",LINKS['honeygain']); st.success("Installed!")
st.divider(); st.subheader("💼 Freelance Market - Founder 20%")
job=st.selectbox("Service", ["Logo N5000","Video Edit N3000","Flyer N1000","App N25000"])
if st.button("POST SERVICE",use_container_width=True): add_tx(user['username'],"POSTED JOB",0,job); st.success(f"Posted {job}"); st.link_button("Find Buyers",f"https://wa.me/{WA}?text=I%20want%20{job}")

# DAILY TASKS
st.divider(); st.subheader("📱 Social - Video - Combo - Cipher - Quiz - Spin - Chest")
def social_task(key,label,link):
    if did_today(user['username'],key): st.success(f"✅ {label} Done!"); return
    st.write(f"**{label} - You N{user_get('social')} (20%)**")
    col_a,col_b=st.columns(2)
    with col_a:
        if st.button(f"1. OPEN {label}",key=f"o_{key}",use_container_width=True): upd(user['username'], social_open_time=str(datetime.now())[:19]); st.link_button(f"Open {label}",link); st.success("Opened! Timer in DB, refresh won't reset.")
    with col_b:
        open_time=get_user(user['username']).get("social_open_time","")
        if not open_time: st.button("2. VERIFY - Open First",key=f"v_{key}",disabled=True,use_container_width=True)
        else:
            try: waited=(datetime.now()-datetime.strptime(open_time,"%Y-%m-%d %H:%M:%S")).total_seconds()
            except: waited=999
            if waited<10: st.info(f"Wait {int(10-waited)}s")
            else:
                if st.button(f"2. I JOINED - +N{user_get('social')}",key=f"vo_{key}",use_container_width=True): earn("social",label); st.rerun()
social_task("youtube","YouTube",LINKS['youtube']); social_task("telegram","Telegram",LINKS['telegram']); social_task("whatsapp","WhatsApp",LINKS['whatsapp_group'])
if user.get("videos_watched",0)<10:
    if st.button(f"WATCH VIDEO - {user.get('videos_watched',0)}/10",use_container_width=True): upd(user['username'], videos_watched=user.get("videos_watched",0)+1); st.link_button("Watch",LINKS['youtube']); st.rerun()
else:
    if not did_today(user['username'],"video"):
        if st.button("CLAIM VIDEO BONUS",use_container_width=True): earn("video","VIDEO"); upd(user['username'], videos_watched=0); st.rerun()
    else: st.success("✅ Video done!")
if not did_today(user['username'],"combo"):
    cb=st.multiselect("Combo: Hilltop+Adsterra+Propeller",["Hilltop","Adsterra","Propeller"],key="cb")
    if st.button("CHECK COMBO"):
        if set(cb)==set(["Hilltop","Adsterra","Propeller"]): earn("combo","COMBO"); st.rerun()
        else: st.error("Wrong!")
else: st.success("✅ Combo done!")
if not did_today(user['username'],"cipher"):
    cp=st.text_input("Cipher TAIWO")
    if st.button("DECODE"):
        if cp.upper()=="TAIWO": earn("cipher","CIPHER"); st.rerun()
else: st.success("✅ Cipher done!")
if not did_today(user['username'],"quiz"):
    qq=st.radio("Who is Founder?",["Taiwo David","Elon Musk"],key="qq")
    if st.button("Submit Quiz"):
        if qq=="Taiwo David": earn("quiz","QUIZ"); st.rerun()
else: st.success("✅ Quiz done!")
if not did_today(user['username'],"spin"):
    if st.button("SPIN NOW"): earn("spin","SPIN"); st.rerun()
else: st.success("✅ Spin done!")
if not did_today(user['username'],"chest"):
    ch1,ch2,ch3=st.columns(3)
    for i,col in enumerate([ch1,ch2,ch3]):
        if col.button(f"Chest {i+1}",key=f"ch{i}"): earn("chest","CHEST"); st.rerun()
else: st.success("✅ Chest done!")

# TAP
st.divider(); st.subheader("👆 Tap - Captcha Every 3 Taps")
st.write(f"Anti-Bot: {st.session_state.captcha_q}")
cap2=st.text_input("Answer Captcha to Tap",key="cap_tap")
if st.button("💰 TAP COIN - N5",use_container_width=True):
    if st.session_state.tap_count>=3 and cap2.strip()!=str(st.session_state.captcha_a): st.error("Wrong Captcha!"); new_cap(); st.session_state.tap_count=0
    elif user.get("energy",100)<=0: st.warning("No Energy!")
    else:
        fresh=get_user(user['username']); upd(user['username'], balance=fresh['balance']+5, coins=fresh['coins']+1, energy=fresh['energy']-5); st.session_state.tap_count+=1; st.toast("+N5"); st.rerun()
if st.button("⚡ Refill Energy - Watch Ad",use_container_width=True): upd(user['username'], energy=100, tasks=get_user(user['username'])['tasks']+1); st.link_button("Watch Ad",LINKS['hilltop'])

# VIP + STAKING
st.divider(); st.subheader("👑 VIP - FREE 20% | BRONZE 30% | SILVER 40% | GOLD 50%")
st.write(f"Your VIP: {user.get('vip_level')} - {vip_mult}X")
for lvl,price in [("BRONZE",2000),("SILVER",5000),("GOLD",10000)]:
    if st.button(f"UPGRADE TO {lvl} - N{price}",use_container_width=True,key=lvl): st.link_button(f"Pay {lvl}",f"https://wa.me/{WA}?text=I%20want%20{lvl}%20VIP%20N{price}%20User%20{user['username']}")
st.divider(); st.subheader("💎 STAKING - Locked 7 Days")
stake_amt=st.number_input("Amount to Stake",min_value=1000,max_value=50000,step=1000,value=5000)
if st.button("STAKE NOW",use_container_width=True):
    if user.get("balance",0)-user.get("staked",0)>=stake_amt:
        upd(user['username'], balance=user['balance']-stake_amt, staked=user.get("staked",0)+stake_amt, stake_until=str(datetime.now()+timedelta(days=7))[:19]); add_tx(user['username'],"STAKE",-stake_amt,f"Staked"); st.success(f"Staked N{stake_amt}! Get N{int(stake_amt*1.2)} in 7 days.")
    else: st.error("Not enough available!")
if user.get("staked",0)>0:
    st.info(f"Staked: N{user.get('staked')} | Unlock: {user.get('stake_until')}")
    if user.get("stake_until","") and user.get("stake_until","")<str(datetime.now()):
        if st.button("CLAIM STAKE +20%",use_container_width=True):
            payout=int(user.get("staked",0)*1.2); upd(user['username'], balance=get_user(user['username'])['balance']+payout, staked=0); add_tx(user['username'],"STAKE CLAIM",payout,"Matured"); st.success(f"Claimed N{payout}!"); st.rerun()

# HISTORY + LEADERBOARD + WITHDRAW
st.divider(); st.subheader("📜 History")
for r in DB.execute("SELECT type,amount,detail,time FROM transactions WHERE username=? ORDER BY id DESC LIMIT 10",(user['username'],)).fetchall(): st.write(f"{r[0]} | N{r[1]} | {r[2]}")
st.divider(); st.subheader("🏆 Leaderboard")
for i,row in enumerate(DB.execute("SELECT username,balance,badge FROM users ORDER BY balance DESC LIMIT 5").fetchall(),1): st.write(f"{i}. {row[0]} - N{row[1]} - {row[2]}")
st.divider(); st.subheader("💳 Withdraw - PIN + 3 Attempts Lock")
if not user.get("is_vip",0) and user.get("tasks",0)<30: st.error(f"Complete {30-user.get('tasks',0)} more tasks!")
elif user.get("pin_locked_until","") and user.get("pin_locked_until","")>str(datetime.now()): st.error(f"PIN Locked until {user.get('pin_locked_until')}")
else:
    st.success(f"Available: N{available_balance} (Staked N{user.get('staked',0)} locked)")
    opay=st.text_input("OPay Number",value=user['phone']); pin_in=st.text_input("4-Digit PIN",type="password",max_chars=4)
    if st.button("WITHDRAW NOW",type="primary",use_container_width=True):
        if hash_pw(pin_in)!=user['pin']:
            na=user.get("pin_attempts",0)+1
            if na>=3: lock_until=str(datetime.now()+timedelta(minutes=10))[:19]; upd(user['username'], pin_attempts=0, pin_locked_until=lock_until); st.error(f"Wrong PIN 3x! Locked 10 mins until {lock_until}")
            else: upd(user['username'], pin_attempts=na); st.error(f"Wrong PIN! {3-na} left.")
        elif opay!=user['phone']: st.error("OPay must match signup!")
        elif available_balance<=0: st.error("No available balance!")
        else: upd(user['username'], pin_attempts=0); st.success(f"Withdraw N{available_balance} to {opay} requested!"); st.link_button("Confirm",f"https://wa.me/{WA}?text=Withdraw%20N{available_balance}%20to%20{opay}%20User%20{user['username']}"); add_tx(user['username'],"WITHDRAW REQUEST",available_balance,f"To {opay}")

st.divider(); st.subheader("🎓 Learn N15k | Clone N25k | Custom N100k")
if st.button("LEARN N15k",use_container_width=True): st.link_button("Learn",f"https://wa.me/{WA}?text=Learn%20N15000%20User%20{user['username']}")
if st.button("BUY CLONE N25k - V16 Always Signed In",use_container_width=True): st.link_button("Clone",f"https://wa.me/{WA}?text=Clone%20V16%20N25000%20User%20{user['username']}")

with st.expander("🛡️ ADMIN - Only Taiwo David"):
    ap=st.text_input("Admin Pass",type="password")
    if ap==ADMIN_PASS:
        st.success("Admin Granted")
        tu=DB.execute("SELECT COUNT(*) FROM users").fetchone()[0]; tb=DB.execute("SELECT SUM(balance) FROM users").fetchone()[0] or 0; tt=DB.execute("SELECT COUNT(*) FROM task_logs").fetchone()[0]
        st.write(f"📊 Users: {tu} | User Balances (20%): N{tb} | YOUR 80% Est: N{int(tb*4)} | Tasks: {tt}")
        for r in DB.execute("SELECT username,phone,balance,tasks,vip_level,banned,staked FROM users ORDER BY balance DESC").fetchall():
            c1,c2,c3,c4=st.columns([2,1,1,1]); c1.write(f"{r[0]} {r[1]} Bal N{r[2]} VIP {r[4]} Staked {r[6]} {'BANNED' if r[5] else ''}")
            if c2.button(f"VIP {r[0]}",key=f"av{r[0]}"): upd(r[0],is_vip=1,vip_level="BRONZE"); st.rerun()
            if c3.button(f"Ban {r[0]}",key=f"ab{r[0]}"): upd(r[0],banned=1); st.rerun()
            if c4.button(f"Unban {r[0]}",key=f"aub{r[0]}"): upd(r[0],banned=0); st.rerun()
    elif ap: st.error("Wrong Admin Pass!")
st.caption(f"Taiwo Earn V16 | {FOUNDER} | OPay {PHONE} | 80/20 | Always Signed In | No KeyError | 1 Phone=1 Account")
