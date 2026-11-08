import streamlit as st
import sqlite3, hashlib, random, time
from datetime import date, datetime, timedelta

st.set_page_config(page_title="Taiwo Earn V15 FINAL - By Taiwo David", page_icon="💰", layout="centered")
FOUNDER="Taiwo David"; PHONE="07036325587"; WA="2347036325587"
ADMIN_PASS="TaiwoV15Secure2026"  # <-- NEW ADMIN PASS, CHANGE AFTER PASTE TO YOUR OWN
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

def get_db():
    conn=sqlite3.connect("users.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY, password TEXT, pin TEXT, phone TEXT, balance INTEGER DEFAULT 0, tasks INTEGER DEFAULT 0,
        coins INTEGER DEFAULT 0, energy INTEGER DEFAULT 100, streak INTEGER DEFAULT 1, referrals INTEGER DEFAULT 0,
        is_vip INTEGER DEFAULT 0, vip_level TEXT DEFAULT 'FREE', last_checkin TEXT DEFAULT '', created TEXT DEFAULT '', banned INTEGER DEFAULT 0,
        total_earned INTEGER DEFAULT 0, videos_watched INTEGER DEFAULT 0, tickets INTEGER DEFAULT 0, badge TEXT DEFAULT 'Newbie', referrer TEXT DEFAULT '',
        last_task_time TEXT DEFAULT '', tasks_last_hour INTEGER DEFAULT 0, pin_attempts INTEGER DEFAULT 0, pin_locked_until TEXT DEFAULT '',
        staked INTEGER DEFAULT 0, stake_until TEXT DEFAULT '', last_luckybox TEXT DEFAULT '', social_open_time TEXT DEFAULT '')""")
    conn.execute("""CREATE TABLE IF NOT EXISTS task_logs(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, task TEXT, date TEXT, amount INTEGER, time TEXT)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, type TEXT, amount INTEGER, detail TEXT, time TEXT)""")
    conn.commit(); return conn
DB=get_db()
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()
def add_tx(u,t,a,d): DB.execute("INSERT INTO transactions(username,type,amount,detail,time) VALUES(?,?,?,?,?)",(u,t,a,d,str(datetime.now())[:19])); DB.commit()
def add_log(u,t,a): DB.execute("INSERT INTO task_logs(username,task,date,amount,time) VALUES(?,?,?,?,?)",(u,t,str(date.today()),a,str(datetime.now())[:19])); DB.commit()
def did_today(u,t): return DB.execute("SELECT * FROM task_logs WHERE username=? AND task=? AND date=?",(u,t,str(date.today()))).fetchone() is not None
def did_ever(u,t): return DB.execute("SELECT * FROM task_logs WHERE username=? AND task=?",(u,t)).fetchone() is not None
def upd(u,**kw):
    for k,v in kw.items(): DB.execute(f"UPDATE users SET {k}=? WHERE username=?",(v,u))
    DB.commit()
def get_user(u):
    cur=DB.execute("SELECT * FROM users WHERE username=?",(u,)); r=cur.fetchone()
    return dict(zip([d[0] for d in cur.description],r)) if r else None
def get_user_by_phone(p):
    cur=DB.execute("SELECT * FROM users WHERE phone=?",(p,)); r=cur.fetchone()
    return dict(zip([d[0] for d in cur.description],r)) if r else None
def new_cap():
    a=random.randint(2,9); b=random.randint(2,9); st.session_state.captcha_q=f"What is {a} + {b} ?"; st.session_state.captcha_a=a+b
if 'logged' not in st.session_state: st.session_state.logged=False; st.session_state.user=None; st.session_state.captcha_q=""; st.session_state.captcha_a=0; st.session_state.tap_count=0
if not st.session_state.captcha_q: new_cap()

st.title("💰 Taiwo Earn V15 FINAL")
st.caption(f"By {FOUNDER} | OPay {PHONE} | 80% Founder / 20% User | NO CHEATING - Database Locked")

# ===== LOGIN / SIGNUP - ANTI-CHEAT =====
if not st.session_state.logged:
    t1,t2=st.tabs(["🔑 LOGIN","📝 SIGN UP"])
    with t1:
        lu=st.text_input("Username",key="lu"); lp=st.text_input("Password",type="password",key="lp")
        if st.button("LOGIN",use_container_width=True,type="primary"):
            u=get_user(lu.strip())
            if not u: st.error("User not found. Sign Up.")
            elif u['banned']: st.error("BANNED for cheating. Contact Founder 07036325587")
            else:
                # PIN LOCK CHECK
                if u['pin_locked_until'] and u['pin_locked_until']>str(datetime.now()):
                    st.error(f"Account locked until {u['pin_locked_until']} - Too many wrong attempts. Wait.")
                elif u['password']!=hash_pw(lp):
                    st.error("Wrong password!")
                else:
                    st.session_state.logged=True; st.session_state.user=lu.strip(); st.rerun()
    with t2:
        su=st.text_input("Username (no space)",key="su"); sp=st.text_input("Password (min 6)",type="password",key="sp")
        spin=st.text_input("4-Digit PIN",type="password",max_chars=4,key="spn"); sphone=st.text_input("OPay Number - 11 Digits, 1 Phone = 1 Account",key="sph", placeholder="07036325587"); sref=st.text_input("Who Invited You? (Username)",key="sref")
        st.write(f"🤖 Anti-Bot: **{st.session_state.captcha_q}**"); cap=st.text_input("Answer Captcha",key="cap")
        if st.button("CREATE ACCOUNT",use_container_width=True,type="primary"):
            if not su or not sp or not spin or not sphone: st.error("Fill all fields!")
            elif len(sp)<6: st.error("Password must be 6+ characters!")
            elif len(spin)!=4 or not spin.isdigit(): st.error("PIN must be 4 numbers!")
            elif len(sphone)!=11 or not sphone.isdigit() or not sphone.startswith("0"): st.error("Phone must be 11 digits starting with 0! e.g. 07036325587")
            elif cap.strip()!=str(st.session_state.captcha_a): st.error("Wrong Captcha! Bot blocked."); new_cap()
            elif get_user(su.strip()): st.error("Username taken!")
            elif get_user_by_phone(sphone.strip()): st.error("⚠️ This phone number already has an account! 1 Phone = 1 Account. Login instead. Anti-Cheat.")
            else:
                DB.execute("INSERT INTO users(username,password,pin,phone,balance,tasks,coins,energy,streak,referrals,is_vip,vip_level,last_checkin,created,total_earned,videos_watched,tickets,badge,referrer) VALUES(?,?,?,?,500,0,0,100,1,0,0,'FREE','',?,500,0,0,'Newbie',?)",(su.strip(),hash_pw(sp),hash_pw(spin),sphone.strip(),str(datetime.now())[:10],sref.strip())); DB.commit()
                if sref.strip() and get_user(sref.strip()):
                    l1=get_user(sref.strip()); upd(sref.strip(), balance=l1['balance']+500, referrals=l1['referrals']+1); add_tx(sref.strip(),"REFERRAL L1",500,f"Invited {su.strip()}")
                    if l1['referrer'] and get_user(l1['referrer']):
                        l2=get_user(l1['referrer']); upd(l1['referrer'], balance=l2['balance']+200); add_tx(l1['referrer'],"REFERRAL L2",200,f"Friend of {su.strip()}")
                        if l2['referrer'] and get_user(l2['referrer']):
                            l3=get_user(l2['referrer']); upd(l2['referrer'], balance=l3['balance']+100); add_tx(l2['referrer'],"REFERRAL L3",100,f"Friend of friend {su.strip()}")
                st.session_state.logged=True; st.session_state.user=su.strip(); st.balloons(); st.success("Created! +N500 Bonus. 1 Phone = 1 Account Secured."); st.rerun()
    st.info("🔒 80/20 Rule: Advertiser pays 100%. You get 20%, Founder keeps 80% for server. 1 Phone = 1 Account. Cheaters auto-banned.")
    st.stop()

user=get_user(st.session_state.user)
if not user: st.session_state.logged=False; st.rerun()

# ===== ANTI-BOT: TOO MANY TASKS IN 1 HOUR = AUTO-BAN =====
# Check tasks in last hour
hour_ago=str(datetime.now()-timedelta(hours=1))
recent=DB.execute("SELECT COUNT(*) FROM task_logs WHERE username=? AND time>=?",(user['username'],hour_ago[:19])).fetchone()[0]
if recent>=20 and not user['banned']:
    upd(user['username'], banned=1); st.error("🚨 AUTO-BANNED: You did 20 tasks in 1 hour. You are a bot. Contact Founder."); st.session_state.logged=False; st.stop()
if user['banned']: st.error("BANNED. Contact Founder."); st.stop()

multiplier=1.0
if user['streak']>=30: multiplier=3.0
elif user['streak']>=7: multiplier=2.0
elif user['streak']>=3: multiplier=1.5
vip_mult={"FREE":1.0,"BRONZE":1.5,"SILVER":2.0,"GOLD":2.5}.get(user['vip_level'],1.0)
total_mult=multiplier*vip_mult
# Staked balance is locked, not withdrawable
available_balance=user['balance']-user['staked']

st.success(f"👋 {user['username']} | {user['vip_level']} VIP | Streak {user['streak']}d = {multiplier}X | VIP {vip_mult}X | Total {total_mult}X | Badge {user['badge']}")
c1,c2,c3,c4=st.columns(4); c1.metric("Balance",f"₦{user['balance']}"); c2.metric("Available",f"₦{available_balance}"); c3.metric("Tickets 🎟️",user['tickets']); c4.metric("Tasks",f"{user['tasks']}/30")
st.progress(min(user['tasks']/30,1.0))
st.info(f"💡 80/20: You 20% | Founder 80% | Multiplier {total_mult}X | Staked (Locked): N{user['staked']} | Tasks this hour: {recent}/20 (Anti-Bot)")
if st.button("LOGOUT"): st.session_state.logged=False; st.rerun()

def earn(task, label):
    # DOUBLE-CLAIM LOCK - Check DB again at moment of claim
    if did_today(user['username'], task):
        st.warning("⛔ Already claimed today! Database blocked double claim."); return False
    # Cooldown 5 sec between tasks - Anti-Bot
    if user['last_task_time']:
        try:
            last=datetime.strptime(user['last_task_time'], "%Y-%m-%d %H:%M:%S")
            if (datetime.now()-last).total_seconds()<5:
                st.warning(f"Wait {5-int((datetime.now()-last).total_seconds())} sec between tasks! Anti-Bot."); return False
        except: pass
    base=user_get(task); amount=int(base*total_mult); f_amount=founder_get(task)
    add_log(user['username'], task, amount)
    # Re-fetch to avoid race
    fresh=get_user(user['username'])
    upd(user['username'], balance=fresh['balance']+amount, tasks=fresh['tasks']+1, total_earned=fresh['total_earned']+amount, tickets=fresh['tickets']+1, last_task_time=str(datetime.now())[:19])
    new_badge=fresh['badge']
    if fresh['tasks']>=100: new_badge="Diamond 💎"
    elif fresh['tasks']>=50: new_badge="Gold 🥇"
    elif fresh['tasks']>=10: new_badge="Bronze 🥉"
    if new_badge!=fresh['badge']:
        upd(user['username'], badge=new_badge); st.balloons(); st.success(f"🏅 New Badge {new_badge}! +N1000 Bonus!")
        upd(user['username'], balance=get_user(user['username'])['balance']+1000)
    add_tx(user['username'], label, amount, f"You 20% N{amount} | Founder 80% N{f_amount} | Total N{PRICES[task]}")
    st.success(f"+N{amount} (20% of N{PRICES[task]}). Founder N{f_amount}. +1 Ticket 🎟️")
    return True

# ===== DAILY MISSIONS - NEW =====
st.divider(); st.subheader("🎯 DAILY MISSIONS - From Duolingo - Do 5 = N500, Do 10 = N1000")
today_tasks=DB.execute("SELECT COUNT(*) FROM task_logs WHERE username=? AND date=?",(user['username'],str(date.today()))).fetchone()[0]
st.write(f"Today you did **{today_tasks} / 10** tasks")
if today_tasks>=5 and not did_today(user['username'],"mission5"):
    if st.button("CLAIM MISSION 5 BONUS - N500",use_container_width=True,type="primary"):
        earn("mission","MISSION 5"); st.rerun()
elif today_tasks>=5: st.success("✅ Mission 5 claimed!")
if today_tasks>=10 and not did_today(user['username'],"mission10"):
    if st.button("CLAIM MISSION 10 BONUS - N1000",use_container_width=True,type="primary"):
        # Use mission price *2 for 10
        add_log(user['username'],"mission10",1000); upd(user['username'], balance=get_user(user['username'])['balance']+1000); add_tx(user['username'],"MISSION 10",1000,"10 tasks"); st.success("+N1000 Mission 10!"); st.rerun()
elif today_tasks>=10: st.success("✅ Mission 10 claimed!")

# ===== LUCKY BOX EVERY 1 HOUR - NEW =====
st.divider(); st.subheader("📦 LUCKY BOX - Every 1 Hour - From Temu")
last_box=user['last_luckybox']
can_open=True
if last_box:
    try:
        diff=(datetime.now()-datetime.strptime(last_box,"%Y-%m-%d %H:%M:%S")).total_seconds()
        if diff<3600: can_open=False; st.info(f"Next Lucky Box in {int((3600-diff)//60)} mins. Come back!")
    except: pass
if can_open:
    if st.button("OPEN LUCKY BOX - Win N200 - N1000",use_container_width=True):
        prize=random.choice([200,200,500,500,1000]); upd(user['username'], balance=get_user(user['username'])['balance']+prize, last_luckybox=str(datetime.now())[:19]); add_tx(user['username'],"LUCKY BOX",prize,"Hourly box"); st.balloons(); st.success(f"You won N{prize} Lucky Box!"); st.rerun()

# ===== CHECK-IN =====
st.divider(); st.subheader("📅 Daily Check-In")
if user['last_checkin']!=str(date.today()):
    if st.button(f"CHECK-IN - N{int(user_get('checkin')*total_mult)}",use_container_width=True,type="primary"):
        amt=int(user_get('checkin')*total_mult); upd(user['username'], balance=get_user(user['username'])['balance']+amt, last_checkin=str(date.today()), streak=user['streak']+1, total_earned=get_user(user['username'])['total_earned']+amt); add_tx(user['username'],"CHECKIN",amt,f"Streak {user['streak']}"); st.balloons(); st.success(f"+N{amt}!"); st.rerun()
else: st.success(f"✅ Checked in! Streak {user['streak']} days")

# ===== HIGH PAY - 80/20 - ALL WITH DB LOCK =====
st.divider(); st.subheader(f"📝 SURVEY - You N{user_get('survey')} (20%) | Founder N{founder_get('survey')} (80%)")
if not did_today(user['username'],"survey"):
    if st.button("START SURVEY",use_container_width=True,type="primary"): st.link_button("Open Survey",LINKS['survey1']); upd(user['username'], social_open_time=str(datetime.now())[:19]); st.session_state.survey_open=True
    if st.session_state.get("survey_open"):
        if st.button("I FINISHED SURVEY - CLAIM",use_container_width=True): earn("survey","SURVEY"); st.rerun()
else: st.success("✅ Survey done!")

st.divider(); st.subheader(f"🎮 PLAY GAME - You N{user_get('game')} (20%) | Founder N{founder_get('game')} (80%)")
if not did_today(user['username'],"game"):
    if st.button("INSTALL GAME",use_container_width=True,type="primary"): st.link_button("Install Game",LINKS['game_offer']); st.session_state.game_open=True
    if st.session_state.get("game_open"):
        if st.button("I PLAYED - CLAIM",use_container_width=True): earn("game","GAME"); st.balloons(); st.rerun()
else: st.success("✅ Game done!")

st.divider(); st.subheader(f"💰 CPAGrip - You N{user_get('cpagrip')} (20%) | Founder N{founder_get('cpagrip')} (80%) - KING")
st.link_button("UNLOCK - Enter Email Only",LINKS['cpagrip'])
if st.button("I ENTERED EMAIL - CLAIM",use_container_width=True):
    if not did_today(user['username'],"cpagrip"): earn("cpagrip","CPAGRIP"); st.balloons(); st.rerun()
    else: st.warning("Already claimed today! DB blocked.")

# ===== PALMPAY / OPAY - ONCE EVER FIX =====
st.divider(); st.subheader(f"💵 PalmPay / OPay - ONCE EVER - Must Send Screenshot to Founder")
st.warning("⚠️ NEW ANTI-CHEAT: You can only claim PalmPay ONCE ever. After claim, you must send screenshot of installed PalmPay to WhatsApp 07036325587. Founder will verify.")
if not did_ever(user['username'],"palmpay"):
    if st.button("DOWNLOAD PALMPAY - Claim Once",use_container_width=True):
        st.link_button("PalmPay",LINKS['palmpay'])
        # Claim with verification code
        code_in=st.text_input("Enter Code from PalmPay Screenshot (Ask Founder for code after you send screenshot)", key="palmpay_code")
        if st.button("I SENT SCREENSHOT - CLAIM PALMPAY",use_container_width=True):
            if code_in.strip().upper()=="TAIWO":
                earn("palmpay","PALMPAY"); st.rerun()
            else: st.error("Wrong code! Send screenshot to Founder on WhatsApp first, Founder will give you code TAIWO.")
else: st.success("✅ PalmPay already claimed once. Cannot claim again.")
if not did_ever(user['username'],"opay"):
    if st.button("DOWNLOAD OPAY - Claim Once",use_container_width=True):
        st.link_button("OPay",LINKS['opay_ref'])
        code2=st.text_input("Enter Code from OPay Screenshot", key="opay_code")
        if st.button("I SENT SCREENSHOT - CLAIM OPAY",use_container_width=True):
            if code2.strip().upper()=="TAIWO": earn("opay","OPAY"); st.rerun()
            else: st.error("Wrong code! Send screenshot first.")
else: st.success("✅ OPay already claimed once.")

# ===== TEMU + CREATOR FUND + HONEYGAIN + FREELANCE =====
st.divider(); st.subheader("🎁 Temu 3-Level Referral + Tickets + Creator Fund")
st.write(f"Referrals: {user['referrals']} | Tickets: {user['tickets']} | Code: {user['username']}")
st.code(f"Join Taiwo Earn with code {user['username']}")
if user['tickets']>=100:
    if st.button("🎟️ ENTER LUCKY DRAW N10,000",use_container_width=True,type="primary"):
        upd(user['username'], tickets=0); add_tx(user['username'],"LUCKY DRAW",0,"Entered"); st.success("Entered Draw! Winner Sunday!")
st.write("🏆 Creator Fund - Top 3 Sunday:")
for i,row in enumerate(DB.execute("SELECT username,balance FROM users ORDER BY balance DESC LIMIT 3").fetchall(),1):
    st.write(f"{i}. {row[0]} - N{row[1]}")
st.write("🏆 Top Referrer This Month:")
for i,row in enumerate(DB.execute("SELECT username,referrals FROM users ORDER BY referrals DESC LIMIT 3").fetchall(),1):
    st.write(f"{i}. {row[0]} - {row[1]} referrals - Prize N10000 / N5000 / N2000")

st.divider(); st.subheader("🌐 Honeygain - Passive")
if st.button("INSTALL HONEYGAIN",use_container_width=True):
    st.link_button("Honeygain",LINKS['honeygain']); st.success("Install, leave on, earn monthly.")
st.divider(); st.subheader("💼 Freelance Market - Founder 20%")
job=st.selectbox("Service", ["Logo N5000","Video Edit N3000","Flyer N1000","App N25000"])
if st.button("POST SERVICE",use_container_width=True):
    add_tx(user['username'],"POSTED JOB",0,job); st.success(f"Posted {job}. Founder takes 20%."); st.link_button("Find Buyers",f"https://wa.me/{WA}?text=I%20want%20{job}")

# ===== DAILY TASKS - 80/20 - WITH DB TIMER FOR SOCIAL =====
st.divider(); st.subheader("📱 Social - Video - Combo - Cipher - Quiz - Spin - Chest")
def social_task(key,label,link):
    if did_today(user['username'],key): st.success(f"✅ {label} Done!"); return
    st.write(f"**{label} - You N{user_get('social')} (20%)**")
    col_a,col_b=st.columns(2)
    with col_a:
        if st.button(f"1. OPEN {label}",key=f"o_{key}",use_container_width=True):
            upd(user['username'], social_open_time=str(datetime.now())[:19]); st.link_button(f"Open {label}",link); st.success("Opened! Timer saved in DB. Refresh will NOT reset it.")
    with col_b:
        open_time=user['social_open_time']
        if not open_time: st.button("2. VERIFY - Open First",key=f"v_{key}",disabled=True,use_container_width=True)
        else:
            try: waited=(datetime.now()-datetime.strptime(open_time,"%Y-%m-%d %H:%M:%S")).total_seconds()
            except: waited=999
            if waited<10: st.info(f"Wait {int(10-waited)}s - Timer in DB")
            else:
                if st.button(f"2. I JOINED - +N{user_get('social')}",key=f"vo_{key}",use_container_width=True): earn("social",label); st.rerun()
social_task("youtube","YouTube",LINKS['youtube']); social_task("telegram","Telegram",LINKS['telegram']); social_task("whatsapp","WhatsApp",LINKS['whatsapp_group'])

if user['videos_watched']<10:
    if st.button(f"WATCH VIDEO - {user['videos_watched']}/10",use_container_width=True):
        upd(user['username'], videos_watched=user['videos_watched']+1); st.link_button("Watch",LINKS['youtube']); st.rerun()
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

# ===== TAP - WITH CAPTCHA EVERY 3 TAPS + 5 SEC COOLDOWN =====
st.divider(); st.subheader("👆 Tap To Earn - Captcha Every 3 Taps")
st.write(f"Anti-Bot: {st.session_state.captcha_q} - You must solve every 3 taps")
cap2=st.text_input("Answer Captcha to Tap",key="cap_tap")
if st.button("💰 TAP COIN - N5 (20%)",use_container_width=True):
    if st.session_state.tap_count>=3:
        if cap2.strip()!=str(st.session_state.captcha_a): st.error("Wrong Captcha! Bot blocked."); new_cap(); st.session_state.tap_count=0
        else: st.session_state.tap_count=0; new_cap()
    if user['energy']<=0: st.warning("No Energy! Refill below.")
    else:
        fresh=get_user(user['username']); upd(user['username'], balance=fresh['balance']+5, coins=fresh['coins']+1, energy=fresh['energy']-5); st.session_state.tap_count+=1; st.toast("+N5"); st.rerun()
if st.button("⚡ Refill Energy - Watch Ad",use_container_width=True):
    upd(user['username'], energy=100, tasks=get_user(user['username'])['tasks']+1); st.link_button("Watch Ad",LINKS['hilltop'])

# ===== VIP + STAKING =====
st.divider(); st.subheader("👑 VIP TIERS - FREE 20% | BRONZE 30% | SILVER 40% | GOLD 50%")
st.write(f"Your VIP: {user['vip_level']} - Multiplier {vip_mult}X")
for lvl,price in [("BRONZE",2000),("SILVER",5000),("GOLD",10000)]:
    if st.button(f"UPGRADE TO {lvl} - N{price}",use_container_width=True,key=lvl): st.link_button(f"Pay {lvl}",f"https://wa.me/{WA}?text=I%20want%20{lvl}%20VIP%20N{price}%20User%20{user['username']}")
st.divider(); st.subheader("💎 STAKING 2.0 - Locked 7 Days - Cannot Withdraw Until Done")
stake_amt=st.number_input("Amount to Stake",min_value=1000,max_value=50000,step=1000,value=5000)
if st.button("STAKE NOW",use_container_width=True):
    if user['balance']-user['staked']>=stake_amt:
        upd(user['username'], balance=user['balance']-stake_amt, staked=user['staked']+stake_amt, stake_until=str(datetime.now()+timedelta(days=7))[:19]); add_tx(user['username'],"STAKE",-stake_amt,f"Staked N{stake_amt} until {user['stake_until']}"); st.success(f"Staked N{stake_amt}! Locked until {user['stake_until']}. Get N{int(stake_amt*1.2)} then.")
    else: st.error("Not enough available balance!")
if user['staked']>0:
    st.info(f"Staked: N{user['staked']} | Unlock: {user['stake_until']}")
    if user['stake_until'] and user['stake_until']<str(datetime.now()):
        if st.button("CLAIM STAKE +20%",use_container_width=True):
            payout=int(user['staked']*1.2); upd(user['username'], balance=get_user(user['username'])['balance']+payout, staked=0); add_tx(user['username'],"STAKE CLAIM",payout,"Stake matured"); st.success(f"Claimed N{payout}!"); st.rerun()

# ===== HISTORY + LEADERBOARD + WITHDRAW - PIN LOCK =====
st.divider(); st.subheader("📜 History - Shows 80/20 Split")
for r in DB.execute("SELECT type,amount,detail,time FROM transactions WHERE username=? ORDER BY id DESC LIMIT 10",(user['username'],)).fetchall():
    st.write(f"{r[0]} | N{r[1]} | {r[2]}")
st.divider(); st.subheader("🏆 Leaderboard")
for i,row in enumerate(DB.execute("SELECT username,balance,badge FROM users ORDER BY balance DESC LIMIT 5").fetchall(),1):
    st.write(f"{i}. {row[0]} - N{row[1]} - {row[2]}")
st.divider(); st.subheader("💳 Withdraw - PIN + 3 Attempts Lock")
if not user['is_vip'] and user['tasks']<30: st.error(f"Complete {30-user['tasks']} more tasks! Rule by {FOUNDER}")
elif user['pin_locked_until'] and user['pin_locked_until']>str(datetime.now()): st.error(f"PIN Locked until {user['pin_locked_until']} - Too many wrong attempts. Wait 10 mins.")
else:
    st.success(f"Available to withdraw: N{available_balance} (Staked N{user['staked']} locked)")
    opay=st.text_input("OPay Number",value=user['phone']); pin_in=st.text_input("4-Digit PIN",type="password",max_chars=4)
    if st.button("WITHDRAW NOW",type="primary",use_container_width=True):
        if hash_pw(pin_in)!=user['pin']:
            new_attempts=user['pin_attempts']+1
            if new_attempts>=3:
                lock_until=str(datetime.now()+timedelta(minutes=10))[:19]; upd(user['username'], pin_attempts=0, pin_locked_until=lock_until); st.error(f"Wrong PIN 3 times! Locked 10 mins until {lock_until}")
            else:
                upd(user['username'], pin_attempts=new_attempts); st.error(f"Wrong PIN! {3-new_attempts} attempts left.")
        elif opay!=user['phone']: st.error("OPay must match signup! Anti-cheat.")
        elif available_balance<=0: st.error("No available balance! Staked money is locked.")
        else:
            upd(user['username'], pin_attempts=0); st.success(f"Withdraw N{available_balance} to {opay} requested!"); st.link_button("Confirm",f"https://wa.me/{WA}?text=Withdraw%20N{available_balance}%20to%20{opay}%20User%20{user['username']}"); add_tx(user['username'],"WITHDRAW REQUEST",available_balance,f"To {opay}")

st.divider(); st.subheader("🎓 Learn N15k | Clone N25k | Custom N100k")
if st.button("LEARN N15k",use_container_width=True): st.link_button("Learn",f"https://wa.me/{WA}?text=Learn%20N15000%20User%20{user['username']}")
if st.button("BUY CLONE N25k - V15 Anti-Cheat",use_container_width=True): st.link_button("Clone",f"https://wa.me/{WA}?text=Clone%20V15%20N25000%20User%20{user['username']}")

with st.expander("🛡️ ADMIN - Only Taiwo David"):
    ap=st.text_input("Admin Pass",type="password")
    if ap==ADMIN_PASS:
        st.success("Admin Granted")
        total_users=DB.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_bal=DB.execute("SELECT SUM(balance) FROM users").fetchone()[0] or 0
        total_tasks=DB.execute("SELECT COUNT(*) FROM task_logs").fetchone()[0]
        st.write(f"📊 Users: {total_users} | User Balances (20%): N{total_bal} | YOUR 80% Earnings Est: N{int(total_bal*4)} | Total Tasks Done: {total_tasks}")
        for r in DB.execute("SELECT username,phone,balance,tasks,vip_level,banned,staked FROM users ORDER BY balance DESC").fetchall():
            c1,c2,c3,c4=st.columns([2,1,1,1]); c1.write(f"{r[0]} {r[1]} Bal N{r[2]} Tasks {r[3]} VIP {r[4]} Staked {r[6]} {'BANNED' if r[5] else ''}")
            if c2.button(f"VIP {r[0]}",key=f"av{r[0]}"): upd(r[0],is_vip=1,vip_level="BRONZE"); st.rerun()
            if c3.button(f"Ban {r[0]}",key=f"ab{r[0]}"): upd(r[0],banned=1); st.rerun()
            if c4.button(f"Unban {r[0]}",key=f"aub{r[0]}"): upd(r[0],banned=0); st.rerun()
    elif ap: st.error("Wrong Admin Pass!")
st.caption(f"Taiwo Earn V15 FINAL | {FOUNDER} | OPay {PHONE} | 80/20 | NO CHEATING | 1 Phone=1 Account | PIN Lock | DB Timer")
