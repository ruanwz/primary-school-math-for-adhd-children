"""用户相关API路由"""
from flask import Blueprint, jsonify, request
from models.user import User, UserProgress, Achievement, UserAchievement
from models.curriculum import Topic
from app import db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """注册新用户"""
    data = request.json
    username = data.get('username')
    nickname = data.get('nickname')
    grade_level = data.get('grade_level', 3)

    if not username or not nickname:
        return jsonify({
            'success': False,
            'message': '用户名和昵称不能为空'
        }), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({
            'success': False,
            'message': '用户名已存在'
        }), 400

    # 创建新用户
    user = User(
        username=username,
        nickname=nickname,
        grade_level=grade_level
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '注册成功',
        'data': user.to_dict()
    }), 201

@user_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.json
    username = data.get('username')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        }), 404

    # 更新最后登录时间
    user.last_login = datetime.now()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '登录成功',
        'data': user.to_dict()
    })

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取用户信息"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'success': True,
        'data': user.to_dict()
    })

@user_bp.route('/<int:user_id>/progress', methods=['GET'])
def get_user_progress(user_id):
    """获取用户学习进度"""
    user = User.query.get_or_404(user_id)
    progress_list = UserProgress.query.filter_by(user_id=user_id).all()

    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict(),
            'progress': [p.to_dict() for p in progress_list]
        }
    })

@user_bp.route('/<int:user_id>/progress/<int:topic_id>', methods=['GET'])
def get_topic_progress(user_id, topic_id):
    """获取特定主题的学习进度"""
    user = User.query.get_or_404(user_id)
    topic = Topic.query.get_or_404(topic_id)

    progress = UserProgress.query.filter_by(
        user_id=user_id,
        topic_id=topic_id
    ).first()

    if not progress:
        # 如果没有进度记录，创建一个新的
        progress = UserProgress(user_id=user_id, topic_id=topic_id)
        db.session.add(progress)
        db.session.commit()

    return jsonify({
        'success': True,
        'data': progress.to_dict()
    })

@user_bp.route('/<int:user_id>/progress/<int:topic_id>', methods=['PUT'])
def update_progress(user_id, topic_id):
    """更新学习进度"""
    user = User.query.get_or_404(user_id)
    topic = Topic.query.get_or_404(topic_id)
    data = request.json

    progress = UserProgress.query.filter_by(
        user_id=user_id,
        topic_id=topic_id
    ).first()

    if not progress:
        progress = UserProgress(user_id=user_id, topic_id=topic_id)
        db.session.add(progress)

    # 更新进度数据
    if 'exercises_completed' in data:
        progress.exercises_completed = data['exercises_completed']
    if 'correct_count' in data:
        progress.correct_count = data['correct_count']
    if 'wrong_count' in data:
        progress.wrong_count = data['wrong_count']
    if 'time_spent' in data:
        progress.time_spent += data['time_spent']

    progress.last_practiced = datetime.now()

    # 计算星星
    total_attempts = progress.correct_count + progress.wrong_count
    if total_attempts > 0:
        accuracy = progress.correct_count / total_attempts
        if accuracy >= 0.95:
            progress.stars_earned = 3
        elif accuracy >= 0.80:
            progress.stars_earned = 2
        elif accuracy >= 0.60:
            progress.stars_earned = 1
        else:
            progress.stars_earned = 0

    # 检查是否完成
    if data.get('completed', False):
        progress.completed = True
        progress.completed_at = datetime.now()

        # 更新用户总星星数
        user.total_stars += progress.stars_earned
        user.total_points += progress.stars_earned * 100

    db.session.commit()

    return jsonify({
        'success': True,
        'message': '进度更新成功',
        'data': progress.to_dict()
    })

@user_bp.route('/<int:user_id>/achievements', methods=['GET'])
def get_user_achievements(user_id):
    """获取用户的成就"""
    user = User.query.get_or_404(user_id)
    user_achievements = UserAchievement.query.filter_by(user_id=user_id).all()

    return jsonify({
        'success': True,
        'data': [ua.to_dict() for ua in user_achievements]
    })

@user_bp.route('/<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """获取用户统计数据"""
    user = User.query.get_or_404(user_id)
    progress_list = UserProgress.query.filter_by(user_id=user_id).all()

    total_exercises = sum(p.exercises_completed for p in progress_list)
    total_correct = sum(p.correct_count for p in progress_list)
    total_wrong = sum(p.wrong_count for p in progress_list)
    total_time = sum(p.time_spent for p in progress_list)
    completed_topics = sum(1 for p in progress_list if p.completed)

    accuracy = 0
    if total_correct + total_wrong > 0:
        accuracy = round(total_correct / (total_correct + total_wrong) * 100, 1)

    return jsonify({
        'success': True,
        'data': {
            'user': user.to_dict(),
            'stats': {
                'total_exercises': total_exercises,
                'total_correct': total_correct,
                'total_wrong': total_wrong,
                'total_time_minutes': round(total_time / 60, 1),
                'completed_topics': completed_topics,
                'accuracy': accuracy,
                'total_stars': user.total_stars,
                'total_points': user.total_points
            }
        }
    })
