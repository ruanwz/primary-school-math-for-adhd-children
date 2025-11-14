"""课程内容数据模型"""
from datetime import datetime
from database import db
import json

class Grade(db.Model):
    """年级模型"""
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False, unique=True)  # 2-6年级
    name = db.Column(db.String(50), nullable=False)  # 如"二年级"
    description = db.Column(db.Text)

    # 关联关系
    topics = db.relationship('Topic', backref='grade', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'name': self.name,
            'description': self.description,
            'topics_count': len(self.topics) if self.topics else 0
        }


class Topic(db.Model):
    """主题/章节模型"""
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('grades.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)  # 顺序
    icon = db.Column(db.String(100))  # 图标
    color = db.Column(db.String(20))  # 主题颜色

    # ADHD友好设计参数
    estimated_time = db.Column(db.Integer, default=10)  # 预计学习时间(分钟)
    difficulty = db.Column(db.Integer, default=1)  # 难度等级(1-5)

    # 关联关系
    exercises = db.relationship('Exercise', backref='topic', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_exercises=False):
        data = {
            'id': self.id,
            'grade_id': self.grade_id,
            'name': self.name,
            'description': self.description,
            'order': self.order,
            'icon': self.icon,
            'color': self.color,
            'estimated_time': self.estimated_time,
            'difficulty': self.difficulty,
            'exercises_count': len(self.exercises) if self.exercises else 0
        }

        if include_exercises and self.exercises:
            data['exercises'] = [ex.to_dict() for ex in self.exercises]

        return data


class Exercise(db.Model):
    """练习题模型"""
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=False)

    # 题目内容
    question_type = db.Column(db.String(50), nullable=False)
    # 'multiple_choice', 'fill_blank', 'drag_drop', 'interactive'

    question_text = db.Column(db.Text, nullable=False)
    question_data = db.Column(db.Text)  # JSON格式的额外数据

    # 答案和选项
    correct_answer = db.Column(db.String(200), nullable=False)
    options = db.Column(db.Text)  # JSON格式的选项
    explanation = db.Column(db.Text)  # 解释

    # 可视化和互动
    animation_type = db.Column(db.String(50))  # 'manim', 'p5js', 'interactive'
    animation_data = db.Column(db.Text)  # JSON格式的动画配置

    # 难度和元数据
    difficulty = db.Column(db.Integer, default=1)  # 1-5
    points = db.Column(db.Integer, default=10)  # 分数
    order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'topic_id': self.topic_id,
            'question_type': self.question_type,
            'question_text': self.question_text,
            'question_data': json.loads(self.question_data) if self.question_data else None,
            'correct_answer': self.correct_answer,
            'options': json.loads(self.options) if self.options else None,
            'explanation': self.explanation,
            'animation_type': self.animation_type,
            'animation_data': json.loads(self.animation_data) if self.animation_data else None,
            'difficulty': self.difficulty,
            'points': self.points,
            'order': self.order
        }
