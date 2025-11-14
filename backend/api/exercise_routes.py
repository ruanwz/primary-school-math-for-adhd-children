"""练习题相关API路由"""
from flask import Blueprint, jsonify, request
from models.curriculum import Exercise
from database import db

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/check', methods=['POST'])
def check_answer():
    """检查答案是否正确"""
    data = request.json
    exercise_id = data.get('exercise_id')
    user_answer = data.get('answer', '').strip()

    exercise = Exercise.query.get_or_404(exercise_id)

    # 比较答案
    is_correct = str(user_answer).lower() == str(exercise.correct_answer).lower()

    response_data = {
        'success': True,
        'is_correct': is_correct,
        'correct_answer': exercise.correct_answer,
        'explanation': exercise.explanation if not is_correct else None,
        'points': exercise.points if is_correct else 0
    }

    return jsonify(response_data)

@exercise_bp.route('/random', methods=['GET'])
def get_random_exercises():
    """获取随机练习题"""
    topic_id = request.args.get('topic_id', type=int)
    difficulty = request.args.get('difficulty', type=int)
    count = request.args.get('count', default=5, type=int)

    query = Exercise.query

    if topic_id:
        query = query.filter_by(topic_id=topic_id)

    if difficulty:
        query = query.filter_by(difficulty=difficulty)

    # 随机获取指定数量的题目
    exercises = query.order_by(db.func.random()).limit(count).all()

    return jsonify({
        'success': True,
        'count': len(exercises),
        'data': [exercise.to_dict() for exercise in exercises]
    })
