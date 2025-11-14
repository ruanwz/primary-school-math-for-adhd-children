"""初始化一年级课程内容 - 游戏化设计"""
import json

def init_grade_1(db, Grade, Topic, Exercise):
    """初始化一年级数学内容（上下册）"""

    # ========== 一年级 ==========
    grade_1 = Grade(
        level=1,
        name="一年级",
        description="一年级数学内容 - 数学启蒙"
    )
    db.session.add(grade_1)
    db.session.flush()

    # ==================== 一年级上册 ====================

    topics_grade_1_first = [
        # 1. 准备课：数一数、比多少
        {
            'name': '数一数、比多少',
            'description': '学习数数和比较多少',
            'icon': '🔢',
            'color': '#FF6B9D',
            'estimated_time': 5,
            'difficulty': 1,
            'exercises': [
                # 游戏1：喂小动物
                {
                    'question_type': 'drag_drop',
                    'question_text': '小兔子想吃3个萝卜，请拖动3个萝卜给它！',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'feed_animals',
                        'animal': '🐰',
                        'food': '🥕',
                        'target_count': 3,
                        'available_count': 10
                    }),
                    'explanation': '数一数：1、2、3，一共3个萝卜',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'drag_drop'
                },
                {
                    'question_type': 'drag_drop',
                    'question_text': '小猫想吃5条鱼，请拖动5条鱼给它！',
                    'correct_answer': '5',
                    'question_data': json.dumps({
                        'game_type': 'feed_animals',
                        'animal': '🐱',
                        'food': '🐟',
                        'target_count': 5,
                        'available_count': 10
                    }),
                    'difficulty': 1,
                    'points': 10
                },
                # 游戏2：比一比谁多
                {
                    'question_type': 'click',
                    'question_text': '哪边的苹果更多？点击更多的那边',
                    'correct_answer': 'right',
                    'question_data': json.dumps({
                        'game_type': 'compare',
                        'left_count': 3,
                        'right_count': 5,
                        'object': '🍎'
                    }),
                    'explanation': '左边3个，右边5个，5比3多，所以右边多',
                    'difficulty': 1,
                    'points': 10
                },
                {
                    'question_type': 'click',
                    'question_text': '哪边的星星更多？点击更多的那边',
                    'correct_answer': 'left',
                    'question_data': json.dumps({
                        'game_type': 'compare',
                        'left_count': 7,
                        'right_count': 4,
                        'object': '⭐'
                    }),
                    'difficulty': 1,
                    'points': 10
                }
            ]
        },

        # 2. 位置：上、下、前、后、左、右
        {
            'name': '位置',
            'description': '认识上下前后左右',
            'icon': '🧭',
            'color': '#4ECDC4',
            'estimated_time': 5,
            'difficulty': 1,
            'exercises': [
                # 游戏：小猫找玩具
                {
                    'question_type': 'click',
                    'question_text': '玩具在箱子的上面，请点击玩具！',
                    'correct_answer': 'top',
                    'question_data': json.dumps({
                        'game_type': 'find_position',
                        'positions': ['top', 'bottom', 'left', 'right'],
                        'correct_position': 'top'
                    }),
                    'explanation': '"上面"就是箱子的顶部',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'click'
                },
                {
                    'question_type': 'click',
                    'question_text': '小球在桌子的下面，请点击小球！',
                    'correct_answer': 'bottom',
                    'question_data': json.dumps({
                        'game_type': 'find_position',
                        'correct_position': 'bottom'
                    }),
                    'difficulty': 1,
                    'points': 10
                },
                {
                    'question_type': 'click',
                    'question_text': '谁在小明的前面？',
                    'correct_answer': 'person_1',
                    'question_data': json.dumps({
                        'game_type': 'queue_position',
                        'people': ['小红', '小明', '小刚'],
                        'target': '小明',
                        'direction': 'front'
                    }),
                    'explanation': '前面就是靠前的位置，小红在小明前面',
                    'difficulty': 1,
                    'points': 10
                }
            ]
        },

        # 3. 1-5的认识和加减法
        {
            'name': '1-5的认识和加减法',
            'description': '认识数字1到5，学习简单加减法',
            'icon': '1️⃣',
            'color': '#FFD93D',
            'estimated_time': 8,
            'difficulty': 1,
            'exercises': [
                # 游戏1：数字钓鱼
                {
                    'question_type': 'drag_drop',
                    'question_text': '看到数字3，请钓起3条鱼！',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'fishing',
                        'number': 3,
                        'total_fish': 8
                    }),
                    'explanation': '数字3表示3个东西',
                    'difficulty': 1,
                    'points': 10
                },
                # 游戏2：水果拼盘（加法）
                {
                    'question_type': 'fill_blank',
                    'question_text': '2个草莓加1个草莓，一共几个？',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'fruit_plate',
                        'fruit': '🍓',
                        'addend1': 2,
                        'addend2': 1
                    }),
                    'explanation': '2 + 1 = 3，一共3个草莓',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'combine_objects', 'objects': '🍓'})
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '3个橙子加2个橙子，一共几个？',
                    'correct_answer': '5',
                    'question_data': json.dumps({
                        'game_type': 'fruit_plate',
                        'fruit': '🍊',
                        'addend1': 3,
                        'addend2': 2
                    }),
                    'explanation': '3 + 2 = 5',
                    'difficulty': 1,
                    'points': 10
                },
                # 游戏3：分糖果（减法）
                {
                    'question_type': 'fill_blank',
                    'question_text': '有5个糖果，吃掉2个，还剩几个？',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'candy_subtract',
                        'total': 5,
                        'eaten': 2
                    }),
                    'explanation': '5 - 2 = 3，还剩3个糖果',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'remove_objects', 'object': '🍬'})
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '4个气球，飞走了1个，还剩几个？',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'candy_subtract',
                        'object': '🎈',
                        'total': 4,
                        'removed': 1
                    }),
                    'difficulty': 1,
                    'points': 10
                }
            ]
        },

        # 4. 认识图形（一）
        {
            'name': '认识图形',
            'description': '认识长方体、正方体、圆柱、球',
            'icon': '🔷',
            'color': '#95E1D3',
            'estimated_time': 6,
            'difficulty': 1,
            'exercises': [
                # 游戏1：形状配对
                {
                    'question_type': 'drag_drop',
                    'question_text': '把魔方放到正方体的洞里',
                    'correct_answer': 'cube',
                    'question_data': json.dumps({
                        'game_type': 'shape_match',
                        'object': '魔方',
                        'shape': 'cube',
                        'options': ['cube', 'sphere', 'cylinder', 'cuboid']
                    }),
                    'explanation': '魔方是正方体形状',
                    'difficulty': 1,
                    'points': 10,
                    'animation_type': 'drag_drop'
                },
                {
                    'question_type': 'drag_drop',
                    'question_text': '把篮球放到球形的洞里',
                    'correct_answer': 'sphere',
                    'question_data': json.dumps({
                        'game_type': 'shape_match',
                        'object': '篮球',
                        'shape': 'sphere'
                    }),
                    'difficulty': 1,
                    'points': 10
                },
                # 游戏2：找形状
                {
                    'question_type': 'click',
                    'question_text': '找出房间里所有球形的东西',
                    'correct_answer': json.dumps(['basketball', 'orange', 'globe']),
                    'question_data': json.dumps({
                        'game_type': 'find_shapes',
                        'target_shape': 'sphere',
                        'items': [
                            {'id': 'basketball', 'name': '篮球', 'shape': 'sphere'},
                            {'id': 'box', 'name': '盒子', 'shape': 'cuboid'},
                            {'id': 'orange', 'name': '橙子', 'shape': 'sphere'},
                            {'id': 'can', 'name': '易拉罐', 'shape': 'cylinder'},
                            {'id': 'globe', 'name': '地球仪', 'shape': 'sphere'}
                        ]
                    }),
                    'explanation': '篮球、橙子、地球仪都是球形的',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 5. 6-10的认识和加减法
        {
            'name': '6-10的认识和加减法',
            'description': '认识6到10，学习加减运算',
            'icon': '6️⃣',
            'color': '#6BCB77',
            'estimated_time': 8,
            'difficulty': 2,
            'exercises': [
                # 游戏1：停车场
                {
                    'question_type': 'fill_blank',
                    'question_text': '停车场有10个车位，已经停了7辆车，还能停几辆？',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'parking',
                        'total_spaces': 10,
                        'parked': 7
                    }),
                    'explanation': '10 - 7 = 3，还能停3辆车',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'parking_lot'})
                },
                # 游戏2：凑十游戏
                {
                    'question_type': 'click',
                    'question_text': '7和几凑成10？',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'make_ten',
                        'first_number': 7,
                        'options': [1, 2, 3, 4, 5]
                    }),
                    'explanation': '7 + 3 = 10',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '6 + 3 = ?',
                    'correct_answer': '9',
                    'explanation': '6 + 3 = 9',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '10 - 4 = ?',
                    'correct_answer': '6',
                    'explanation': '10 - 4 = 6',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 6. 11-20各数的认识
        {
            'name': '11-20各数的认识',
            'description': '认识11到20的数',
            'icon': '🔟',
            'color': '#4D96FF',
            'estimated_time': 6,
            'difficulty': 2,
            'exercises': [
                # 游戏1：数星星
                {
                    'question_type': 'fill_blank',
                    'question_text': '数一数有多少颗星星？（提示：10个一组数）',
                    'correct_answer': '15',
                    'question_data': json.dumps({
                        'game_type': 'count_stars',
                        'total': 15,
                        'group_by': 10
                    }),
                    'explanation': '一组10个，加上5个，一共15个',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'group_counting'})
                },
                # 游戏2：数的顺序
                {
                    'question_type': 'sort',
                    'question_text': '把这些数字从小到大排列：15、11、20、17',
                    'correct_answer': json.dumps([11, 15, 17, 20]),
                    'question_data': json.dumps({
                        'game_type': 'number_sort',
                        'numbers': [15, 11, 20, 17]
                    }),
                    'explanation': '11最小，然后是15、17，最后是20',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '18里面有几个十和几个一？',
                    'correct_answer': '1个十,8个一',
                    'question_data': json.dumps({
                        'game_type': 'place_value',
                        'number': 18
                    }),
                    'explanation': '18 = 1个十 + 8个一',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 7. 认识钟表
        {
            'name': '认识钟表',
            'description': '学习看整点时间',
            'icon': '🕐',
            'color': '#FF6B6B',
            'estimated_time': 7,
            'difficulty': 2,
            'exercises': [
                # 游戏1：一天的时间
                {
                    'question_type': 'match',
                    'question_text': '什么时间做什么事？把时间和活动连起来',
                    'correct_answer': json.dumps({
                        '7:00': '起床',
                        '12:00': '吃午饭',
                        '20:00': '睡觉'
                    }),
                    'question_data': json.dumps({
                        'game_type': 'match_time_activity',
                        'pairs': [
                            {'time': '7:00', 'activity': '起床'},
                            {'time': '12:00', 'activity': '吃午饭'},
                            {'time': '20:00', 'activity': '睡觉'}
                        ]
                    }),
                    'explanation': '早上7点起床，中午12点吃饭，晚上8点睡觉',
                    'difficulty': 2,
                    'points': 15
                },
                # 游戏2：拨时钟
                {
                    'question_type': 'interactive',
                    'question_text': '现在是3点，请把时针拨到3',
                    'correct_answer': '3',
                    'question_data': json.dumps({
                        'game_type': 'set_clock',
                        'target_hour': 3
                    }),
                    'explanation': '时针（短针）指向3，分针（长针）指向12，就是3点整',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'clock_interactive'})
                },
                {
                    'question_type': 'click',
                    'question_text': '哪个钟表显示的是8点？',
                    'correct_answer': 'clock_b',
                    'question_data': json.dumps({
                        'game_type': 'identify_time',
                        'options': [
                            {'id': 'clock_a', 'hour': 6},
                            {'id': 'clock_b', 'hour': 8},
                            {'id': 'clock_c', 'hour': 10}
                        ]
                    }),
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 8. 20以内的进位加法
        {
            'name': '20以内的进位加法',
            'description': '学习9+几、8+几等进位加法',
            'icon': '➕',
            'color': '#C4E538',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                # 游戏1：购物游戏
                {
                    'question_type': 'fill_blank',
                    'question_text': '笔9元，本子5元，一共多少钱？',
                    'correct_answer': '14',
                    'question_data': json.dumps({
                        'game_type': 'shopping',
                        'items': [
                            {'name': '笔', 'price': 9},
                            {'name': '本子', 'price': 5}
                        ]
                    }),
                    'explanation': '9 + 5 = 14元，可以想：9 + 1 = 10，10 + 4 = 14',
                    'difficulty': 3,
                    'points': 20,
                    'animation_type': 'interactive',
                    'animation_data': json.dumps({'type': 'shopping_cart'})
                },
                # 游戏2：跳格子
                {
                    'question_type': 'fill_blank',
                    'question_text': '青蛙先跳8格，再跳7格，一共跳了多少格？',
                    'correct_answer': '15',
                    'question_data': json.dumps({
                        'game_type': 'hop_frog',
                        'jump1': 8,
                        'jump2': 7
                    }),
                    'explanation': '8 + 7 = 15',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '9 + 6 = ?',
                    'correct_answer': '15',
                    'explanation': '9 + 6 = 15，先凑十：9 + 1 = 10，10 + 5 = 15',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '8 + 5 = ?',
                    'correct_answer': '13',
                    'explanation': '8 + 5 = 13',
                    'difficulty': 3,
                    'points': 20
                }
            ]
        }
    ]

    # 添加一年级上册主题
    for topic_data in topics_grade_1_first:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_1.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    # ==================== 一年级下册 ====================

    topics_grade_1_second = [
        # 1. 认识图形（二）：平面图形
        {
            'name': '认识平面图形',
            'description': '认识三角形、正方形、长方形、圆',
            'icon': '△',
            'color': '#FF6B9D',
            'estimated_time': 6,
            'difficulty': 1,
            'exercises': [
                {
                    'question_type': 'drag_drop',
                    'question_text': '把三角形的积木放到三角形的框里',
                    'correct_answer': 'triangle',
                    'question_data': json.dumps({
                        'game_type': 'shape_sort',
                        'shapes': ['triangle', 'square', 'rectangle', 'circle']
                    }),
                    'explanation': '三角形有3个角、3条边',
                    'difficulty': 1,
                    'points': 10
                },
                {
                    'question_type': 'click',
                    'question_text': '找出所有的圆形',
                    'correct_answer': json.dumps(['coin', 'plate', 'wheel']),
                    'question_data': json.dumps({
                        'game_type': 'find_shapes',
                        'target_shape': 'circle'
                    }),
                    'difficulty': 1,
                    'points': 10
                }
            ]
        },

        # 2. 20以内的退位减法
        {
            'name': '20以内的退位减法',
            'description': '学习十几减9、减8等退位减法',
            'icon': '➖',
            'color': '#4ECDC4',
            'estimated_time': 10,
            'difficulty': 3,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '有15个豆子，吃掉9个，还剩几个？',
                    'correct_answer': '6',
                    'question_data': json.dumps({
                        'game_type': 'pacman',
                        'total': 15,
                        'eaten': 9
                    }),
                    'explanation': '15 - 9 = 6，可以想：15 - 5 = 10，10 - 4 = 6',
                    'difficulty': 3,
                    'points': 20
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '12 - 8 = ?',
                    'correct_answer': '4',
                    'explanation': '12 - 8 = 4',
                    'difficulty': 3,
                    'points': 20
                }
            ]
        },

        # 3. 分类与整理
        {
            'name': '分类与整理',
            'description': '学习按不同标准分类',
            'icon': '📦',
            'color': '#FFD93D',
            'estimated_time': 6,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'drag_drop',
                    'question_text': '把玩具放到正确的箱子里：车类、娃娃类、球类',
                    'correct_answer': json.dumps({
                        'vehicles': ['car', 'train', 'plane'],
                        'dolls': ['teddy', 'doll'],
                        'balls': ['basketball', 'football']
                    }),
                    'question_data': json.dumps({
                        'game_type': 'toy_sort',
                        'categories': ['vehicles', 'dolls', 'balls']
                    }),
                    'explanation': '按照玩具的类型分类',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 4. 100以内数的认识
        {
            'name': '100以内数的认识',
            'description': '认识100以内的数',
            'icon': '💯',
            'color': '#6BCB77',
            'estimated_time': 8,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '数豆子，用框框圈出每10个，一共有多少个？',
                    'correct_answer': '35',
                    'question_data': json.dumps({
                        'game_type': 'count_beans',
                        'total': 35,
                        'group_size': 10
                    }),
                    'explanation': '3组10个是30，加上5个，一共35',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive'
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '56里面有几个十和几个一？',
                    'correct_answer': '5个十,6个一',
                    'explanation': '56 = 5个十 + 6个一',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 5. 认识人民币
        {
            'name': '认识人民币',
            'description': '认识人民币，学习简单计算',
            'icon': '💰',
            'color': '#4D96FF',
            'estimated_time': 8,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'drag_drop',
                    'question_text': '橡皮5元，用钱币付款',
                    'correct_answer': json.dumps(['5yuan']),
                    'question_data': json.dumps({
                        'game_type': 'pay_money',
                        'price': 5,
                        'available_money': ['1yuan', '2yuan', '5yuan', '10yuan']
                    }),
                    'explanation': '可以用1张5元，或者5张1元',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'drag_drop'
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '买10元的东西，给了20元，应该找回多少钱？',
                    'correct_answer': '10',
                    'question_data': json.dumps({
                        'game_type': 'cashier',
                        'price': 10,
                        'paid': 20
                    }),
                    'explanation': '20 - 10 = 10元',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 6. 100以内的加法和减法（一）
        {
            'name': '100以内的加减法',
            'description': '整十数加减和两位数加减整十数',
            'icon': '🧮',
            'color': '#FF6B6B',
            'estimated_time': 10,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'fill_blank',
                    'question_text': '公交车上有30人，下去10人，还剩多少人？',
                    'correct_answer': '20',
                    'question_data': json.dumps({
                        'game_type': 'bus',
                        'initial': 30,
                        'off': 10
                    }),
                    'explanation': '30 - 10 = 20',
                    'difficulty': 2,
                    'points': 15,
                    'animation_type': 'interactive'
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '35 + 20 = ?',
                    'correct_answer': '55',
                    'explanation': '35 + 20 = 55',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        },

        # 7. 找规律
        {
            'name': '找规律',
            'description': '发现并延续规律',
            'icon': '🔍',
            'color': '#C4E538',
            'estimated_time': 6,
            'difficulty': 2,
            'exercises': [
                {
                    'question_type': 'click',
                    'question_text': '⭐🌙⭐🌙⭐？下一个是什么？',
                    'correct_answer': '🌙',
                    'question_data': json.dumps({
                        'game_type': 'pattern',
                        'sequence': ['⭐', '🌙', '⭐', '🌙', '⭐'],
                        'options': ['⭐', '🌙', '☀️']
                    }),
                    'explanation': '星星和月亮交替出现',
                    'difficulty': 2,
                    'points': 15
                },
                {
                    'question_type': 'fill_blank',
                    'question_text': '2、4、6、8、？下一个数字是多少？',
                    'correct_answer': '10',
                    'question_data': json.dumps({
                        'game_type': 'number_pattern',
                        'sequence': [2, 4, 6, 8]
                    }),
                    'explanation': '每次加2：2、4、6、8、10',
                    'difficulty': 2,
                    'points': 15
                }
            ]
        }
    ]

    # 添加一年级下册主题
    for topic_data in topics_grade_1_second:
        exercises_data = topic_data.pop('exercises', [])
        topic = Topic(grade_id=grade_1.id, **topic_data)
        db.session.add(topic)
        db.session.flush()

        for ex_data in exercises_data:
            exercise = Exercise(topic_id=topic.id, **ex_data)
            db.session.add(exercise)

    print("✅ 一年级课程内容初始化完成！")
    return grade_1
