// Topbar component - floating card style
function renderTopbar(activePage = '') {
  const currentUser = getCurrentUser();
  const isLoggedIn = !!currentUser;
  const _isAutoUsername = currentUser && currentUser.username && /^User_\d+/.test(currentUser.username);
  const displayName = isLoggedIn
    ? (currentUser.name
        || (!_isAutoUsername ? currentUser.username : null)
        || (currentUser.email ? currentUser.email.split('@')[0] : null)
        || 'User')
    : '';

  // Nav link style
  const navLink = (href, label, key) => {
    const isActive = activePage === key;
    return `
      <a href="${href}" style="padding:6px 4px;font-size:14px;font-weight:500;color:${isActive ? '#0f172a' : '#64748b'};text-decoration:none;transition:color .15s;white-space:nowrap;"
         onmouseover="if(!this.dataset.active)this.style.color='#0f172a'"
         onmouseout="if(!this.dataset.active)this.style.color='#64748b'"
         ${isActive ? 'data-active="true"' : ''}>
        ${label}
      </a>`;
  };

  let navLinks = navLink('index.html', 'Trang chủ', 'home');
  navLinks += navLink('solver.html', 'Giải bài', 'solver');
  if (isLoggedIn) {
    navLinks += navLink('history.html', 'Lịch sử', 'history');
    navLinks += navLink('practice.html', 'Luyện tập', 'practice');
  }
  navLinks += navLink('docs.html', 'Tài liệu', 'docs');

  // Avatar HTML
  const avatarHtml = currentUser && currentUser.picture
    ? `<img src="${currentUser.picture}" alt="avatar"
         style="width:30px;height:30px;border-radius:50%;object-fit:cover;flex-shrink:0;"
         onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
       <span style="width:30px;height:30px;border-radius:50%;background:#e2e8f0;display:none;align-items:center;justify-content:center;flex-shrink:0;font-size:12px;font-weight:600;color:#475569;">
         ${displayName ? displayName[0].toUpperCase() : 'U'}
       </span>`
    : `<span style="width:30px;height:30px;border-radius:50%;background:#e2e8f0;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:12px;font-weight:600;color:#475569;">
         ${displayName ? displayName[0].toUpperCase() : 'U'}
       </span>`;

  return `
<div id="topbarWrapper" style="position:fixed;top:0;left:0;right:0;z-index:10000;padding:20px 32px;transition:padding .3s ease;">
  <header id="topbarHeader" style="max-width:1240px;margin:0 auto;background:rgba(255,255,255,0.35);backdrop-filter:blur(28px) saturate(180%);-webkit-backdrop-filter:blur(28px) saturate(180%);border:1px solid rgba(255,255,255,0.4);border-radius:20px;box-shadow:0 4px 24px rgba(15,23,42,0.04);padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:24px;transition:all .3s ease;">

    <!-- Logo -->
    <a href="index.html" style="display:flex;align-items:center;gap:10px;text-decoration:none;flex-shrink:0;">
      <div style="width:34px;height:34px;background:#0f172a;border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0;">
        <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2l3 7 7 3-7 3-3 7-3-7-7-3 7-3z"></path>
        </svg>
      </div>
      <span id="logoText" style="font-family:'Outfit','Inter',sans-serif;font-size:20px;font-weight:700;color:#0f172a;letter-spacing:-0.02em;transition:all .3s ease;overflow:hidden;">Geo3D</span>
    </a>

    <!-- Nav -->
    <nav style="display:flex;align-items:center;gap:32px;">
      ${navLinks}
    </nav>

    <!-- Right -->
    <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
      <button id="loginBtn"
        onclick="window.location.href='login.html'"
        style="display:${isLoggedIn ? 'none' : 'inline-flex'};align-items:center;padding:10px 22px;background:#0f172a;color:white;border:none;border-radius:999px;font-size:13px;font-weight:600;cursor:pointer;transition:opacity .15s;"
        onmouseover="this.style.opacity='0.9'"
        onmouseout="this.style.opacity='1'">
        Đăng nhập
      </button>

      <div id="userDropdown" style="display:${isLoggedIn ? 'block' : 'none'};position:relative;">
        <button class="user-avatar-btn" onclick="toggleUserMenu()"
          style="display:flex;align-items:center;gap:8px;padding:3px 10px 3px 3px;background:white;border:1px solid #e2e8f0;border-radius:999px;cursor:pointer;transition:box-shadow .15s;"
          onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.08)'"
          onmouseout="this.style.boxShadow='none'">
          ${avatarHtml}
          <span id="userName" style="font-size:13px;font-weight:500;color:#0f172a;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${displayName}</span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2.5">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>

        <div id="userMenu" style="display:none;position:absolute;right:0;top:calc(100% + 8px);width:220px;background:white;border:1px solid #f1f5f9;border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,0.08);padding:6px;z-index:9999;">
          <a href="profile.html" style="display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;text-decoration:none;color:#334155;font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            Hồ sơ cá nhân
          </a>
          <a href="history.html" style="display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;text-decoration:none;color:#334155;font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
            Lịch sử giải bài
          </a>
          <a href="docs.html" style="display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;text-decoration:none;color:#334155;font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
            Tài liệu học tập
          </a>
          <div style="height:1px;background:#f1f5f9;margin:6px 0;"></div>
          <a href="#" onclick="handleLogout(event)" style="display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:8px;text-decoration:none;color:#ef4444;font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='#fef2f2'" onmouseout="this.style.background='transparent'">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
            Đăng xuất
          </a>
        </div>
      </div>
    </div>

  </header>
</div>
  `;
}

