import streamlit as st
import hashlib, random, time, json, os
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Taiwo Earn V18 FINAL - By Taiwo David", page_icon="💰", layout="centered")
FOUNDER="Taiwo David"; PHONE="07036325587"; WA="2347036325587"
ADMIN_PASS="TaiwoV18Final2026"
USER_SHARE=0.20; FOUNDER_SHARE=0.80
DB_FILE="users_v18.json"

PRICES={"survey":4000,"game":7500,"cpagrip":20000,"palmpay":7500,"opay":5000,"video":1000,"social":1000,"combo":2500,"cipher":5000,"quiz":1500,"spin":1000,"chest":1000,"checkin":500,"referral":2500,"mission":2500,"luckybox":2000,"mission10":5000}
def user_get(t): return int(PRICES.get(t,500)*USER_SHARE)
def founder_get(t): return int(PRICES.get(t,500)*FOUNDER_SHARE)

LINKS={
 "youtube":"https://youtube.com/@YOUR_CHANNEL","telegram":"https://t.me/YOUR_GROUP","whatsapp_group":"https://chat.whatsapp.com/YOUR_GROUP_LINK",
 "hilltop":"https://hilltopads.com/?ref=YOUR_ID","adsterra":"https://www.adsterra.com/?ref=YOUR_ID","monetag":"https://monetag.com/YOUR_SMARTLINK",
 "cpagrip":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=LOCKER","palmpay":"https://palmpay.com/YOUR_REF_CODE","opay_ref":"https://opay.com/YOUR_REF_CODE",
 "survey1":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=SURVEY","game_offer":"https://www.cpagrip.com/show.php?l=0&u=YOUR_ID&id=GAME","honeygain":"https://r.honeygain.me/YOUR_CODE",
}

# ===== JSON DATABASE - NO SQLITE, NO ERROR =====
def load_data():
    if not os.path.exists(DB_FILE):
        return {"users":{},"logs":[],"txs":[]}
    try:
        with open(DB_FILE,"r") as f: d=json.load(f)
        if "users" not in d: d={"users":{},"logs":[],"txs":[]}
        if "logs" not in d: d["logs"]=[]
        if "txs" not in d: d["txs"]=[]
        return d
    except: return {"users":{},"logs":[],"txs":[]}

def save_data(d):
    try:
        with open(DB_FILE,"w") as f: json.dump(d,f)
    except: pass

DATA=load_data()
def hash_pw(p): return hashlib.sha256(str(p).encode()).hexdigest()
def make_token(u,ph): return hashlib.sha256(f"{u}:{ph}:TaiwoV18".encode()).hexdigest()[:20]
def get_user(u):
    if not u: return None
    user=DATA["users"].get(u)
    if not user: return None
    defaults={"password":"","pin":"","phone":"","balance":0,"tasks":0,"coins":0,"energy":100,"streak":1,"referrals":0,"is_vip":0,"vip_level":"FREE","last_checkin":"","created":"","banned":0,"total_earned":0,"videos_watched":0,"tickets":0,"badge":"Newbie","referrer":"","last_task_time":"","pin_attempts":0,"pin_locked_until":"","staked":0,"stake_until":"","last_luckybox":"","social_open_time":""}
    for k,v in defaults.items():
        if k not in user or user[k] is None: user[k]=v
    return user
def get_by_phone(p):
    for u in DATA["users"].values():
        if u.get("phone")==p: return u
    return None
def add_tx(u,t,a,d):
    DATA["txs"].append({"user":u,"type":t,"amount":a,"detail":d,"time":str(datetime.now())[:19]}); save_data(DATA)
def add_log(u,t,a):
    DATA["logs"].append({"user":u,"task":t,"date":str(date.today()),"amount":a,"time":str(datetime.now())[:19]}); save_data(DATA)
def did_today(u,t):
    today=str(date.today())
    for l in DATA["logs"]:
        if l.get("user")==u and l.get("task")==t and l.get("date")==today: return True
    return False
def did_ever(u,t):
    for l in DATA["logs"]:
        if l.get("user")==u and l.get("task")==t: return True
    return False
