/**
 * History Page - Backend Integration
 * Kết nối với API backend để lấy lịch sử bài toán từ database
 */

import { API_BASE_URL } from './config.js';

let currentFilter = 'all';
let allHistory = [];

// Load history from backend
async function loadHistory() {
  const maNguoiDung = localStorage.getItem('maNguoiDung');
  
  if (!maNguoiDung) {
    console.warn('No user ID found');
    showEmptyState();
    return;
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}/bai-toan/user/${maNguoiDung}`);
    
    if (!response.ok) {
      throw new Error('Failed to load history');
    }
    
    const data = await response.json();
    
    // Transform backend data to frontend format
    allHistory = data.map(item => ({
      id: item.maBaiToan,
      title: item.tomTatDe || 'Bài toán hình học không gian',
      description: item.deBaiTho ? item.deBaiTho.substring(0, 100) + '...' : 'Hình chóp S.ABCD với các điều kiện cho trước',
      type: item.loaiHinh || 'Hình chóp',
      timestamp: item.ngayTao,
      solveTime: '3 phút', // Mock data - có thể tính từ database sau
      status: 'completed'
    }));
    
    if (allHistory.length === 0) {
      showEmptyState();
    } else {
      hideEmptyState();
      displayHistory(allHistory);
    }
    
    updateStatistics();
    
  } catch (error) {
    console.error('Error loading history:', error);
    showEmptyState();
  }
}

function showEmptyState() {
  document.getElementById('emptyState').style.display = 'block';
  document.getElementById('historyList').style.display = 'none';
}

function hideEmptyState() {
  document.getElementById('emptyState').style.display = 'none';
  document.getElementById('historyList').style.display = 'grid';
}

function displayHistory(history) {
  const historyList = document.getElementById('historyList');
  
  if (history.length === 0) {
    historyList.innerHTML = '<p style="text-align:center;color:var(--ink-3);padding:40px;">Không tìm thấy bài toán nào</p>';
    return;
  }
  
  historyList.innerHTML = history.map((item) => {
    const date = new Date(item.timestamp);
    const dateStr = date.toLocaleDateString('vi-VN');
    const timeStr = date.toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'});
    
    return `
      <div class="history-card" onclick="viewProblem(${item.id})">
        <div class="history-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
            <polyline points="2 17 12 22 22 17"></polyline>
            <polyline points="2 12 12 17 22 12"></polyline>
          </svg>
        </div>
        
        <div class="history-content">
          <h3 class="history-problem-title">${item.title}</h3>
          <p class="history-problem-desc">${item.description}</p>
          
          <div class="history-meta">
            <div class="history-meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              <span>${item.solveTime}</span>
            </div>
            <div class="history-meta-item">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>${item.type}</span>
            </div>
          </div>
        </div>
        
        <div class="history-actions">
          <div class="history-date">${dateStr} ${timeStr}</div>
          <span class="history-status status-completed">✓ Hoàn thành</span>
        </div>
      </div>
    `;
  }).join('');
}

function updateStatistics() {
  const history = allHistory;
  
  // Total solved
  document.getElementById('totalSolved').textContent = history.length;
  
  // This week
  const weekAgo = new Date();
  weekAgo.setDate(weekAgo.getDate() - 7);
  const thisWeek = history.filter(item => new Date(item.timestamp) > weekAgo).length;
  document.getElementById('thisWeek').textContent = thisWeek;
  
  // This month
  const monthAgo = new Date();
  monthAgo.setMonth(monthAgo.getMonth() - 1);
  const thisMonth = history.filter(item => new Date(item.timestamp) > monthAgo).length;
  document.getElementById('thisMonth').textContent = thisMonth;
  
  // Average time (mock data for now)
  document.getElementById('avgTime').textContent = '3m';
}

function filterHistory(filter) {
  currentFilter = filter;
  
  // Update active button
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  event.target.classList.add('active');
  
  let filtered = allHistory;
  
  if (filter === 'week') {
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);
    filtered = allHistory.filter(item => new Date(item.timestamp) > weekAgo);
  } else if (filter === 'month') {
    const monthAgo = new Date();
    monthAgo.setMonth(monthAgo.getMonth() - 1);
    filtered = allHistory.filter(item => new Date(item.timestamp) > monthAgo);
  } else if (filter === 'completed') {
    filtered = allHistory.filter(item => item.status === 'completed' || true);
  }
  
  displayHistory(filtered);
}

async function viewProblem(problemId) {
  // Redirect to solver page with problem ID
  window.location.href = `solver.html?id=${problemId}`;
}

// Export functions to global scope
window.loadHistory = loadHistory;
window.filterHistory = filterHistory;
window.viewProblem = viewProblem;
