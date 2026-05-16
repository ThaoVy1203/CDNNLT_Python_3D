function renderPricing() {
  return `
    <section class="py-24 bg-[#fafafa]">
      <div class="max-w-[1200px] mx-auto px-6 sm:px-12">
        
        <!-- Header -->
        <div class="flex flex-col items-center text-center mb-16">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white border border-slate-200 shadow-sm mb-6">
            <span class="text-[10px] font-semibold tracking-widest text-slate-800 uppercase">Gói dịch vụ</span>
          </div>
          <h2 class="font-sans text-[36px] md:text-[48px] leading-[1.1] font-medium text-slate-900 tracking-tight mb-4">
            Bảng giá linh hoạt
          </h2>
          <p class="text-[16px] text-slate-600 max-w-[500px]">
            Lựa chọn gói dịch vụ phù hợp nhất với nhu cầu học tập và luyện thi của bạn.
          </p>
          
          <!-- Toggle -->
          <div class="mt-8 flex items-center p-1 bg-slate-100 rounded-lg">
            <button class="px-6 py-2 rounded-md bg-white shadow-sm text-[13px] font-semibold text-slate-900 transition-all">Hàng tháng</button>
            <button class="px-6 py-2 rounded-md text-[13px] font-semibold text-slate-500 hover:text-slate-900 transition-all">Hàng năm</button>
          </div>
        </div>

        <!-- Pricing Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8 items-start">
          
          <!-- Starter Plan -->
          <div class="bg-white rounded-[24px] p-8 border border-slate-100 shadow-[0_8px_30px_rgba(0,0,0,0.03)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] transition-all duration-300">
            <div class="flex items-center gap-2 mb-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-blue-500"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
              <h3 class="text-[18px] font-semibold text-slate-900">Cơ bản</h3>
            </div>
            <p class="text-[13px] text-slate-500 mb-8">Trải nghiệm Geo3D hoàn toàn miễn phí</p>
            
            <div class="mb-8">
              <span class="text-[40px] font-medium text-slate-900 tracking-tight">Miễn phí</span>
            </div>
            
            <button class="w-full py-3 px-4 rounded-xl border border-slate-200 text-[14px] font-semibold text-slate-900 hover:bg-slate-50 transition-all mb-8">
              Bắt đầu ngay
            </button>
            
            <div>
              <p class="text-[12px] font-semibold text-slate-900 uppercase tracking-wider mb-4">Bao gồm:</p>
              <ul class="space-y-4">
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">5 lượt giải bài / ngày</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Mô hình 3D cơ bản</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Lưu lịch sử 7 ngày</span>
                </li>
              </ul>
            </div>
          </div>

          <!-- Plus Plan -->
          <div class="bg-white rounded-[24px] p-8 border border-purple-100 shadow-[0_20px_40px_rgba(0,0,0,0.08)] relative overflow-hidden transition-all duration-300 transform md:-translate-y-4">
            <div class="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-purple-400 via-pink-500 to-red-500"></div>
            <div class="absolute top-0 right-0 w-32 h-32 bg-purple-100 rounded-full blur-3xl -mr-10 -mt-10 opacity-60"></div>
            
            <div class="relative z-10">
              <div class="flex items-center gap-2 mb-2">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-purple-500"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                <h3 class="text-[18px] font-semibold text-slate-900">Nâng cao</h3>
                <span class="ml-auto px-2 py-0.5 bg-slate-900 text-white text-[10px] font-bold rounded-full uppercase tracking-wider">Phổ biến</span>
              </div>
              <p class="text-[13px] text-slate-500 mb-8">Mở khóa toàn bộ sức mạnh AI</p>
              
              <div class="mb-8 flex items-end gap-1">
                <span class="text-[40px] font-medium text-slate-900 tracking-tight">49.000đ</span>
                <span class="text-[14px] text-slate-500 mb-2">/tháng</span>
              </div>
              
              <button class="w-full py-3 px-4 rounded-xl bg-slate-900 text-[14px] font-semibold text-white hover:bg-slate-800 transition-all mb-8 shadow-md hover:shadow-lg">
                Đăng ký Nâng cao
              </button>
              
              <div>
                <p class="text-[12px] font-semibold text-slate-900 uppercase tracking-wider mb-4">Bao gồm:</p>
                <ul class="space-y-4">
                  <li class="flex items-start gap-3">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-purple-600 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    <span class="text-[14px] text-slate-800 font-medium">Giải bài không giới hạn</span>
                  </li>
                  <li class="flex items-start gap-3">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    <span class="text-[14px] text-slate-600">Dựng hình từng bước chi tiết</span>
                  </li>
                  <li class="flex items-start gap-3">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    <span class="text-[14px] text-slate-600">Lưu trữ lịch sử vĩnh viễn</span>
                  </li>
                  <li class="flex items-start gap-3">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    <span class="text-[14px] text-slate-600">Không quảng cáo</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Pro Plan -->
          <div class="bg-white rounded-[24px] p-8 border border-slate-100 shadow-[0_8px_30px_rgba(0,0,0,0.03)] hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] transition-all duration-300">
            <div class="flex items-center gap-2 mb-2">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-pink-500"><path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"></path></svg>
              <h3 class="text-[18px] font-semibold text-slate-900">Chuyên gia</h3>
            </div>
            <p class="text-[13px] text-slate-500 mb-8">Dành cho giáo viên và gia sư</p>
            
            <div class="mb-8 flex items-end gap-1">
              <span class="text-[40px] font-medium text-slate-900 tracking-tight">149.000đ</span>
              <span class="text-[14px] text-slate-500 mb-2">/tháng</span>
            </div>
            
            <button class="w-full py-3 px-4 rounded-xl border border-slate-200 text-[14px] font-semibold text-slate-900 hover:bg-slate-50 transition-all mb-8">
              Đăng ký Chuyên gia
            </button>
            
            <div>
              <p class="text-[12px] font-semibold text-slate-900 uppercase tracking-wider mb-4">Bao gồm:</p>
              <ul class="space-y-4">
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Tất cả tính năng Nâng cao</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Trích xuất lời giải PDF/Word</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Tạo tài khoản học viên phụ</span>
                </li>
                <li class="flex items-start gap-3">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" class="text-slate-800 mt-0.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                  <span class="text-[14px] text-slate-600">Hỗ trợ kỹ thuật ưu tiên 24/7</span>
                </li>
              </ul>
            </div>
          </div>

        </div>
      </div>
    </section>
  `;
}