def upd(u,**kw):
    if u in DATA["users"]:
        for k,v in kw.items(): DATA["users"][u][k]=v
        save_data(DATA)
def new_cap():
    a=random.randint(2,9); b=random.randint(2,9); st.session_state.captcha_q=f"What is {a} + {b} ?"; st.session_state.captcha_a=a+b

if 'logged' not in st.session_state: st.session_state.logged=False; st.session_state.user=None; st.session_state.captcha_q=""; st.session_state.captcha_a=0; st.session_state.tap_count=0
if not st.session_state.captcha_q: new_cap()

# ALWAYS SIGNED IN
try:
    qp=st.query_params; q_user=qp.get("user",""); q_token=qp.get("token","")
    if q_user and q_token and not st.session_state.logged:
        u=get_user(q_user)
        if u and not u.get("banned",0) and q_token==make_token(u["username"] if "username" in u else q_user, u["password"]):
            st.session_state.logged=True; st.session_state.user=q_user
except: pass

def do_login(username):
    u=get_user(username); token=make_token(username, u["password"])
    st.session_state.logged=True; st.session_state.user=username
    try: st.query_params["user"]=username; st.query_params["token"]=token
    except: pass
    st.rerun()
def do_logout():
    st.session_state.logged=False; st.session_state.user=None
    try: st.query_params.clear()
    except: pass
    st.rerun()

st.title("💰 Taiwo Earn V18 FINAL")
st.caption(f"By {FOUNDER} | OPay {PHONE} | 80% Founder / 20% User | JSON - NO SQLite Error")

if not st.session_state.logged:
    t1,t2=st.tabs(["🔑 LOGIN","📝 SIGN UP"])
    with t1:
        lu=st.text_input("Username",key="lu"); lp=st.text_input("Password",type="password",key="lp")
        st.caption("✅ Stay signed in: After login, bookmark link. Close app, open link = still logged in.")
        if st.button("LOGIN",use_container_width=True,type="primary"):
            u=get_user(lu.strip())
            if not u: st.error("User not found. Sign Up first.")
            elif u.get("banned",0): st.error("BANNED. Contact Founder.")
            elif u.get("pin_locked_until","") and u.get("pin_locked_until","")>str(datetime.now()): st.error("Locked. Wait 10 mins.")
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
            elif get_by_phone(sphone.strip()): st.error("This phone already has account! 1 Phone = 1 Account.")
            else:
                DATA["users"][su.strip()]={"username":su.strip(),"password":hash_pw(sp),"pin":hash_pw(spin),"phone":sphone.strip(),"balance":500,"tasks":0,"coins":0,"energy":100,"streak":1,"referrals":0,"is_vip":0,"vip_level":"FREE","last_checkin":"","created":str(datetime.now())[:10],"banned":0,"total_earned":500,"videos_watched":0,"tickets":0,"badge":"Newbie","referrer":sref.strip(),"last_task_time":"","pin_attempts":0,"pin_locked_until":"","staked":0,"stake_until":"","last_luckybox":"","social_open_time":""}
                save_data(DATA)
                if sref.strip() and get_user(sref.strip()):
                    l1=get_user(sref.strip()); upd(sref.strip(), balance=l1.get('balance',0)+500, referrals=l1.get('referrals',0)+1); add_tx(sref.strip(),"REFERRAL L1",500,f"Invited {su.strip()}")
                do_login(su.strip())
    st.info("🔒 80/20: You 20% | Founder 80% | 1 Phone = 1 Account | Stay Signed In")
    st.stop()

user=get_user(st.session_state.user)
if not user: do_logout()
if user.get("banned",0): st.error("BANNED. Contact Founder."); st.stop()

# Anti-bot
recent=0
try:
    hour_ago=str(datetime.now()-timedelta(hours=1))[:19]
    for l in DATA["logs"]:
        if l.get("user")==user['username'] and l.get("time","")>=hour_ago: recent+=1
except: recent=0
if recent>=20: upd(user['username'], banned=1); st.error("AUTO-BANNED: Bot."); do_logout()

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
st.info(f"💡 80/20: You 20% | Founder 80% | Multiplier {total_mult}X | Staked: N{user.get('staked',0)} | Hour: {recent}/20")
if st.button("LOGOUT", use_container_width=True): do_logout()

