import streamlit as st
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Bridge Hand Calculator-Improve your hand counting skills",
    page_icon="🃏",
    layout="centered"
)

# Initialize session state
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'round_number' not in st.session_state:
    st.session_state.round_number = 0
if 'total_rounds' not in st.session_state:
    st.session_state.total_rounds = 10
if 'scores' not in st.session_state:
    st.session_state.scores = []
if 'current_hand' not in st.session_state:
    st.session_state.current_hand = None
if 'hidden_suit' not in st.session_state:
    st.session_state.hidden_suit = None
if 'round_start_time' not in st.session_state:
    st.session_state.round_start_time = None
if 'waiting_for_answer' not in st.session_state:
    st.session_state.waiting_for_answer = False
if 'show_result' not in st.session_state:
    st.session_state.show_result = False
if 'last_answer' not in st.session_state:
    st.session_state.last_answer = None
if 'last_time' not in st.session_state:
    st.session_state.last_time = None
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = None

def generate_hand():
    """Generate a random bridge hand with constraints"""
    suits = ['spades', 'hearts', 'diamonds', 'clubs']
    
    # First, generate a complete realistic bridge hand (4 suits totaling 13)
    remaining_cards = 13
    hand = {}
    
    # Randomly distribute cards among all 4 suits
    for i, suit in enumerate(suits):
        if i == len(suits) - 1:  # Last suit gets remaining cards
            hand[suit] = remaining_cards
        else:
            # Random number between 0 and remaining cards
            max_cards = min(13, remaining_cards)
            cards = random.randint(0, max_cards)
            hand[suit] = cards
            remaining_cards -= cards
    
    # Now choose which suit to hide
    hidden_suit = random.choice(suits)
    
    return hand, hidden_suit

def get_suit_symbol(suit):
    """Get the symbol for each suit"""
    symbols = {
        'spades': '♠️',
        'hearts': '♥️', 
        'diamonds': '♦️',
        'clubs': '♣️'
    }
    return symbols[suit]

def start_new_round():
    """Start a new round"""
    st.session_state.round_number += 1
    st.session_state.current_hand, st.session_state.hidden_suit = generate_hand()
    st.session_state.round_start_time = time.time()
    st.session_state.waiting_for_answer = True
    st.session_state.show_result = False
    st.session_state.last_answer = None

def calculate_score(time_taken):
    """Calculate score based on time taken"""
    return max(0, 100 - int(time_taken))

def reset_game():
    """Reset the entire game"""
    st.session_state.game_started = False
    st.session_state.round_number = 0
    st.session_state.scores = []
    st.session_state.current_hand = None
    st.session_state.hidden_suit = None
    st.session_state.round_start_time = None
    st.session_state.waiting_for_answer = False
    st.session_state.show_result = False
    st.session_state.last_answer = None
    st.session_state.last_time = None
    st.session_state.correct_answer = None

# Main UI
st.title("🃏 Bridge Hand Calculator")
st.markdown("Calculate the missing suit in a bridge hand and do it fast! Each hand has exactly 13 cards.")

# Game setup
if not st.session_state.game_started:
    st.markdown("### Game Setup")
    
    col1, col2 = st.columns(2)
    with col1:
        rounds = st.number_input("Number of rounds:", min_value=1, max_value=50, value=10)
        st.session_state.total_rounds = rounds
    
    with col2:
        if st.button("Start Game", type="primary"):
            st.session_state.game_started = True
            start_new_round()
            st.rerun()

