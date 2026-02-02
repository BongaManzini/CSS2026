import streamlit as st
import random

# ---------------------------------------------------------
# Global Configuration & Strict Theming
# ---------------------------------------------------------
st.set_page_config(page_title="Bonga Manzini's Game Hub", layout="wide")

def set_page_theme(bg_color="#D3D3D3"):
    """Forces solid neutral backgrounds and black text for professional visibility."""
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
            border: 2px solid #000000;
        }}
        h1, h2, h3, p, span, label, li, .stMarkdown, .stMetric, .stHeader {{
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
    set_page_theme("#D3D3D3") 
    st.title("Al Sweigart Arcade")
    st.header("Bonga Manzini's StreamLit Game Hub")
    
    st.subheader("General System Instructions")
    st.write("Welcome to the Arcade. All the games were collected and were based on the book, **The Big Book of Small Python Projects**, by **Al Sweigart**. This system is designed to showcase modular Python logic to appear on the web using Streamlit. Use the sidebar on the left to navigate between different modules.")
    
    st.markdown("""
    **Navigation Guide:**
    * **Logic & Deduction:** Hangman, Bagels.
    * **Cryptography:** Caesar Hacker.
    * **Probability & Math:** Blackjack.
    
    This application uses Streamlit Session State to track game variables. 
    **If the page is refreshed manually, current game progress will be reset.**
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

def hangman_game():
    set_page_theme("#E0E0E0")
    st.title("Hangman")
    if "hangman_secret" not in st.session_state:
        st.session_state.hangman_secret = random.choice(['PYTHON', 'INFORMATICS', 'NETWORK', 'LINUX', 'DATABASE', 'TERMINAL'])
        st.session_state.hangman_missed = []
        st.session_state.hangman_correct = []
        st.session_state.hangman_over = False

    if st.button("Show Answer"):
        st.warning(f"Secret Word: {st.session_state.hangman_secret}")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.code(HANGMAN_PICS[len(st.session_state.hangman_missed)], language="text")
    with col2:
        display = [l if l in st.session_state.hangman_correct else "_" for l in st.session_state.hangman_secret]
        st.header(" ".join(display))
        if not st.session_state.hangman_over:
            guess = st.text_input("Guess Letter:", max_chars=1, key="h_input").upper()
            if st.button("Submit"):
                if guess.isalpha() and guess not in (st.session_state.hangman_missed + st.session_state.hangman_correct):
                    if guess in st.session_state.hangman_secret:
                        st.session_state.hangman_correct.append(guess)
                        if all(l in st.session_state.hangman_correct for l in st.session_state.hangman_secret):
                            st.success(f"Success! Word: {st.session_state.hangman_secret}"); st.session_state.hangman_over = True
                    else:
                        st.session_state.hangman_missed.append(guess)
                        if len(st.session_state.hangman_missed) >= 6:
                            st.error(f"Defeat. Word: {st.session_state.hangman_secret}"); st.session_state.hangman_over = True
                st.rerun()
    if st.button("🔄 Reset Game"):
        del st.session_state.hangman_secret; st.rerun()

# ---------------------------------------------------------
# 🕵️ Smart Caesar Hacker
# ---------------------------------------------------------
def caesar_hacker():
    set_page_theme("#E5E5E5")
    st.title("Smart Caesar Hacker")
    message = st.text_input("Encrypted Message:", "QEB NRFZH YOLTK CLU", key="c_input").upper()
    SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    BRAIN = ['THE', 'AND', 'ARE', 'FOR', 'WAS', 'YOU', 'NOT', 'WITH', 'THIS']

    if st.button("Auto-Detect Answer"):
        results = []
        for key in range(26):
            translated = "".join([SYMBOLS[(SYMBOLS.find(s)-key)%26] if s in SYMBOLS else s for s in message])
            score = sum(1 for word in BRAIN if word in translated)
            results.append((score, translated, key))
        results.sort(reverse=True, key=lambda x: x[0])
        st.success(f"Best Match (Key #{results[0][2]}):")
        st.header(results[0][1])
        with st.expander("Show all possibilities"):
            for s, t, k in results: st.text(f"Key {k}: {t}")

# ---------------------------------------------------------
# 🥯 Bagels
# ---------------------------------------------------------
def bagels_game():
    set_page_theme("#DCDCDC")
    st.title("Bagels")
    if "b_secret" not in st.session_state:
        st.session_state.b_secret = "".join(random.sample("0123456789", 3))
        st.session_state.b_history = []
        st.session_state.b_tries = 0

    if st.button("Show Answer"):
        st.warning(f"Secret Number: {st.session_state.b_secret}")
    
    if st.button("Get Smart Hint"):
        wrong_digits = [h.split(":")[0] for h in st.session_state.b_history if "Bagels" in h]
        known_bad = "".join(set("".join(wrong_digits)))
        if known_bad: st.info(f"Analysis: The digits [{known_bad}] are definitely NOT in the secret code.")
        else: st.info("Analysis: No data yet. Make some guesses first.")

    if st.session_state.b_tries < 10:
        guess = st.text_input(f"Guess ({st.session_state.b_tries + 1}/10):", max_chars=3, key="b_input")
        if st.button("Check"):
            if len(guess) == 3 and guess.isdigit():
                st.session_state.b_tries += 1
                if guess == st.session_state.b_secret:
                    st.success(f"Confirmed: {st.session_state.b_secret}"); st.session_state.b_tries = 10
                else:
                    clues = ["Fermi" if guess[i] == st.session_state.b_secret[i] else "Pico" if guess[i] in st.session_state.b_secret else "" for i in range(3)]
                    res = " ".join(filter(None, clues)) or "Bagels"
                    st.session_state.b_history.append(f"{guess}: {res}"); st.rerun()

    for h in reversed(st.session_state.b_history): st.text(h)
    if st.button("🔄 Reset Game"):
        del st.session_state.b_secret; st.rerun()

# ---------------------------------------------------------
# 🃏 Blackjack
# ---------------------------------------------------------
def blackjack_game():
    set_page_theme("#BDBDBD")
    st.title("Blackjack")
    SUITS = {'H': '♥', 'D': '♦', 'S': '♠', 'C': '♣'}
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    
    def calc(hand):
        v, aces = 0, 0
        for r, s in hand:
            if r in 'JQK': v += 10
            elif r == 'A': aces += 1; v += 11
            else: v += int(r)
        while v > 21 and aces: v -= 10; aces -= 1
        return v

    if "bj_deck" not in st.session_state:
        deck = [(r, s) for r in RANKS for s in SUITS.values()]
        random.shuffle(deck)
        st.session_state.bj_deck = deck
        st.session_state.bj_player = [st.session_state.bj_deck.pop(), st.session_state.bj_deck.pop()]
        st.session_state.bj_dealer = [st.session_state.bj_deck.pop(), st.session_state.bj_deck.pop()]
        st.session_state.bj_over = False

    if st.button("Show Answer"):
        st.warning(f"Dealer face-down card: {st.session_state.bj_dealer[0][0]}{st.session_state.bj_dealer[0][1]}")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Player Hand")
        st.header(" ".join([f"{r}{s}" for r, s in st.session_state.bj_player]))
        st.write(f"Value: {calc(st.session_state.bj_player)}")
    with c2:
        st.subheader("Dealer Hand")
        if not st.session_state.bj_over: st.header(f"?? {st.session_state.bj_dealer[1][0]}{st.session_state.bj_dealer[1][1]}")
        else:
            st.header(" ".join([f"{r}{s}" for r, s in st.session_state.bj_dealer]))
            st.write(f"Value: {calc(st.session_state.bj_dealer)}")

    if not st.session_state.bj_over:
        if st.button("Hit"):
            st.session_state.bj_player.append(st.session_state.bj_deck.pop())
            if calc(st.session_state.bj_player) > 21: st.session_state.bj_over = True
            st.rerun()
        if st.button("Stand"):
            dv = calc(st.session_state.bj_dealer)
            while dv < 17: st.session_state.bj_dealer.append(st.session_state.bj_deck.pop()); dv = calc(st.session_state.bj_dealer)
            st.session_state.bj_over = True; st.rerun()
            
    if st.session_state.bj_over:
        pv, dv = calc(st.session_state.bj_player), calc(st.session_state.bj_dealer)
        if pv > 21: st.error("Bust")
        elif dv > 21 or pv > dv: st.success("Win")
        elif pv < dv: st.error("Loss")
        else: st.info("Push")

    if st.button("🔄 Reset Game"):
        del st.session_state.bj_deck; st.rerun()

# ---------------------------------------------------------
# Router
# ---------------------------------------------------------
menu = st.sidebar.radio("Navigation", ["Home", "Hangman", "Caesar Hacker", "Bagels", "Blackjack"])
if menu == "Home": home_page()
elif menu == "Hangman": hangman_game()
elif menu == "Caesar Hacker": caesar_hacker()
elif menu == "Bagels": bagels_game()
elif menu == "Blackjack": blackjack_game()
