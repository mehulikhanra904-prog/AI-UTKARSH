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
