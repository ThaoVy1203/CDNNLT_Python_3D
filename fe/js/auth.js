// ═══════════════════════════════════════════════════════════
// AUTHENTICATION SYSTEM
// ═══════════════════════════════════════════════════════════

// User roles
const ROLES = {
  GUEST: 'guest',
  MEMBER: 'member',
  ADMIN: 'admin'
};

// Initialize demo accounts (in real app, this would be backend)
function initDemoAccounts() {
  const users = localStorage.getItem('geo3d_users');
  if (!users) {
    const demoUsers = [
      {
        id: 1,
        username: 'admin',
        email: 'admin@geo3d.com',
        password: 'admin123',
        fullname: 'Admin',
        role: ROLES.ADMIN,
        createdAt: new Date().toISOString()
      },
      {
        id: 2,
        username: 'user',
        email: 'user@example.com',
        password: '123456',
        fullname: 'Người dùng demo',
        role: ROLES.MEMBER,
        createdAt: new Date().toISOString()
      }
    ];
    localStorage.setItem('geo3d_users', JSON.stringify(demoUsers));
  }
}

// Get all users
function getUsers() {
  const users = localStorage.getItem('geo3d_users');
  return users ? JSON.parse(users) : [];
}

// Save users
function saveUsers(users) {
  localStorage.setItem('geo3d_users', JSON.stringify(users));
}

// Get current user
function getCurrentUser() {
  const user = localStorage.getItem('geo3d_current_user');
  return user ? JSON.parse(user) : null;
}

// Set current user
function setCurrentUser(user) {
  localStorage.setItem('geo3d_current_user', JSON.stringify(user));
}

// Logout
function logout() {
  localStorage.removeItem('geo3d_current_user');
  window.location.href = 'index.html';
}

// Show alert
function showAlert(message, type = 'error') {
  const alert = document.getElementById('alert');
  if (alert) {
    alert.textContent = message;
    alert.className = `alert alert-${type}`;
    alert.style.display = 'block';
    
    setTimeout(() => {
      alert.style.display = 'none';
    }, 5000);
  }
}

// ═══════════════════════════════════════════════════════════
// LOGIN
// ═══════════════════════════════════════════════════════════
function handleLogin(event) {
  event.preventDefault();
  
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  
  const users = getUsers();
  const user = users.find(u => 
    (u.username === username || u.email === username) && u.password === password
  );
  
  if (user) {
    // Remove password before storing
    const userSession = { ...user };
    delete userSession.password;
    
    setCurrentUser(userSession);
    showAlert('Đăng nhập thành công!', 'success');
    
    setTimeout(() => {
      if (user.role === ROLES.ADMIN) {
        window.location.href = 'admin.html';
      } else {
        window.location.href = 'solver.html';
      }
    }, 1000);
  } else {
    showAlert('Tên đăng nhập hoặc mật khẩu không đúng!');
  }
}

// ═══════════════════════════════════════════════════════════
// REGISTER
// ═══════════════════════════════════════════════════════════
function handleRegister(event) {
  event.preventDefault();
  
  const fullname = document.getElementById('fullname').value.trim();
  const email = document.getElementById('email').value.trim();
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirmPassword').value;
  
  // Validation
  if (password !== confirmPassword) {
    showAlert('Mật khẩu xác nhận không khớp!');
    return;
  }
  
  const users = getUsers();
  
  // Check if username or email exists
  if (users.find(u => u.username === username)) {
    showAlert('Tên đăng nhập đã tồn tại!');
    return;
  }
  
  if (users.find(u => u.email === email)) {
    showAlert('Email đã được sử dụng!');
    return;
  }
  
  // Create new user
  const newUser = {
    id: users.length + 1,
    username,
    email,
    password,
    fullname,
    role: ROLES.MEMBER,
    createdAt: new Date().toISOString()
  };
  
  users.push(newUser);
  saveUsers(users);
  
  showAlert('Đăng ký thành công! Đang chuyển đến trang đăng nhập...', 'success');
  
  setTimeout(() => {
    window.location.href = 'login.html';
  }, 2000);
}

// ═══════════════════════════════════════════════════════════
// GUEST MODE
// ═══════════════════════════════════════════════════════════
function continueAsGuest() {
  const guestUser = {
    id: 'guest_' + Date.now(),
    username: 'Khách',
    role: ROLES.GUEST,
    isGuest: true
  };
  
  setCurrentUser(guestUser);
  window.location.href = 'solver.html';
}

// ═══════════════════════════════════════════════════════════
// CHECK AUTH ON PAGE LOAD
// ═══════════════════════════════════════════════════════════
function checkAuthOld() {
  const currentUser = getCurrentUser();
  
  // Update UI based on user status
  const loginBtn = document.querySelector('.btn-line');
  const signupBtn = document.querySelector('.btn-filled');
  
  if (currentUser) {
    if (loginBtn) {
      loginBtn.textContent = currentUser.fullname || currentUser.username;
      loginBtn.onclick = () => {
        if (currentUser.role === ROLES.ADMIN) {
          window.location.href = 'admin.html';
        } else {
          window.location.href = 'profile.html';
        }
      };
    }
    
    if (signupBtn) {
      signupBtn.textContent = 'Đăng xuất';
      signupBtn.onclick = logout;
    }
  }
  
  return currentUser;
}

function showUserMenu() {
  // Redirect to profile page
  window.location.href = 'profile.html';
}

// ═══════════════════════════════════════════════════════════
// HISTORY MANAGEMENT (for members only)
// ═══════════════════════════════════════════════════════════
function saveToHistory(problem) {
  const currentUser = getCurrentUser();
  
  if (!currentUser || currentUser.role === ROLES.GUEST) {
    return; // Guests don't save history
  }
  
  const historyKey = `geo3d_history_${currentUser.id}`;
  let history = localStorage.getItem(historyKey);
  history = history ? JSON.parse(history) : [];
  
  history.unshift({
    ...problem,
    timestamp: new Date().toISOString()
  });
  
  // Keep only last 50 items
  if (history.length > 50) {
    history = history.slice(0, 50);
  }
  
  localStorage.setItem(historyKey, JSON.stringify(history));
}

function getHistory() {
  const currentUser = getCurrentUser();
  
  if (!currentUser || currentUser.role === ROLES.GUEST) {
    return [];
  }
  
  const historyKey = `geo3d_history_${currentUser.id}`;
  const history = localStorage.getItem(historyKey);
  return history ? JSON.parse(history) : [];
}

// ═══════════════════════════════════════════════════════════
// INITIALIZE
// ═══════════════════════════════════════════════════════════
initDemoAccounts();

// Check auth on page load - only for pages that don't have custom checkAuth
if (typeof window !== 'undefined') {
  window.addEventListener('DOMContentLoaded', function() {
    // Only run checkAuthOld if page doesn't use topbar.js
    if (typeof initTopbar === 'undefined' && typeof checkAuth === 'undefined') {
      checkAuthOld();
    }
  });
}