else:
    # Game in progress
    st.markdown(f"### Round {st.session_state.round_number} of {st.session_state.total_rounds}")
    
    # Score display
    if st.session_state.scores:
        total_score = sum(st.session_state.scores)
        average_score = total_score / len(st.session_state.scores)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Score", f"{total_score}")
        with col2:
            st.metric("Average Score", f"{average_score:.1f}")
        with col3:
            st.metric("Rounds Completed", f"{len(st.session_state.scores)}")
    
    st.markdown("---")
    
    if st.session_state.waiting_for_answer and st.session_state.current_hand:
        # Display the current hand
        st.markdown("### Current Hand")
        
        # Create 4 columns for the suits
        cols = st.columns(4)
        suits = ['spades', 'hearts', 'diamonds', 'clubs']
        
        user_answer = None
        
        for i, suit in enumerate(suits):
            with cols[i]:
                symbol = get_suit_symbol(suit)
                st.markdown(f"<div style='text-align: center; font-size: 2em;'>{symbol}</div>", 
                           unsafe_allow_html=True)
                
                if suit == st.session_state.hidden_suit:
                    # This is the hidden suit - show input box
                    user_answer = st.number_input(
                        f"{suit.title()}",
                        min_value=0,
                        max_value=13,
                        value=0,
                        key=f"input_{suit}",
                        label_visibility="collapsed"
                    )
                else:
                    # Show the number of cards
                    cards = st.session_state.current_hand[suit]
                    st.markdown(f"<div style='text-align: center; font-size: 2em; font-weight: bold; background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;'>{cards}</div>", 
                               unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Submit button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Submit Answer", type="primary"):
                if user_answer is not None:
                    # Calculate time taken
                    time_taken = time.time() - st.session_state.round_start_time
                    
                    # Check if answer is correct
                    correct_answer = st.session_state.current_hand[st.session_state.hidden_suit]
                    is_correct = user_answer == correct_answer
                    
                    # Calculate score
                    if is_correct:
                        score = calculate_score(time_taken)
                        st.session_state.scores.append(score)
                    else:
                        st.session_state.scores.append(0)
                    
                    # Store results for display
                    st.session_state.last_answer = user_answer
                    st.session_state.correct_answer = correct_answer
                    st.session_state.last_time = time_taken
                    st.session_state.show_result = True
                    st.session_state.waiting_for_answer = False
                    
                    st.rerun()
    
    elif st.session_state.show_result:
        # Show result of the last round
        st.markdown("### Round Result")
        
        is_correct = st.session_state.last_answer == st.session_state.correct_answer
        
        if is_correct:
            st.success(f"✅ Correct! You answered {st.session_state.last_answer}")
            score = calculate_score(st.session_state.last_time)
            st.info(f"Time taken: {st.session_state.last_time:.1f} seconds | Score: {score} points")
        else:
            st.error(f"❌ Wrong! You answered {st.session_state.last_answer}, correct answer was {st.session_state.correct_answer}")
            st.info(f"Time taken: {st.session_state.last_time:.1f} seconds | Score: 0 points")
        
        # Show the complete hand for reference
        st.markdown("**Complete hand:**")
        hand_display = ""
        suits = ['spades', 'hearts', 'diamonds', 'clubs']
        for suit in suits:
            symbol = get_suit_symbol(suit)
            cards = st.session_state.current_hand[suit]
            hand_display += f"{symbol} {cards}  "
        st.markdown(hand_display)
        
        st.markdown("---")
        
        # Next round or finish game
        if st.session_state.round_number < st.session_state.total_rounds:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("Next Round", type="primary"):
                    start_new_round()
                    st.rerun()
        else:
            # Game finished
            st.markdown("### 🎉 Game Complete!")
            
            total_score = sum(st.session_state.scores)
            average_score = total_score / len(st.session_state.scores)
            
            st.balloons()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Final Total Score", f"{total_score}")
            with col2:
                st.metric("Final Average Score", f"{average_score:.1f}")
            
            # Show score breakdown
            st.markdown("**Round-by-round scores:**")
            score_text = " | ".join([f"R{i+1}: {score}" for i, score in enumerate(st.session_state.scores)])
            st.text(score_text)
    
    # Reset game button
    st.markdown("---")
    if st.button("Reset Game"):
        reset_game()
        st.rerun()

# Instructions
with st.expander("How to Play"):
    st.markdown("""
    **Objective:** Calculate how many cards are in the missing suit to complete a bridge hand of exactly 13 cards.
    
    **Rules:**
    - Each suit can have 0-13 cards
    - Total cards in all 4 suits must equal exactly 13
    - The faster you answer correctly, the higher your score
    
    **Scoring:**
    - Round Score = 100 - seconds taken (minimum 0)
    - Wrong answers = 0 points
    - Game Score = sum of all round scores
    - Average Score = Game Score ÷ Number of rounds
    
    **Example:** If you see ♠️6, ♥️5, ♦️1, then ♣️ = 13 - (6+5+1) = 1
    """)
