import streamlit as st
import json
import random
from pathlib import Path
from streamlit_extras.let_it_rain import rain

# Page config
st.set_page_config(
    page_title="Milano Di Rouge Fit Quiz",
    page_icon="👖",
    layout="centered"
)

# Load quiz data
@st.cache_data
def load_quiz_data():
    with open('data/quiz_data.json', 'r') as f:
        return json.load(f)

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.game_over = False

def start_game():
    """Initialize a new game with no repeating fits"""
    quiz_data = load_quiz_data()
    all_fits = quiz_data['fits']
    
    # Select 3 random fits for this game (no repeats)
    selected_fits = random.sample(all_fits, 3)
    
    # For each fit, create wrong answer options (ensuring no repeats across the game)
    questions = []
    used_as_wrong_answer = set()
    
    for fit in selected_fits:
        available_fits = [
            f for f in all_fits 
            if f['name'] != fit['name'] and f['name'] not in used_as_wrong_answer
            and f['name'] not in [sf['name'] for sf in selected_fits]
        ]
        
        wrong_answers = random.sample(available_fits, min(2, len(available_fits)))
        
        for wa in wrong_answers:
            used_as_wrong_answer.add(wa['name'])
        
        options = [fit['name']] + [f['name'] for f in wrong_answers]
        random.shuffle(options)
        
        questions.append({
            'fit': fit,
            'options': options,
            'correct_answer': fit['name']
        })
    
    st.session_state.questions = questions
    st.session_state.game_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.game_over = False
    st.rerun()

def submit_answer(selected_option):
    """Process the selected answer"""
    current_q = st.session_state.questions[st.session_state.current_question]
    is_correct = selected_option == current_q['correct_answer']
    
    st.session_state.answers.append({
        'question': current_q,
        'selected': selected_option,
        'correct': is_correct
    })
    
    if is_correct:
        st.session_state.score += 1
    
    if st.session_state.current_question < 2:
        st.session_state.current_question += 1
    else:
        st.session_state.game_over = True
    
    st.rerun()

def reset_game():
    """Reset for a new game"""
    st.session_state.game_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.game_over = False
    st.rerun()

