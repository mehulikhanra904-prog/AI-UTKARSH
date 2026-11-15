const API_BASE="https://ai-utkarsh-3.onrender.com";
const status=document.getElementById("apiStatus"),toast=document.getElementById("toast");
function showToast(message){toast.textContent=message;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),2600)}
async function loadProjects(){try{const res=await fetch(API_BASE+"/api/projects");if(!res.ok)throw new Error();const data=await res.json();if(Array.isArray(data.projects)){const count=document.getElementById("projectCount");if(count)count.textContent=String(data.projects.length).padStart(2,"0")}if(status)status.textContent="● API CONNECTED"}catch(e){if(status)status.textContent="● LOCAL MODE"}}
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("visible");observer.unobserve(entry.target)}}),{threshold:.12});
document.querySelectorAll(".metric,.subject-grid article,.gap-grid>div,.projects article,.road,.hero-card").forEach((el,i)=>{el.style.opacity="0";el.style.transform="translateY(18px)";el.style.transition="opacity .65s ease,transform .65s ease";el.style.transitionDelay=(i%5)*60+"ms";observer.observe(el)});
const animationStyle=document.createElement("style");animationStyle.textContent=".visible{opacity:1!important;transform:translateY(0)!important}";document.head.appendChild(animationStyle);
document.getElementById("openProfile")?.addEventListener("click",()=>showToast("Student profile module is ready for the next data layer."));
loadProjects();
/* Daily focus tracker — persists in this browser */
(()=>{
 const checks=[...document.querySelectorAll("[data-focus]")],key="utkarsh_daily_focus_v1";
 const dateEl=document.getElementById("focusDate");
 if(dateEl)dateEl.textContent=new Date().toLocaleDateString(undefined,{weekday:"short",day:"2-digit",month:"short"}).toUpperCase();
 let state={date:new Date().toDateString(),done:[false,false,false]};
 try{const saved=JSON.parse(localStorage.getItem(key)||"null");if(saved&&saved.date===state.date)state=saved}catch(e){}
 const count=document.getElementById("focusCount"),pct=document.getElementById("focusPercent"),bar=document.getElementById("focusBar");
 function paint(){const n=state.done.filter(Boolean).length;checks.forEach((c,i)=>c.checked=!!state.done[i]);if(count)count.textContent=n+" / 3 complete";if(pct)pct.textContent=Math.round(n/3*100)+"%";if(bar)bar.style.width=(n/3*100)+"%";localStorage.setItem(key,JSON.stringify(state))}
 checks.forEach((c,i)=>c.addEventListener("change",()=>{state.done[i]=c.checked;paint()}));paint();
})();

/* Accessible mobile navigation */
(()=>{const toggle=document.getElementById("menuToggle"),nav=document.querySelector(".nav nav");if(!toggle||!nav)return;toggle.addEventListener("click",()=>{const open=nav.classList.toggle("open");toggle.setAttribute("aria-expanded",String(open));toggle.textContent=open?"✕":"☰"});nav.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{nav.classList.remove("open");toggle.setAttribute("aria-expanded","false");toggle.textContent="☰"}));})();

/* Account + profile API integration */
(()=>{
 const API=API_BASE,modal=document.getElementById("authModal"),form=document.getElementById("authForm"),message=document.getElementById("authMessage");
 if(!modal||!form)return;
 let mode="login",token=localStorage.getItem("utkarsh_token"),user=null;
 const el=id=>document.getElementById(id);
 function setMsg(t,good=false){message.textContent=t;message.style.color=good?"#55764b":"#a45d45"}
 function showModal(){modal.classList.add("open");modal.setAttribute("aria-hidden","false");setMsg("");el("authEmail").focus()}
 function hideModal(){modal.classList.remove("open");modal.setAttribute("aria-hidden","true")}
 function setMode(next){mode=next;document.querySelectorAll("[data-auth]").forEach(b=>b.classList.toggle("active",b.dataset.auth===mode));el("authNameLabel").style.display=mode==="register"?"grid":"none";el("authTitle").textContent=mode==="register"?"Create your account.":"Welcome back.";el("authSubmit").textContent=mode==="register"?"Create account →":"Sign in →";el("authPassword").autocomplete=mode==="register"?"new-password":"current-password";setMsg("")}
 document.querySelectorAll("[data-auth]").forEach(b=>b.addEventListener("click",()=>setMode(b.dataset.auth)));
 el("authOpen").addEventListener("click",showModal);el("authClose").addEventListener("click",hideModal);modal.addEventListener("click",e=>{if(e.target===modal)hideModal()});document.addEventListener("keydown",e=>{if(e.key==="Escape")hideModal()});
 el("openProfile")?.addEventListener("click",()=>document.getElementById("profile").scrollIntoView({behavior:"smooth"}));
 function showUser(u){user=u;el("profileName").textContent=u.name;el("profileEmail").textContent=u.email;el("profileAvatar").textContent=(u.name||"U").trim().charAt(0).toUpperCase();el("authOpen").textContent="Account ✓";el("signOut").hidden=false;const p=u.profile||{};el("college").value=p.college||"";el("degree").value=p.degree||"B.Tech CSE";el("semester").value=String(p.semester||1);el("targetRole").value=p.target_role||"AI/ML Engineer";el("dailyHours").value=p.daily_hours??2}
 async function request(path,opts={}){const r=await fetch(API+path,{...opts,headers:{...(opts.headers||{}),...(token?{Authorization:"Bearer "+token}:{})}});const d=await r.json().catch(()=>({detail:"Unexpected server response"}));if(!r.ok)throw Error(d.detail||"Request failed");return d}
 form.addEventListener("submit",async e=>{e.preventDefault();setMsg("Connecting…");el("authSubmit").disabled=true;try{const body={email:el("authEmail").value,password:el("authPassword").value};if(mode==="register")body.name=el("authName").value;const d=await request("/api/auth/"+mode,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});token=d.token;localStorage.setItem("utkarsh_token",token);showUser(d.user);hideModal();el("profileMessage").textContent="Account ready. Your profile is now connected."}catch(e){setMsg(e.message)}finally{el("authSubmit").disabled=false}});
 el("profileForm").addEventListener("submit",async e=>{e.preventDefault();const out=el("profileMessage");if(!token){out.textContent="Sign in first to save your profile.";showModal();return}out.textContent="Saving profile…";try{const profile={college:el("college").value,degree:el("degree").value,semester:Number(el("semester").value),target_role:el("targetRole").value,daily_hours:Number(el("dailyHours").value),skills:user?.profile?.skills||{}};const d=await request("/api/profile/me",{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(profile)});user.profile=d.profile;out.textContent="Profile saved securely to your account ✓"}catch(e){out.textContent=e.message}});
 el("signOut").addEventListener("click",()=>{token=null;user=null;localStorage.removeItem("utkarsh_token");el("profileName").textContent="Guest learner";el("profileEmail").textContent="Create an account to save your profile online.";el("profileAvatar").textContent="U";el("authOpen").textContent="Sign in ↗";el("signOut").hidden=true;el("profileMessage").textContent="Signed out."});
 async function restore(){if(!token)return;try{const d=await request("/api/profile/me");showUser(d.user)}catch(e){token=null;localStorage.removeItem("utkarsh_token")}}
 restore();
})();
