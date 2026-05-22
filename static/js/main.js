// ===== THEME TOGGLE =====
const THEME_KEY = 'koshpes-theme';

function initTheme() {
  const saved = localStorage.getItem(THEME_KEY) || 'light';
  document.documentElement.setAttribute('data-theme', saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem(THEME_KEY, next);
}

initTheme();

document.addEventListener('DOMContentLoaded', () => {
  // Theme toggle button
  const themeBtn = document.getElementById('themeToggle');
  if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

  // Mobile nav
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  const mobileClose = document.getElementById('mobileClose');

  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', () => {
      mobileNav.classList.toggle('open');
      document.body.style.overflow = mobileNav.classList.contains('open') ? 'hidden' : '';
    });
  }
  if (mobileClose && mobileNav) {
    mobileClose.addEventListener('click', () => {
      mobileNav.classList.remove('open');
      document.body.style.overflow = '';
    });
  }
  // Close nav on link click
  if (mobileNav) {
    mobileNav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // Auto-dismiss alerts
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(el => {
      el.style.transition = 'all 0.4s ease';
      el.style.opacity = '0';
      el.style.transform = 'translateX(20px)';
      setTimeout(() => el.remove(), 400);
    });
  }, 4000);

  // Image thumbnails
  const mainImg = document.getElementById('mainDetailImage');
  if (mainImg) {
    document.querySelectorAll('.detail-thumb').forEach(thumb => {
      thumb.addEventListener('click', () => {
        mainImg.src = thumb.src;
        document.querySelectorAll('.detail-thumb').forEach(t => t.classList.remove('active'));
        thumb.classList.add('active');
      });
    });
  }

  // Animate stat counters
  animateCounters();

  // Hero particles
  createParticles();

  // Card stagger animation
  staggerCards();
});

// ===== COUNTER ANIMATION =====
function animateCounters() {
  const counters = document.querySelectorAll('[data-counter]');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.getAttribute('data-counter'));
        const duration = 1500;
        const start = performance.now();
        function update(now) {
          const elapsed = now - start;
          const progress = Math.min(elapsed / duration, 1);
          const eased = 1 - Math.pow(1 - progress, 3);
          el.textContent = Math.floor(eased * target).toLocaleString();
          if (progress < 1) requestAnimationFrame(update);
        }
        requestAnimationFrame(update);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => observer.observe(c));
}

// ===== HERO PARTICLES =====
function createParticles() {
  const container = document.querySelector('.hero-particles');
  if (!container) return;
  const colors = ['#FF6B35', '#00D4AA', '#FFD166', '#FF8C5C'];
  for (let i = 0; i < 15; i++) {
    const p = document.createElement('div');
    p.className = 'hero-particle';
    const size = Math.random() * 8 + 4;
    const color = colors[Math.floor(Math.random() * colors.length)];
    p.style.cssText = `
      width: ${size}px;
      height: ${size}px;
      background: ${color};
      left: ${Math.random() * 100}%;
      animation-duration: ${Math.random() * 10 + 8}s;
      animation-delay: ${Math.random() * 8}s;
    `;
    container.appendChild(p);
  }
}

// ===== CARD STAGGER =====
function staggerCards() {
  const cards = document.querySelectorAll('.property-card, .category-card');
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 0.07}s`;
  });
}

// ===== FAVORITE TOGGLE =====
function toggleFavorite(btn, propertyId) {
  btn.style.transform = 'scale(1.3)';
  setTimeout(() => btn.style.transform = '', 300);

  fetch(`/properties/${propertyId}/favorite/`, {
    method: 'POST',
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken'),
    }
  }).then(r => r.json()).then(data => {
    btn.classList.toggle('active', data.is_favorite);
    btn.textContent = data.is_favorite ? '❤️' : '🤍';
  });
}

// ===== CSRF =====
function getCookie(name) {
  let val = null;
  document.cookie.split(';').forEach(c => {
    const [k, v] = c.trim().split('=');
    if (k === name) val = decodeURIComponent(v);
  });
  return val;
}

// ===== DELETE CONFIRM =====
function confirmDelete(url) {
  const modal = document.getElementById('deleteModal');
  if (modal) {
    modal.classList.remove('hidden');
    document.getElementById('deleteConfirmBtn').onclick = () => {
      document.getElementById('deleteForm').action = url;
      document.getElementById('deleteForm').submit();
    };
    document.getElementById('deleteCancelBtn').onclick = () => {
      modal.classList.add('hidden');
    };
  }
}

// ===== AI CHAT =====
const chatHistory = [];

function initChat() {
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const messages = document.getElementById('chatMessages');
  const clearBtn = document.getElementById('clearChat');

  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (!msg) return;

    appendMessage('user', msg);
    chatHistory.push({ role: 'user', content: msg });
    input.value = '';
    input.style.height = 'auto';

    const typing = showTyping();

    try {
      const resp = await fetch('/ai/chat/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ message: msg, history: chatHistory })
      });
      const data = await resp.json();
      typing.remove();
      appendMessage('ai', data.reply);
      chatHistory.push({ role: 'assistant', content: data.reply });
    } catch (err) {
      typing.remove();
      appendMessage('ai', 'Qáte júz berdi. Qayta urınıń.');
    }
  });

  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event('submit'));
    }
  });

  input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 120) + 'px';
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      chatHistory.length = 0;
      messages.innerHTML = '';
      appendMessage('ai', 'Sálem! Sizge eń jaqsı múlk tabıwda járdem beriwim múmkin. Sorawıńızdı bere beriń!');
    });
  }
}

function appendMessage(role, text) {
  const messages = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `message ${role}`;
  const avatar = role === 'ai' ? '🏠' : '👤';
  div.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-bubble">${escapeHtml(text).replace(/\n/g, '<br>')}</div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function showTyping() {
  const messages = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'message ai';
  div.innerHTML = `
    <div class="msg-avatar">🏠</div>
    <div class="typing-indicator">
      <span></span><span></span><span></span>
    </div>
  `;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

function escapeHtml(text) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(text));
  return d.innerHTML;
}

document.addEventListener('DOMContentLoaded', initChat);

// ===== IMAGE UPLOAD PREVIEW =====
document.addEventListener('DOMContentLoaded', () => {
  const fileInput = document.getElementById('imageUpload');
  const preview = document.getElementById('imagePreview');
  if (fileInput && preview) {
    fileInput.addEventListener('change', () => {
      preview.innerHTML = '';
      Array.from(fileInput.files).forEach(file => {
        const reader = new FileReader();
        reader.onload = e => {
          const img = document.createElement('img');
          img.src = e.target.result;
          img.style.cssText = 'width:80px;height:60px;object-fit:cover;border-radius:8px;';
          preview.appendChild(img);
        };
        reader.readAsDataURL(file);
      });
    });
  }
});
