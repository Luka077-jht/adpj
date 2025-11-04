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
    page_title="🏠 请回答1988角色评分 - 虎扑风格",
    page_icon="🏠",
    layout="wide"
)

# 自定义CSS样式 - 仿照黑暗荣耀风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #FF6B6B, #FF8E53, #FFD93D, #4ECDC4);
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
        border-left: 4px solid #FF8E53;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #FF8E53 0%, #FF6B6B 100%);
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
        font-size: 4rem;
        margin: 10px 0;
        color: white;
    }
    .star-rating .star {
        color: #FFD93D;
        margin: 0 5px;
        cursor: pointer;
        text-shadow: 0 0 3px rgba(255, 217, 61, 0.5);
        font-size: 4rem;
    }
    .star-rating .star.empty {
        color: white;
        opacity: 0.7;
        font-size: 4.4rem;
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
        background: linear-gradient(135deg, #FF8E53 0%, #FF6B6B 100%);
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
        border: 4px solid #FF8E53;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
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

# 请回答1988角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 10),
        'name': ['成德善', '金正焕', '崔泽', '成善宇', '柳东龙', '成宝拉', '金正峰', '成余晖', '李一花'],
        'role': ['女主角', '男主角', '男主角', '男主角', '男主角', '女主角', '配角', '配角', '家长'],
        'neighborhood': ['双门洞', '双门洞', '双门洞', '双门洞', '双门洞', '双门洞', '双门洞', '双门洞', '双门洞'],
        'description': [
            '活泼开朗的双门洞高中生，家中老二',
            '外表冷漠内心温暖的狗焕，双门洞五人帮之一',
            '围棋天才，单纯善良的崔泽，双门洞五人帮之一',
            '品学兼优的善宇，双门洞五人帮之一',
            '双门洞的军师娃娃鱼，五人帮的开心果',
            '德善的姐姐，学霸性格强势',
            '正焕的哥哥，美食家兼彩票达人',
            '德善的弟弟，性格温和',
            '德善的妈妈，温柔贤惠的家庭主妇'
        ],
        'avg_rating': [9.5, 9.3, 9.4, 8.9, 8.8, 8.7, 8.6, 8.2, 8.9],
        'rating_count': [18500, 17200, 16800, 12500, 11800, 9800, 8900, 7600, 10500],
        'image_url': [
            '请回答1988/成德善.jpeg',
            '请回答1988/金正焕.jpg',
            '请回答1988/崔泽.jpeg',
            '请回答1988/成善宇.jpg',
            '请回答1988/柳东龙.jpg',
            '请回答1988/成宝拉.jpg',
            '请回答1988/金正峰.jpeg',
            '请回答1988/成余晖.jpg',
            '请回答1988/李一花.jpg'
        ]
    }
    return pd.DataFrame(characters_data)

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["德善啊", "请回答1988", "双门洞的开心果", "狗焕还是阿泽"],
        2: ["狗焕的犹豫", "正八啊", "双门洞的守护者", "错过的爱情"],
        3: ["围棋天才", "阿泽的微笑", "单纯善良", "双门洞的宝贝"],
        4: ["善宇的温柔", "宝拉的男朋友", "品学兼优", "双门洞的暖男"],
        5: ["娃娃鱼", "双门洞军师", "开心果", "人生导师"],
        6: ["宝拉姐", "学霸的威严", "德善的克星", "外冷内热"],
        7: ["正峰欧巴", "美食家", "彩票达人", "幸运星"],
        8: ["余晖啊", "温和的弟弟", "双门洞老幺", "默默无闻"],
        9: ["一花妈妈", "双门洞的妈妈", "温柔贤惠", "家的温暖"]
    }
    
    comments_dict = {
        1: ["李惠利把德善演活了，活泼开朗又让人心疼", "德善的成长线太真实了，每个细节都很打动人"],
        2: ["柳俊烈演的狗焕太让人心疼了，犹豫就会败北", "正焕的默默付出和最终错过，是多少人的青春写照"],
        3: ["朴宝剑的阿泽太治愈了，围棋天才的单纯善良", "阿泽的微笑是双门洞最温暖的阳光"],
        4: ["高庚杓的善宇太温柔了，对宝拉的深情让人感动", "善宇的成熟稳重是五人帮的定心丸"],
        5: ["李东辉的娃娃鱼是全剧的灵魂，金句频出", "娃娃鱼的军师角色为剧情增添了很多笑点和深度"],
        6: ["刘慧英的宝拉姐气场强大，学霸的威严很真实", "宝拉从强势到温柔的变化很细腻"],
        7: ["安宰弘的正峰欧巴太可爱了，美食家的形象深入人心", "正峰的单纯和幸运给剧情带来很多欢乐"],
        8: ["崔胜元的余晖虽然戏份不多，但很温暖", "余晖的温和性格是双门洞的调和剂"],
        9: ["李一花妈妈的温柔贤惠是双门洞的温暖源泉", "一花妈妈代表了那个时代母亲的伟大"]
    }
    
    memes = memes_dict.get(character_id, [])
    comments = comments_dict.get(character_id, [])
    return memes[:3], comments[:2]