function renderMarqueeSlider() {
  return `
    <section class="py-32 bg-[#fafafa] overflow-hidden relative border-t border-slate-100 flex flex-col items-center justify-center">
      <!-- Decorative background blur -->
      <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-40">
        <div class="w-96 h-96 bg-gradient-to-tr from-purple-200 to-pink-200 rounded-full blur-[100px]"></div>
      </div>
      
      <style>
        @keyframes scrollText {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-scroll-text {
          animation: scrollText 20s linear infinite;
        }
      </style>

      <div class="relative w-full max-w-[100vw] overflow-hidden flex items-center">
        <!-- Overlay fade edges -->
        <div class="absolute left-0 top-0 bottom-0 w-32 bg-gradient-to-r from-[#fafafa] to-transparent z-10"></div>
        <div class="absolute right-0 top-0 bottom-0 w-32 bg-gradient-to-l from-[#fafafa] to-transparent z-10"></div>
        
        <!-- Center Icon Button -->
        <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-20">
          <div class="w-24 h-24 rounded-full bg-white/60 backdrop-blur-md shadow-[0_8px_32px_rgba(0,0,0,0.08)] border border-white flex items-center justify-center cursor-pointer hover:scale-105 transition-transform duration-300">
            <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-purple-100 to-pink-50 flex items-center justify-center shadow-inner">
               <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#grad1)" stroke-width="2">
                 <defs>
                   <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                     <stop offset="0%" stop-color="#8b5cf6" />
                     <stop offset="100%" stop-color="#ec4899" />
                   </linearGradient>
                 </defs>
                 <path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"></path>
               </svg>
            </div>
          </div>
        </div>

        <!-- Scrolling Text Track -->
        <div class="flex whitespace-nowrap animate-scroll-text">
          <!-- First set -->
          <div class="flex items-center text-[100px] md:text-[140px] font-medium font-sans text-slate-900 tracking-tight leading-none px-4">
            Khám phá tư duy <span class="mx-8 text-slate-300">&bull;</span> Giải bài không gian <span class="mx-8 text-slate-300">&bull;</span>
          </div>
          <!-- Second set (duplicate for infinite scroll) -->
          <div class="flex items-center text-[100px] md:text-[140px] font-medium font-sans text-slate-900 tracking-tight leading-none px-4">
            Khám phá tư duy <span class="mx-8 text-slate-300">&bull;</span> Giải bài không gian <span class="mx-8 text-slate-300">&bull;</span>
          </div>
        </div>
      </div>
      
      <!-- Bottom CTA -->
      <div class="mt-16 text-center relative z-10">
        <p class="text-slate-600 mb-6 text-[18px]">Bắt đầu giải quyết bài toán không gian của bạn ngay hôm nay.</p>
        <button onclick="window.location.href='register.html'" class="px-8 py-3.5 bg-black text-white rounded-xl font-semibold text-[15px] hover:bg-slate-800 transition-all shadow-[0_8px_20px_rgba(0,0,0,0.1)] hover:-translate-y-1">
          Đăng ký miễn phí
        </button>
      </div>
    </section>
  `;
}
