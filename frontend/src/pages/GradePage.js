import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useUser } from '../context/UserContext';
import { curriculumAPI } from '../services/api';
import './GradePage.css';

const GradePage = () => {
  const { gradeId } = useParams();
  const navigate = useNavigate();
  const { user } = useUser();
  const [grade, setGrade] = useState(null);
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadGradeData();
  }, [gradeId, user, navigate]);

  const loadGradeData = async () => {
    try {
      setLoading(true);
      const response = await curriculumAPI.getGrade(gradeId);

      if (response.data.success) {
        setGrade(response.data.data);
        setTopics(response.data.data.topics || []);
      }
    } catch (error) {
      console.error('Error loading grade:', error);
      toast.error('加载年级数据失败');
    } finally {
      setLoading(false);
    }
  };

  const getTopicColor = (index) => {
    const colors = [
      '#FF6B6B', '#4ECDC4', '#95E1D3', '#FFD93D',
      '#6BCB77', '#4D96FF', '#FF6B9D', '#C4E538'
    ];
    return colors[index % colors.length];
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="grade-page">
      {/* 顶部导航 */}
      <div className="page-header">
        <motion.button
          className="back-btn"
          onClick={() => navigate('/home')}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← 返回
        </motion.button>
        <h1>{grade?.name}</h1>
      </div>

      <div className="container">
        {/* 年级信息卡片 */}
        <motion.div
          className="grade-info-card"
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
        >
          <div className="grade-number">{grade?.level}</div>
          <div className="grade-details">
            <h2>{grade?.name}数学</h2>
            <p>{grade?.description}</p>
            <div className="topic-count">
              共 {topics.length} 个学习主题
            </div>
          </div>
        </motion.div>

        {/* 主题列表 */}
        <div className="topics-section">
          <h2 className="section-title">学习主题</h2>
          <div className="topics-grid">
            {topics.map((topic, index) => (
              <motion.div
                key={topic.id}
                className="topic-card"
                onClick={() => navigate(`/topic/${topic.id}`)}
                whileHover={{ scale: 1.03, y: -5 }}
                whileTap={{ scale: 0.97 }}
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
                style={{
                  borderLeft: `6px solid ${getTopicColor(index)}`,
                }}
              >
                <div
                  className="topic-icon"
                  style={{ background: getTopicColor(index) }}
                >
                  {topic.icon || '📚'}
                </div>

                <div className="topic-content">
                  <h3>{topic.name}</h3>
                  <p>{topic.description}</p>

                  <div className="topic-meta">
                    <span className="meta-item">
                      ⏱️ {topic.estimated_time || 10} 分钟
                    </span>
                    <span className="meta-item">
                      📝 {topic.exercises_count || 0} 题
                    </span>
                    <span className="meta-item difficulty">
                      {'⭐'.repeat(topic.difficulty || 1)}
                    </span>
                  </div>
                </div>

                <div className="topic-arrow">→</div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GradePage;
