"""用户相关数据模型"""
from datetime import datetime
from database import db

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.String(200), default='default_avatar.png')
    grade_level = db.Column(db.Integer, default=3)  # 当前年级
    current_difficulty = db.Column(db.Integer, default=2)  # 当前难度等级(1-5)
    total_stars = db.Column(db.Integer, default=0)  # 总星星数
    total_points = db.Column(db.Integer, default=0)  # 总积分
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now)

    # 关联关系
    progress = db.relationship('UserProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'grade_level': self.grade_level,
            'current_difficulty': self.current_difficulty,
            'total_stars': self.total_stars,
            'total_points': self.total_points,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class UserProgress(db.Model):
    """用户学习进度"""
    __tablename__ = 'user_progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    # 进度数据
    completed = db.Column(db.Boolean, default=False)
    stars_earned = db.Column(db.Integer, default=0)  # 本主题获得的星星(0-3)
    exercises_completed = db.Column(db.Integer, default=0)  # 完成的练习数
    correct_count = db.Column(db.Integer, default=0)  # 正确数
    wrong_count = db.Column(db.Integer, default=0)  # 错误数
    time_spent = db.Column(db.Integer, default=0)  # 花费时间(秒)

    last_practiced = db.Column(db.DateTime, default=datetime.now)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """转换为字典"""
        accuracy = 0
        if self.correct_count + self.wrong_count > 0:
            accuracy = round(self.correct_count / (self.correct_count + self.wrong_count) * 100, 1)

        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'completed': self.completed,
            'stars_earned': self.stars_earned,
            'exercises_completed': self.exercises_completed,
            'correct_count': self.correct_count,
            'wrong_count': self.wrong_count,
            'accuracy': accuracy,
            'time_spent': self.time_spent,
            'last_practiced': self.last_practiced.isoformat() if self.last_practiced else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class Achievement(db.Model):
    """成就定义"""
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    icon = db.Column(db.String(100))
    category = db.Column(db.String(50))  # 'learning', 'streak', 'mastery', 'special'
    requirement_type = db.Column(db.String(50))  # 'total_stars', 'consecutive_days', 'topic_complete', etc.
    requirement_value = db.Column(db.Integer)
    points_reward = db.Column(db.Integer, default=100)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'category': self.category,
            'requirement_type': self.requirement_type,
            'requirement_value': self.requirement_value,
            'points_reward': self.points_reward
        }


class UserAchievement(db.Model):
    """用户获得的成就"""
    __tablename__ = 'user_achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.now)

    # 关联关系
    achievement = db.relationship('Achievement', backref='user_achievements')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'achievement_id': self.achievement_id,
            'achievement': self.achievement.to_dict() if self.achievement else None,
            'earned_at': self.earned_at.isoformat() if self.earned_at else None
        }


class TopicMastery(db.Model):
    """知识点掌握度评估"""
    __tablename__ = 'topic_mastery'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    # 掌握度等级：1=需加强, 2=基本掌握, 3=完全掌握
    mastery_level = db.Column(db.Integer, default=0)  # 0=未评估

    # 评估数据
    total_attempts = db.Column(db.Integer, default=0)  # 总尝试次数
    successful_attempts = db.Column(db.Integer, default=0)  # 成功次数
    average_time = db.Column(db.Float, default=0.0)  # 平均答题时间(秒)
    hints_used = db.Column(db.Integer, default=0)  # 使用提示次数

    # 最近表现（最近5次）
    recent_accuracy = db.Column(db.Float, default=0.0)  # 最近正确率

    # 自适应难度
    current_difficulty = db.Column(db.Integer, default=1)  # 当前难度 1-3

    # 时间记录
    first_assessed = db.Column(db.DateTime, default=datetime.now)
    last_assessed = db.Column(db.DateTime, default=datetime.now)
    next_review_date = db.Column(db.DateTime)  # 建议复习日期

    def to_dict(self):
        accuracy = 0
        if self.total_attempts > 0:
            accuracy = round((self.successful_attempts / self.total_attempts) * 100, 1)

        # 掌握度文字描述
        mastery_text = ['未评估', '需要加强', '基本掌握', '完全掌握'][self.mastery_level]

        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'mastery_level': self.mastery_level,
            'mastery_text': mastery_text,
            'total_attempts': self.total_attempts,
            'successful_attempts': self.successful_attempts,
            'accuracy': accuracy,
            'recent_accuracy': self.recent_accuracy,
            'average_time': self.average_time,
            'hints_used': self.hints_used,
            'current_difficulty': self.current_difficulty,
            'first_assessed': self.first_assessed.isoformat() if self.first_assessed else None,
            'last_assessed': self.last_assessed.isoformat() if self.last_assessed else None,
            'next_review_date': self.next_review_date.isoformat() if self.next_review_date else None
        }


class GameAttempt(db.Model):
    """游戏尝试记录"""
    __tablename__ = 'game_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # 游戏类型
    game_type = db.Column(db.String(50))  # 'drag_drop', 'click', 'match', etc.

    # 答题数据
    is_correct = db.Column(db.Boolean, nullable=False)
    time_spent = db.Column(db.Integer)  # 秒
    attempt_count = db.Column(db.Integer, default=1)  # 尝试次数
    hints_used = db.Column(db.Integer, default=0)  # 使用提示次数

    # 详细记录（JSON格式）
    attempt_data = db.Column(db.Text)  # 存储详细操作数据

    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'topic_id': self.topic_id,
            'exercise_id': self.exercise_id,
            'game_type': self.game_type,
            'is_correct': self.is_correct,
            'time_spent': self.time_spent,
            'attempt_count': self.attempt_count,
            'hints_used': self.hints_used,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
