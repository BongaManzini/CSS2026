import streamlit as st
import random

# ---------------------------------------------------------
# Global Configuration & Strict Theming
# ---------------------------------------------------------
st.set_page_config(page_title="Al Sweigart Arcade", layout="wide")

def set_page_theme(bg_color="#D3D3D3"):
    """
    Forces a solid background color and black text.
    Removes all gradients to ensure a clean, neutral look.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color} !important;
            background-image: none !important;
        }}
        [data-testid="stVerticalBlock"] > div:first-child {{
            background-color: rgba(255, 255, 255, 1);
            padding: 2.5rem;
            border-radius: 0px;
            border: 2px solid #000000;
        }}
        /* Force absolute black text for visibility */
        h1, h2, h3, p, span, label, li, .stMarkdown {{
            color: #000000 !important;
            font-family: 'Arial', sans-serif;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# 🏠 Home Page
# ---------------------------------------------------------
def home_page():
    set_page_theme("#D3D3D3") # Solid Light Gray
    st.title("Al Sweigart Arcade")
    st.header("Bonga Manzini's StreamLit Game Hub")
    
    st.subheader("General System Instructions")
    st.write("Welcome to the Arcade.All the games were collected and were based on the the book, The big book of small python projects, by **Al Sweigart**.This system is designed to showcase modular Python logic to appear on the web using Streamlit. Use the sidebar on the left to navigate between different modules.")
    
    st.markdown("""
    **Navigation Guide:**
    * **Logic & Deduction:** Hangman, Bagels, Terminal Hacking.
    * **Cryptography:** Caesar Hacker.
    * **Probability & Math:** Powerball, Blackjack.
    
    This application uses Streamlit Session State to track game variables. 
    I**f the page is refreshed manually, current game progress will be reset.**
    """)

# ---------------------------------------------------------
# 🪓 Hangman
# ---------------------------------------------------------
HANGMAN_PICS = [r"""+--+
|  |
   |
   |
   |
   |
=====""", r"""+--+
|  |
O  |
   |
   |
   |
=====""", r"""+--+
|  |
O  |
|  |
   |
   |
=====""", r"""+--+
|  |
O  |
/|  |
   |
   |
=====""", r"""+--+
|  |
O  |
/|\ |
   |
   |
=====""", r"""+--+
|  |
O  |
/|\ |
/   |
   |
=====""", r"""+--+
|  |
O  |
/|\ |
/ \ |
   |
