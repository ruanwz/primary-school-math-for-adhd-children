import axios from 'axios';

// 确保API URL总是包含 /api 路径
const getApiBaseUrl = () => {
  const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:5000';
  // 如果URL已经包含 /api，直接使用；否则添加 /api
  return baseUrl.endsWith('/api') ? baseUrl : `${baseUrl}/api`;
};

const API_BASE_URL = getApiBaseUrl();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 用户相关API
export const userAPI = {
  register: (username, nickname, gradeLevel) =>
    api.post('/user/register', { username, nickname, grade_level: gradeLevel }),

  login: (username) =>
    api.post('/user/login', { username }),

  getUser: (userId) =>
    api.get(`/user/${userId}`),

  getProgress: (userId) =>
    api.get(`/user/${userId}/progress`),

  getTopicProgress: (userId, topicId) =>
    api.get(`/user/${userId}/progress/${topicId}`),

  updateProgress: (userId, topicId, data) =>
    api.put(`/user/${userId}/progress/${topicId}`, data),

  getAchievements: (userId) =>
    api.get(`/user/${userId}/achievements`),

  getStats: (userId) =>
    api.get(`/user/${userId}/stats`),
};

// 课程相关API
export const curriculumAPI = {
  getGrades: () =>
    api.get('/curriculum/grades'),

  getGrade: (gradeId) =>
    api.get(`/curriculum/grades/${gradeId}`),

  getTopic: (topicId, includeExercises = false) =>
    api.get(`/curriculum/topics/${topicId}`, {
      params: { include_exercises: includeExercises }
    }),

  getTopicExercises: (topicId, difficulty = null) =>
    api.get(`/curriculum/topics/${topicId}/exercises`, {
      params: difficulty ? { difficulty } : {}
    }),

  searchTopics: (keyword, gradeLevel = null) =>
    api.get('/curriculum/search', {
      params: { q: keyword, grade: gradeLevel }
    }),
};

// 练习题相关API
export const exerciseAPI = {
  getExercise: (exerciseId) =>
    api.get(`/curriculum/exercises/${exerciseId}`),

  checkAnswer: (exerciseId, answer) =>
    api.post('/exercise/check', { exercise_id: exerciseId, answer }),

  getRandomExercises: (topicId = null, difficulty = null, count = 5) =>
    api.get('/exercise/random', {
      params: { topic_id: topicId, difficulty, count }
    }),
};

export default api;
