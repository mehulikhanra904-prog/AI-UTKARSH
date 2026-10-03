const observer=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add("show");observer.unobserve(e.target)}}),{threshold:.12});document.querySelectorAll(".section,.project,.principles article,.stack-grid div,.stats div").forEach((el,i)=>{el.style.opacity="0";el.style.transform="translateY(18px)";el.style.transition="opacity .7s ease,transform .7s ease";el.style.transitionDelay=(i%5)*60+"ms";observer.observe(el)});const style=document.createElement("style");style.textContent=".show{opacity:1!important;transform:translateY(0)!important}";document.head.appendChild(style);
const API_BASE=(window.API_BASE_URL||"https://ai-utkarsh-3.onrender.com").replace(/\\/$/,"");
const form=document.getElementById("contact-form");
const status=document.getElementById("form-status");
if(form){
 form.addEventListener("submit",async(e)=>{
  e.preventDefault();
  status.textContent="Sending...";
  const data=Object.fromEntries(new FormData(form).entries());
  try{
   const response=await fetch((API_BASE||"http://localhost:8000")+"/api/contact",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
   const result=await response.json();
   if(!response.ok) throw new Error(result.detail?.[0]?.msg||"Unable to send message.");
   status.textContent=result.message||"Message sent successfully.";
   form.reset();
  }catch(error){
   status.textContent="Backend unavailable. Please email me directly for now.";
   console.error(error);
  }
 });
}
