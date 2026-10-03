const API_BASE="https://ai-utkarsh-3.onrender.com";
const status=document.getElementById("apiStatus"),toast=document.getElementById("toast");
function showToast(message){toast.textContent=message;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),2600)}
async function loadProjects(){try{const res=await fetch(API_BASE+"/api/projects");if(!res.ok)throw new Error();const data=await res.json();if(Array.isArray(data.projects)){const count=document.getElementById("projectCount");if(count)count.textContent=String(data.projects.length).padStart(2,"0")}if(status)status.textContent="● API CONNECTED"}catch(e){if(status)status.textContent="● LOCAL MODE"}}
const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add("visible");observer.unobserve(entry.target)}}),{threshold:.12});
document.querySelectorAll(".metric,.subject-grid article,.gap-grid>div,.projects article,.road,.hero-card").forEach((el,i)=>{el.style.opacity="0";el.style.transform="translateY(18px)";el.style.transition="opacity .65s ease,transform .65s ease";el.style.transitionDelay=(i%5)*60+"ms";observer.observe(el)});
const animationStyle=document.createElement("style");animationStyle.textContent=".visible{opacity:1!important;transform:translateY(0)!important}";document.head.appendChild(animationStyle);
document.getElementById("openProfile")?.addEventListener("click",()=>showToast("Student profile module is ready for the next data layer."));
loadProjects();