# Custom CSS - Editorial Style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500&display=swap');
    
    .main {
        background-color: #E8E8E8;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 0.5rem;
        line-height: 1.1;
        letter-spacing: -0.02em;
        color: #1a1a1a;
        text-transform: uppercase;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        text-align: center;
        color: #1a1a1a;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.05em;
    }
    
    .personality-box {
        background-color: #ffffff;
        padding: 1rem 1.2rem;
        border-radius: 0px;
        margin: 0.5rem 0 0.8rem 0;
        font-family: 'Playfair Display', serif;
        font-size: 0.9rem;
        line-height: 1.6;
        color: #1a1a1a;
        border-left: 5px solid #1a1a1a;
        font-weight: 400;
        font-style: italic;
    }
    
    .personality-box::before {
        content: '"';
        font-size: 1.8rem;
        font-family: 'Playfair Display', serif;
        color: #1a1a1a;
        line-height: 0;
        margin-right: 0.3rem;
        font-style: normal;
        float: left;
    }
    
    .personality-box::after {
        content: '"';
        font-size: 1.8rem;
        font-family: 'Playfair Display', serif;
        color: #1a1a1a;
        line-height: 0;
        margin-left: 0.3rem;
        font-style: normal;
    }
    
    .progress-text {
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #1a1a1a;
        margin-bottom: 0.3rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 500;
    }
    
    .score-display {
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 2rem 0;
    }
    
    .discount-code-container {
        background-color: #1a1a1a;
        color: #E8E8E8;
        padding: 3rem 2rem;
        border-radius: 0px;
        text-align: center;
        margin: 3rem 0;
    }
    
    .discount-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        font-weight: 300;
    }
    
    .discount-code {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: 0.2em;
        margin: 1rem 0;
    }
    
    .section-header {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        color: #1a1a1a;
    }
    
    .fit-name {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin: 0.5rem 0 0.6rem 0;
        color: #1a1a1a;
    }
    
    .image-caption {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #666;
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Button styling - compact */
    .stButton > button {
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border-radius: 0px;
        border: 2px solid #1a1a1a;
        background-color: transparent;
        color: #1a1a1a;
        padding: 0.55rem 1rem !important;
        transition: all 0.3s ease;
        width: 100%;
        font-size: 0.85rem !important;
    }
    
    .stButton > button:hover {
        background-color: #1a1a1a;
        color: #E8E8E8;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #1a1a1a;
        color: #E8E8E8;
        border: 2px solid #1a1a1a;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: transparent;
        color: #1a1a1a;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #1a1a1a;
    }

    /* Tighten up default streamlit spacing */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main App Logic
if not st.session_state.game_started:
    # WELCOME SCREEN
    st.markdown('<div class="main-title">Denim That<br/>Fits Like<br/>A Dream</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Premium stretch, perfect washes, and a fit that feels custom.<br/>Match 3 denim styles and unlock your exclusive discount.</div>', unsafe_allow_html=True)
    
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    st.markdown("##### How It Works", unsafe_allow_html=True)
    st.markdown("""
    **1.** View a denim personality and image  
    **2.** Guess which Milano Di Rouge fit it is  
    **3.** Get all 3 correct to unlock your discount code
    """)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Quiz", use_container_width=True, type="primary"):
            start_game()

elif st.session_state.game_over:
    # WIN/LOSE SCREEN
    perfect_score = st.session_state.score == 3
    
    if perfect_score:
        rain(
            emoji="✨",
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )
        st.toast("🎉 Perfect Score!", icon="✨")

        st.markdown('<div class="main-title">Perfect<br/>Score</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-display">{st.session_state.score}/3 Correct</div>', unsafe_allow_html=True)
        
        quiz_data = load_quiz_data()
        st.markdown(f'''
        <div class="discount-code-container">
            <div class="discount-label">Your Exclusive Discount Code</div>
            <div class="discount-code">{quiz_data["discount_code"]}</div>
            <div class="discount-label">10% Off Your Order</div>
        </div>
        ''', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Copy Code", use_container_width=True):
                st.code(quiz_data["discount_code"], language=None)
                st.success("Code copied! Ready to paste at checkout.")
        with col2:
            st.link_button("Shop Milano Di Rouge", quiz_data["shop_url"], use_container_width=True, type="primary")
        
    else:
        st.markdown('<div class="main-title">Almost<br/>There</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="score-display">{st.session_state.score}/3 Correct</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">Let\'s Review</div>', unsafe_allow_html=True)
        
        for i, answer in enumerate(st.session_state.answers):
            fit_name = answer['question']['fit']['name']
            if not answer['correct']:
                st.markdown(f"""
                **Question {i+1}**  
                You guessed: **{answer['selected']}**  
                Correct answer: **{fit_name}** ✓
                
                *{answer['question']['fit']['personality']}*
                """)
                st.markdown("---")
    
    st.markdown("<br/>", unsafe_allow_html=True)
    quiz_data = load_quiz_data()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Try Again", use_container_width=True, type="primary"):
            reset_game()
    with col2:
        st.link_button("Shop Anyway", quiz_data["shop_url"], use_container_width=True)

else:
    # GAME SCREEN - SIDE BY SIDE LAYOUT
    current_q = st.session_state.questions[st.session_state.current_question]
    
    # Progress indicator
    progress = (st.session_state.current_question + 1) / 3
    st.progress(progress)
    st.markdown(f'<div class="progress-text">Question {st.session_state.current_question + 1} of 3</div>', unsafe_allow_html=True)
    
    # Score tracker
    score_icons = "✓ " * st.session_state.score + "○ " * (st.session_state.current_question - st.session_state.score)
    if score_icons.strip():
        st.markdown(f"<p style='text-align: center; margin: 0.2rem 0;'><strong>{score_icons}</strong></p>", unsafe_allow_html=True)
    
    # Side-by-side layout - image bigger
    col_img, col_content = st.columns([1.2, 1])
    
    with col_img:
        st.image(current_q['fit'].get('image_url', 'https://via.placeholder.com/400x600/E8E8E8/1a1a1a?text=' + current_q['fit']['name']), 
                 use_container_width=True)
        if current_q['fit'].get('caption'):
            st.markdown(f'<div class="image-caption">{current_q["fit"]["caption"]}</div>', unsafe_allow_html=True)
    
    with col_content:
        # Personality description
        st.markdown(f'<div class="personality-box">{current_q["fit"]["personality"]}</div>', 
                    unsafe_allow_html=True)
        
        st.markdown('<div class="fit-name">Who am I?</div>', unsafe_allow_html=True)
        
        # Answer options
        for option in current_q['options']:
            if st.button(option, use_container_width=True, key=f"option_{option}"):
                submit_answer(option)

