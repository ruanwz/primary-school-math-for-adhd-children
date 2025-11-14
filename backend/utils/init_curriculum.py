"""初始化课程内容数据"""
from models.curriculum import Grade, Topic, Exercise
from models.user import Achievement
from utils.init_grade1 import init_grade_1
import json

def initialize_curriculum(db):
    """初始化中国小学数学教纲内容 (1-6年级)"""

    # ========== 一年级 ==========
    # 使用专门的一年级初始化函数（包含游戏化设计）
    print("正在初始化一年级内容...")
    init_grade_1(db, Grade, Topic, Exercise)

    # ========== 二年级 ==========
    grade_2 = Grade(
        level=2,
        name="二年级",
        description="二年级数学内容"
    )
    db.session.add(grade_2)
    db.session.flush()

    # 二年级主题
    topics_grade_2 = [
        {
            'name': '100以内的加减法',
            'description': '学习100以内数的加减运算',
            'icon': '➕',
            'color': '#FF6B6B',
            'estimated_time': 8,
            'difficulty': 1,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '计算：23 + 15 = ?',
                    'correct_answer': '38',
                    'options': json.dumps(['36', '37', '38', '39']),
                    'explanation': '23 + 15 = 38，可以先算 20 + 10 = 30，再算 3 + 5 = 8，最后 30 + 8 = 38',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'number_line', 'start': 23, 'add': 15})
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '45 - 28 = ?',
                    'correct_answer': '17',
                    'explanation': '45 - 28 = 17，可以先算 45 - 20 = 25，再算 25 - 8 = 17',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'number_blocks', 'total': 45, 'subtract': 28})
                },
                {
                    'question_type': 'multiple_choice',
                    'question_text': '56 + 37 = ?',
                    'correct_answer': '93',
                    'options': json.dumps(['91', '92', '93', '94']),
                    'explanation': '56 + 37 = 93',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },
        {
            'name': '表内乘法',
            'description': '学习九九乘法口诀',
            'icon': '✖️',
            'color': '#4ECDC4',
            'estimated_time': 10,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '3 × 4 = ?',
                    'correct_answer': '12',
                    'options': json.dumps(['10', '11', '12', '13']),
                    'explanation': '三四十二，3 × 4 = 12',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'multiplication_grid', 'rows': 3, 'cols': 4})
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '6 × 7 = ?',
                    'correct_answer': '42',
                    'explanation': '六七四十二，6 × 7 = 42',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'multiplication_array', 'factor1': 6, 'factor2': 7})
                },
                {
                    'question_type': 'multiple_choice',
                    'question_text': '8 × 9 = ?',
                    'correct_answer': '72',
                    'options': json.dumps(['70', '71', '72', '73']),
                    'explanation': '八九七十二，8 × 9 = 72',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },
        {
            'name': '认识图形',
            'description': '认识常见的平面图形',
            'icon': '🔷',
            'color': '#95E1D3',
            'estimated_time': 7,
            'difficulty': 1,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '正方形有几条边？',
                    'correct_answer': '4',
                    'options': json.dumps(['3', '4', '5', '6']),
                    'explanation': '正方形有4条边，而且4条边都相等',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'shape_highlight', 'shape': 'square'})
                },
                {
                    'question_type': 'multiple_choice',
                    'question_text': '三角形有几个角？',
                    'correct_answer': '3',
                    'options': json.dumps(['2', '3', '4', '5']),
                    'explanation': '三角形有3个角',
                    'difficulty': 1,
                    'points': 10
                }
            ]
        }
    ]

    for topic_data in topics_grade_2:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_2.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ========== 三年级 ==========
    grade_3 = Grade(
        level=3,
        name="三年级",
        description="三年级数学内容"
    )
    db.session.add(grade_3)
    db.session.flush()

    topics_grade_3 = [
        {
            'name': '万以内的加减法',
            'description': '学习更大数字的加减运算',
            'icon': '🔢',
            'color': '#FFD93D',
            'estimated_time': 10,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '256 + 374 = ?',
                    'correct_answer': '630',
                    'explanation': '256 + 374 = 630，从个位开始相加',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '812 - 345 = ?',
                    'correct_answer': '467',
                    'explanation': '812 - 345 = 467',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },
        {
            'name': '表内除法',
            'description': '学习除法运算',
            'icon': '➗',
            'color': '#6BCB77',
            'estimated_time': 10,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '12 ÷ 3 = ?',
                    'correct_answer': '4',
                    'options': json.dumps(['3', '4', '5', '6']),
                    'explanation': '12 ÷ 3 = 4，可以想：3乘以多少等于12？',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'division_groups', 'total': 12, 'groups': 3})
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '35 ÷ 7 = ?',
                    'correct_answer': '5',
                    'explanation': '35 ÷ 7 = 5',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },
        {
            'name': '多位数乘法',
            'description': '学习多位数乘一位数',
            'icon': '📊',
            'color': '#4D96FF',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '23 × 4 = ?',
                    'correct_answer': '92',
                    'explanation': '23 × 4 = 92，可以先算 20 × 4 = 80，再算 3 × 4 = 12，最后 80 + 12 = 92',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '156 × 3 = ?',
                    'correct_answer': '468',
                    'explanation': '156 × 3 = 468',
                    'difficulty': 3,
                    'points': 20
                }
            ]
        },
        {
            'name': '分数初步认识',
            'description': '认识简单的分数',
            'icon': '🍕',
            'color': '#FF6B9D',
            'estimated_time': 8,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '把一个苹果平均分成2份，每份是几分之几？',
                    'correct_answer': '1/2',
                    'options': json.dumps(['1/2', '1/3', '1/4', '2/1']),
                    'explanation': '平均分成2份，每份是二分之一，写作 1/2',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'fraction_circle', 'parts': 2, 'shaded': 1})
                }
            ]
        }
    ]

    for topic_data in topics_grade_3:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_3.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ========== 四年级 ==========
    grade_4 = Grade(
        level=4,
        name="四年级",
        description="四年级数学内容"
    )
    db.session.add(grade_4)
    db.session.flush()

    topics_grade_4 = [
        {
            'name': '大数的认识',
            'description': '认识亿以内的数',
            'icon': '🔟',
            'color': '#C4E538',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '1000000是多少？',
                    'correct_answer': '一百万',
                    'options': json.dumps(['十万', '一百万', '一千万', '一亿']),
                    'explanation': '1000000 是一百万',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },
        {
            'name': '四则运算',
            'description': '学习混合运算',
            'icon': '🧮',
            'color': '#FF6B6B',
            'estimated_time': 12,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '12 + 8 × 2 = ?',
                    'correct_answer': '28',
                    'explanation': '先算乘法：8 × 2 = 16，再算加法：12 + 16 = 28',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '(15 - 3) × 4 = ?',
                    'correct_answer': '48',
                    'explanation': '先算括号内：15 - 3 = 12，再算乘法：12 × 4 = 48',
                    'difficulty': 3,
                    'points': 20
                }
            ]
        },
        {
            'name': '小数的认识',
            'description': '学习小数的概念和运算',
            'icon': '•',
            'color': '#4ECDC4',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '0.5 + 0.3 = ?',
                    'correct_answer': '0.8',
                    'explanation': '0.5 + 0.3 = 0.8',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'multiple_choice',
                    'question_text': '1.2 - 0.7 = ?',
                    'correct_answer': '0.5',
                    'options': json.dumps(['0.4', '0.5', '0.6', '0.7']),
                    'explanation': '1.2 - 0.7 = 0.5',
                    'difficulty': 3,
                    'points': 20
                }
            ]
        },
        {
            'name': '图形的面积',
            'description': '学习计算长方形和正方形的面积',
            'icon': '📐',
            'color': '#95E1D3',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '一个长方形长5厘米，宽3厘米，面积是多少平方厘米？',
                    'correct_answer': '15',
                    'explanation': '长方形面积 = 长 × 宽 = 5 × 3 = 15平方厘米',
                    'difficulty': 3,
                    'points': 20,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'rectangle_area', 'length': 5, 'width': 3})
                }
            ]
        }
    ]

    for topic_data in topics_grade_4:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_4.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ========== 五年级 ==========
    grade_5 = Grade(
        level=5,
        name="五年级",
        description="五年级数学内容"
    )
    db.session.add(grade_5)
    db.session.flush()

    topics_grade_5 = [
        {
            'name': '小数乘除法',
            'description': '学习小数的乘除运算',
            'icon': '💯',
            'color': '#FFD93D',
            'estimated_time': 12,
            'difficulty': 4,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '2.5 × 4 = ?',
                    'correct_answer': '10',
                    'explanation': '2.5 × 4 = 10',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '7.2 ÷ 3 = ?',
                    'correct_answer': '2.4',
                    'explanation': '7.2 ÷ 3 = 2.4',
                    'difficulty': 4,
                    'points': 25
                }
            ]
        },
        {
            'name': '分数加减法',
            'description': '学习分数的加减运算',
            'icon': '➕➖',
            'color': '#6BCB77',
            'estimated_time': 12,
            'difficulty': 4,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '1/4 + 1/4 = ?',
                    'correct_answer': '1/2',
                    'explanation': '1/4 + 1/4 = 2/4 = 1/2',
                    'difficulty': 3,
                    'points': 20,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'fraction_addition', 'fraction1': '1/4', 'fraction2': '1/4'})
                }
            ]
        },
        {
            'name': '长方体和正方体',
            'description': '认识立体图形，学习体积计算',
            'icon': '📦',
            'color': '#4D96FF',
            'estimated_time': 10,
            'difficulty': 4,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '一个正方体棱长是2厘米，体积是多少立方厘米？',
                    'correct_answer': '8',
                    'explanation': '正方体体积 = 棱长³ = 2 × 2 × 2 = 8立方厘米',
                    'difficulty': 4,
                    'points': 25
                }
            ]
        }
    ]

    for topic_data in topics_grade_5:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_5.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ========== 六年级 ==========
    grade_6 = Grade(
        level=6,
        name="六年级",
        description="六年级数学内容"
    )
    db.session.add(grade_6)
    db.session.flush()

    topics_grade_6 = [
        {
            'name': '分数乘除法',
            'description': '学习分数的乘除运算',
            'icon': '✖️➗',
            'color': '#FF6B9D',
            'estimated_time': 12,
            'difficulty': 4,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '2/3 × 3/4 = ?',
                    'correct_answer': '1/2',
                    'explanation': '2/3 × 3/4 = 6/12 = 1/2',
                    'difficulty': 4,
                    'points': 25
                }
            ]
        },
        {
            'name': '比和比例',
            'description': '学习比例的概念和应用',
            'icon': '⚖️',
            'color': '#C4E538',
            'estimated_time': 12,
            'difficulty': 4,
            'exercises': [
                {
                    'question_type': 'multiple_choice',
                    'question_text': '2:3 = 4:?',
                    'correct_answer': '6',
                    'options': json.dumps(['5', '6', '7', '8']),
                    'explanation': '2:3 = 4:6，因为 2 × 2 = 4，所以 3 × 2 = 6',
                    'difficulty': 4,
                    'points': 25
                }
            ]
        },
        {
            'name': '圆的认识',
            'description': '学习圆的周长和面积',
            'icon': '⭕',
            'color': '#4ECDC4',
            'estimated_time': 12,
            'difficulty': 5,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '圆的半径是5厘米，周长约是多少厘米？(π取3.14)',
                    'correct_answer': '31.4',
                    'explanation': '圆的周长 = 2πr = 2 × 3.14 × 5 = 31.4厘米',
                    'difficulty': 5,
                    'points': 30,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'circle_circumference', 'radius': 5})
                }
            ]
        }
    ]

    for topic_data in topics_grade_6:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_6.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ========== 初始化成就系统 ==========
    achievements = [
        {
            'name': '初来乍到',
            'description': '完成第一个练习',
            'icon': '🎉',
            'category': 'learning',
            'requirement_type': 'exercises_completed',
            'requirement_value': 1,
            'points_reward': 50
        },
        {
            'name': '小小数学家',
            'description': '获得10颗星星',
            'icon': '⭐',
            'category': 'mastery',
            'requirement_type': 'total_stars',
            'requirement_value': 10,
            'points_reward': 100
        },
        {
            'name': '坚持不懈',
            'description': '连续学习3天',
            'icon': '🔥',
            'category': 'streak',
            'requirement_type': 'consecutive_days',
            'requirement_value': 3,
            'points_reward': 150
        },
        {
            'name': '完美答卷',
            'description': '一个主题全部答对',
            'icon': '💯',
            'category': 'mastery',
            'requirement_type': 'perfect_topic',
            'requirement_value': 1,
            'points_reward': 200
        },
        {
            'name': '数学大师',
            'description': '获得50颗星星',
            'icon': '👑',
            'category': 'mastery',
            'requirement_type': 'total_stars',
            'requirement_value': 50,
            'points_reward': 500
        }
    ]

    for ach_data in achievements:
        achievement = Achievement(**ach_data)
        db.session.add(achievement)

    db.session.commit()
    print("✅ 课程内容初始化完成！")
