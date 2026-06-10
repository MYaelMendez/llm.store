// Viewport height fix for mobile browsers
(function(){
  function setVh(){
    document.documentElement.style.setProperty('--vh', (window.innerHeight * 0.01) + 'px');
  }
  setVh();
  window.addEventListener('resize', setVh);
})();

// Smooth scroll behavior
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Model card interactivity
document.querySelectorAll('.model-card').forEach(card => {
  card.addEventListener('click', function() {
    const modelName = this.querySelector('.model-name').textContent;
    console.log(`Clicked: ${modelName}`);
  });
});

// Feature cards animation on scroll
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.animation = 'fadeInUp 0.6s ease-out forwards';
    }
  });
}, observerOptions);

document.querySelectorAll('.feature, .model-card').forEach(el => {
  observer.observe(el);
});

// Add hover ripple effect
document.querySelectorAll('.btn, .model-link, .feature').forEach(element => {
  element.addEventListener('mousemove', function(e) {
    const rect = this.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
  });
});

console.log('llm.store — interactive site loaded');
