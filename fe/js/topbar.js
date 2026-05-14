// Topbar component - shared across all pages
function renderTopbar(activePage = '') {
  // Check if user is logged in
  const currentUser = getCurrentUser();
  
  // Build nav items - only show History and Practice if logged in
  let navItems = `
    <li><a href="index.html" class="${activePage === 'home' ? 'active' : ''}">Trang chủ</a></li>
    <li><a href="solver.html" class="${activePage === 'solver' ? 'active' : ''}">Giải bài</a></li>`;
  
  if (currentUser) {
    navItems += `
    <li><a href="history.html" class="${activePage === 'history' ? 'active' : ''}">Lịch sử</a></li>
    <li><a href="practice.html" class="${activePage === 'practice' ? 'active' : ''}">Luyện tập</a></li>`;
  }
  
  navItems += `
    <li><a href="docs.html" class="${activePage === 'docs' ? 'active' : ''}">Tài liệu</a></li>`;
  
  return `
<header class="topbar">
  <div class="logo">Geo<em>3D</em></div>
  <nav><ul class="nav">
    ${navItems}
  </ul></nav>
  <div class="topbar-right">
    <button class="btn-filled" id="loginBtn" onclick="window.location.href='login.html'">Đăng nhập</button>
    
    <!-- User Profile Dropdown -->
    <div class="user-dropdown" id="userDropdown" style="display:none;">
      <button class="user-avatar-btn" onclick="toggleUserMenu()">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
        <span class="user-name" id="userName"></span>
        <svg class="chevron-icon" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="margin-left:4px">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </button>
      
      <div class="user-menu" id="userMenu">
        <a href="profile.html" class="user-menu-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <span>Hồ sơ cá nhân</span>
        </a>
        
        <a href="history.html" class="user-menu-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 20h9"></path>
            <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
          </svg>
          <span>Lịch sử giải bài</span>
        </a>
        
        <a href="docs.html" class="user-menu-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
          </svg>
          <span>Tài liệu học tập</span>
        </a>
        
        <a href="#" class="user-menu-item">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
          </svg>
          <span>Trợ giúp</span>
        </a>
        
        <div class="user-menu-divider"></div>
        
        <a href="#" class="user-menu-item logout" onclick="handleLogout(event)">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
          <span>Đăng xuất</span>
        </a>
      </div>
    </div>
  </div>
</header>
  `;
}

// Toggle user dropdown menu
function toggleUserMenu() {
  const dropdown = document.getElementById('userDropdown');
  const menu = document.getElementById('userMenu');
  
  if (menu && dropdown) {
    // Toggle show class on menu
    menu.classList.toggle('show');
    // Toggle open class on dropdown for chevron rotation
    dropdown.classList.toggle('open');
  }
}

// Close dropdown when clicking outside
window.addEventListener('click', function(e) {
  const dropdown = document.getElementById('userDropdown');
  const menu = document.getElementById('userMenu');
  
  if (dropdown && menu && !dropdown.contains(e.target)) {
    menu.classList.remove('show');
    dropdown.classList.remove('open');
  }
});

// Close dropdown when mouse leaves - with delay to allow moving to menu items
let closeMenuTimeout;

document.addEventListener('DOMContentLoaded', function() {
  const dropdown = document.getElementById('userDropdown');
  const menu = document.getElementById('userMenu');
  
  if (dropdown && menu) {
    // When mouse leaves the entire dropdown area
    dropdown.addEventListener('mouseleave', function(e) {
      if (menu.classList.contains('show')) {
        // Set timeout to close after 800ms
        closeMenuTimeout = setTimeout(() => {
          menu.classList.remove('show');
          dropdown.classList.remove('open');
        }, 800);
      }
    });
    
    // When mouse enters back, cancel the close
    dropdown.addEventListener('mouseenter', function() {
      if (closeMenuTimeout) {
        clearTimeout(closeMenuTimeout);
        closeMenuTimeout = null;
      }
    });
  }
});

// Handle logout from dropdown
function handleLogout(e) {
  e.preventDefault();
  localStorage.removeItem('geo3d_current_user');
  window.location.href = 'index.html';
}

// Check auth and update topbar
function initTopbar() {
  const currentUser = getCurrentUser();
  const loginBtn = document.getElementById('loginBtn');
  const userDropdown = document.getElementById('userDropdown');
  const userName = document.getElementById('userName');
  
  if (currentUser) {
    // User is logged in - show dropdown, hide login button
    if (loginBtn) loginBtn.style.display = 'none';
    if (userDropdown) userDropdown.style.display = 'block';
    
    // Display username (not email)
    if (userName) {
      userName.textContent = currentUser.username || 'User';
    }
  } else {
    // User is not logged in - show login button, hide dropdown
    if (loginBtn) loginBtn.style.display = 'inline-block';
    if (userDropdown) userDropdown.style.display = 'none';
  }
  
  return currentUser;
}
