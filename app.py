import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="리센느 가사 맞추기 게임", page_icon="🎶", layout="centered")

# 1. 리센느(RESCENE) 가사 문제 데이터 (가사 힌트 : 정답 곡명)
QUIZ_DATA = [
    {"lyric": "네 맘을 훔칠 러브 어택, 멈출 수 없는 이 떨림...", "answer": "LOVE ATTACK"},
    {"lyric": "어제와는 달라진 눈빛, 더 눈부시게 Glow Up...", "answer": "Glow Up"},
    {"lyric": "빙글빙글 돌아가는 YoYo처럼 네 주위를 맴돌아...", "answer": "YoYo"},
    {"lyric": "튕겨 오르는 마음, 어디로 튈지 모르는 Pinball...", "answer": "Pinball"},
    {"lyric": "당당하게 걸어가 UhUh, 시선을 모두 집중시켜...", "answer": "UhUh"},
    {"lyric": "너와 함께라면 어디든 좋아, 영원히 Stay With me...", "answer": "With"},
    {"lyric": "두근거리는 심장 소리, 너에게 빠진 Heart Drop...", "answer": "Heart Drop"},
    {"lyric": "마치 꿈에서 본 것 같아, 선명하게 떠오르는 Deja Vu...", "answer": "Deja Vu"}
]

ALL_SONGS = [q["answer"] for q in QUIZ_DATA]

# 2. 멤버별 랜덤 멘트 데이터
MEMBERS = ["원이", "리브", "미나미", "메이", "제나"]

WIN_COMMENTS = [
    "우와 대박! 역시 우리 찐팬이네요! ✨",
    "이걸 바로 맞힌다고요? 리센느 마스터 인정합니다 💖",
    "정답! 오늘 감이 엄청 좋으신데요? 👏",
    "완벽해요! 다음 문제도 거뜬하겠죠? 🌸"
]

LOSE_COMMENTS = [
    "앗 아깝다~ 노래 한 번 더 듣고 오셔야겠어요! 😜",
    "땡! 다음 판엔 제가 힌트 드릴까요? 👀",
    "삐빅! 아쉽지만 하트가 하나 깎였습니다 💔",
    "조금 더 분발해 주세요! 파이팅 💪"
]

# 3. 게임 상태(세션) 초기화 함수
def init_game():
    st.session_state.lives = 3
    st.session_state.score = 0
    st.session_state.combo = 0
    st.session_state.last_result = None
    st.session_state.last_msg = ""
    next_question()

def next_question():
    q = random.choice(QUIZ_DATA)
    st.session_state.current_q = q
    # 정답 1개 + 오답 3개 랜덤 추출 후 섞기
    wrong_choices = random.sample([s for s in ALL_SONGS if s != q["answer"]], 3)
    options = wrong_choices + [q["answer"]]
    random.shuffle(options)
    st.session_state.options = options

# 첫 실행 시 초기화
if "lives" not in st.session_state:
    init_game()

# --- UI 화면 구성 ---
st.title("🎶 리센느(RESCENE) 가사 맞추기 게임")
st.write("가사 한 소절을 보고 어떤 노래인지 맞혀보세요! 하트 3개가 다 깎이면 게임 오버입니다.")
st.divider()

# 상단 전적판 (목숨, 점수, 콤보)
col1, col2, col3 = st.columns(3)
with col1:
    hearts = "❤️" * st.session_state.lives + "🖤" * (3 - st.session_state.lives)
    st.metric(label="남은 목숨", value=hearts)
with col2:
    st.metric(label="현재 점수", value=f"{st.session_state.score} 점")
with col3:
    st.metric(label="연속 콤보", value=f"🔥 {st.session_state.combo} 콤보")

st.divider()

# 직전 문제 결과 및 멤버 멘트 출력
if st.session_state.last_result == "win":
    st.success(st.session_state.last_msg)
elif st.session_state.last_result == "lose":
    st.error(st.session_state.last_msg)

# 게임 오버 처리 vs 문제 출제
if st.session_state.lives <= 0:
    st.warning(f"💀 게임 오버! 최종 점수는 **{st.session_state.score}점**입니다.")
    if st.button("🔄 처음부터 다시 도전하기", use_container_width=True):
        init_game()
        st.rerun()
else:
    # 문제 카드 표시
    st.info(f"🎵 **문제 가사:**\n\n### \"{st.session_state.current_q['lyric']}\"")
    st.write("👇 아래 4개 중 정답을 선택하세요!")

    # 객관식 버튼 2x2 배치
    btn_cols = st.columns(2)
    for idx, option in enumerate(st.session_state.options):
        with btn_cols[idx % 2]:
            if st.button(f"🎧 {option}", key=f"opt_{idx}", use_container_width=True):
                member = random.choice(MEMBERS)
                correct_ans = st.session_state.current_q["answer"]
                
                if option == correct_ans:
                    st.session_state.score += 10
                    st.session_state.combo += 1
                    st.session_state.last_result = "win"
                    comment = random.choice(WIN_COMMENTS)
                    st.session_state.last_msg = f"🎉 정답입니다! ({correct_ans}) | **{member}:** \"{comment}\""
                    st.balloons()
                else:
                    st.session_state.lives -= 1
                    st.session_state.combo = 0
                    st.session_state.last_result = "lose"
                    comment = random.choice(LOSE_COMMENTS)
                    st.session_state.last_msg = f"❌ 틀렸습니다! 정답은 **{correct_ans}**였어요. | **{member}:** \"{comment}\""
                
                next_question()
                st.rerun()
