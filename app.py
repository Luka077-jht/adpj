import streamlit as st
import pandas as pd
import numpy as np
import random
import time
from datetime import datetime
import streamlit.components.v1 as components
import json
import base64
import os

# 页面配置
st.set_page_config(
    page_title="🎬 黑暗荣耀角色评分 - 虎扑风格",
    page_icon="⚔️",
    layout="wide"
)

# 自定义CSS样式 - 保持66.7%文件的风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #1E3C72, #2A5298, #667EEA, #764BA2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .character-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1E3C72;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: #FFFFFF;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        font-weight: 500;
    }
    .rating-section h1, .rating-section h2, .rating-section h3, .rating-section h4 {
        color: #FFFFFF;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
    }
    .meme-tag {
        display: inline-block;
        background-color: #FFE082;
        color: #333;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        border-radius: 15px;
        font-size: 1rem;
        font-weight: bold;
    }
    .hot-comment {
        background-color: #BBDEFB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #1976D2;
        color: #1565C0;
        font-weight: 500;
    }
    .score-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .star-rating {
        font-size: 2rem;
        margin: 10px 0;
        color: white;
    }
    .star-rating .star {
        color: #FFD93D;
        margin: 0 5px;
        cursor: pointer;
        text-shadow: 0 0 3px rgba(255, 217, 61, 0.5);
        font-size: 2rem;
    }
    .star-rating .star.empty {
        color: white;
        opacity: 0.7;
        font-size: 2.2rem;
    }
    .score-highlight {
        background: linear-gradient(135deg, #FF6B6B, #FF8E53);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 8px rgba(255, 107, 107, 0.3);
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin: 10px 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
        font-weight: 500;
    }
    .stat-card h3 {
        color: #FFFFFF;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
    }
    .character-image {
        width: 200px;
        height: 200px;
        border-radius: 15px;
        object-fit: cover;
        border: 4px solid #1E3C72;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .actor-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    .actor-section h3 {
        color: white;
        text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        font-weight: 600;
        margin-bottom: 1rem;
    }
    .works-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 1rem;
    }
    .work-item {
        background: rgba(255, 255, 255, 0.2);
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    .actor-info {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 1rem;
    }
    .actor-name {
        font-size: 1.3rem;
        font-weight: bold;
        color: #FFD93D;
    }
</style>
""", unsafe_allow_html=True)

# 初始化数据
def init_data():
    if 'character_ratings' not in st.session_state:
        st.session_state.character_ratings = {}
    if 'rating_sessions' not in st.session_state:
        st.session_state.rating_sessions = 0
    if 'characters_df' not in st.session_state:
        st.session_state.characters_df = initialize_characters()

# 黑暗荣耀角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 7),
        'name': ['文东恩', '朴妍珍', '周汝正', '全在俊', '李莎拉', '崔惠程'],
        'role': ['女主角', '反派', '男主角', '反派', '反派', '反派'],
        'description': [
            '遭受校园暴力后精心策划复仇的教师',
            '校园暴力的主导者，气象主播',
            '帮助文东恩的整形外科医生',
            '朴妍珍的丈夫，高尔夫球场代表',
            '画家，校园暴力参与者',
            '空姐，校园暴力参与者'
        ],
        'mbti_type': ['INTJ', 'ESTJ', 'INFJ', 'ISTP', 'ISFP', 'ESFJ'],
        'mbti_description': [
            'INTJ（建筑师型）：战略家性格，善于长期规划，理性冷静，目标导向',
            'ESTJ（总经理型）：务实领导者，注重规则和秩序，强势果断，追求效率',
            'INFJ（提倡者型）：理想主义者，富有同情心，洞察力强，追求意义',
            'ISTP（鉴赏家型）：实用主义者，冷静理性，善于解决问题，行动派',
            'ISFP（探险家型）：艺术家性格，敏感细腻，追求美感，活在当下',
            'ESFJ（执政官型）：社交达人，注重和谐，乐于助人，传统保守'
        ],
        'actor_name': ['宋慧乔', '林智妍', '李到晛', '朴成焄', '金赫拉', '车珠英'],
        'actor_bio': [
            '韩国著名女演员，以《浪漫满屋》《太阳的后裔》等作品闻名，演技精湛，深受观众喜爱。',
            '韩国实力派女演员，擅长演绎复杂角色，在《黑暗荣耀》中成功塑造了令人印象深刻的反派形象。',
            '韩国新生代男演员，演技自然细腻，在多部作品中展现出色的表演实力。',
            '韩国资深演员，演技扎实，擅长演绎各种类型的角色，表演富有层次感。',
            '韩国女演员，在《黑暗荣耀》中展现了出色的演技，成功塑造了李莎拉这一复杂角色。',
            '韩国女演员，以清纯形象出道，在《黑暗荣耀》中展现了突破性的演技。'
        ],
        'famous_works': [
            ['太阳的后裔', '浪漫满屋', '那年冬天风在吹'],
            ['黑暗荣耀', '人间中毒', '奸臣'],
            ['黑暗荣耀', '再次十八岁', '忧郁症'],
            ['黑暗荣耀', '鱿鱼游戏', '模范出租车'],
            ['黑暗荣耀', '黑话律师', '纸钞屋'],
            ['黑暗荣耀', '我的ID是江南美人', '顶楼']
        ],
        'avg_rating': [9.2, 8.1, 8.7, 7.8, 7.5, 7.3],
        'rating_count': [15200, 12800, 11500, 9800, 8900, 7600],
        'image_url': [
            'https://via.placeholder.com/200x300/1E3C72/FFFFFF?text=文东恩',
            'https://via.placeholder.com/200x300/2A5298/FFFFFF?text=朴妍珍',
            'https://via.placeholder.com/200x300/667EEA/FFFFFF?text=周汝正',
            'https://via.placeholder.com/200x300/764BA2/FFFFFF?text=全在俊',
            'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=李莎拉',
            'https://via.placeholder.com/200x300/FF8E53/FFFFFF?text=崔惠程'
        ],
        'actor_photo_url': [
            'https://via.placeholder.com/200x300/4CAF50/FFFFFF?text=宋慧乔',
            'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=林智妍',
            'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=李到晛',
            'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=朴成焄',
            'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=金赫拉',
            'https://via.placeholder.com/200x300/795548/FFFFFF?text=车珠英'
        ]
    }
    return pd.DataFrame(characters_data)

# 代表作品图片映射
def get_work_images(work_name):
    work_images = {
        '太阳的后裔': 'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=太阳的后裔',
        '浪漫满屋': 'https://via.placeholder.com/200x300/4CAF50/FFFFFF?text=浪漫满屋',
        '那年冬天风在吹': 'https://via.placeholder.com/200x300/2196F3/FFFFFF?text=那年冬天风在吹',
        '人间中毒': 'https://via.placeholder.com/200x300/9C27B0/FFFFFF?text=人间中毒',
        '奸臣': 'https://via.placeholder.com/200x300/FF9800/FFFFFF?text=奸臣',
        '再次十八岁': 'https://via.placeholder.com/200x300/607D8B/FFFFFF?text=再次十八岁',
        '忧郁症': 'https://via.placeholder.com/200x300/795548/FFFFFF?text=忧郁症',
        '鱿鱼游戏': 'https://via.placeholder.com/200x300/1E3C72/FFFFFF?text=鱿鱼游戏',
        '模范出租车': 'https://via.placeholder.com/200x300/2A5298/FFFFFF?text=模范出租车',
        '黑话律师': 'https://via.placeholder.com/200x300/667EEA/FFFFFF?text=黑话律师',
        '纸钞屋': 'https://via.placeholder.com/200x300/764BA2/FFFFFF?text=纸钞屋',
        '我的ID是江南美人': 'https://via.placeholder.com/200x300/FF8E53/FFFFFF?text=我的ID是江南美人',
        '顶楼': 'https://via.placeholder.com/200x300/FFD93D/FFFFFF?text=顶楼',
        '黑暗荣耀': 'https://via.placeholder.com/200x300/1E3C72/FFFFFF?text=黑暗荣耀'
    }
    return work_images.get(work_name, 'https://via.placeholder.com/200x300/666666/FFFFFF?text=默认作品')

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["妍珍啊", "欢迎来到我的地狱", "河道英的沉默", "我需要的是刽子手"],
        2: ["西八", "气象主播的优雅", "校园暴力的代价", "富家女的堕落"],
        3: ["整形医生的温柔", "文东恩的守护者", "周医生的选择", "爱情与复仇之间"],
        4: ["高尔夫球场代表", "妍珍的丈夫", "商业精英的冷漠", "上流社会的虚伪"],
        5: ["画家的疯狂", "毒品的奴隶", "艺术家的悲剧", "校园暴力的参与者"],
        6: ["空姐的虚荣", "校园暴力的帮凶", "美貌的代价", "底层挣扎"]
    }
    
    comments_dict = {
        1: ["宋慧乔演技炸裂，文东恩的复仇让人心疼又解气", "从受害者到复仇者，角色的转变太精彩了"],
        2: ["林智妍把朴妍珍演活了，让人恨得牙痒痒", "反派塑造得太成功了，每个细节都很到位"],
        3: ["李到晛的周医生太温柔了，是黑暗中的一束光", "周汝正的选择展现了真正的人性光辉"],
        4: ["全在俊这个角色展现了上流社会的冷漠", "演员的表演很有层次感"],
        5: ["李莎拉的疯狂和悲剧让人印象深刻", "演员成功塑造了复杂的人物形象"],
        6: ["崔惠程的虚荣和挣扎很真实", "空姐身份的设定很有讽刺意味"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统 - 使用Streamlit原生组件
def star_rating_component(character_id, current_rating=0):
    # 使用Streamlit的selectbox替代复杂的JavaScript交互
    rating_options = ["未评分", "1星 ⭐", "2星 ⭐⭐", "3星 ⭐⭐⭐", "4星 ⭐⭐⭐⭐", "5星 ⭐⭐⭐⭐⭐"]
    
    # 创建唯一的key
    rating_key = f"rating_{character_id}"
    
    # 显示当前评分状态
    if current_rating > 0:
        st.markdown(f'<div style="text-align: center; background: #4CAF50; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_rating}星</div>', unsafe_allow_html=True)
    
    # 使用selectbox进行评分
    selected_rating = st.selectbox(
        "选择评分",
        options=rating_options,
        index=current_rating,
        key=rating_key
    )
    
    # 解析评分值
    new_rating = rating_options.index(selected_rating)
    
    # 如果评分有变化，更新session state
    if new_rating != current_rating and new_rating > 0:
        st.session_state.character_ratings[character_id] = new_rating
        st.session_state.rating_sessions += 1
        st.success(f"✅ 已为{st.session_state.characters_df[st.session_state.characters_df['id'] == character_id]['name'].iloc[0]}评分 {new_rating}星")
        st.rerun()
    
    return None

# 角色评分界面
def character_rating_interface():
    st.markdown('<div class="main-header">⚔️ 黑暗荣耀角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 虎扑风格评分系统 · 实时统计 · 热评互动</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 评分范围
        min_score, max_score = st.slider(
            "评分范围", 
            min_value=0.0, 
            max_value=10.0, 
            value=(7.0, 9.5),
            step=0.1
        )
        
        # 搜索框
        search_term = st.text_input("🔎 搜索角色", placeholder="输入角色名或描述...")
        
        # 应用筛选
        filtered_characters = st.session_state.characters_df.copy()
        if selected_role != '全部':
            filtered_characters = filtered_characters[filtered_characters['role'] == selected_role]
        
        filtered_characters = filtered_characters[
            (filtered_characters['avg_rating'] >= min_score) & 
            (filtered_characters['avg_rating'] <= max_score)
        ]
        
        if search_term:
            filtered_characters = filtered_characters[
                filtered_characters['name'].str.contains(search_term, case=False) |
                filtered_characters['description'].str.contains(search_term, case=False)
            ]
    
    # 主内容区
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("👥 角色评分区")
        
        # 排序选项
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        else:
            ranked_characters = filtered_characters.sort_values('name', ascending=True)
        
        # 角色展示和评分
        for _, character in ranked_characters.iterrows():
            with st.container():
                st.markdown(f'<div class="character-card">', unsafe_allow_html=True)
                
                # 角色信息布局 - 优化图片和评分布局
                col_a, col_b = st.columns([2, 3])
                
                with col_a:
                    # 角色图片 - 放大到与评分框等宽
                    st.image(character['image_url'], width='stretch', caption=character['name'])
                    
                    # 评分显示 - 与图片宽度对齐
                    st.markdown(f'<div class="score-highlight" style="text-align: center; margin-top: 10px;">评分: {character["avg_rating"]}</div>', 
                               unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 5px;">👥 {character["rating_count"]}人评分</div>', 
                               unsafe_allow_html=True)
                
                with col_b:
                    # 角色基本信息 - 放大字体
                    st.markdown(f"<h2 style='font-size: 1.8rem; margin-bottom: 10px;'>{character['name']}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #1E3C72; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 虎扑式热评和梗 - 放大字体
                    memes, comments = get_character_memes(character['id'])
                    
                    if memes:
                        st.markdown("<h4 style='font-size: 1.3rem; margin-bottom: 10px;'>🔥 角色热梗</h4>", unsafe_allow_html=True)
                        meme_cols = st.columns(len(memes))
                        for i, meme in enumerate(memes):
                            with meme_cols[i]:
                                st.markdown(f'<div class="meme-tag" style="font-size: 1rem;">{meme}</div>', unsafe_allow_html=True)
                    
                    # 五星评分系统 - 优化布局
                    st.markdown("### ⭐ 为角色评分")
                    current_user_rating = st.session_state.character_ratings.get(character['id'], 0)
                    
                    # 创建五星评分组件
                    star_rating_component(character['id'], current_user_rating)
                    
                    # 显示热评 - 放大字体
                    if comments:
                        st.markdown("<h4 style='font-size: 1.3rem; margin-bottom: 10px;'>💬 虎扑热评</h4>", unsafe_allow_html=True)
                        for comment in comments:
                            st.markdown(f'<div class="hot-comment" style="font-size: 1.1rem; line-height: 1.4;">{comment}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("---")
    
    with col2:
        st.subheader("📊 实时统计")
        
        # 统计卡片
        total_characters = len(filtered_characters)
        avg_rating = filtered_characters['avg_rating'].mean() if total_characters > 0 else 0
        total_ratings = filtered_characters['rating_count'].sum()
        
        col_stat1, col_stat2 = st.columns(2)
        
        with col_stat1:
            st.markdown(f'''
            <div class="stat-card">
                <h3>👥 角色数量</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{total_characters}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            st.markdown(f'''
            <div class="stat-card">
                <h3>⭐ 平均评分</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{avg_rating:.1f}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col_stat2:
            st.markdown(f'''
            <div class="stat-card">
                <h3>📈 总评分数</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{total_ratings:,}</div>
            </div>
            ''', unsafe_allow_html=True)
            
            user_rated_count = len(st.session_state.character_ratings)
            st.markdown(f'''
            <div class="stat-card">
                <h3>🎯 我已评分</h3>
                <div style="font-size: 1.5rem; font-weight: bold;">{user_rated_count}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        # 排行榜
        st.subheader("🏆 角色排行榜")
        
        for i, (_, character) in enumerate(ranked_characters.head(5).iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 10px;'>{medal} <strong>{character['name']}</strong></div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  评分: <strong>{character['avg_rating']}</strong> 🌟</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 5px;'>  身份: {character['role']}</div>", unsafe_allow_html=True)
            
            # 显示用户评分
            user_score = st.session_state.character_ratings.get(character['id'])
            if user_score:
                st.markdown(f"<div style='font-size: 1.1rem; margin-bottom: 10px;'>  我的评分: <strong>{user_score}</strong> 🌟</div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析角色特点和观剧体验")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    actor_name = character_data['actor_name']
    famous_works = character_data['famous_works']
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹", "演员简介", "代表作品分析", "演艺生涯发展"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析角色...'):
            time.sleep(2)  # 模拟AI分析过程
            
            # 根据分析类型生成不同的分析结果
            if analysis_type == "角色性格分析":
                analysis_result = f"""
                **{selected_character}的性格深度解析：**
                
                {character_data['mbti_description']}
                
                **性格特点：**
                - **理性思维**：{selected_character}展现出{character_data['mbti_type'][0]}型人格的典型特征
                - **目标导向**：在复仇计划中表现出极强的执行力和耐心
                - **情感控制**：能够有效控制情绪，保持冷静思考
                
                **性格优势：**
                - 战略规划能力强
                - 执行力突出
                - 情绪管理得当
                
                **性格局限：**
                - 可能过于理性而忽视情感需求
                - 复仇执念可能影响判断
                """
            elif analysis_type == "剧情作用分析":
                analysis_result = f"""
                **{selected_character}在剧情中的核心作用：**
                
                **角色定位：** {character_data['role']}
                
                **剧情推动力：**
                - 作为{character_data['role']}，{selected_character}是剧情发展的关键驱动力
                - 与其他角色的互动构成了复杂的人物关系网
                - 角色的选择和行动直接影响剧情走向
                
                **象征意义：**
                - 代表了社会中的特定群体或现象
                - 通过角色命运反映社会问题
                - 展现了人性的复杂性和多面性
                """
            elif analysis_type == "演技评价":
                analysis_result = f"""
                **{actor_name}饰演{selected_character}的演技评价：**
                
                **表演亮点：**
                - **情感表达**：成功塑造了角色的内心世界
                - **细节处理**：微表情和肢体语言丰富角色层次
                - **角色理解**：对角色的理解深入，表演自然真实
                
                **突破表现：**
                - 在{character_data['role']}这一角色类型上有新的突破
                - 展现了不同于以往作品的表演风格
                - 成功挑战了复杂的人物性格
                
                **观众反馈：**
                - 获得了{character_data['rating_count']}名观众的认可
                - 平均评分达到{character_data['avg_rating']}分
                - 在社交媒体上获得广泛讨论
                """
            else:
                analysis_result = f"""
                **{selected_character}的{analysis_type}：**
                
                这是一个复杂而深刻的角色，在{character_data['role']}这一身份下展现了丰富的人物层次。
                
                **关键特点：**
                - 角色定位清晰，性格鲜明
                - 在剧情发展中起到重要作用
                - 演员{actor_name}的表演为角色注入了生命力
                
                **观众评价：**
                - 获得了{character_data['rating_count']}名观众的评分
                - 平均评分：{character_data['avg_rating']}分
                - 角色深度和复杂性受到认可
                """
            
            st.success("✅ AI分析完成！")
            st.markdown(f"### 📋 {analysis_type}报告")
            st.markdown(analysis_result)
            
            # 显示相关图片
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(character_data['image_url'], caption=f"{selected_character}角色形象", use_column_width=True)
            with col_img2:
                st.image(character_data['actor_photo_url'], caption=f"演员{actor_name}", use_column_width=True)

# 演员信息界面
def actor_info_interface():
    st.markdown("## 🎭 演员信息")
    st.markdown("### 🌟 了解演员的演艺生涯和代表作品")
    
    # 演员选择
    actor_names = list(st.session_state.characters_df['actor_name'].unique())
    selected_actor = st.selectbox("选择演员", actor_names, key="actor_select")
    
    # 获取演员信息
    actor_data = st.session_state.characters_df[st.session_state.characters_df['actor_name'] == selected_actor].iloc[0]
    
    # 显示演员信息
    col_actor1, col_actor2 = st.columns([1, 2])
    
    with col_actor1:
        st.image(actor_data['actor_photo_url'], caption=selected_actor, use_column_width=True)
    
    with col_actor2:
        st.markdown(f"### {selected_actor}")
        st.markdown(f"**饰演角色：** {actor_data['name']} ({actor_data['role']})")
        st.markdown(f"**角色描述：** {actor_data['description']}")
        st.markdown(f"**演员简介：** {actor_data['actor_bio']}")
    
    # 代表作品展示
    st.markdown("### 🎬 代表作品")
    
    works = actor_data['famous_works']
    if len(works) > 0:
        cols = st.columns(min(3, len(works)))
        
        for i, work in enumerate(works):
            with cols[i % 3]:
                st.markdown(f'<div class="work-item">{work}</div>', unsafe_allow_html=True)
                # 显示作品图片（如果有）
                work_image = get_work_images(work)
                st.image(work_image, caption=work, use_column_width=True)

# 主程序
def main():
    # 初始化数据
    init_data()
    
    # 导航菜单
    st.sidebar.title("⚔️ 导航菜单")
    menu_options = ["角色评分", "AI角色分析", "演员信息"]
    selected_menu = st.sidebar.radio("选择功能", menu_options)
    
    # 根据选择显示不同界面
    if selected_menu == "角色评分":
        character_rating_interface()
    elif selected_menu == "AI角色分析":
        ai_character_analysis()
    elif selected_menu == "演员信息":
        actor_info_interface()
    
    # 页脚信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 系统信息")
    st.sidebar.markdown(f"**评分会话数：** {st.session_state.rating_sessions}")
    st.sidebar.markdown(f"**已评分角色：** {len(st.session_state.character_ratings)}")
    st.sidebar.markdown(f"**最后更新：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 关于信息
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ 关于")
    st.sidebar.markdown("**黑暗荣耀角色评分系统**")
    st.sidebar.markdown("基于Streamlit开发的互动评分应用")
    st.sidebar.markdown("支持角色评分、AI分析和演员信息查看")

if __name__ == "__main__":
    main()