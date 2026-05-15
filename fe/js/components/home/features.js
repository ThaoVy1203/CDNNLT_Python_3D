function renderFeatures() {
  return `
    <section class="py-20 bg-[#fafafa]">
      <div class="max-w-[1100px] mx-auto px-6 sm:px-12">
        
        <!-- Section Header -->
        <div class="flex flex-col items-center text-center mb-20">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white border border-slate-200 shadow-sm mb-6">
            <span class="text-[10px] font-semibold tracking-widest text-slate-800 uppercase">Tính năng nổi bật</span>
          </div>
          <h2 class="font-sans text-[32px] md:text-[44px] leading-[1.1] font-medium text-slate-900 tracking-tight mb-6 max-w-[700px]">
            Giải pháp toàn diện cho <br/>Hình Học Không Gian
          </h2>
          <p class="text-[16px] md:text-[17px] leading-[1.6] text-slate-600 max-w-[600px]">
            Geo3D mang đến công cụ học tập tương tác mạnh mẽ, giúp học sinh nắm bắt không gian 3D và tự động hóa quy trình giải toán phức tạp.
          </p>
        </div>

        <!-- Sticky Stacking Cards Container -->
        <div class="flex flex-col gap-16 pb-32">
          
          <!-- Card 1: Nhận diện AI -->
          <div class="sticky top-24 z-[1] bg-white rounded-lg border border-slate-200 p-[5px] transition-all">
            <div class="flex flex-col md:flex-row items-stretch gap-2 md:gap-6">
              <!-- Text Content -->
              <div class="w-full md:w-1/2 py-10 px-6 md:px-12 flex flex-col justify-center">
                <h3 class="text-[26px] md:text-[32px] font-semibold text-slate-900 mb-4 tracking-tight leading-[1.2]">
                  Nhận diện đề bài bằng AI
                </h3>
                <p class="text-[15px] text-slate-600 leading-relaxed mb-8">
                  Chỉ cần chụp ảnh đề bài, hệ thống AI tiên tiến sẽ tự động đọc hiểu, trích xuất dữ kiện và thiết lập bài toán ngay lập tức mà không cần gõ phím.
                </p>
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Quét ảnh siêu tốc 1 chạm</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 7 4 4 20 4 20 7"></polyline><line x1="9" y1="20" x2="15" y2="20"></line><line x1="12" y1="4" x2="12" y2="20"></line></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Trích xuất văn bản chính xác</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Thiết lập thông số tự động</span>
                  </div>
                </div>
              </div>
              <!-- Visual -->
              <div class="w-full md:w-1/2 min-h-[340px] rounded-md bg-gradient-to-br from-violet-100 via-fuchsia-50 to-pink-100 flex items-center justify-center p-8 relative overflow-hidden">
                  <div class="absolute w-64 h-64 bg-white/40 rounded-full blur-3xl -top-10 -left-10"></div>
                  <div class="relative z-10 w-full max-w-[320px] bg-white/60 backdrop-blur-xl rounded-xl p-6 shadow-sm border border-white flex flex-col gap-4 scale-105">
                     <div class="flex items-center gap-3 pb-4 border-b border-white/50">
                       <div class="w-10 h-10 rounded-full bg-violet-600 flex items-center justify-center text-white shadow-sm">
                         <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path><circle cx="12" cy="13" r="4"></circle></svg>
                       </div>
                       <div>
                         <div class="text-[13px] font-semibold text-slate-800">Quét đề bài AI</div>
                         <div class="text-[11px] text-slate-500">Đang phân tích hình học...</div>
                       </div>
                     </div>
                     <div class="flex items-center gap-3 bg-white/80 rounded-lg p-3 border border-white">
                       <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                       <div class="h-2 w-full bg-slate-200 rounded-full">
                         <div class="h-2 w-3/4 bg-violet-500 rounded-full"></div>
                       </div>
                     </div>
                  </div>
              </div>
            </div>
          </div>

          <!-- Card 2: Mô hình 3D -->
          <div class="sticky top-32 z-[2] bg-white rounded-lg border border-slate-200 p-[5px] transition-all">
            <div class="flex flex-col md:flex-row-reverse items-stretch gap-2 md:gap-6">
              <!-- Text Content -->
              <div class="w-full md:w-1/2 py-10 px-6 md:px-12 flex flex-col justify-center">
                <h3 class="text-[26px] md:text-[32px] font-semibold text-slate-900 mb-4 tracking-tight leading-[1.2]">
                  Mô hình 3D tương tác
                </h3>
                <p class="text-[15px] text-slate-600 leading-relaxed mb-8">
                  Dựng lại hình học không gian với khả năng tương tác toàn diện: xoay 360 độ, phóng to, thu nhỏ để quan sát mọi góc độ và mặt cắt.
                </p>
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Xoay 360 độ linh hoạt</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Zoom cận cảnh chi tiết</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="21" y1="10" x2="3" y2="10"></line><line x1="21" y1="6" x2="3" y2="6"></line><line x1="21" y1="14" x2="3" y2="14"></line><line x1="21" y1="18" x2="3" y2="18"></line></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Hiển thị mặt cắt chuyên sâu</span>
                  </div>
                </div>
              </div>
              <!-- Visual -->
              <div class="w-full md:w-1/2 min-h-[340px] rounded-md bg-gradient-to-tr from-sky-100 via-indigo-50 to-blue-100 flex items-center justify-center p-8 relative overflow-hidden">
                  <div class="absolute w-72 h-72 bg-blue-200/40 rounded-full blur-3xl -bottom-10 -right-10"></div>
                  <div class="relative z-10 w-full max-w-[300px] bg-white rounded-xl p-6 shadow-sm border border-slate-100 flex flex-col items-center scale-105">
                     <div class="w-full flex justify-between items-center mb-6">
                       <div class="flex gap-1.5">
                         <div class="w-2.5 h-2.5 rounded-full bg-slate-200"></div>
                         <div class="w-2.5 h-2.5 rounded-full bg-slate-200"></div>
                         <div class="w-2.5 h-2.5 rounded-full bg-slate-200"></div>
                       </div>
                       <div class="text-[11px] font-medium text-slate-400">View 3D</div>
                     </div>
                     <div class="relative w-32 h-32 mb-4 animate-[spin_10s_linear_infinite]">
                       <svg viewBox="0 0 100 100" class="w-full h-full text-blue-600 opacity-80" fill="none" stroke="currentColor" stroke-width="2">
                         <polygon points="50 10 90 30 90 70 50 90 10 70 10 30"></polygon>
                         <polyline points="50 10 50 50 90 30"></polyline>
                         <line x1="50" y1="50" x2="10" y2="30"></line>
                         <line x1="50" y1="50" x2="50" y2="90"></line>
                       </svg>
                     </div>
                     <div class="flex gap-2">
                       <div class="px-3 py-1 bg-slate-50 text-slate-600 rounded-md text-[10px] font-semibold border border-slate-100">Xoay</div>
                       <div class="px-3 py-1 bg-slate-50 text-slate-600 rounded-md text-[10px] font-semibold border border-slate-100">Zoom</div>
                     </div>
                  </div>
              </div>
            </div>
          </div>

          <!-- Card 3: Dựng hình -->
          <div class="sticky top-40 z-[3] bg-white rounded-lg border border-slate-200 p-[5px] transition-all">
            <div class="flex flex-col md:flex-row items-stretch gap-2 md:gap-6">
              <!-- Text Content -->
              <div class="w-full md:w-1/2 py-10 px-6 md:px-12 flex flex-col justify-center">
                <h3 class="text-[26px] md:text-[32px] font-semibold text-slate-900 mb-4 tracking-tight leading-[1.2]">
                  Dựng hình từng bước
                </h3>
                <p class="text-[15px] text-slate-600 leading-relaxed mb-8">
                  Hệ thống hướng dẫn chi tiết cách vẽ hình tuần tự, giúp học sinh hiểu rõ bản chất, quy trình dựng hình và không bị mất điểm trình bày.
                </p>
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Tiến trình vẽ minh hoạ</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Thuyết minh logic hình học</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Chuẩn mực sách giáo khoa</span>
                  </div>
                </div>
              </div>
              <!-- Visual -->
              <div class="w-full md:w-1/2 min-h-[340px] rounded-md bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-100 flex items-center justify-center p-8 relative overflow-hidden">
                  <div class="absolute w-80 h-80 bg-emerald-200/30 rounded-full blur-3xl top-0 right-0"></div>
                  <div class="relative z-10 w-full max-w-[340px] bg-white/80 backdrop-blur-xl rounded-xl shadow-sm border border-white p-6 scale-105">
                     <div class="text-[13px] font-semibold text-slate-800 mb-5">Tiến trình dựng hình</div>
                     
                     <div class="flex items-start gap-4 mb-5">
                       <div class="w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white font-bold text-[10px] flex-shrink-0 mt-0.5">
                         <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                       </div>
                       <div>
                         <div class="h-3 w-32 bg-slate-300 rounded-full mb-2"></div>
                         <div class="h-2 w-48 bg-slate-200 rounded-full"></div>
                       </div>
                     </div>
                     
                     <div class="flex items-start gap-4 mb-5">
                       <div class="w-6 h-6 rounded-full bg-teal-500 flex items-center justify-center text-white font-bold text-[11px] flex-shrink-0 mt-0.5 shadow-sm">2</div>
                       <div>
                         <div class="h-3 w-40 bg-slate-800 rounded-full mb-2"></div>
                         <div class="h-2 w-56 bg-slate-300 rounded-full"></div>
                       </div>
                     </div>
                     
                     <div class="flex items-start gap-4 opacity-40">
                       <div class="w-6 h-6 rounded-full border-2 border-slate-300 flex items-center justify-center text-slate-400 font-bold text-[11px] flex-shrink-0 mt-0.5">3</div>
                       <div>
                         <div class="h-3 w-28 bg-slate-300 rounded-full mb-2"></div>
                         <div class="h-2 w-32 bg-slate-200 rounded-full"></div>
                       </div>
                     </div>
                  </div>
              </div>
            </div>
          </div>

          <!-- Card 4: Lời giải -->
          <div class="sticky top-48 z-[4] bg-white rounded-lg border border-slate-200 p-[5px] transition-all">
            <div class="flex flex-col md:flex-row-reverse items-stretch gap-2 md:gap-6">
              <!-- Text Content -->
              <div class="w-full md:w-1/2 py-10 px-6 md:px-12 flex flex-col justify-center">
                <h3 class="text-[26px] md:text-[32px] font-semibold text-slate-900 mb-4 tracking-tight leading-[1.2]">
                  Lời giải phân tích sâu
                </h3>
                <p class="text-[15px] text-slate-600 leading-relaxed mb-8">
                  Cung cấp lời giải đầy đủ, logic kèm gợi ý và lập luận chặt chẽ như một gia sư chuyên nghiệp ngay tại nhà.
                </p>
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Trình bày rõ ràng, mạch lạc</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Gợi ý tư duy giải bài</span>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-600"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg></div>
                    <span class="text-slate-700 font-medium text-[14px]">Bảo mật và độ tin cậy cao</span>
                  </div>
                </div>
              </div>
              <!-- Visual -->
              <div class="w-full md:w-1/2 min-h-[340px] rounded-md bg-gradient-to-bl from-rose-100 via-orange-50 to-amber-100 flex items-center justify-center p-8 relative overflow-hidden">
                  <div class="absolute w-64 h-64 bg-rose-200/40 rounded-full blur-3xl -top-20 -right-10"></div>
                  <div class="relative z-10 w-full max-w-[320px] bg-white rounded-xl shadow-sm border border-slate-100 p-7 scale-105">
                     <div class="flex items-center gap-3 mb-6">
                       <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center">
                         <svg width="16" height="16" class="text-green-600" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"></polyline></svg>
                       </div>
                       <span class="text-[15px] font-semibold text-slate-800">Lời giải hoàn chỉnh</span>
                     </div>
                     <div class="space-y-4">
                       <div class="h-2.5 w-full bg-slate-100 rounded-full"></div>
                       <div class="h-2.5 w-11/12 bg-slate-100 rounded-full"></div>
                       <div class="h-2.5 w-4/5 bg-slate-100 rounded-full"></div>
                       <div class="h-2.5 w-full bg-slate-100 rounded-full mt-6"></div>
                       <div class="h-2.5 w-3/4 bg-slate-100 rounded-full"></div>
                     </div>
                     <div class="mt-6 inline-flex px-3 py-1.5 bg-green-50 text-green-700 text-[11px] font-bold rounded-md">
                       Đã xác minh
                     </div>
                  </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Blue Background Marquee Slider -->
        <div class="relative w-full h-[100px] md:h-[120px] rounded-[8px] overflow-hidden flex items-center mt-[-40px]">
          <!-- Video Background -->
          <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover opacity-90">
            <source src="../assets/images/bg_card2.mp4" type="video/mp4">
          </video>
          
          <div class="absolute inset-0 bg-blue-500/10 mix-blend-overlay"></div>
          
          <style>
            @keyframes scrollPills {
              0% { transform: translateX(0); }
              100% { transform: translateX(-50%); }
            }
            .animate-scroll-pills {
              animation: scrollPills 30s linear infinite;
            }
          </style>

          <div class="relative w-full overflow-hidden flex items-center">
            <!-- Overlay fade edges -->
            <div class="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-[#fafafa] to-transparent z-10 pointer-events-none"></div>
            <div class="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-[#fafafa] to-transparent z-10 pointer-events-none"></div>
            
            <div class="flex whitespace-nowrap animate-scroll-pills hover:[animation-play-state:paused] cursor-default gap-4 px-4 w-max relative z-20">
              <!-- First set of pills -->
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Nhận diện ảnh AI
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Dựng hình đa giác
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Tính toán thể tích
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Mặt cắt không gian
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Lời giải chi tiết
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Tương tác 3D
              </div>
              
              <!-- Duplicate set for infinite scrolling -->
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Nhận diện ảnh AI
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Dựng hình đa giác
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Tính toán thể tích
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Mặt cắt không gian
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Lời giải chi tiết
              </div>
              <div class="px-5 md:px-6 py-3 bg-white/95 backdrop-blur-md rounded-xl text-slate-800 font-semibold text-[14px] md:text-[15px] shadow-[0_4px_12px_rgba(0,0,0,0.05)] border border-white/50">
                Tương tác 3D
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>
  `;
}
