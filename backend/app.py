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

# 启用CORS - 允许Netlify前端访问
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # 本地开发
            "https://adhd-math-learning-app.netlify.app",  # Netlify生产环境
            "https://*.netlify.app"  # 所有Netlify预览部署
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": False
    }
})

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
    from models.curriculum import Grade
    try:
        grade_count = Grade.query.count()
    except:
        grade_count = 'error'

    return jsonify({
        'name': 'ADHD儿童数学学习API',
        'version': '1.0.1',
        'deployment': 'auto-init-v2',
        'status': 'running',
        'port': os.environ.get('PORT', 'unknown'),
        'db_initialized': _db_initialized,
        'grades_count': grade_count,
        'endpoints': {
            'curriculum': '/api/curriculum',
            'user': '/api/user',
            'exercise': '/api/exercise',
            'health': '/api/health',
            'init': '/api/init'
        }
    })

@app.route('/ping')
def ping():
    """最简单的ping端点"""
    return 'pong', 200

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

# 数据库初始化将在第一个请求时执行，而不是在启动时
# 这避免了worker之间的竞争条件
_db_initialized = False

def init_db():
    """初始化数据库（懒加载）"""
    global _db_initialized
    if not _db_initialized:
        with app.app_context():
            try:
                db.create_all()
                print("✅ 数据库表创建成功！", flush=True)

                # 检查是否需要初始化课程数据
                grade_count = Grade.query.count()
                if grade_count == 0:
                    print("🔄 数据库为空，正在自动初始化课程数据...", flush=True)
                    from utils.init_curriculum import initialize_curriculum
                    initialize_curriculum(db)
                    print("✅ 课程数据自动初始化完成！", flush=True)
                else:
                    print(f"💡 数据库已有 {grade_count} 个年级数据", flush=True)

                _db_initialized = True
            except Exception as e:
                print(f"⚠️ 数据库初始化警告: {e}", flush=True)

# 在第一个请求时初始化数据库
@app.before_request
def before_first_request():
    """在第一个请求前初始化数据库"""
    init_db()

if __name__ == '__main__':
    # 从环境变量获取端口，Railway等平台会动态分配端口
    port = int(os.environ.get('PORT', 5000))
    # 从环境变量判断是否为生产环境
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
