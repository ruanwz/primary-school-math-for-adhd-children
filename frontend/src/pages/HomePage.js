import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useUser } from '../context/UserContext';
import { curriculumAPI, userAPI } from '../services/api';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const { user, logout } = useUser();
  const [grades, setGrades] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, navigate]);

  const loadData = async () => {
    try {
      setLoading(true);

      // 加载年级数据
      const gradesResponse = await curriculumAPI.getGrades();
      if (gradesResponse.data.success) {
        setGrades(gradesResponse.data.data);
      }

      // 加载用户统计数据
      if (user) {
        const statsResponse = await userAPI.getStats(user.id);
        if (statsResponse.data.success) {
          setStats(statsResponse.data.data.stats);
        }
      }
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    toast.success('已退出登录');
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="home-page">
      {/* 顶部导航栏 */}
      <nav className="navbar">
        <div className="navbar-content">
          <h1 className="logo">数学学习助手</h1>
          <div className="nav-right">
            <motion.button
              className="nav-btn"
              onClick={() => navigate('/profile')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              我的信息
            </motion.button>
            <motion.button
              className="nav-btn"
              onClick={() => navigate('/achievements')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              成就
            </motion.button>
            <motion.button
              className="nav-btn logout"
              onClick={handleLogout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              退出
            </motion.button>
          </div>
        </div>
      </nav>

      <div className="container">
        {/* 欢迎区域 */}
        <motion.div
          className="welcome-section"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="welcome-card">
            <div className="welcome-text">
              <h2>你好，{user?.nickname}！</h2>
              <p>今天也要加油学习哦！</p>
            </div>
            <motion.div
              className="avatar"
              animate={{
                rotate: [0, 10, -10, 0],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            >
              👦
            </motion.div>
          </div>

          {/* 统计卡片 */}
          {stats && (
            <div className="stats-grid">
              <motion.div
                className="stat-card"
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
              >
                <div className="stat-icon">⭐</div>
                <div className="stat-value">{stats.total_stars}</div>
                <div className="stat-label">获得星星</div>
              </motion.div>

              <motion.div
                className="stat-card"
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                <div className="stat-icon">✅</div>
                <div className="stat-value">{stats.completed_topics}</div>
                <div className="stat-label">完成主题</div>
              </motion.div>

              <motion.div
                className="stat-card"
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                <div className="stat-icon">🎯</div>
                <div className="stat-value">{stats.accuracy}%</div>
                <div className="stat-label">正确率</div>
              </motion.div>

              <motion.div
                className="stat-card"
                whileHover={{ scale: 1.05 }}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                <div className="stat-icon">💯</div>
                <div className="stat-value">{stats.total_points}</div>
                <div className="stat-label">总积分</div>
              </motion.div>
            </div>
          )}
        </motion.div>

        {/* 年级选择 */}
        <div className="grades-section">
          <h2 className="section-title">选择年级</h2>
          <div className="grades-grid">
            {grades.map((grade, index) => (
              <motion.div
                key={grade.id}
                className="grade-card"
                onClick={() => navigate(`/grade/${grade.id}`)}
                whileHover={{ scale: 1.05, y: -5 }}
                whileTap={{ scale: 0.95 }}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="grade-icon">{grade.level}</div>
                <h3>{grade.name}</h3>
                <p>{grade.description}</p>
                <div className="grade-badge">
                  {grade.topics_count} 个主题
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
