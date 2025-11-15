import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Confetti from 'react-confetti';
import toast from 'react-hot-toast';
import { useUser } from '../context/UserContext';
import { curriculumAPI, exerciseAPI, userAPI } from '../services/api';
import './ExercisePage.css';

const ExercisePage = () => {
  const { topicId } = useParams();
  const navigate = useNavigate();
  const { user, updateUser } = useUser();

  const [exercises, setExercises] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState('');
  const [showFeedback, setShowFeedback] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [loading, setLoading] = useState(true);
  const [showConfetti, setShowConfetti] = useState(false);

  // 统计数据
  const [stats, setStats] = useState({
    correct: 0,
    wrong: 0,
    startTime: Date.now(),
  });

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    loadExercises();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [topicId, user, navigate]);

  const loadExercises = async () => {
    try {
      setLoading(true);
      const response = await curriculumAPI.getTopicExercises(topicId);

      if (response.data.success && response.data.data.length > 0) {
        setExercises(response.data.data);
      } else {
        toast.error('没有找到练习题');
        navigate(-1);
      }
    } catch (error) {
      console.error('Error loading exercises:', error);
      toast.error('加载练习题失败');
      navigate(-1);
    } finally {
      setLoading(false);
    }
  };

  const currentExercise = exercises[currentIndex];

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!userAnswer.trim()) {
      toast.error('请输入答案');
      return;
    }

    try {
      const response = await exerciseAPI.checkAnswer(
        currentExercise.id,
        userAnswer
      );

      if (response.data.success) {
        const correct = response.data.is_correct;
        setIsCorrect(correct);
        setShowFeedback(true);

        // 更新统计
        setStats((prev) => ({
          ...prev,
          correct: prev.correct + (correct ? 1 : 0),
          wrong: prev.wrong + (correct ? 0 : 1),
        }));

        if (correct) {
          toast.success('太棒了！答对了！');
          setShowConfetti(true);
          setTimeout(() => setShowConfetti(false), 3000);
        } else {
          toast.error('再想想看哦');
        }
      }
    } catch (error) {
      console.error('Error checking answer:', error);
      toast.error('检查答案失败');
    }
  };

  const handleNext = async () => {
    setShowFeedback(false);
    setUserAnswer('');

    if (currentIndex < exercises.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      // 完成所有练习
      await saveProgress();
      navigate(`/topic/${topicId}`);
    }
  };

  const saveProgress = async () => {
    try {
      const timeSpent = Math.floor((Date.now() - stats.startTime) / 1000);

      const progressData = {
        exercises_completed: exercises.length,
        correct_count: stats.correct,
        wrong_count: stats.wrong,
        time_spent: timeSpent,
        completed: true,
      };

      await userAPI.updateProgress(user.id, topicId, progressData);

      // 计算星星
      const accuracy = stats.correct / exercises.length;
      let stars = 0;
      if (accuracy >= 0.95) stars = 3;
      else if (accuracy >= 0.80) stars = 2;
      else if (accuracy >= 0.60) stars = 1;

      // 更新用户总星星数
      if (stars > 0) {
        updateUser({
          total_stars: (user.total_stars || 0) + stars,
          total_points: (user.total_points || 0) + stars * 100,
        });
      }

      toast.success(`完成练习！获得${stars}颗星星！`);
    } catch (error) {
      console.error('Error saving progress:', error);
      toast.error('保存进度失败');
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
    <div className="exercise-page">
      {showConfetti && <Confetti recycle={false} numberOfPieces={200} />}

      {/* 顶部导航 */}
      <div className="exercise-header">
        <motion.button
          className="exit-btn"
          onClick={() => navigate(`/topic/${topicId}`)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ✕ 退出
        </motion.button>

        {/* 进度指示器 */}
        <div className="exercise-progress">
          <span className="progress-text">
            {currentIndex + 1} / {exercises.length}
          </span>
          <div className="progress-bar">
            <motion.div
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{
                width: `${((currentIndex + 1) / exercises.length) * 100}%`,
              }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>

        {/* 实时统计 */}
        <div className="live-stats">
          <span className="stat-item correct">✅ {stats.correct}</span>
          <span className="stat-item wrong">❌ {stats.wrong}</span>
        </div>
      </div>

      <div className="exercise-container">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            className="exercise-card"
            initial={{ x: 300, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -300, opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* 题目 */}
            <div className="question-section">
              <div className="question-number">
                第 {currentIndex + 1} 题
              </div>
              <h2 className="question-text">
                {currentExercise?.question_text}
              </h2>
            </div>

            {/* 答案输入区 */}
            {!showFeedback ? (
              <form onSubmit={handleSubmit} className="answer-section">
                {currentExercise?.question_type === 'multiple_choice' ? (
                  <div className="options-grid">
                    {currentExercise?.options?.map((option, index) => (
                      <motion.button
                        key={index}
                        type="button"
                        className={`option-btn ${userAnswer === option ? 'selected' : ''}`}
                        onClick={() => setUserAnswer(option)}
                        whileHover={{ scale: 1.03 }}
                        whileTap={{ scale: 0.97 }}
                      >
                        {option}
                      </motion.button>
                    ))}
                  </div>
                ) : (
                  <input
                    type="text"
                    className="answer-input"
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    placeholder="请输入答案"
                    autoFocus
                  />
                )}

                <motion.button
                  type="submit"
                  className="submit-btn"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  提交答案
                </motion.button>
              </form>
            ) : (
              <div className={`feedback-section ${isCorrect ? 'correct' : 'wrong'}`}>
                <div className="feedback-icon">
                  {isCorrect ? '🎉' : '💡'}
                </div>
                <div className="feedback-text">
                  {isCorrect ? '答对了！真棒！' : '再想想看'}
                </div>
                {!isCorrect && currentExercise?.explanation && (
                  <div className="explanation">
                    <strong>解释：</strong>
                    <p>{currentExercise.explanation}</p>
                    <p>
                      <strong>正确答案：</strong>
                      {currentExercise.correct_answer}
                    </p>
                  </div>
                )}

                <motion.button
                  className="next-btn"
                  onClick={handleNext}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {currentIndex < exercises.length - 1 ? '下一题 →' : '完成 ✓'}
                </motion.button>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default ExercisePage;
