// Danh sách testimonials
const TESTIMONIALS = [
  {
    quote: "Trước đây mình rất sợ hình học không gian, nhưng với Geo3D, mình có thể xoay mô hình 3D và hiểu rõ từng bước dựng hình. Hệ thống giải bài tự động và tương tác hoàn hảo đã giúp điểm thi của mình tăng từ 5 lên 8. Một công cụ thực sự thay đổi cách mình tư duy!",
    name: "Nguyễn Minh Anh",
    role: "Học sinh lớp 12A1, THPT Chuyên Lê Hồng Phong",
    avatar: "https://i.pravatar.cc/150?u=a042581f4e29026704d"
  },
  {
    quote: "Mình là giáo viên Toán và Geo3D giúp mình minh họa các bài hình học không gian trực quan hơn rất nhiều. Học sinh tương tác tốt hơn, hiểu nhanh hơn. Đây là công cụ không thể thiếu trong tiết dạy của mình.",
    name: "Trần Thanh Hà",
    role: "Giáo viên Toán, THPT Nguyễn Du",
    avatar: "https://i.pravatar.cc/150?u=teacher2"
  },
  {
    quote: "Tính năng dựng hình từng bước thực sự ấn tượng. Mình có thể xem AI giải thích chi tiết cách tiếp cận bài toán, không chỉ là đáp án cuối cùng. Điều này giúp mình rèn tư duy giải quyết vấn đề rất tốt.",
    name: "Lê Hoàng Nam",
    role: "Sinh viên năm nhất, ĐH Bách Khoa HN",
    avatar: "https://i.pravatar.cc/150?u=student3"
  },
  {
    quote: "Con tôi học lớp 11, từng học rất kém phần hình học không gian. Sau khi dùng Geo3D, cháu đã chủ động luyện tập mỗi ngày và đạt 9 điểm bài kiểm tra gần nhất. Cảm ơn đội ngũ phát triển!",
    name: "Phạm Quỳnh Trang",
    role: "Phụ huynh học sinh",
    avatar: "https://i.pravatar.cc/150?u=parent4"
  }
];

let currentTestimonial = 0;

function renderTestimonialCard(idx) {
  const t = TESTIMONIALS[idx];
  return `
    <p class="text-[16px] md:text-[20px] text-slate-800 font-medium leading-[1.6] mb-8 tracking-tight">
      "${t.quote}"
    </p>
    <div class="flex items-center gap-4">
      <div class="w-14 h-14 rounded-full bg-slate-200 overflow-hidden flex items-center justify-center text-slate-500 font-bold text-xl shadow-inner border border-slate-100">
        <img src="${t.avatar}" alt="Avatar" class="w-full h-full object-cover" />
      </div>
      <div>
        <div class="font-bold text-[17px] text-slate-900 tracking-tight">${t.name}</div>
        <div class="text-[14px] text-slate-500 font-medium">${t.role}</div>
      </div>
    </div>
  `;
}

function changeTestimonial(direction) {
  currentTestimonial = (currentTestimonial + direction + TESTIMONIALS.length) % TESTIMONIALS.length;
  const card = document.getElementById('testimonialCard');
  if (!card) return;

  // Slide out
  card.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
  card.style.opacity = '0';
  card.style.transform = direction > 0 ? 'translateX(-40px)' : 'translateX(40px)';

  setTimeout(() => {
    card.innerHTML = renderTestimonialCard(currentTestimonial);
    // Slide in from opposite side
    card.style.transition = 'none';
    card.style.opacity = '0';
    card.style.transform = direction > 0 ? 'translateX(40px)' : 'translateX(-40px)';

    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        card.style.opacity = '1';
        card.style.transform = 'translateX(0)';
      });
    });
  }, 200);
}

