import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import './App.css';

// 页面组件
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import GradePage from './pages/GradePage';
import TopicPage from './pages/TopicPage';
import ExercisePage from './pages/ExercisePage';
import ProfilePage from './pages/ProfilePage';
import AchievementsPage from './pages/AchievementsPage';

// Context
import { UserProvider } from './context/UserContext';

function App() {
  // 用户状态由UserContext管理，不需要在这里维护

  return (
    <UserProvider>
      <Router>
        <div className="App">
          <Toaster
            position="top-center"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#fff',
                color: '#333',
                fontSize: '16px',
                fontWeight: '500',
                padding: '16px 24px',
                borderRadius: '12px',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
              },
              success: {
                iconTheme: {
                  primary: '#4CAF50',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#f44336',
                  secondary: '#fff',
                },
              },
            }}
          />

          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/grade/:gradeId" element={<GradePage />} />
            <Route path="/topic/:topicId" element={<TopicPage />} />
            <Route path="/exercise/:topicId" element={<ExercisePage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/achievements" element={<AchievementsPage />} />
            <Route path="/" element={<Navigate to="/login" replace />} />
          </Routes>
        </div>
      </Router>
    </UserProvider>
  );
}

export default App;