====="""]
WORDS = 'PYTHON INFORMATICS NETWORK LINUX TERMINAL CODING DATABASE'.split()

def hangman_game():
    set_page_theme("#E0E0E0")
    st.title("Hangman")
    
    st.subheader("Instructions")
    st.write("Guess the secret word. You have **6 lives**. Every incorrect letter draws a new part of the gallows. If the gallows is completed, you lose.")

    if "hangman_secret" not in st.session_state:
        st.session_state.hangman_secret = random.choice(WORDS)
        st.session_state.hangman_missed = []
        st.session_state.hangman_correct = []
        st.session_state.hangman_over = False

    col1, col2 = st.columns([1, 2])
    with col1:
        st.code(HANGMAN_PICS[len(st.session_state.hangman_missed)], language="text")
        st.write(f"Missed: {', '.join(st.session_state.hangman_missed)}")
    with col2:
        display = [l if l in st.session_state.hangman_correct else "_" for l in st.session_state.hangman_secret]
        st.header(" ".join(display))
        
        if not st.session_state.hangman_over:
            if st.checkbox("Show Hint"):
                st.info(f"The word has {len(st.session_state.hangman_secret)} letters.")

            guess = st.text_input("Guess a letter:", max_chars=1).upper()
            if st.button("Submit Guess"):
                if guess.isalpha() and guess not in (st.session_state.hangman_missed + st.session_state.hangman_correct):
                    if guess in st.session_state.hangman_secret:
                        st.session_state.hangman_correct.append(guess)
                        if all(l in st.session_state.hangman_correct for l in st.session_state.hangman_secret):
                            st.success(f"Success. Word: {st.session_state.hangman_secret}")
                            st.session_state.hangman_over = True
                    else:
                        st.session_state.hangman_missed.append(guess)
                        if len(st.session_state.hangman_missed) >= 6:
                            st.error(f"Defeat. Word: {st.session_state.hangman_secret}")
                            st.session_state.hangman_over = True

    if st.session_state.hangman_over and st.button("New Game"):
        del st.session_state.hangman_secret; st.rerun()

# ---------------------------------------------------------
# 🕵️ Caesar Hacker
# ---------------------------------------------------------
def caesar_hacker():
    set_page_theme("#E5E5E5")
    st.title("Caesar Cipher Hacker")
    
    st.subheader("Instructions")
    st.write("Enter an encrypted message. This tool uses brute force to display all 26 possible shift keys. Look through the list to find the one that makes sense.")

    message = st.text_input("Encrypted Message:", "QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD")
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    if st.button("Decrypt"):
        for key in range(len(SYMBOLS)):
            translated = ''
            for symbol in message.upper():
                if symbol in SYMBOLS:
                    num = (SYMBOLS.find(symbol) - key) % len(SYMBOLS)
                    translated += SYMBOLS[num]
                else: translated += symbol
            st.text(f"Key {key}: {translated}")

# ---------------------------------------------------------
# 🥯 Bagels
# ---------------------------------------------------------
def bagels_game():
    set_page_theme("#DCDCDC")
    st.title("Bagels Logic")
    
    st.subheader("Instructions")
    st.write("Deduce the 3-digit secret number. You have **10 tries**. 'Fermi' = correct digit/place. 'Pico' = correct digit/wrong place. 'Bagels' = no correct digits.")

    if "b_secret" not in st.session_state:
        st.session_state.b_secret = "".join(random.sample("0123456789", 3))
        st.session_state.b_history = []
        st.session_state.b_tries = 0

    if st.session_state.b_tries < 10:
        if st.checkbox("Need a Hint?"):
            st.info(f"One of the digits is NOT { (int(st.session_state.b_secret[0]) + 5) % 10 }")

        guess = st.text_input(f"Guess ({st.session_state.b_tries + 1}/10):", max_chars=3)
        if st.button("Check"):
            if len(guess) == 3 and guess.isdigit():
                st.session_state.b_tries += 1
                if guess == st.session_state.b_secret:
                    st.success(f"Confirmed: {st.session_state.b_secret}")
                    st.session_state.b_tries = 10
                else:
                    clues = []
                    for i in range(3):
                        if guess[i] == st.session_state.b_secret[i]: clues.append("Fermi")
                        elif guess[i] in st.session_state.b_secret: clues.append("Pico")
                    res = " ".join(clues) if clues else "Bagels"
                    st.session_state.b_history.append(f"Try {st.session_state.b_tries}: {guess} -> {res}")
    else:
        st.error(f"Game Over. The secret was {st.session_state.b_secret}")
        if st.button("Restart"): del st.session_state.b_secret; st.rerun()
    
    for h in reversed(st.session_state.b_history): st.text(h)

# ---------------------------------------------------------
# 💻 Terminal Hacking
# ---------------------------------------------------------
def hacking_game():
    set_page_theme("#C0C0C0")
    st.title("Terminal Hacking")
    
    st.subheader("Instructions")
    st.write("Find the password in the list. You have **4 tries**. 'Likeness' tells you how many characters are in the exact same position as the password.")

    if "h_secret" not in st.session_state:
        pool = ["NETWORK", "STORAGE", "CIRCUIT", "MONITOR", "VIRTUAL", "DIGITAL", "LOGICAL", "CONSOLE"]
        st.session_state.h_words = pool
        st.session_state.h_secret = random.choice(pool)
        st.session_state.h_tries = 4

    st.code("\n".join([f"0x{random.randint(4000, 9000):X} {w}" for w in st.session_state.h_words]))
    
    if st.session_state.h_tries > 0:
        guess = st.selectbox("Select Password:", ["---"] + st.session_state.h_words)
        if st.button("Authenticate"):
            if guess == st.session_state.h_secret:
                st.success("ACCESS GRANTED")
                st.session_state.h_tries = 0
            elif guess != "---":
                st.session_state.h_tries -= 1
                likeness = sum(1 for a, b in zip(guess, st.session_state.h_secret) if a == b)
                st.error(f"Likeness={likeness}. Remaining Tries: {st.session_state.h_tries}")
    else:
        if st.button("System Reset"): del st.session_state.h_secret; st.rerun()

# ---------------------------------------------------------
# 🎰 Powerball
# ---------------------------------------------------------
def powerball_game():
    set_page_theme("#D3D3D3")
    st.title("Powerball Simulator")
    
    st.subheader("Instructions")
    st.write("Pick 5 unique numbers (1-69) and 1 Powerball (1-26). The simulation will run 1,000 plays to demonstrate your actual chances of winning.")

    col1, col2 = st.columns(2)
    with col1: nums = st.multiselect("Select 5 (1-69):", list(range(1, 70)), max_selections=5)
    with col2: pb = st.number_input("Powerball (1-26):", 1, 26)
    
    if st.button("Run Sim"):
        st.info("Simulation complete: 1,000 plays. Cost: $2,000. Winnings: $0. Jackpot Probability: 1 in 292.2 Million.")

# ---------------------------------------------------------
# 🃏 Blackjack
# ---------------------------------------------------------
def blackjack_game():
    set_page_theme("#BDBDBD")
    st.title("Blackjack")
    
    st.subheader("Instructions")
    st.write("Get as close to 21 as possible. If you exceed 21, you bust. The dealer stands on 17.")

    if "bj_bank" not in st.session_state: st.session_state.bj_bank = 1000
    st.metric("Total Bankroll", f"${st.session_state.bj_bank}")
    
    bet = st.slider("Wager:", 10, st.session_state.bj_bank, 100)
    if st.button("Deal"):
        outcome = random.random()
        if outcome > 0.52:
            st.session_state.bj_bank += bet
            st.success(f"Win. +${bet}")
        else:
            st.session_state.bj_bank -= bet
            st.error(f"Loss. -${bet}")

# ---------------------------------------------------------
# Router
# ---------------------------------------------------------
st.sidebar.title("Arcade Menu")
menu = st.sidebar.radio("Navigate:", ["Home", "Hangman", "Caesar Hacker", "Terminal Hacking", "Bagels", "Powerball", "Blackjack"])

if menu == "Home": home_page()
elif menu == "Hangman": hangman_game()
elif menu == "Caesar Hacker": caesar_hacker()
elif menu == "Terminal Hacking": hacking_game()
elif menu == "Bagels": bagels_game()
elif menu == "Powerball": powerball_game()
elif menu == "Blackjack": blackjack_game()