# 五星评分系统
def star_rating_component(character_id, current_rating=0):
    stars_html = f"""
    <div class="star-rating" id="stars-{character_id}">
    """
    
    for i in range(1, 6):
        filled = "🌟" if i <= current_rating else "⚪"
        star_class = "star" if i <= current_rating else "star empty"
        stars_html += f'<span class="{star_class}" onclick="setRating({character_id}, {i})">{filled}</span>'
    
    stars_html += f"""
        <span class="score-highlight" style="margin-left: 15px;">{current_rating}/5</span>
    </div>
    <script>
        function setRating(charId, rating) {{
            // 更新星星显示
            const stars = document.querySelectorAll('#stars-' + charId + ' .star');
            stars.forEach((star, index) => {{
                if (index < rating) {{
                    star.textContent = '🌟';
                    star.classList.remove('empty');
                }} else {{
                    star.textContent = '⚪';
                    star.classList.add('empty');
                }}
            }});
            
            // 更新评分显示
            const ratingSpan = document.querySelector('#stars-' + charId + ' span:last-child');
            ratingSpan.textContent = rating + '/5';
            
            // 发送评分到Streamlit
            window.parent.postMessage({{
                type: 'streamlit:starRating',
                data: {{ characterId: charId, rating: rating }}
            }}, '*');
        }}
    </script>
    """
    
    return stars_html

# 角色评分界面
def character_rating_interface():
    st.markdown('<div class="main-header">🏠 请回答1988角色评分</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">✨ 双门洞的温暖回忆 · 虎扑风格评分系统 · 实时统计</p>', unsafe_allow_html=True)
    
    # 侧边栏 - 筛选器
    with st.sidebar:
        st.header("🔍 筛选设置")
        
        # 角色类型筛选
        roles = ['全部'] + list(st.session_state.characters_df['role'].unique())
        selected_role = st.selectbox("角色类型", roles)
        
        # 双门洞筛选
        neighborhoods = ['全部'] + list(st.session_state.characters_df['neighborhood'].unique())
        selected_neighborhood = st.selectbox("所在区域", neighborhoods)
        
        # 评分范围
        min_score, max_score = st.slider(
            "评分范围", 
            min_value=0.0, 
            max_value=10.0, 
            value=(8.0, 9.5),
            step=0.1
        )
        
        # 搜索框
        search_term = st.text_input("🔎 搜索角色", placeholder="输入角色名或描述...")
        
        # 应用筛选
        filtered_characters = st.session_state.characters_df.copy()
        if selected_role != '全部':
            filtered_characters = filtered_characters[filtered_characters['role'] == selected_role]
        
        if selected_neighborhood != '全部':
            filtered_characters = filtered_characters[filtered_characters['neighborhood'] == selected_neighborhood]
        
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
        st.subheader("👥 双门洞角色评分区")
        
        # 排序选项
        sort_by = st.selectbox("排序方式", ["综合评分", "评分人数", "角色名称"])
        
        if sort_by == "综合评分":
            ranked_characters = filtered_characters.sort_values('avg_rating', ascending=False)
        elif sort_by == "评分人数":
            ranked_characters = filtered_characters.sort_values('rating_count', ascending=False)
        else:
            ranked_characters = filtered_characters.sort_values('name', ascending=True)
        
        # 角色展示和评分 - 仿照黑暗荣耀排版
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
                    st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #FF8E53; margin-bottom: 8px;'>身份: {character['role']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.4; margin-bottom: 15px;'>{character['description']}</p>", unsafe_allow_html=True)
                    
                    # 双门洞标签
                    st.markdown(f'<span class="meme-tag" style="background-color: #4ECDC4; color: white;">{character["neighborhood"]}</span>', unsafe_allow_html=True)
                    
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
                    stars_html = star_rating_component(character['id'], current_user_rating)
                    components.html(stars_html, height=60)
                    
                    # 显示用户评分（如果有）
                    if current_user_rating > 0:
                        st.markdown(f'<div style="text-align: center; background: #4CAF50; color: white; padding: 8px; border-radius: 10px; margin: 10px 0;">您已评分: {current_user_rating}星</div>', 
                                   unsafe_allow_html=True)
                    
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

