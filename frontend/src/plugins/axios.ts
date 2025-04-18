import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  async (config) => {
    let token = localStorage.getItem('access_token');
    const refreshToken = localStorage.getItem('refresh_token');

    if (token) {
      const now = Math.floor(Date.now() / 1000);
      const tokenParts = JSON.parse(atob(token.split('.')[1]));

      if (tokenParts.exp > now) {
        config.headers['Authorization'] = `Bearer ${token}`;
        return config;
      } else if (refreshToken) {
        try {
          const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: refreshToken
          });
          localStorage.setItem('access_token', response.data.access);
          config.headers['Authorization'] = `Bearer ${response.data.access}`;
          return config;
        } catch (error) {
          console.error('Token refresh failed:', error);
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          window.location.href = '/login';
          return Promise.reject(error);
        }
      }
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;
