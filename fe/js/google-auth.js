/**
 * Google Authentication Handler
 * Xử lý đăng nhập Google OAuth và lưu user vào database
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Xử lý callback từ Google OAuth
 * @param {Object} response - Response từ Google Sign-In
 */
async function handleGoogleLogin(response) {
  try {
    console.log('Google login response:', response);
    
    // Decode JWT token từ Google
    const credential = response.credential;
    const payload = parseJwt(credential);
    
    console.log('Google user info:', payload);
    
    // Gọi API backend để tạo/lấy user
    const backendResponse = await fetch(`${API_BASE_URL}/auth/google-login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        googleId: payload.sub,
        email: payload.email,
        name: payload.name,
        picture: payload.picture
      })
    });
    
    if (!backendResponse.ok) {
      const error = await backendResponse.json();
      throw new Error(error.detail || 'Đăng nhập thất bại');
    }
    
    const data = await backendResponse.json();
    console.log('Backend response:', data);
    
    if (data.success && data.user) {
      // Lưu thông tin user vào localStorage
      localStorage.setItem('maNguoiDung', data.user.maNguoiDung);
      localStorage.setItem('geo3d_current_user', JSON.stringify({
        id: data.user.maNguoiDung,
        username: data.user.tenDangNhap,
        email: data.user.email,
        role: data.user.vaiTro,
        isGoogle: true
      }));
      
      // Hiển thị thông báo thành công
      alert('✅ Đăng nhập thành công!');
      
      // Redirect đến trang solver
      window.location.href = 'solver.html';
    } else {
      throw new Error('Không nhận được thông tin user từ server');
    }
    
  } catch (error) {
    console.error('Google login error:', error);
    alert('❌ Lỗi đăng nhập: ' + error.message);
  }
}

/**
 * Parse JWT token
 * @param {string} token - JWT token
 * @returns {Object} Decoded payload
 */
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (error) {
    console.error('Error parsing JWT:', error);
    return {};
  }
}

/**
 * Khởi tạo Google Sign-In button
 */
function initGoogleSignIn() {
  if (typeof google !== 'undefined' && google.accounts) {
    google.accounts.id.initialize({
      client_id: 'YOUR_GOOGLE_CLIENT_ID', // TODO: Thay bằng Client ID thực
      callback: handleGoogleLogin
    });
    
    // Render button
    const buttonDiv = document.getElementById('google-signin-button');
    if (buttonDiv) {
      google.accounts.id.renderButton(
        buttonDiv,
        {
          theme: 'outline',
          size: 'large',
          text: 'signin_with',
          locale: 'vi'
        }
      );
    }
    
    // Prompt one-tap
    google.accounts.id.prompt();
  }
}

// Export functions
window.handleGoogleLogin = handleGoogleLogin;
window.initGoogleSignIn = initGoogleSignIn;