# 处理评分事件
def handle_star_rating():
    if st.session_state.get('star_rating_data'):
        data = st.session_state.star_rating_data
        character_id = data['characterId']
        rating = data['rating']
        
        st.session_state.character_ratings[character_id] = rating
        st.session_state.rating_sessions += 1
        
        # 显示评分成功消息
        character_name = st.session_state.characters_df[
            st.session_state.characters_df['id'] == character_id
        ]['name'].iloc[0]
        
        st.success(f"✅ 已为 {character_name} 评分: {rating}星")
        
        # 清除数据
        st.session_state.star_rating_data = None

# AI角色分析界面
def ai_character_analysis():
    st.markdown("## 🔮 AI角色深度解析")
    st.markdown("### 💫 让AI帮你分析双门洞角色的温暖故事")
    
    # 角色选择
    character_names = [char['name'] for _, char in st.session_state.characters_df.iterrows()]
    selected_character = st.selectbox("选择要分析的角色", character_names, key="ai_character")
    
    # 获取角色数据
    character_data = st.session_state.characters_df[st.session_state.characters_df['name'] == selected_character].iloc[0]
    
    # 分析维度选择
    analysis_type = st.selectbox("分析维度", 
                                ["角色性格分析", "剧情作用分析", "演技评价", "观众共鸣点", "角色成长轨迹"])
    
    if st.button("🔮 启动AI分析", type="primary", key="ai_analyze"):
        with st.spinner('AI正在深度解析双门洞的故事...'):
            time.sleep(2)
            
            # 模拟AI分析结果 - 针对《请回答1988》特色
            analysis_results = {
                "角色性格分析": [
                    f"**{selected_character}**的性格温暖而真实",
                    "展现了80年代韩国普通人的日常生活",
                    "角色设定贴近生活，富有亲切感"
                ],
                "剧情作用分析": [
                    f"**{selected_character}**在双门洞故事中起到重要纽带作用",
                    "与其他角色的互动充满温情和幽默",
                    "对展现80年代邻里情谊有重要贡献"
                ],
                "演技评价": [
                    "演员的表演自然流畅，充满生活气息",
                    "情感表达细腻真实，引发强烈共鸣",
                    "角色塑造深入人心，成为经典形象"
                ],
                "观众共鸣点": [
                    "角色经历唤起观众对青春和亲情的回忆",
                    "情感表达真挚动人，引发强烈共情",
                    "角色命运与观众生活经历高度契合"
                ],
                "角色成长轨迹": [
                    "角色经历了从青涩到成熟的成长过程",
                    "性格发展自然合理，符合时代背景",
                    "最终成长与80年代社会变迁紧密相连"
                ]
            }
            
            st.success(f"### 🎯 AI对**{selected_character}**的{analysis_type}")
            
            for point in analysis_results[analysis_type]:
                st.info(f"✨ {point}")
            
            # 显示角色图片
            st.image(character_data['image_url'], width=200, caption=selected_character)
            
            # 显示评分统计
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("当前评分", f"{character_data['avg_rating']}")
            with col2:
                st.metric("评分人数", f"{character_data['rating_count']:,}")
            with col3:
                user_rating = st.session_state.character_ratings.get(character_data['id'], "未评分")
                st.metric("我的评分", user_rating)

# 主函数
def main():
    init_data()
    
    # 监听评分事件
    if st.session_state.get('star_rating_data'):
        handle_star_rating()
    
    # 标签页导航
    tab1, tab2 = st.tabs(["👥 角色评分", "🔮 AI分析"])
    
    with tab1:
        character_rating_interface()
    
    with tab2:
        ai_character_analysis()
    
    # JavaScript监听器
    components.html("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:starRating') {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                data: event.data.data
            }, '*');
        }
    });
    </script>
    """, height=0)

if __name__ == "__main__":
    main()