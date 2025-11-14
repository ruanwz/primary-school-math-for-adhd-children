"""
ADHD儿童数学学习应用 - Flask后端
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

# 初始化Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'adhd-math-learning-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adhd_math.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 启用CORS
CORS(app)

# 初始化数据库
from database import db
db.init_app(app)

# 导入模型和路由
from models.user import User, UserProgress, Achievement
from models.curriculum import Grade, Topic, Exercise
from api.curriculum_routes import curriculum_bp
from api.user_routes import user_bp
from api.exercise_routes import exercise_bp

# 注册蓝图
app.register_blueprint(curriculum_bp, url_prefix='/api/curriculum')
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(exercise_bp, url_prefix='/api/exercise')

@app.route('/')
def index():
    """API根路径"""
    return jsonify({
        'name': 'ADHD儿童数学学习API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'curriculum': '/api/curriculum',
            'user': '/api/user',
            'exercise': '/api/exercise'
        }
    })

@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/init')
def manual_init():
    """手动初始化数据库（仅在数据库为空时执行）"""
    try:
        from models.curriculum import Grade
        grade_count = Grade.query.count()

        if grade_count == 0:
            from utils.init_curriculum import initialize_curriculum
            initialize_curriculum(db)
            return jsonify({
                'status': 'success',
                'message': '数据库初始化完成',
                'grades_created': Grade.query.count()
            })
        else:
            return jsonify({
                'status': 'already_initialized',
                'message': '数据库已经初始化',
                'grades_count': grade_count
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# 创建数据库表
with app.app_context():
    db.create_all()
    print("✅ 数据库表创建成功！")
    print("💡 提示: 访问 /api/init 来初始化课程数据")

if __name__ == '__main__':
    # 从环境变量获取端口，Railway等平台会动态分配端口
    port = int(os.environ.get('PORT', 5000))
    # 从环境变量判断是否为生产环境
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
