// ═══════════════════════════════════════════════════════════
// HOME PAGE INTERACTIONS
// ═══════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', function() {
  
  // Hero video - simple and clean
  const heroVideo = document.querySelector('.hero-video-float');
  
  if (heroVideo) {
    // Force mute
    heroVideo.muted = true;
    heroVideo.volume = 0;
    
    // Disable audio tracks
    heroVideo.addEventListener('loadedmetadata', function() {
      if (this.audioTracks && this.audioTracks.length > 0) {
        for (let i = 0; i < this.audioTracks.length; i++) {
          this.audioTracks[i].enabled = false;
        }
      }
    });
    
    // Prevent volume changes
    heroVideo.addEventListener('volumechange', function(e) {
      e.preventDefault();
      this.muted = true;
      this.volume = 0;
    });
    
    // Pause when out of viewport
    const videoObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) {
          heroVideo.pause();
        } else {
          heroVideo.play().catch(() => {});
        }
      });
    }, { threshold: 0.3 });
    
    videoObserver.observe(heroVideo);
  }
  
  // Demo video control
  const demoVideoContainer = document.querySelector('.demo-video-container');
  const demoVideo = demoVideoContainer?.querySelector('video');
  const demoPlayBtn = document.querySelector('.demo-play-btn');
  
  if (demoVideo && demoPlayBtn) {
    // Force mute completely - no sound ever
    demoVideo.muted = true;
    demoVideo.volume = 0;
    
    // Disable all audio tracks
    demoVideo.addEventListener('loadedmetadata', function() {
      if (this.audioTracks && this.audioTracks.length > 0) {
        for (let i = 0; i < this.audioTracks.length; i++) {
          this.audioTracks[i].enabled = false;
        }
      }
    });
    
    // Prevent any volume changes
    demoVideo.addEventListener('volumechange', function(e) {
      e.preventDefault();
      this.muted = true;
      this.volume = 0;
    });
    
    demoPlayBtn.addEventListener('click', function() {
      demoVideo.play();
      demoVideoContainer.classList.add('playing');
    });
    
    demoVideo.addEventListener('play', function() {
      demoVideoContainer.classList.add('playing');
    });
    
    demoVideo.addEventListener('pause', function() {
      demoVideoContainer.classList.remove('playing');
    });
    
    demoVideo.addEventListener('ended', function() {
      demoVideoContainer.classList.remove('playing');
    });
    
    // Click on video to pause/play
    demoVideo.addEventListener('click', function() {
      if (this.paused) {
        this.play();
      } else {
        this.pause();
      }
    });
  }
  
  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);
  
  // Observe all animated elements
  const animatedElements = document.querySelectorAll(
    '.feat, .benefit-card, .testimonial-card, .step-card'
  );
  
  animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
  
  // Add visible class styling
  const style = document.createElement('style');
  style.textContent = `
    .visible {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  `;
  document.head.appendChild(style);
  
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Add parallax effect to hero background
  let ticking = false;
  
  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(function() {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        
        if (hero && scrolled < window.innerHeight) {
          hero.style.transform = `translateY(${scrolled * 0.3}px)`;
          hero.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;
        }
        
        ticking = false;
      });
      
      ticking = true;
    }
  });
  
  // Add hover effect to preview card
  const previewCard = document.querySelector('.hero-preview');
  if (previewCard) {
    previewCard.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      
      const rotateX = (y - centerY) / 20;
      const rotateY = (centerX - x) / 20;
      
      this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    
    previewCard.addEventListener('mouseleave', function() {
      this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0)';
    });
  }
  
  // Animate stats numbers on scroll
  const stats = document.querySelectorAll('.stat-num');
  let statsAnimated = false;
  
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !statsAnimated) {
        statsAnimated = true;
        animateStats();
      }
    });
  }, { threshold: 0.5 });
  
  if (stats.length > 0) {
    statsObserver.observe(stats[0].parentElement);
  }
  
  function animateStats() {
    stats.forEach(stat => {
      const text = stat.textContent;
      const number = parseInt(text.match(/\d+/)?.[0] || 0);
      
      if (number > 0) {
        let current = 0;
        const increment = number / 50;
        const timer = setInterval(() => {
          current += increment;
          if (current >= number) {
            current = number;
            clearInterval(timer);
          }
          stat.textContent = text.replace(/\d+/, Math.floor(current));
        }, 30);
      }
    });
  }
  
  // Add ripple effect to buttons
  const buttons = document.querySelectorAll('.btn-hero, .btn-ghost');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;
      
      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');
      
      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
  
  // Add ripple styles
  const rippleStyle = document.createElement('style');
  rippleStyle.textContent = `
    .btn-hero, .btn-ghost {
      position: relative;
      overflow: hidden;
    }
    
    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.5);
      transform: scale(0);
      animation: ripple-animation 0.6s ease-out;
      pointer-events: none;
    }
    
    @keyframes ripple-animation {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }
  `;
  document.head.appendChild(rippleStyle);
  
  console.log('🎨 Geo3D homepage initialized');
});