def earn(task, label):
    if did_today(user['username'], task): st.warning("⛔ Already claimed today!"); return False
    last=user.get("last_task_time","")
    if last:
        try:
            if (datetime.now()-datetime.strptime(last,"%Y-%m-%d %H:%M:%S")).total_seconds()<3: st.warning("Wait 3 sec!"); return False
        except: pass
    base=user_get(task); amount=int(base*total_mult); f_amount=founder_get(task)
    add_log(user['username'], task, amount)
    fresh=get_user(user['username'])
    if not fresh: return False
    upd(user['username'], balance=fresh.get('balance',0)+amount, tasks=fresh.get('tasks',0)+1, total_earned=fresh.get("total_earned",0)+amount, tickets=fresh.get("tickets",0)+1, last_task_time=str(datetime.now())[:19])
    add_tx(user['username'], label, amount, f"You 20% N{amount} | Founder 80% N{f_amount}")
    st.success(f"+N{amount} (20% of N{PRICES.get(task,500)}). Founder N{f_amount}. +1 Ticket 🎟️")
    return True

st.divider(); st.subheader("🎯 Daily Missions - Do 5 = N500, Do 10 = N1000")
today_tasks=sum(1 for l in DATA["logs"] if l.get("user")==user['username'] and l.get("date")==str(date.today()))
st.write(f"Today: **{today_tasks} / 10**")
if today_tasks>=5 and not did_today(user['username'],"mission5"):
    if st.button("CLAIM MISSION 5 - N500",use_container_width=True,type="primary"): earn("mission","MISSION 5"); st.rerun()
elif today_tasks>=5: st.success("✅ Mission 5 claimed!")
if today_tasks>=10 and not did_today(user['username'],"mission10"):
    if st.button("CLAIM MISSION 10 - N1000",use_container_width=True,type="primary"):
        add_log(user['username'],"mission10",1000); upd(user['username'], balance=get_user(user['username']).get('balance',0)+1000); add_tx(user['username'],"MISSION 10",1000,"10 tasks"); st.success("+N1000!"); st.rerun()
elif today_tasks>=10: st.success("✅ Mission 10 claimed!")

st.divider(); st.subheader("📦 Lucky Box - Every 1 Hour")
last_box=user.get("last_luckybox",""); can_open=True
if last_box:
    try:
        diff=(datetime.now()-datetime.strptime(last_box,"%Y-%m-%d %H:%M:%S")).total_seconds()
        if diff<3600: can_open=False; st.info(f"Next in {int((3600-diff)//60)} mins")
    except: pass
if can_open:
    if st.button("OPEN LUCKY BOX",use_container_width=True):
        prize=random.choice([200,200,500,500,1000]); upd(user['username'], balance=get_user(user['username']).get('balance',0)+prize, last_luckybox=str(datetime.now())[:19]); add_tx(user['username'],"LUCKY BOX",prize,"Hourly"); st.balloons(); st.success(f"Won N{prize}!"); st.rerun()

st.divider(); st.subheader("📅 Daily Check-In")
if user.get("last_checkin","")!=str(date.today()):
    check_amt=int(user_get('checkin')*total_mult)
    if st.button(f"CHECK-IN - N{check_amt}",use_container_width=True,type="primary"):
        fresh=get_user(user['username'])
        upd(user['username'], balance=fresh.get('balance',0)+check_amt, last_checkin=str(date.today()), streak=fresh.get("streak",1)+1, total_earned=fresh.get("total_earned",0)+check_amt)
        add_tx(user['username'],"CHECKIN",check_amt,"Daily")
        st.balloons(); st.success(f"+N{check_amt}!"); st.rerun()
else: st.success(f"✅ Checked in! Streak {user.get('streak')} days")

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

