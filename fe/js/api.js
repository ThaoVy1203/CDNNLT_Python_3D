// ═══════════════════════════════════════════════════════════
// API SERVICE - Backend Integration
// ═══════════════════════════════════════════════════════════

// Load config if available, otherwise use default
const API_BASE_URL = typeof CONFIG !== 'undefined' ? CONFIG.API_BASE_URL : 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Helper method for fetch requests
  async request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const config = {
      headers: {
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  // ═══════════════════════════════════════════════════════════
  // GEOMETRY API - 3 Steps Flow
  // ═══════════════════════════════════════════════════════════

  /**
   * Step 1: Upload and analyze image
   * @param {File} file - Image file
   * @param {number|null} userId - User ID (null for guest)
   * @returns {Promise<Object>}
   */
  async uploadAndAnalyze(file, userId = null) {
    const formData = new FormData();
    formData.append('file', file);
    if (userId) {
      formData.append('ma_nguoi_dung', userId.toString());
    }

    return this.request('/geometry/upload-and-save', {
      method: 'POST',
      body: formData,
    });
  }

  /**
   * Step 2: Solve problem with AI
   * @param {number} problemId - Problem ID from step 1
   * @returns {Promise<Object>}
   */
  async solveProblem(problemId) {
    return this.request(`/geometry/solve-problem/${problemId}`, {
      method: 'POST',
    });
  }

  /**
   * Step 3: Generate 3D rendering instructions
   * @param {number} problemId - Problem ID from step 1
   * @param {boolean} forceRefresh - Bỏ qua cache, render lại từ đầu
   * @returns {Promise<Object>}
   */
  async render3D(problemId, forceRefresh = false) {
    const url = forceRefresh
      ? `/geometry/render-3d/${problemId}?force_refresh=true`
      : `/geometry/render-3d/${problemId}`;
    return this.request(url, {
      method: 'POST',
    });
  }

  /**
   * Get full problem data
   * @param {number} problemId
   * @returns {Promise<Object>}
   */
  async getProblem(problemId) {
    return this.request(`/geometry/problem/${problemId}`);
  }

  /**
   * Get solution
   * @param {number} problemId
   * @returns {Promise<Object>}
   */
  async getSolution(problemId) {
    return this.request(`/geometry/solution/${problemId}`);
  }

  /**
   * Get drawing guide
   * @param {number} problemId
   * @returns {Promise<Object>}
   */
  async getDrawingGuide(problemId) {
    return this.request(`/geometry/drawing-guide/${problemId}`);
  }

  // ═══════════════════════════════════════════════════════════
  // USER API
  // ═══════════════════════════════════════════════════════════

  /**
   * Get all users
   * @returns {Promise<Array>}
   */
  async getUsers() {
    return this.request('/nguoi-dung/');
  }

  /**
   * Get user by ID
   * @param {number} userId
   * @returns {Promise<Object>}
   */
  async getUser(userId) {
    return this.request(`/nguoi-dung/${userId}`);
  }

  // ═══════════════════════════════════════════════════════════
  // PROBLEM API
  // ═══════════════════════════════════════════════════════════

  /**
   * Get all problems
   * @returns {Promise<Array>}
   */
  async getAllProblems() {
    return this.request('/bai-toan/');
  }

  /**
   * Get problems by user
   * @param {number} userId
   * @returns {Promise<Array>}
   */
  async getUserProblems(userId) {
    return this.request(`/bai-toan/user/${userId}`);
  }

  // ═══════════════════════════════════════════════════════════
  // HEALTH CHECK
  // ═══════════════════════════════════════════════════════════

  /**
   * Check API health
   * @returns {Promise<Object>}
   */
  async healthCheck() {
    return this.request('/health');
  }
}

// Create singleton instance
const apiService = new ApiService();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = apiService;
}
