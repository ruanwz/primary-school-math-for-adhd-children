import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useUser } from '../context/UserContext';
import { curriculumAPI, userAPI } from '../services/api';
import './TopicPage.css';

const TopicPage = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();
  const { user } = useUser();
  const [topic, setTopic] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadData();
  }, [topicId, user, navigate]);

  const loadData = async () => {
    try {
      setLoading(true);

      // 加载主题数据
      const topicResponse = await curriculumAPI.getTopic(topicId, true);
      if (topicResponse.data.success) {
        setTopic(topicResponse.data.data);
      }

      // 加载用户进度
      if (user) {
        const progressResponse = await userAPI.getTopicProgress(user.id, topicId);
        if (progressResponse.data.success) {
          setProgress(progressResponse.data.data);
        }
      }
    } catch (error) {
      console.error('Error loading data:', error);
      toast.error('加载数据失败');
    } finally {
      setLoading(false);
    }
  };

  const startExercise = () => {
    navigate(`/exercise/${topicId}`);
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="topic-page">
      {/* 顶部导航 */}
      <div className="page-header">
        <motion.button
          className="back-btn"
          onClick={() => navigate(-1)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 返回
        </motion.button>
        <h1>{topic?.name}</h1>
      </div>

      <div className="container">
        {/* 主题详情卡片 */}
        <motion.div
          className="topic-detail-card"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          <div
            className="topic-header"
            style={{ background: topic?.color || '#667eea' }}
          >
            <div className="topic-icon-large">{topic?.icon || '📚'}</div>
            <div className="topic-info">
              <h2>{topic?.name}</h2>
              <p>{topic?.description}</p>
            </div>
          </div>

          <div className="topic-stats">
            <div className="stat-box">
              <div className="stat-icon">📝</div>
              <div className="stat-text">
                <span className="stat-value">{topic?.exercises_count || 0}</span>
                <span className="stat-label">练习题</span>
              </div>
            </div>

            <div className="stat-box">
              <div className="stat-icon">⏱️</div>
              <div className="stat-text">
                <span className="stat-value">{topic?.estimated_time || 10}</span>
                <span className="stat-label">分钟</span>
              </div>
            </div>

            <div className="stat-box">
              <div className="stat-icon">⭐</div>
              <div className="stat-text">
                <span className="stat-value">{progress?.stars_earned || 0}/3</span>
                <span className="stat-label">星星</span>
              </div>
            </div>
          </div>

          {/* 进度显示 */}
          {progress && progress.exercises_completed > 0 && (
            <div className="progress-section">
              <div className="progress-header">
                <span>学习进度</span>
                <span className="progress-percent">
                  {progress.accuracy || 0}% 正确率
                </span>
              </div>
              <div className="progress-bar">
                <motion.div
                  className="progress-fill"
                  initial={{ width: 0 }}
                  animate={{
                    width: `${(progress.exercises_completed / (topic?.exercises_count || 1)) * 100}%`,
                  }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                />
              </div>
              <div className="progress-stats">
                <span>✅ {progress.correct_count} 题正确</span>
                <span>❌ {progress.wrong_count} 题错误</span>
              </div>
            </div>
          )}

          {/* 开始练习按钮 */}
          <motion.button
            className="start-btn"
            onClick={startExercise}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {progress && progress.exercises_completed > 0 ? '继续练习' : '开始学习'}
            <span className="btn-icon">→</span>
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
};

export default TopicPage;