st.divider(); st.subheader("💵 PalmPay / OPay - ONCE EVER - Code TAIWO")
if not did_ever(user['username'],"palmpay"):
    if st.button("DOWNLOAD PALMPAY",use_container_width=True): st.link_button("PalmPay",LINKS['palmpay'])
    code_in=st.text_input("Enter Code after screenshot (TAIWO)", key="palm_code")
    if st.button("I SENT SCREENSHOT - CLAIM PALMPAY",use_container_width=True):
        if code_in.strip().upper()=="TAIWO": earn("palmpay","PALMPAY"); st.rerun()
        else: st.error("Wrong code! Send screenshot to 07036325587 first.")
else: st.success("✅ PalmPay already claimed.")
if not did_ever(user['username'],"opay"):
    if st.button("DOWNLOAD OPAY",use_container_width=True): st.link_button("OPay",LINKS['opay_ref'])
    code2=st.text_input("Enter Code for OPay", key="opay_code")
    if st.button("I SENT SCREENSHOT - CLAIM OPAY",use_container_width=True):
        if code2.strip().upper()=="TAIWO": earn("opay","OPAY"); st.rerun()
        else: st.error("Wrong code!")
else: st.success("✅ OPay already claimed.")

st.divider(); st.subheader("🎁 Temu Referral + Creator Fund")
st.write(f"Referrals: {user.get('referrals')} | Tickets: {user.get('tickets')} | Code: {user['username']}")
st.code(f"Join Taiwo Earn with code {user['username']}")
if user.get("tickets",0)>=100:
    if st.button("🎟️ ENTER LUCKY DRAW N10,000",use_container_width=True,type="primary"): upd(user['username'], tickets=0); add_tx(user['username'],"LUCKY DRAW",0,"Entered"); st.success("Entered Draw!")
st.write("🏆 Top 3 Sunday:")
for u in sorted(DATA["users"].values(), key=lambda x: x.get("balance",0), reverse=True)[:3]: st.write(f"{u.get('username')} - N{u.get('balance',0)}")
st.divider(); st.subheader("🌐 Honeygain - Passive")
if st.button("INSTALL HONEYGAIN",use_container_width=True): st.link_button("Honeygain",LINKS['honeygain']); st.success("Installed!")
st.divider(); st.subheader("💼 Freelance Market")
job=st.selectbox("Service", ["Logo N5000","Video Edit N3000","Flyer N1000","App N25000"])
if st.button("POST SERVICE",use_container_width=True): add_tx(user['username'],"POSTED JOB",0,job); st.success(f"Posted {job}"); st.link_button("Find Buyers",f"https://wa.me/{WA}?text=I%20want%20{job}")

st.divider(); st.subheader("📱 Social - Video - Combo - Cipher - Quiz - Spin - Chest")
def social_task(key,label,link):
    if did_today(user['username'],key): st.success(f"✅ {label} Done!"); return
    st.write(f"**{label} - You N{user_get('social')} (20%)**")
    col_a,col_b=st.columns(2)
    with col_a:
        if st.button(f"1. OPEN {label}",key=f"o_{key}",use_container_width=True): upd(user['username'], social_open_time=str(datetime.now())[:19]); st.link_button(f"Open {label}",link); st.success("Opened! Timer saved.")
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

st.divider(); st.subheader("👆 Tap - Captcha Every 3 Taps")
st.write(f"Anti-Bot: {st.session_state.captcha_q}")
cap2=st.text_input("Answer Captcha to Tap",key="cap_tap")
if st.button("💰 TAP COIN - N5",use_container_width=True):
    if st.session_state.tap_count>=3 and cap2.strip()!=str(st.session_state.captcha_a): st.error("Wrong Captcha!"); new_cap(); st.session_state.tap_count=0
    elif user.get("energy",100)<=0: st.warning("No Energy!")
    else:
        fresh=get_user(user['username']); upd(user['username'], balance=fresh.get('balance',0)+5, coins=fresh.get('coins',0)+1, energy=fresh.get('energy',100)-5); st.session_state.tap_count+=1; st.toast("+N5"); st.rerun()
if st.button("⚡ Refill Energy - Watch Ad",use_container_width=True): upd(user['username'], energy=100, tasks=get_user(user['username']).get('tasks',0)+1); st.link_button("Watch Ad",LINKS['hilltop'])

