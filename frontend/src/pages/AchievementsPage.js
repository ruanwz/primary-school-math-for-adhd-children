import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useUser } from '../context/UserContext';
import { userAPI } from '../services/api';
import './AchievementsPage.css';

const AchievementsPage = () => {
  const navigate = useNavigate();
  const { user } = useUser();
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadAchievements();
  }, [user, navigate]);

  const loadAchievements = async () => {
    try {
      const response = await userAPI.getAchievements(user.id);
      if (response.data.success) {
        setAchievements(response.data.data);
      }
    } catch (error) {
      console.error('Error loading achievements:', error);
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
    <div className="achievements-page">
      <div className="page-header">
        <motion.button
          className="back-btn"
          onClick={() => navigate('/home')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 返回
        </motion.button>
        <h1>我的成就</h1>
      </div>

      <div className="container">
        <div className="achievements-header">
          <h2>已获得 {achievements.length} 个成就</h2>
          <p>继续努力，解锁更多成就！</p>
        </div>

        <div className="achievements-grid">
          {achievements.length > 0 ? (
            achievements.map((userAchievement, index) => (
              <motion.div
                key={userAchievement.id}
                className="achievement-card"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
              >
                <div className="achievement-icon">
                  {userAchievement.achievement?.icon || '🏆'}
                </div>
                <h3>{userAchievement.achievement?.name}</h3>
                <p>{userAchievement.achievement?.description}</p>
                <div className="achievement-points">
                  +{userAchievement.achievement?.points_reward} 积分
                </div>
                <div className="achievement-date">
                  {new Date(userAchievement.earned_at).toLocaleDateString('zh-CN')}
                </div>
              </motion.div>
            ))
          ) : (
            <div className="no-achievements">
              <div className="empty-icon">🎯</div>
              <p>还没有获得成就</p>
              <p className="empty-hint">继续学习，解锁你的第一个成就！</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AchievementsPage;
