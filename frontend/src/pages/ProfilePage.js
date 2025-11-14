import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useUser } from '../context/UserContext';
import { userAPI } from '../services/api';
import './ProfilePage.css';

const ProfilePage = () => {
  const navigate = useNavigate();
  const { user } = useUser();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadStats();
  }, [user, navigate]);

  const loadStats = async () => {
    try {
      const response = await userAPI.getStats(user.id);
      if (response.data.success) {
        setStats(response.data.data.stats);
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="profile-page">
      <div className="page-header">
        <motion.button
          className="back-btn"
          onClick={() => navigate('/home')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 返回
        </motion.button>
        <h1>我的信息</h1>
      </div>

      <div className="container">
        {/* 用户信息卡片 */}
        <motion.div
          className="profile-card"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          <div className="profile-avatar">👦</div>
          <div className="profile-info">
            <h2>{user?.nickname}</h2>
            <p className="username">@{user?.username}</p>
            <div className="grade-badge">
              {user?.grade_level}年级
            </div>
          </div>
        </motion.div>

        {/* 统计数据 */}
        <div className="stats-section">
          <h2 className="section-title">学习统计</h2>
          <div className="stats-grid">
            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <div className="stat-icon">⭐</div>
              <div className="stat-value">{stats?.total_stars || 0}</div>
              <div className="stat-label">总星星数</div>
            </motion.div>

            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <div className="stat-icon">💯</div>
              <div className="stat-value">{stats?.total_points || 0}</div>
              <div className="stat-label">总积分</div>
            </motion.div>

            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <div className="stat-icon">✅</div>
              <div className="stat-value">{stats?.completed_topics || 0}</div>
              <div className="stat-label">完成主题</div>
            </motion.div>

            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              <div className="stat-icon">📝</div>
              <div className="stat-value">{stats?.total_exercises || 0}</div>
              <div className="stat-label">完成练习</div>
            </motion.div>

            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <div className="stat-icon">🎯</div>
              <div className="stat-value">{stats?.accuracy || 0}%</div>
              <div className="stat-label">正确率</div>
            </motion.div>

            <motion.div
              className="stat-card"
              whileHover={{ scale: 1.03 }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <div className="stat-icon">⏱️</div>
              <div className="stat-value">{stats?.total_time_minutes || 0}</div>
              <div className="stat-label">学习分钟数</div>
            </motion.div>
          </div>
        </div>

        {/* 成就预览 */}
        <div className="achievements-preview">
          <h2 className="section-title">我的成就</h2>
          <motion.button
            className="view-achievements-btn"
            onClick={() => navigate('/achievements')}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            查看所有成就 →
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
