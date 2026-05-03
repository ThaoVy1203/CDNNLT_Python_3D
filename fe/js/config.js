// ═══════════════════════════════════════════════════════════
// CONFIGURATION - Frontend Config
// ═══════════════════════════════════════════════════════════

const CONFIG = {
  // API Configuration
  API_BASE_URL: 'http://localhost:8000',
  
  // Google OAuth Configuration
  // Note: Client ID is safe to expose in frontend
  // NEVER put Client Secret here!
  GOOGLE_CLIENT_ID: '937311065493-1viejtr911lbokveh34sr99hpe35kmbp.apps.googleusercontent.com',
  
  // App Configuration
  APP_NAME: 'Geo3D',
  APP_VERSION: '1.0.0',
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}
