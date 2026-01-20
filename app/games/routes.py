from flask import render_template, url_for, flash, redirect, request, jsonify, session
from flask_login import login_required, current_user
from app import db
from app.models import GameRecord, PracticeRecord, RoundRecord
from app.games import games
from src import game
from src.ai import playerguess
import random
from datetime import datetime

@games.route('/practice')
@login_required
def practice():
    """练习模式页面"""
    return render_template('practice.html', title='Practice Mode')

@games.route('/practice/start', methods=['POST'])
@login_required
def start_practice():
    """开始练习模式
    
    请求参数：
        difficulty: 难度级别，可选值：beginner, easy, advanced, medium, hard
        
    返回：
        JSON格式的响应，包含游戏ID、状态和消息
    """
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        
        # 根据难度获取权重
        weights = get_difficulty_weights(difficulty)
        
        # 随机选择题目
        selected_problem = weighted_randproblem(weights)
        
        # 生成游戏ID
        game_id = f"practice_{current_user.id}_{int(datetime.now().timestamp())}"
        
        # 存储游戏状态到session
        session[game_id] = {
            'game_id': game_id,
            'problem': selected_problem,
            'difficulty': difficulty,
            'guess_count': 0,
            'start_time': datetime.now().isoformat(),
            'is_active': True
        }
        
        return jsonify({
            'status': 'success',
            'message': '练习游戏已开始',
            'game_id': game_id,
            'difficulty': difficulty
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

@games.route('/practice/guess', methods=['POST'])
@login_required
def practice_guess():
    """处理练习模式的猜测
    
    请求参数：
        game_id: 游戏ID
        question: 玩家的问题或猜测
        
    返回：
        JSON格式的响应，包含AI回答、猜测次数和是否猜对
    """
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        question = data.get('question', '').strip()
        
        # 验证请求参数
        if not game_id or not question:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
        
        # 获取游戏状态
        game_state = session.get(game_id)
        if not game_state or not game_state.get('is_active'):
            return jsonify({
                'status': 'error',
                'message': '游戏不存在或已结束'
            }), 400
        
        # 更新猜测次数
        game_state['guess_count'] += 1
        session[game_id] = game_state
        
        # 调用AI获取回答
        answer = playerguess(game_state['problem'], question)
        
        # 检查是否猜对
        is_correct = answer == 'CORRECT'
        
        # 如果猜对了，结束游戏
        if is_correct:
            # 计算得分
            score = calculate_practice_score(game_state['guess_count'], game_state['difficulty'])
            
            # 更新游戏状态
            game_state['is_active'] = False
            game_state['end_time'] = datetime.now().isoformat()
            game_state['score'] = score
            session[game_id] = game_state
            
            return jsonify({
                'status': 'success',
                'answer': answer,
                'guess_count': game_state['guess_count'],
                'is_correct': is_correct,
                'score': score,
                'correct_substance': game_state['problem'],
                'game_ended': True
            })
        
        # 游戏未结束，返回当前状态
        return jsonify({
            'status': 'success',
            'answer': answer,
            'guess_count': game_state['guess_count'],
            'is_correct': is_correct,
            'game_ended': False
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

@games.route('/practice/end', methods=['POST'])
@login_required
def end_practice():
    """结束练习模式
    
    请求参数：
        game_id: 游戏ID
        
    返回：
        JSON格式的响应，包含状态和消息
    """
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        
        # 验证请求参数
        if not game_id:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
        
        # 获取游戏状态
        game_state = session.get(game_id)
        if not game_state:
            return jsonify({
                'status': 'error',
                'message': '游戏不存在'
            }), 400
        
        # 更新游戏状态为已结束
        game_state['is_active'] = False
        game_state['end_time'] = datetime.now().isoformat()
        session[game_id] = game_state
        
        return jsonify({
            'status': 'success',
            'message': '游戏已结束',
            'correct_substance': game_state['problem']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500



@games.route('/pvp')
@login_required
def pvp():
    """PVP对战模式页面"""
    return render_template('pvp.html', title='PVP Mode')

@games.route('/pvp/match')
@login_required
def pvp_match():
    """开始PVP匹配"""
    return redirect(url_for('games.pvp'))



@games.route('/ai')
@login_required
def ai():
    """AI对战模式页面"""
    return render_template('ai.html', title='AI Mode')

@games.route('/ai/start', methods=['POST'])
@login_required
def start_ai():
    """开始AI对战模式
    
    请求参数：
        difficulty: 难度级别，可选值：beginner, easy, advanced, medium, hard
        
    返回：
        JSON格式的响应，包含游戏ID、状态和消息
    """
    try:
        data = request.get_json()
        difficulty = data.get('difficulty', 'easy')
        
        # 根据难度获取权重
        weights = get_difficulty_weights(difficulty)
        
        # 随机选择题目
        selected_problem = weighted_randproblem(weights)
        
        # 生成游戏ID
        game_id = f"ai_{current_user.id}_{int(datetime.now().timestamp())}"
        
        # 初始化AI对战状态
        session[game_id] = {
            'game_id': game_id,
            'problem': selected_problem,
            'difficulty': difficulty,
            'round': 1,
            'player_hp': 100,
            'ai_hp': 100,
            'player_guess_count': 0,
            'ai_guess_count': 0,
            'player_answer_locked': False,
            'ai_answer_locked': False,
            'player_final_guess': '',
            'ai_final_guess': '',
            'player_correct': False,
            'ai_correct': False,
            'start_time': datetime.now().isoformat(),
            'is_active': True,
            'ai_conversation': [],  # 存储AI对话历史，用于上下文管理
            'round_start_time': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'message': 'AI对战游戏已开始',
            'game_id': game_id,
            'difficulty': difficulty,
            'player_hp': 100,
            'ai_hp': 100,
            'round': 1
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

@games.route('/ai/guess', methods=['POST'])
@login_required
def ai_guess():
    """处理AI对战模式的玩家猜测
    
    请求参数：
        game_id: 游戏ID
        question: 玩家的问题或猜测
        
    返回：
        JSON格式的响应，包含AI回答、猜测次数和当前游戏状态
    """
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        question = data.get('question', '').strip()
        
        # 验证请求参数
        if not game_id or not question:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
        
        # 获取游戏状态
        game_state = session.get(game_id)
        if not game_state or not game_state.get('is_active'):
            return jsonify({
                'status': 'error',
                'message': '游戏不存在或已结束'
            }), 400
        
        # 检查玩家是否已锁定答案
        if game_state['player_answer_locked']:
            return jsonify({
                'status': 'error',
                'message': '您已锁定答案，无法继续猜测'
            }), 400
        
        # 更新玩家猜测次数
        game_state['player_guess_count'] += 1
        session[game_id] = game_state
        
        # 调用AI获取回答
        answer = playerguess(game_state['problem'], question)
        
        # 检查是否是直接猜测物质名称
        is_final_guess = answer in ['CORRECT', 'INCORRECT']
        
        # 如果是最终猜测，锁定玩家答案
        if is_final_guess:
            game_state['player_answer_locked'] = True
            game_state['player_final_guess'] = question
            game_state['player_correct'] = (answer == 'CORRECT')
            session[game_id] = game_state
            
            # 触发AI进行猜测
            ai_response = trigger_ai_guess(game_state)
            
            # 如果AI也已锁定答案，结算本轮
            if ai_response['ai_answer_locked']:
                return settle_round(game_state)
        
        return jsonify({
            'status': 'success',
            'answer': answer,
            'guess_count': game_state['player_guess_count'],
            'player_answer_locked': game_state['player_answer_locked'],
            'ai_answer_locked': game_state['ai_answer_locked'],
            'round': game_state['round'],
            'player_hp': game_state['player_hp'],
            'ai_hp': game_state['ai_hp']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

@games.route('/ai/lock_answer', methods=['POST'])
@login_required
def ai_lock_answer():
    """玩家手动锁定答案
    
    请求参数：
        game_id: 游戏ID
        
    返回：
        JSON格式的响应，包含当前游戏状态
    """
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        
        # 验证请求参数
        if not game_id:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
        
        # 获取游戏状态
        game_state = session.get(game_id)
        if not game_state or not game_state.get('is_active'):
            return jsonify({
                'status': 'error',
                'message': '游戏不存在或已结束'
            }), 400
        
        # 检查玩家是否已锁定答案
        if game_state['player_answer_locked']:
            return jsonify({
                'status': 'error',
                'message': '您已锁定答案，无法再次锁定'
            }), 400
        
        # 锁定玩家答案（使用最后一次猜测作为最终答案）
        game_state['player_answer_locked'] = True
        game_state['player_final_guess'] = ''  # 这里应该使用玩家的最后一次猜测，暂时留空
        game_state['player_correct'] = False
        session[game_id] = game_state
        
        # 触发AI进行猜测
        ai_response = trigger_ai_guess(game_state)
        
        # 如果AI也已锁定答案，结算本轮
        if ai_response['ai_answer_locked']:
            return settle_round(game_state)
        
        return jsonify({
            'status': 'success',
            'message': '答案已锁定',
            'player_answer_locked': True,
            'ai_answer_locked': game_state['ai_answer_locked'],
            'round': game_state['round'],
            'player_hp': game_state['player_hp'],
            'ai_hp': game_state['ai_hp']
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

@games.route('/ai/end', methods=['POST'])
@login_required
def end_ai():
    """结束AI对战
    
    请求参数：
        game_id: 游戏ID
        
    返回：
        JSON格式的响应，包含状态和消息
    """
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        
        # 验证请求参数
        if not game_id:
            return jsonify({
                'status': 'error',
                'message': '缺少必要参数'
            }), 400
        
        # 获取游戏状态
        game_state = session.get(game_id)
        if not game_state:
            return jsonify({
                'status': 'error',
                'message': '游戏不存在'
            }), 400
        
        # 更新游戏状态为已结束
        game_state['is_active'] = False
        game_state['end_time'] = datetime.now().isoformat()
        session[game_id] = game_state
        
        return jsonify({
            'status': 'success',
            'message': '游戏已结束'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500



@games.route('/leaderboard')
def leaderboard():
    """排行榜页面"""
    return render_template('leaderboard.html', title='Leaderboard')

# 辅助函数
def get_difficulty_weights(difficulty):
    """根据难度获取题目池权重
    
    Args:
        difficulty: 难度级别，可选值：beginner, easy, advanced, medium, hard
        
    Returns:
        包含不同难度题目池权重的字典
    """
    weights_map = {
        'beginner': {'easy': 0.9, 'mideasy': 0.1, 'mid': 0},
        'easy': {'easy': 0.5, 'mideasy': 0.5, 'mid': 0},
        'advanced': {'easy': 0.2, 'mideasy': 0.8, 'mid': 0},
        'medium': {'easy': 0.1, 'mideasy': 0.8, 'mid': 0.1},
        'hard': {'easy': 0, 'mideasy': 0.3, 'mid': 0.7}
    }
    return weights_map.get(difficulty, weights_map['easy'])

def weighted_randproblem(weights):
    """带权重的随机选择题目
    
    Args:
        weights: 包含不同难度题目池权重的字典
        
    Returns:
        随机选择的题目（化学物质名称）
    """
    # 随机选择题目池
    problem_library = random.choices(
        population=['easy', 'mideasy', 'mid'],
        weights=[weights['easy'], weights['mideasy'], weights['mid']],
        k=1
    )[0]
    
    # 从选择的题目池中随机选择题目
    if problem_library == 'easy':
        return game.randproblem(game.ProblemLibs.easy)
    elif problem_library == 'mideasy':
        return game.randproblem(game.ProblemLibs.mideasy)
    else:
        return game.randproblem(game.ProblemLibs.mid)

def calculate_practice_score(guess_count, difficulty):
    """计算练习模式得分
    
    得分规则：
        基础分数为100分
        根据猜测次数扣分，每次猜测扣5分
        根据难度加分：beginner(0), easy(10), advanced(20), medium(30), hard(50)
        
    Args:
        guess_count: 猜测次数
        difficulty: 难度级别
        
    Returns:
        计算得到的分数
    """
    # 基础分数
    base_score = 100
    
    # 根据猜测次数扣分（最少扣到0分）
    guess_penalty = max(0, guess_count * 5)
    
    # 根据难度加分
    difficulty_bonus = {
        'beginner': 0,
        'easy': 10,
        'advanced': 20,
        'medium': 30,
        'hard': 50
    }.get(difficulty, 0)
    
    # 计算最终分数
    final_score = max(0, base_score - guess_penalty + difficulty_bonus)
    
    return final_score

def trigger_ai_guess(game_state):
    """触发AI进行猜测
    
    Args:
        game_state: 当前游戏状态
        
    Returns:
        更新后的游戏状态
    """
    # 如果AI已经锁定答案，直接返回
    if game_state['ai_answer_locked']:
        return game_state
    
    # 更新AI猜测次数
    game_state['ai_guess_count'] += 1
    
    # 简单AI策略：随机生成问题或猜测
    ai_actions = [
        "该物质是否是氧化物？",
        "该物质是否含有金属元素？",
        "该物质是否是酸？",
        "该物质是否是碱？",
        "该物质是否是盐？",
        "该物质是否溶于水？",
        "该物质是否是白色固体？",
        "氯化钠",
        "碳酸钠",
        "硫酸铜",
        "碳酸钙"
    ]
    
    # 根据难度调整AI行为：难度越高，越可能直接猜测物质名称
    difficulty_factor = {
        'beginner': 0.1,
        'easy': 0.2,
        'advanced': 0.3,
        'medium': 0.4,
        'hard': 0.6
    }.get(game_state['difficulty'], 0.2)
    
    # 决定AI是提问还是直接猜测
    if random.random() < difficulty_factor or game_state['ai_guess_count'] >= 5:
        # 直接猜测物质名称
        ai_guess = random.choice(ai_actions[-4:])
        answer = playerguess(game_state['problem'], ai_guess)
        
        # 锁定AI答案
        game_state['ai_answer_locked'] = True
        game_state['ai_final_guess'] = ai_guess
        game_state['ai_correct'] = (answer == 'CORRECT')
    else:
        # 提问
        ai_guess = random.choice(ai_actions[:-4])
        answer = playerguess(game_state['problem'], ai_guess)
        
        # 更新AI对话历史
        game_state['ai_conversation'].append({
            'role': 'user',
            'content': ai_guess
        })
        game_state['ai_conversation'].append({
            'role': 'assistant',
            'content': answer
        })
    
    session[game_state['game_id']] = game_state
    return game_state

def settle_round(game_state):
    """结算本轮游戏
    
    规则：
        1. 计算双方造成的伤害
        2. 更新双方血量
        3. 检查游戏是否结束
        4. 如果游戏未结束，进入下一轮
        
    Args:
        game_state: 当前游戏状态
        
    Returns:
        JSON格式的响应，包含结算结果和当前游戏状态
    """
    try:
        # 计算伤害
        battle_damage_base = 100  # 从.env获取，暂时硬编码
        battle_damage_scale = 0.25  # 从.env获取，暂时硬编码
        round_num = game_state['round']
        
        player_damage = 0
        ai_damage = 0
        
        # 玩家对AI造成的伤害
        if game_state['player_correct']:
            player_damage = (battle_damage_scale * (round_num - 1) + 1) * battle_damage_base / (game_state['player_guess_count'] or 1)
            ai_damage_dealt = max(0, min(100, player_damage))
            game_state['ai_hp'] = max(0, game_state['ai_hp'] - ai_damage_dealt)
        
        # AI对玩家造成的伤害
        if game_state['ai_correct']:
            ai_damage = (battle_damage_scale * (round_num - 1) + 1) * battle_damage_base / (game_state['ai_guess_count'] or 1)
            player_damage_dealt = max(0, min(100, ai_damage))
            game_state['player_hp'] = max(0, game_state['player_hp'] - player_damage_dealt)
        
        # 检查游戏是否结束
        game_ended = game_state['player_hp'] <= 0 or game_state['ai_hp'] <= 0
        
        result = ''
        if game_ended:
            game_state['is_active'] = False
            game_state['end_time'] = datetime.now().isoformat()
            
            if game_state['player_hp'] > game_state['ai_hp']:
                result = 'win'
            elif game_state['ai_hp'] > game_state['player_hp']:
                result = 'lose'
            else:
                result = 'draw'
            

        else:
            # 进入下一轮
            game_state['round'] += 1
            game_state['player_guess_count'] = 0
            game_state['ai_guess_count'] = 0
            game_state['player_answer_locked'] = False
            game_state['ai_answer_locked'] = False
            game_state['player_final_guess'] = ''
            game_state['ai_final_guess'] = ''
            game_state['player_correct'] = False
            game_state['ai_correct'] = False
            game_state['round_start_time'] = datetime.now().isoformat()
            
            # 随机选择新题目
            weights = get_difficulty_weights(game_state['difficulty'])
            game_state['problem'] = weighted_randproblem(weights)
        
        session[game_state['game_id']] = game_state
        
        response = {
            'status': 'success',
            'message': '本轮已结束',
            'round': game_state['round'],
            'player_hp': game_state['player_hp'],
            'ai_hp': game_state['ai_hp'],
            'player_guess_count': game_state['player_guess_count'],
            'ai_guess_count': game_state['ai_guess_count'],
            'player_correct': game_state['player_correct'],
            'ai_correct': game_state['ai_correct'],
            'player_final_guess': game_state['player_final_guess'],
            'ai_final_guess': game_state['ai_final_guess'],
            'player_damage_dealt': ai_damage,
            'ai_damage_dealt': player_damage,
            'game_ended': game_ended
        }
        
        if game_ended:
            response['result'] = result
            response['player_final_hp'] = game_state['player_hp']
            response['ai_final_hp'] = game_state['ai_hp']
        
        return jsonify(response)
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'internal server error: '+str(e)
        }), 500

