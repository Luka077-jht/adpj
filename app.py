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
    page_title="🎬 怪奇物语角色评分 - 虎扑风格",
    page_icon="🔮",
    layout="wide"
)

# 自定义CSS样式 - 保持黑暗荣耀文件的风格
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');
    
    .main-header {
        font-family: 'Noto Sans SC', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #8B0000, #B22222, #DC143C, #FF4500);
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
        border-left: 4px solid #8B0000;
        transition: all 0.3s ease;
    }
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .rating-section {
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
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
        background: linear-gradient(135deg, #8B0000 0%, #B22222 100%);
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
        border: 4px solid #8B0000;
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

# 怪奇物语角色数据
def initialize_characters():
    characters_data = {
        'id': range(1, 9),
        'name': ['Eleven', 'Mike Wheeler', 'Will Byers', 'Dustin Henderson', 'Lucas Sinclair', 'Max Mayfield', 'Steve Harrington', 'Jim Hopper'],
        'role': ['超能力女孩', '团队领袖', '失踪男孩', '科学天才', '怀疑论者', '新成员', '前恶霸', '警长'],
        'description': [
            '拥有超能力的实验体女孩，能够用意念移动物体',
            '团队的核心领导者，勇敢且富有责任感',
            '被颠倒世界抓走的男孩，拥有特殊感知能力',
            '聪明机智的科学爱好者，擅长解决问题',
            '最初对Eleven持怀疑态度，后来成为忠实朋友',
            '勇敢独立的滑板女孩，加入团队后展现价值',
            '从校园恶霸成长为保护孩子们的可靠大哥',
            '霍金斯警长，外表粗犷内心温柔的保护者'
        ],
        'mbti_type': ['INFJ', 'ENFJ', 'ISFP', 'ENTP', 'ISTJ', 'ESTP', 'ESFJ', 'ISTP'],
        'mbti_description': [
            'INFJ（提倡者型）：直觉敏锐，富有同情心，追求深层意义',
            'ENFJ（主人公型）：天生的领导者，富有魅力，关心他人',
            'ISFP（探险家型）：艺术家性格，敏感细腻，活在当下',
            'ENTP（辩论家型）：聪明机智，好奇心强，善于创新',
            'ISTJ（物流师型）：务实可靠，注重规则，忠诚坚定',
            'ESTP（企业家型）：行动派，勇敢果断，适应力强',
            'ESFJ（执政官型）：社交达人，乐于助人，保护欲强',
            'ISTP（鉴赏家型）：实用主义者，冷静理性，行动派'
        ],
        'actor_name': ['Millie Bobby Brown', 'Finn Wolfhard', 'Noah Schnapp', 'Gaten Matarazzo', 'Caleb McLaughlin', 'Sadie Sink', 'Joe Keery', 'David Harbour'],
        'actor_bio': [
            '英国女演员，因饰演Eleven一角而闻名全球，演技备受赞誉',
            '加拿大演员兼音乐人，在怪奇物语中展现出色的表演天赋',
            '美国演员，成功塑造了Will Byers这一复杂角色',
            '美国演员，以独特的表演风格和幽默感深受观众喜爱',
            '美国演员，在剧中展现了出色的舞蹈和表演才能',
            '美国女演员，以勇敢独立的Max形象深入人心',
            '美国演员，成功演绎了Steve从恶霸到英雄的转变',
            '美国资深演员，演技扎实，完美诠释了警长角色'
        ],
        'famous_works': [
            ['怪奇物语', '哥斯拉大战金刚', '福尔摩斯小姐'],
            ['怪奇物语', '小丑回魂', '超能敢死队'],
            ['怪奇物语', '等待安雅', '夏日友晴天'],
            ['怪奇物语', '悲惨世界', '荣誉学生'],
            ['怪奇物语', '具体目标', '新城市'],
            ['怪奇物语', '恐惧街', '鲸鱼'],
            ['怪奇物语', '蜘蛛头', '自由之声'],
            ['怪奇物语', '黑寡妇', '地狱男爵']
        ],
        'avg_rating': [9.4, 8.8, 8.6, 9.1, 8.4, 8.9, 9.2, 9.3],
        'rating_count': [18500, 16200, 14800, 17200, 13500, 15800, 16800, 17500],
        'image_url': [
            # Eleven - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/5/52/Eleven_%28Stranger_Things%29.jpg',
            # Mike Wheeler - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/3/38/An_image_of_the_character_Mike_Wheeler_%28portrayed_by_Finn_Wolfhard%29_from_season_3_of_the_Netflix_series_%22Stranger_Things%22.png',
            # Will Byers - 使用真实的怪奇物语角色图片
            'https://upload.wikimedia.org/wikipedia/en/b/b4/Will_Byers.jpg',
            # Dustin Henderson - 使用真实的怪奇物语角色图片
            'https://static.wikia.nocookie.net/strangerthings8338/images/0/07/Dustin_S4.png/revision/latest/scale-to-width-down/1000?cb=20220531050146',
            # Lucas Sinclair - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbGjQheT203HufCqDZsQ5jqjbXCpHJ4Q02Vc2YfeScm93tfgJiMbn7WosaUYfozhk3a13vt_ppIzBB-p0tBgG7SloCDTMoHE9LGQ9uG-A&s=10',
            # Max Mayfield - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz60kGj9quQAfnP11SEHu_tAzjuOT5a6haneb1gF8SuTZWI95wPVjRyY_g4TvbllLPIIeUoOEEoMhNKDQtMy4QfPfJUeLP7plpTu66Mw&s',
            # Steve Harrington - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRP_FaefNOYhgYDGwKBGYYBIld5mGM3UEx3cP_B65eZnxzbe2xupK5i4TxfF5ouFMET_A4PJ2Ab3s8xYQRr_C-aWdklxbkVXTjXjAmzm6Q&s',
            # Jim Hopper - 使用真实的怪奇物语角色图片
            'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQAGoMcMYdyPH-n55mTSZ5w_2nULnyfe0az2YdwbbzM97SzP3USUnZhwFuJzyavSYfnzmU6mLtibPRwQShKmtg7a8VECZotveAEWSU89ts&s'
        ],
        'actor_photo_url': [
            # Millie Bobby Brown - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Millie_Bobby_Brown_2016.jpg/220px-Millie_Bobby_Brown_2016.jpg',
            # Finn Wolfhard - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Finn_Wolfhard_by_Gage_Skidmore.jpg/220px-Finn_Wolfhard_by_Gage_Skidmore.jpg',
            # Noah Schnapp - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Noah_Schnapp_by_Gage_Skidmore.jpg/220px-Noah_Schnapp_by_Gage_Skidmore.jpg',
            # Gaten Matarazzo - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Gaten_Matarazzo_by_Gage_Skidmore.jpg/220px-Gaten_Matarazzo_by_Gage_Skidmore.jpg',
            # Caleb McLaughlin - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Caleb_McLaughlin_by_Gage_Skidmore.jpg/220px-Caleb_McLaughlin_by_Gage_Skidmore.jpg',
            # Sadie Sink - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Sadie_Sink_by_Gage_Skidmore.jpg/220px-Sadie_Sink_by_Gage_Skidmore.jpg',
            # Joe Keery - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Joe_Keery_by_Gage_Skidmore.jpg/220px-Joe_Keery_by_Gage_Skidmore.jpg',
            # David Harbour - 使用真实的演员照片
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/David_Harbour_by_Gage_Skidmore.jpg/220px-David_Harbour_by_Gage_Skidmore.jpg'
        ]
    }
    return pd.DataFrame(characters_data)

# 角色相关的梗和热评
def get_character_memes(character_id):
    memes_dict = {
        1: ["超能力女孩", "蛋挞爱好者", "超能力觉醒", "实验室实验体"],
        2: ["团队领袖", "勇敢担当", "Eleven的守护者", "自行车男孩"],
        3: ["失踪男孩", "颠倒世界幸存者", "敏感感知", "Will the Wise"],
        4: ["科学天才", "牙套男孩", "机智幽默", "Dusty-bun"],
        5: ["怀疑论者", "弓箭手", "忠诚朋友", "Lucas the Skeptic"],
        6: ["滑板女孩", "新成员", "勇敢独立", "Mad Max"],
        7: ["前恶霸", "可靠大哥", "发胶男孩", "Steve the Babysitter"],
        8: ["霍金斯警长", "父亲形象", "硬汉柔情", "Hopper the Protector"]
    }
    
    comments_dict = {
        1: ["Eleven的超能力太酷了！每次看她用超能力都热血沸腾", "Millie的演技真的绝了，把Eleven的复杂情感演绎得淋漓尽致"],
        2: ["Mike真的是个很棒的领导者，对朋友超级忠诚", "Finn把Mike的成长过程演得太真实了"],
        3: ["Will的经历太让人心疼了，Noah的表演很有感染力", "Will the Wise这个称号真的很适合他"],
        4: ["Dustin绝对是剧中的搞笑担当，每次出场都让人开心", "Gaten的表演太有特色了，把Dustin演活了"],
        5: ["Lucas从怀疑到信任的转变很真实，Caleb的表演很到位", "弓箭手Lucas在关键时刻总是很可靠"],
        6: ["Max的加入让团队更有活力，Sadie把Max的坚强演得很好", "Running Up That Hill那段真的太经典了"],
        7: ["Steve的成长线太棒了，从恶霸到保护者，Joe演得太好了", "发胶男孩现在是最可靠的大哥"],
        8: ["Hopper外表粗犷内心温柔，David的演技太扎实了", "警长和Eleven的父女情真的很感人"]
    }
    
    return memes_dict.get(character_id, []), comments_dict.get(character_id, [])

# 五星评分系统（使用Streamlit原生组件）
def star_rating_component(character_id, current_rating=0):
    # 使用Streamlit的selectbox模拟五星评分
    rating_options = ["⭐", "⭐⭐", "⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐⭐"]
    selected_rating = st.selectbox(
        "请评分：",
        rating_options,
        index=current_rating-1 if current_rating > 0 else 0,
        key=f"rating_select_{character_id}"
    )
    
    # 显示当前评分
    rating_value = rating_options.index(selected_rating) + 1
    st.write(f"当前评分：{rating_value}星")
    
    return rating_value

# 显示角色信息
def display_character_info(character):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 显示角色图片
        st.image(character['image_url'], use_container_width=False)
    
    with col2:
        st.markdown(f"### {character['name']} - {character['role']}")
        st.markdown(f"**角色描述：** {character['description']}")
        
        col3, col4 = st.columns(2)
        with col3:
            st.markdown(f"**MBTI类型：** {character['mbti_type']}")
            st.markdown(f"<div style='font-size: 0.9rem; color: #666;'>{character['mbti_description']}</div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"**平均评分：** <span class='score-highlight'>{character['avg_rating']}</span>", unsafe_allow_html=True)
            st.markdown(f"**评分人数：** {character['rating_count']:,}")

# 显示演员信息
def display_actor_info(character):
    st.markdown("### 🎭 演员信息")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(character['actor_photo_url'], use_container_width=False)
    
    with col2:
        st.markdown(f"**演员姓名：** {character['actor_name']}")
        st.markdown(f"**演员简介：** {character['actor_bio']}")
        
        st.markdown("**代表作品：**")
        works_grid = ""
        for work in character['famous_works']:
            works_grid += f"<div class='work-item'>{work}</div>"
        st.markdown(f"<div class='works-grid'>{works_grid}</div>", unsafe_allow_html=True)

# 显示梗和热评
def display_memes_and_comments(character_id):
    memes, comments = get_character_memes(character_id)
    
    if memes:
        st.markdown("### 🔥 角色梗")
        meme_tags = ""
        for meme in memes:
            meme_tags += f"<span class='meme-tag'>{meme}</span>"
        st.markdown(f"<div>{meme_tags}</div>", unsafe_allow_html=True)
    
    if comments:
        st.markdown("### 💬 热评")
        for comment in comments:
            st.markdown(f"<div class='hot-comment'>{comment}</div>", unsafe_allow_html=True)

# 主应用
def main():
    init_data()
    
    # 页面标题
    st.markdown("<h1 class='main-header'>🎬 怪奇物语角色评分系统</h1>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>虎扑风格 | 角色深度分析 | 演员信息 | 热评梗概</div>", unsafe_allow_html=True)
    
    # 统计信息
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>🎯 评分系统</h3>
            <p>专业五星评分<br>实时数据统计</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <h3>📊 数据分析</h3>
            <p>MBTI性格分析<br>角色深度解析</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <h3>🎭 演员信息</h3>
            <p>完整演员资料<br>代表作品展示</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 角色选择
    st.markdown("### 🔮 选择角色")
    characters_df = st.session_state.characters_df
    
    # 创建角色选择器
    character_names = characters_df['name'].tolist()
    selected_character_name = st.selectbox("请选择要评分的角色：", character_names)
    
    # 获取选中的角色数据
    selected_character = characters_df[characters_df['name'] == selected_character_name].iloc[0]
    character_id = selected_character['id']
    
    # 显示角色信息
    st.markdown("<div class='character-card'>", unsafe_allow_html=True)
    display_character_info(selected_character)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 评分区域
    st.markdown("<div class='rating-section'>", unsafe_allow_html=True)
    st.markdown("### ⭐ 角色评分")
    
    # 获取当前评分（如果有）
    current_rating = st.session_state.character_ratings.get(character_id, 0)
    
    # 显示评分组件
    new_rating = star_rating_component(character_id, current_rating)
    
    # 提交评分按钮
    if st.button("提交评分", key=f"submit_{character_id}"):
        if new_rating > 0:
            st.session_state.character_ratings[character_id] = new_rating
            st.session_state.rating_sessions += 1
            st.success(f"✅ 已为 {selected_character_name} 评分 {new_rating} 星！")
            time.sleep(1)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 显示演员信息
    display_actor_info(selected_character)
    
    # 显示梗和热评
    display_memes_and_comments(character_id)
    
    # 显示统计信息
    if st.session_state.rating_sessions > 0:
        st.markdown("### 📈 评分统计")
        rated_characters = len(st.session_state.character_ratings)
        total_sessions = st.session_state.rating_sessions
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("已评分角色", f"{rated_characters}/8")
        with col2:
            st.metric("评分次数", total_sessions)

if __name__ == "__main__":
    main()