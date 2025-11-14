import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { useUser } from '../context/UserContext';
import { userAPI } from '../services/api';
import './LoginPage.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useUser();
  const [isRegister, setIsRegister] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    nickname: '',
    gradeLevel: 3,
  });

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (isRegister) {
        // 注册
        const response = await userAPI.register(
          formData.username,
          formData.nickname,
          formData.gradeLevel
        );

        if (response.data.success) {
          login(response.data.data);
          toast.success('注册成功！欢迎来到数学世界！');
          navigate('/home');
        }
      } else {
        // 登录
        const response = await userAPI.login(formData.username);

        if (response.data.success) {
          login(response.data.data);
          toast.success('登录成功！继续你的学习之旅！');
          navigate('/home');
        }
      }
    } catch (error) {
      console.error('Error:', error);
      const message = error.response?.data?.message || '操作失败，请重试';
      toast.error(message);
    }
  };

  return (
    <div className="login-page">
      <div className="login-background">
        <div className="floating-shapes">
          {[...Array(10)].map((_, i) => (
            <motion.div
              key={i}
              className="shape"
              animate={{
                y: [0, -30, 0],
                rotate: [0, 360],
              }}
              transition={{
                duration: 3 + i,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
            />
          ))}
        </div>
      </div>

      <motion.div
        className="login-container"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <motion.div
          className="login-card"
          whileHover={{ scale: 1.02 }}
          transition={{ type: 'spring', stiffness: 300 }}
        >
          <div className="login-header">
            <motion.h1
              animate={{ y: [0, -10, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              数学学习助手
            </motion.h1>
            <p className="subtitle">
              专为ADHD儿童设计的趣味数学学习
            </p>
          </div>

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label>用户名</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                placeholder="请输入用户名"
                required
              />
            </div>

            {isRegister && (
              <>
                <motion.div
                  className="form-group"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label>昵称</label>
                  <input
                    type="text"
                    value={formData.nickname}
                    onChange={(e) =>
                      setFormData({ ...formData, nickname: e.target.value })
                    }
                    placeholder="请输入昵称"
                    required={isRegister}
                  />
                </motion.div>

                <motion.div
                  className="form-group"
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                >
                  <label>年级</label>
                  <select
                    value={formData.gradeLevel}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        gradeLevel: parseInt(e.target.value),
                      })
                    }
                  >
                    <option value={2}>二年级</option>
                    <option value={3}>三年级</option>
                    <option value={4}>四年级</option>
                    <option value={5}>五年级</option>
                    <option value={6}>六年级</option>
                  </select>
                </motion.div>
              </>
            )}

            <motion.button
              type="submit"
              className="btn-submit"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isRegister ? '注册' : '登录'}
            </motion.button>

            <button
              type="button"
              className="btn-toggle"
              onClick={() => setIsRegister(!isRegister)}
            >
              {isRegister ? '已有账号？去登录' : '没有账号？去注册'}
            </button>
          </form>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default LoginPage;
