"""课程相关API路由"""
from flask import Blueprint, jsonify, request
from models.curriculum import Grade, Topic, Exercise
from app import db

curriculum_bp = Blueprint('curriculum', __name__)

@curriculum_bp.route('/grades', methods=['GET'])
def get_grades():
    """获取所有年级"""
    grades = Grade.query.order_by(Grade.level).all()
    return jsonify({
        'success': True,
        'data': [grade.to_dict() for grade in grades]
    })

@curriculum_bp.route('/grades/<int:grade_id>', methods=['GET'])
def get_grade(grade_id):
    """获取特定年级详情"""
    grade = Grade.query.get_or_404(grade_id)
    data = grade.to_dict()
    data['topics'] = [topic.to_dict() for topic in grade.topics]
    return jsonify({
        'success': True,
        'data': data
    })

@curriculum_bp.route('/topics/<int:topic_id>', methods=['GET'])
def get_topic(topic_id):
    """获取主题详情"""
    include_exercises = request.args.get('include_exercises', 'false').lower() == 'true'
    topic = Topic.query.get_or_404(topic_id)
    return jsonify({
        'success': True,
        'data': topic.to_dict(include_exercises=include_exercises)
    })

@curriculum_bp.route('/topics/<int:topic_id>/exercises', methods=['GET'])
def get_topic_exercises(topic_id):
    """获取主题的所有练习题"""
    topic = Topic.query.get_or_404(topic_id)
    difficulty = request.args.get('difficulty', type=int)

    exercises_query = Exercise.query.filter_by(topic_id=topic_id)

    if difficulty:
        exercises_query = exercises_query.filter_by(difficulty=difficulty)

    exercises = exercises_query.order_by(Exercise.order).all()

    return jsonify({
        'success': True,
        'data': [exercise.to_dict() for exercise in exercises]
    })

@curriculum_bp.route('/exercises/<int:exercise_id>', methods=['GET'])
def get_exercise(exercise_id):
    """获取单个练习题"""
    exercise = Exercise.query.get_or_404(exercise_id)
    return jsonify({
        'success': True,
        'data': exercise.to_dict()
    })

@curriculum_bp.route('/search', methods=['GET'])
def search_topics():
    """搜索主题"""
    keyword = request.args.get('q', '')
    grade_level = request.args.get('grade', type=int)

    query = Topic.query

    if keyword:
        query = query.filter(
            (Topic.name.contains(keyword)) |
            (Topic.description.contains(keyword))
        )

    if grade_level:
        grade = Grade.query.filter_by(level=grade_level).first()
        if grade:
            query = query.filter_by(grade_id=grade.id)

    topics = query.all()

    return jsonify({
        'success': True,
        'count': len(topics),
        'data': [topic.to_dict() for topic in topics]
    })