function renderTestimonials() {
  return `
    <section class="relative w-full min-h-screen py-24 flex flex-col items-center justify-center overflow-hidden">
      <!-- Full-width background -->
      <div class="absolute inset-0 w-full h-full z-0">
        <img src="../assets/images/bg_static.avif" class="absolute inset-0 w-full h-full object-cover scale-105" alt="Sky Background" />
        <div class="absolute inset-0 bg-white/10 backdrop-blur-[2px]"></div>
      </div>

      <div class="relative z-10 w-full px-6 flex flex-col items-center text-center">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/70 backdrop-blur-xl border border-white/60 shadow-[0_4px_12px_rgba(0,0,0,0.05)] mb-6 hover:scale-105 transition-transform cursor-default">
          <span class="text-[11px] font-bold tracking-widest text-slate-900 uppercase">Wall of Love</span>
        </div>

        <!-- Heading -->
        <h2 class="font-sans text-[32px] md:text-[44px] leading-[1.1] font-medium text-slate-900 tracking-tight mb-12 max-w-[700px]">
          Khách hàng nói gì về Geo<span class="text-slate-600 font-normal">3D</span>
        </h2>

        <!-- Testimonial Slider Container -->
        <div class="relative w-full max-w-[760px] mx-auto mb-24">

          <!-- Prev Button -->
          <button onclick="changeTestimonial(-1)" type="button"
            class="absolute -left-5 md:-left-14 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/90 backdrop-blur-md shadow-[0_8px_20px_rgba(0,0,0,0.08)] border border-white flex items-center justify-center hover:scale-110 hover:bg-white transition-all z-20 text-slate-700 cursor-pointer">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
          </button>

          <!-- Card -->
          <div id="testimonialCard"
            class="bg-white/95 backdrop-blur-2xl rounded-[32px] p-8 md:p-12 shadow-[0_32px_80px_-20px_rgba(0,0,0,0.12)] border border-white/80 relative z-10 text-left hover:shadow-[0_40px_100px_-20px_rgba(0,0,0,0.15)]"
            style="overflow:hidden;">
            ${renderTestimonialCard(0)}
          </div>

          <!-- Background decoration layers -->
          <div class="absolute top-4 bottom-[-16px] left-8 right-8 bg-white/40 backdrop-blur-xl rounded-[32px] shadow-sm -z-10 border border-white/30 pointer-events-none"></div>
          <div class="absolute top-8 bottom-[-32px] left-16 right-16 bg-white/20 backdrop-blur-md rounded-[32px] -z-20 border border-white/10 pointer-events-none"></div>

          <!-- Next Button -->
          <button onclick="changeTestimonial(1)" type="button"
            class="absolute -right-5 md:-right-14 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/90 backdrop-blur-md shadow-[0_8px_20px_rgba(0,0,0,0.08)] border border-white flex items-center justify-center hover:scale-110 hover:bg-white transition-all z-20 text-slate-700 cursor-pointer">
            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
          </button>
        </div>

        <!-- Stats -->
        <div class="flex flex-wrap justify-center gap-10 md:gap-20 mb-16">
          <div class="flex flex-col items-center">
            <div class="text-[36px] md:text-[48px] font-sans font-medium text-slate-900 tracking-tight mb-1">10k+</div>
            <div class="text-[14px] text-slate-600 font-medium tracking-wide">Học sinh hài lòng</div>
          </div>
          <div class="flex flex-col items-center">
            <div class="text-[36px] md:text-[48px] font-sans font-medium text-slate-900 tracking-tight mb-1">500k+</div>
            <div class="text-[14px] text-slate-600 font-medium tracking-wide">Bài toán đã giải</div>
          </div>
          <div class="flex flex-col items-center">
            <div class="text-[36px] md:text-[48px] font-sans font-medium text-slate-900 tracking-tight mb-1">98%</div>
            <div class="text-[14px] text-slate-600 font-medium tracking-wide">Cải thiện điểm số</div>
          </div>
        </div>

        <!-- Logos -->
        <div class="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-60">
          <div class="flex items-center gap-2 font-bold text-[22px] text-slate-800 tracking-tight hover:opacity-100 transition-opacity cursor-default">
             <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" class="text-slate-700"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
             EduTech
          </div>
          <div class="flex items-center gap-2 font-bold text-[22px] text-slate-800 tracking-tight hover:opacity-100 transition-opacity cursor-default">
             <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-700"><circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="4"></circle></svg>
             HọcMãi
          </div>
          <div class="flex items-center gap-2 font-bold text-[22px] text-slate-800 tracking-tight hover:opacity-100 transition-opacity cursor-default">
             <svg width="28" height="28" viewBox="0 0 24 24" fill="currentColor" class="text-slate-700"><path d="M12 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><polyline points="14 3 21 3 21 10"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
             VioEdu
          </div>
        </div>

      </div>
    </section>
  `;
}
