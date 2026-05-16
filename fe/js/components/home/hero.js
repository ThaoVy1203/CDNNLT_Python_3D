function renderHero() {
  return `
    <section class="relative w-full min-h-screen flex items-center overflow-hidden">
      <!-- Background (keeping video as previously requested, with overlay) -->
      <div class="absolute inset-0 w-full h-full z-0">
        <video 
          id="hero-video"
          loop 
          muted 
          playsinline 
          preload="metadata"
          class="absolute inset-0 w-full h-full object-cover opacity-0 transition-opacity duration-1000"
          poster="../assets/images/bg_static.avif"
        >
        </video>
        <!-- Soft gradient overlay to match the airy image vibe -->
        <div class="absolute inset-0 bg-gradient-to-r from-pink-100/60 via-purple-50/40 to-transparent backdrop-blur-[2px]"></div>
        <div class="absolute inset-0 bg-white/20"></div>
      </div>

      <!-- Content -->
      <div class="relative z-10 w-full max-w-[1100px] mx-auto px-6 sm:px-12 pt-32 pb-32 text-left flex flex-col items-start">
        
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/30 backdrop-blur-md border border-white/40 mb-6">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-purple-600">
            <path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"></path>
          </svg>
          <span class="text-[11px] font-semibold tracking-widest text-slate-800 uppercase">GIẢI PHÁP GIÁO DỤC 3D</span>
        </div>

        <!-- Title -->
        <h1 class="font-sans text-[52px] sm:text-[64px] md:text-[76px] leading-[1.02] font-medium text-slate-900 tracking-tight mb-6 max-w-[900px]">
          Nền tảng Giải Hình Học <br class="hidden md:block" />Không Gian Bằng AI
        </h1>

        <!-- Subtitle -->
        <p class="text-[16px] md:text-[18px] leading-[1.6] text-slate-700 mb-10 max-w-[650px] font-normal">
          Geo3D giúp bạn nhận diện đề bài, dựng hình 3D và đưa ra lời giải chi tiết. Mở khóa tiềm năng tư duy không gian và tự động hóa quy trình giải toán phức tạp một cách dễ dàng.
        </p>

        <!-- Actions -->
        <div class="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
          <button onclick="window.location.href='solver.html'" class="px-8 py-3.5 bg-black text-white rounded-[10px] font-medium text-[15px] transition-all duration-300 hover:bg-slate-800 shadow-sm w-full sm:w-auto">
            Bắt đầu giải bài
          </button>
          <button onclick="document.querySelector('.how-it-works').scrollIntoView({behavior: 'smooth'})" class="px-8 py-3.5 bg-white/40 backdrop-blur-md border border-white/60 text-slate-900 rounded-[10px] font-medium text-[15px] transition-all duration-300 hover:bg-white/60 shadow-sm w-full sm:w-auto">
            Xem Demo
          </button>
        </div>

      </div>
    </section>
  `;
}

function initHeroVideo() {
  const video = document.getElementById('hero-video');
  if (video) {
    const source = document.createElement('source');
    source.src = '../assets/images/bg_hero.mp4';
    source.type = 'video/mp4';
    video.appendChild(source);
    
    // Slow down the video playback
    video.playbackRate = 0.5;
    
    video.load();
    video.addEventListener('canplay', () => {
      video.play().catch(e => console.log('Autoplay prevented:', e));
      video.classList.remove('opacity-0');
      video.classList.add('opacity-100');
    }, { once: true });
  }
}
