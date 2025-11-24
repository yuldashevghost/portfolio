const html = document.documentElement;
const modeToggle = document.getElementById('modeToggle');
const themeIcon = document.getElementById('themeIcon');
const filters = document.querySelectorAll('#projectFilters .filter');
const projectCards = document.querySelectorAll('.project-card');
const lightbox = document.getElementById('lightbox');
const lightboxImg = lightbox?.querySelector('img');
const lightboxClose = lightbox?.querySelector('.close');
const nav = document.getElementById('site-nav');
const hamburger = document.getElementById('hamburger');
const blogCards = document.querySelectorAll('[data-blog-card]');
const blogModal = document.getElementById('blogModal');
const blogModalTitle = blogModal?.querySelector('.modal-title');
const blogModalDate = blogModal?.querySelector('.modal-date');
const blogModalContent = blogModal?.querySelector('.modal-content');
const blogModalClose = blogModal?.querySelector('.close');

const THEME_KEY = 'portfolio_theme';

const setTheme = (mode) => {
    html.setAttribute('data-theme', mode);
    localStorage.setItem(THEME_KEY, mode);
    if (themeIcon) {
        themeIcon.className = mode === 'dark' ? 'ri-sun-line' : 'ri-moon-line';
    }
};

const initTheme = () => {
    const stored = localStorage.getItem(THEME_KEY);
    setTheme(stored || 'dark');
};

modeToggle?.addEventListener('click', () => {
    const current = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    setTheme(current);
});

initTheme();

// Intersection Observer for scroll animations
const observer = new IntersectionObserver(
    (entries, obs) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                if (entry.target.classList.contains('skill-card')) {
                    animateSkill(entry.target);
                }
                obs.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.2 }
);

document.querySelectorAll('[data-animate]').forEach((el) => observer.observe(el));

function animateSkill(card) {
    const value = card.dataset.progress;
    const path = card.querySelector('[data-progress-path]');
    if (!path) return;
    const circumference = 100;
    const offset = ((100 - value) / 100) * circumference;
    path.style.strokeDasharray = `${circumference}`;
    path.style.strokeDashoffset = offset;
    path.style.stroke = 'var(--accent-2)';
}

// Project filters
filters.forEach((button) => {
    button.addEventListener('click', () => {
        filters.forEach((btn) => btn.classList.remove('active'));
        button.classList.add('active');
        const target = button.dataset.filter;
        projectCards.forEach((card) => {
            const match = target === 'all' || card.dataset.category === target;
            card.style.display = match ? 'flex' : 'none';
        });
    });
});

// Lightbox
document.querySelectorAll('[data-lightbox]').forEach((img) => {
    img.addEventListener('click', () => {
        if (!lightbox || !lightboxImg) return;
        lightboxImg.src = img.src;
        lightbox.style.display = 'flex';
    });
});

lightboxClose?.addEventListener('click', () => {
    lightbox.style.display = 'none';
});

lightbox?.addEventListener('click', (event) => {
    if (event.target === lightbox) {
        lightbox.style.display = 'none';
    }
});

// Smooth close nav on link click
nav?.querySelectorAll('a').forEach((link) =>
    link.addEventListener('click', () => {
        nav.classList.remove('open');
    })
);

hamburger?.addEventListener('click', () => {
    nav?.classList.toggle('open');
});

function openBlogModal(card) {
    if (!blogModal || !blogModalTitle || !blogModalContent) return;
    const title = card.querySelector('h3')?.textContent?.trim() || '';
    const date = card.querySelector('.muted')?.textContent?.trim() || '';
    const full = card.querySelector('[data-full]');
    const summary = card.querySelector('.blog-body p:not(.muted)');
    blogModalTitle.textContent = title;
    if (blogModalDate) {
        blogModalDate.textContent = date;
    }
    blogModalContent.innerHTML = full ? full.innerHTML : summary?.outerHTML || '';
    blogModal.classList.add('open');
    blogModal.setAttribute('aria-hidden', 'false');
}

function closeBlogModal() {
    if (!blogModal || !blogModalContent) return;
    blogModal.classList.remove('open');
    blogModal.setAttribute('aria-hidden', 'true');
    blogModalContent.innerHTML = '';
}

blogCards.forEach((card) => {
    card.addEventListener('click', (event) => {
        if (event.target.closest('a, button, form')) {
            return;
        }
        openBlogModal(card);
    });
});

blogModalClose?.addEventListener('click', closeBlogModal);

blogModal?.addEventListener('click', (event) => {
    if (event.target === blogModal) {
        closeBlogModal();
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && blogModal?.classList.contains('open')) {
        closeBlogModal();
    }
});

