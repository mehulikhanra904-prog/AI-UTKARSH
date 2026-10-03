const observer = new IntersectionObserver(
  entries => entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("show");
      observer.unobserve(entry.target);
    }
  }),
  { threshold: 0.12 }
);

document.querySelectorAll(".section,.project,.principles article,.stack-grid div,.stats div").forEach((element, index) => {
  element.style.opacity = "0";
  element.style.transform = "translateY(18px)";
  element.style.transition = "opacity .7s ease,transform .7s ease";
  element.style.transitionDelay = (index % 5) * 60 + "ms";
  observer.observe(element);
});

const style = document.createElement("style");
style.textContent = ".show{opacity:1!important;transform:translateY(0)!important}";
document.head.appendChild(style);

const API_BASE = "https://ai-utkarsh-3.onrender.com";

const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");

if (form) {
  form.addEventListener("submit", async event => {
    event.preventDefault();
    status.textContent = "Sending...";

    if (!API_BASE) {
      status.textContent = "API configuration is missing.";
      return;
    }

    const data = Object.fromEntries(new FormData(form).entries());

    try {
      const response = await fetch(API_BASE + "/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail?.[0]?.msg || result.detail || "Unable to send message.");
      }

      status.textContent = result.message || "Message sent successfully.";
      form.reset();
    } catch (error) {
      status.textContent = "Unable to send your message right now.";
      console.error(error);
    }
  });
}