// Toggle user dropdown menu
function toggleUserMenu() {
  const menu = document.getElementById('userMenu');
  if (menu) {
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
  }
}

// Close dropdown when clicking outside
window.addEventListener('click', function(e) {
  const dropdown = document.getElementById('userDropdown');
  const menu = document.getElementById('userMenu');
  if (dropdown && menu && !dropdown.contains(e.target)) {
    menu.style.display = 'none';
  }
});

// Handle logout
function handleLogout(e) {
  e.preventDefault();
  localStorage.removeItem('geo3d_current_user');
  window.location.href = 'index.html';
}

// Check auth and update topbar
function initTopbar() {
  try {
    const raw = localStorage.getItem('geo3d_current_user');
    const currentUser = raw ? JSON.parse(raw) : null;
    const loginBtn = document.getElementById('loginBtn');
    const userDropdown = document.getElementById('userDropdown');
    const userName = document.getElementById('userName');

    if (currentUser && currentUser.id) {
      if (loginBtn) loginBtn.style.display = 'none';
      if (userDropdown) userDropdown.style.display = 'block';
      const _auto = currentUser.username && /^User_\d+/.test(currentUser.username);
      const name = currentUser.name
        || (!_auto ? currentUser.username : null)
        || (currentUser.email ? currentUser.email.split('@')[0] : null)
        || 'User';
      if (userName) userName.textContent = name;
    } else {
      if (loginBtn) loginBtn.style.display = 'inline-flex';
      if (userDropdown) userDropdown.style.display = 'none';
    }
    return currentUser;
  } catch(e) {
    console.error('[initTopbar] error:', e);
    return null;
  }
}

// Shrink topbar on scroll
(function() {
  let ticking = false;

  function updateTopbarOnScroll() {
    const wrapper = document.getElementById('topbarWrapper');
    const header = document.getElementById('topbarHeader');
    if (!wrapper || !header) {
      ticking = false;
      return;
    }

    const scrolled = window.scrollY > 20;

    if (scrolled) {
      // Shrunk state - chỉ còn icon logo, gọn hơn
      wrapper.style.padding = '8px 24px';
      header.style.padding = '6px 14px';
      header.style.maxWidth = '880px';
      header.style.borderRadius = '20px';
      header.style.background = 'rgba(255,255,255,0.75)';
      header.style.boxShadow = '0 8px 28px rgba(15,23,42,0.10)';
      const logoText = document.getElementById('logoText');
      if (logoText) {
        logoText.style.maxWidth = '0';
        logoText.style.opacity = '0';
        logoText.style.marginLeft = '-10px';
      }
    } else {
      // Expanded state - hiện đầy đủ logo
      wrapper.style.padding = '20px 32px';
      header.style.padding = '12px 20px';
      header.style.maxWidth = '1240px';
      header.style.borderRadius = '20px';
      header.style.background = 'rgba(255,255,255,0.35)';
      header.style.boxShadow = '0 4px 24px rgba(15,23,42,0.04)';
      const logoText = document.getElementById('logoText');
      if (logoText) {
        logoText.style.maxWidth = '120px';
        logoText.style.opacity = '1';
        logoText.style.marginLeft = '0';
      }
    }

    ticking = false;
  }

  window.addEventListener('scroll', function() {
    if (!ticking) {
      window.requestAnimationFrame(updateTopbarOnScroll);
      ticking = true;
    }
  }, { passive: true });
})();