st.divider(); st.subheader("👑 VIP - FREE 20% | BRONZE 30% | SILVER 40% | GOLD 50%")
st.write(f"Your VIP: {user.get('vip_level')} - {vip_mult}X")
for lvl,price in [("BRONZE",2000),("SILVER",5000),("GOLD",10000)]:
    if st.button(f"UPGRADE TO {lvl} - N{price}",use_container_width=True,key=lvl): st.link_button(f"Pay {lvl}",f"https://wa.me/{WA}?text=I%20want%20{lvl}%20VIP%20N{price}%20User%20{user['username']}")
st.divider(); st.subheader("💎 STAKING - Locked 7 Days")
stake_amt=st.number_input("Amount to Stake",min_value=1000,max_value=50000,step=1000,value=5000)
if st.button("STAKE NOW",use_container_width=True):
    if user.get("balance",0)-user.get("staked",0)>=stake_amt:
        upd(user['username'], balance=user.get("balance",0)-stake_amt, staked=user.get("staked",0)+stake_amt, stake_until=str(datetime.now()+timedelta(days=7))[:19]); add_tx(user['username'],"STAKE",-stake_amt,"Staked"); st.success(f"Staked N{stake_amt}! Get N{int(stake_amt*1.2)} in 7 days.")
    else: st.error("Not enough available!")
if user.get("staked",0)>0:
    st.info(f"Staked: N{user.get('staked')} | Unlock: {user.get('stake_until')}")
    if user.get("stake_until","") and user.get("stake_until","")<str(datetime.now()):
        if st.button("CLAIM STAKE +20%",use_container_width=True):
            payout=int(user.get("staked",0)*1.2); upd(user['username'], balance=get_user(user['username']).get('balance',0)+payout, staked=0); add_tx(user['username'],"STAKE CLAIM",payout,"Matured"); st.success(f"Claimed N{payout}!"); st.rerun()

st.divider(); st.subheader("📜 History")
for r in [x for x in DATA["txs"] if x.get("user")==user['username']][-10:][::-1]: st.write(f"{r.get('type')} | N{r.get('amount')} | {r.get('detail')}")
st.divider(); st.subheader("🏆 Leaderboard")
for i,u in enumerate(sorted(DATA["users"].values(), key=lambda x: x.get("balance",0), reverse=True)[:5],1): st.write(f"{i}. {u.get('username')} - N{u.get('balance',0)} - {u.get('badge')}")
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
if st.button("BUY CLONE N25k - V18 JSON",use_container_width=True): st.link_button("Clone",f"https://wa.me/{WA}?text=Clone%20V18%20N25000%20User%20{user['username']}")

with st.expander("🛡️ ADMIN - Only Taiwo David"):
    ap=st.text_input("Admin Pass",type="password")
    if ap==ADMIN_PASS:
        st.success("Admin Granted")
        tu=len(DATA["users"]); tb=sum(u.get("balance",0) for u in DATA["users"].values()); tt=len(DATA["logs"])
        st.write(f"📊 Users: {tu} | User Balances (20%): N{tb} | YOUR 80% Est: N{int(tb*4)} | Tasks: {tt}")
        for r in sorted(DATA["users"].values(), key=lambda x: x.get("balance",0), reverse=True):
            c1,c2,c3,c4=st.columns([2,1,1,1]); c1.write(f"{r.get('username')} {r.get('phone')} Bal N{r.get('balance')} VIP {r.get('vip_level')} Staked {r.get('staked')} {'BANNED' if r.get('banned') else ''}")
            if c2.button(f"VIP {r.get('username')}",key=f"av{r.get('username')}"): upd(r.get('username'),is_vip=1,vip_level="BRONZE"); st.rerun()
            if c3.button(f"Ban {r.get('username')}",key=f"ab{r.get('username')}"): upd(r.get('username'),banned=1); st.rerun()
            if c4.button(f"Unban {r.get('username')}",key=f"aub{r.get('username')}"): upd(r.get('username'),banned=0); st.rerun()
    elif ap: st.error("Wrong Admin Pass!")
st.caption(f"Taiwo Earn V18 FINAL | {FOUNDER} | OPay {PHONE} | 80/20 | JSON | Always Signed In | No SQLite Error")
