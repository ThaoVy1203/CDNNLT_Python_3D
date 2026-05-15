function renderBenefits() {
  return `
    <section class="py-24 bg-slate-950 text-white relative overflow-hidden">
      <!-- Glow effects -->
      <div class="absolute top-0 right-0 w-[600px] h-[600px] bg-purple-900/30 rounded-full blur-[120px] pointer-events-none"></div>
      <div class="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-900/20 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="max-w-[1100px] mx-auto px-6 sm:px-12 relative z-10">
        
        <!-- Section Header -->
        <div class="flex flex-col items-center text-center mb-16">
          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 border border-white/20 backdrop-blur-md mb-6">
            <span class="text-[10px] font-semibold tracking-widest text-white uppercase">Lợi ích vượt trội</span>
          </div>
          <h2 class="font-sans text-[32px] md:text-[44px] leading-[1.1] font-medium text-white tracking-tight mb-4 max-w-[600px]">
            Vượt qua <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-pink-400 to-rose-400">giới hạn</span> tư duy.
          </h2>
          <p class="text-[15px] md:text-[16px] text-slate-400 max-w-[500px] leading-relaxed">
            Hệ thống hóa phương pháp giải toán giúp bạn tối ưu thời gian, phát triển nhãn quan không gian và đạt điểm số tối đa.
          </p>
        </div>

        <!-- 3-Column Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- Card 1 -->
          <div class="group relative bg-white/[0.02] border border-white/10 rounded-[20px] p-8 overflow-hidden transition-all duration-500 hover:bg-white/[0.04] hover:border-white/20 hover:-translate-y-1">
            <div class="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-purple-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-2xl"></div>
            <div class="text-[60px] font-bold font-sans text-white/5 leading-none absolute -top-2 -right-2 pointer-events-none transition-transform duration-700 group-hover:scale-110">01</div>
            <div class="relative z-10">
              <h3 class="text-[18px] md:text-[20px] font-semibold text-white mb-3 tracking-tight">Tiết kiệm 80% thời gian</h3>
              <p class="text-[14px] text-slate-400 leading-relaxed">
                AI hoàn thành việc dựng hình và phân tích dữ kiện cực nhanh, giải phóng bạn khỏi việc cặm cụi nháp đi nháp lại.
              </p>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="group relative bg-white/[0.02] border border-white/10 rounded-[20px] p-8 overflow-hidden transition-all duration-500 hover:bg-white/[0.04] hover:border-white/20 hover:-translate-y-1">
            <div class="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-pink-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-2xl"></div>
            <div class="text-[60px] font-bold font-sans text-white/5 leading-none absolute -top-2 -right-2 pointer-events-none transition-transform duration-700 group-hover:scale-110">02</div>
            <div class="relative z-10">
              <h3 class="text-[18px] md:text-[20px] font-semibold text-white mb-3 tracking-tight">Tăng phản xạ không gian</h3>
              <p class="text-[14px] text-slate-400 leading-relaxed">
                Tương tác trực tiếp với không gian 3D mang lại cái nhìn trực quan, hình thành phản xạ nhanh nhạy hơn hẳn sách 2D.
              </p>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="group relative bg-white/[0.02] border border-white/10 rounded-[20px] p-8 overflow-hidden transition-all duration-500 hover:bg-white/[0.04] hover:border-white/20 hover:-translate-y-1">
            <div class="absolute top-0 right-0 w-48 h-48 bg-gradient-to-bl from-blue-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 blur-2xl"></div>
            <div class="text-[60px] font-bold font-sans text-white/5 leading-none absolute -top-2 -right-2 pointer-events-none transition-transform duration-700 group-hover:scale-110">03</div>
            <div class="relative z-10">
              <h3 class="text-[18px] md:text-[20px] font-semibold text-white mb-3 tracking-tight">Đạt điểm số trọn vẹn</h3>
              <p class="text-[14px] text-slate-400 leading-relaxed">
                Hướng dẫn lập luận chặt chẽ như một gia sư chuyên nghiệp giúp bạn nắm bắt chuẩn mực trình bày bài tự luận.
              </p>
            </div>
          </div>

        </div>
      </div>
    </section>
  `;
}

function renderMarqueeSlider() {
  return `
    <section class="py-20 bg-[#050505] relative overflow-hidden flex items-center justify-center border-t border-white/5">
      <!-- Glow effect -->
      <div class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] bg-purple-600/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="w-full max-w-[1100px] mx-auto px-6 sm:px-12 relative z-10 flex flex-col items-center justify-center text-center">
        
        <div class="inline-flex items-center px-4 py-1.5 rounded-full bg-white/5 border border-white/10 mb-6">
          <span class="text-[10px] font-bold tracking-widest text-white uppercase">VƯỢT LÊN DẪN ĐẦU</span>
        </div>
        <h2 class="font-sans text-[40px] md:text-[56px] leading-[1.1] font-medium text-white tracking-tight mb-8 max-w-[600px]">
          Sẵn sàng chinh phục <br/>Hình học không gian?
        </h2>
        <button onclick="window.location.href='register.html'" class="px-8 py-3.5 bg-white text-slate-900 rounded-[12px] font-semibold text-[15px] hover:scale-105 transition-all shadow-[0_8px_30px_rgba(255,255,255,0.15)]">
          Bắt đầu học ngay
        </button>

      </div>
    </section>
  `;
}
