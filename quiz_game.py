import json
import os
import random
from datetime import datetime

from data import DEFAULT_QUIZZES
from quiz import Quiz

# state.json은 항상 이 파일(quiz_game.py)과 같은 디렉터리(프로젝트 루트)에 둔다.
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체 흐름(메뉴, 진행, 파일 저장/불러오기)을 관리하는 클래스."""

    MENU_MIN = 1
    MENU_MAX = 6
    HINT_PENALTY = 5  # 힌트 1회 사용 시 문제당 차감되는 점수

    def __init__(self):
        self.quizzes = []      # 등록된 Quiz 객체 목록
        self.best_score = None  # 최고 점수 기록 (아직 없으면 None)
        self.history = []       # 매 회차 게임 기록 목록
        self.load_state()       # state.json 또는 기본 데이터로 위 속성들을 채운다

    # ---------- 메뉴 ----------
    def print_menu(self):
        """메인 메뉴를 화면에 출력한다."""
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 퀴즈 삭제")
        print("6. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        """메뉴 번호(1~6)를 입력받는다. 검증은 _get_int_input에 위임한다."""
        return self._get_int_input("선택: ", self.MENU_MIN, self.MENU_MAX)

    def _get_int_input(self, prompt, min_value, max_value):
        """숫자 입력을 받는 공통 헬퍼.

        아래 4가지 케이스를 모두 통과할 때까지 같은 prompt로 재입력을 받는다.
        1) 공백 제거  2) 빈 입력  3) 숫자 변환 실패  4) 허용 범위(min~max) 초과
        입력 스트림이 끊기면(EOFError) _handle_eof()로 안전 종료한다.
        """
        while True:
            try:
                raw = input(prompt)
            except EOFError:
                self._handle_eof()
            text = raw.strip()  # 1) 앞뒤 공백 제거

            if text == "":  # 2) 빈 입력
                print(f"⚠️ 입력이 없습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            # "-"를 뗀 나머지가 전부 숫자인지 검사 (음수 형태까지 우선 허용하고 범위에서 걸러냄)
            if not text.lstrip("-").isdigit():  # 3) 숫자 변환 실패
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            value = int(text)
            if value < min_value or value > max_value:  # 4) 허용 범위 초과
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

    def run(self):
        """메인 루프: 메뉴를 반복 출력하고 선택에 따라 각 기능을 호출한다."""
        best_text = "없음" if self.best_score is None else f"{self.best_score['score']}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")

        while True:
            self.print_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.delete_quiz()
            elif choice == 6:
                self.save_state()
                print("게임을 종료합니다. 안녕히 가세요!")
                break
            else:
                print(f"[{choice}] 기능은 아직 구현되지 않았습니다.")

    # ---------- 퀴즈 풀기 ----------
    def play_quiz(self):
        """퀴즈를 몇 문제 풀지 정하고, 무작위로 뽑아 출제한 뒤 채점 결과를 보여준다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        available = len(self.quizzes)
        if available == 1:
            total = 1  # 퀴즈가 1개뿐이면 몇 문제를 풀지 물어볼 필요가 없다
        else:
            total = self._get_int_input(
                f"\n몇 문제를 풀까요? (1-{available}): ", 1, available
            )

        # 중복 없이 무작위로 total개를 뽑는다 → 매번 문제 순서/조합이 달라짐(랜덤 출제 보너스)
        quizzes_to_play = random.sample(self.quizzes, total)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제, 힌트 보기: 0 입력)")
        correct_count = 0
        hints_used = 0

        for index, quiz in enumerate(quizzes_to_play, start=1):
            print("-" * 40)
            correct, used_hint = self._play_single_quiz(quiz, index)
            if correct:
                correct_count += 1
            if used_hint:
                hints_used += 1

        # 점수 계산: 정답률(%) 을 기본 점수로 하고, 힌트 사용 문제 수만큼 감점(0점 밑으로는 안 내려감)
        raw_score = round(correct_count / total * 100)
        score = max(0, raw_score - hints_used * self.HINT_PENALTY)

        print("\n" + "=" * 40)
        result_line = f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점"
        result_line += f", 힌트 {hints_used}회 사용)" if hints_used else ")"
        print(result_line)
        if self.best_score is None or score > self.best_score["score"]:
            self.best_score = {"score": score, "correct": correct_count, "total": total}
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)

        self._record_history(total, correct_count, score, hints_used)
        self.save_state()  # 결과를 즉시 state.json에 반영

    def _play_single_quiz(self, quiz, index):
        """문제 하나를 출제하고 정답을 받아 채점한다. (correct, used_hint) 튜플을 반환."""
        quiz.display(index)
        used_hint = False
        while True:
            answer = self._get_int_input(
                "\n정답 입력 (힌트 보기: 0): ", 0, len(quiz.choices)
            )
            if answer == 0:  # 0을 입력하면 힌트를 보여주고 같은 문제를 다시 묻는다
                quiz.show_hint()
                used_hint = True
                continue
            break

        correct = quiz.is_correct(answer)
        if correct:
            print("✅ 정답입니다!")
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        return correct, used_hint

    def _record_history(self, total, correct_count, score, hints_used):
        """이번 회차 결과를 게임 기록 목록(history)에 한 건 추가한다."""
        self.history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": total,
                "correct": correct_count,
                "score": score,
                "hints_used": hints_used,
            }
        )

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        """문제/선택지 4개/정답 번호/힌트(선택)를 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._get_text_input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choices.append(self._get_text_input(f"선택지 {i}: "))

        answer = self._get_int_input("정답 번호 (1-4): ", 1, 4)
        hint = self._get_optional_text_input("힌트 (선택 사항, 없으면 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()  # 추가 즉시 파일에 반영 (프로그램이 바로 꺼져도 유지되도록)
        print("\n✅ 퀴즈가 추가되었습니다!")

    def _get_text_input(self, prompt):
        """빈 값을 허용하지 않는 필수 텍스트 입력을 받는다."""
        while True:
            try:
                raw = input(prompt)
            except EOFError:
                self._handle_eof()
            text = raw.strip()
            if text == "":
                print("⚠️ 입력이 없습니다. 다시 입력해주세요.")
                continue
            return text

    def _get_optional_text_input(self, prompt):
        """힌트처럼 비워도 되는 텍스트 입력을 받는다. 빈 입력이면 None을 반환."""
        try:
            raw = input(prompt)
        except EOFError:
            self._handle_eof()
        text = raw.strip()
        return text if text else None

    def _handle_eof(self):
        """입력 스트림이 끊겼을 때(EOFError) 공통으로 호출: 저장 후 안전 종료."""
        print("\n⚠️ 입력 스트림이 종료되었습니다. 게임을 저장하고 종료합니다.")
        self.save_state()
        raise SystemExit(0)

    # ---------- 퀴즈 목록 ----------
    def list_quizzes(self):
        """등록된 모든 퀴즈의 문제 목록을 번호와 함께 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    # ---------- 퀴즈 삭제 ----------
    def delete_quiz(self):
        """목록을 보여주고 번호를 입력받아 해당 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        index = self._get_int_input(
            f"\n삭제할 퀴즈 번호 (1-{len(self.quizzes)}): ", 1, len(self.quizzes)
        )
        removed = self.quizzes.pop(index - 1)  # 화면 번호(1부터)를 리스트 인덱스(0부터)로 변환
        self.save_state()
        print(f"\n🗑️ 삭제되었습니다: {removed.question}")

    # ---------- 점수 확인 ----------
    def show_best_score(self):
        """최고 점수와 최근 게임 기록 5개(최신순)를 출력한다."""
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요.")
            return

        b = self.best_score
        print(f"\n🏆 최고 점수: {b['score']}점 ({b['total']}문제 중 {b['correct']}문제 정답)")

        if not self.history:
            print("📜 게임 기록이 없습니다.")
            return

        print("\n📜 최근 게임 기록 (최신순)")
        print("-" * 40)
        # history는 오래된 순으로 쌓이므로, 최근 5개를 잘라 역순으로 출력해 최신순으로 보여준다
        for entry in reversed(self.history[-5:]):
            hint_text = f", 힌트 {entry['hints_used']}회" if entry["hints_used"] else ""
            print(
                f"- {entry['timestamp']} | {entry['correct']}/{entry['total']}문제 "
                f"정답 | {entry['score']}점{hint_text}"
            )
        print("-" * 40)

    # ---------- 파일 저장/불러오기 ----------
    def load_state(self):
        """state.json을 읽어 quizzes/best_score/history를 채운다.

        파일이 없으면(최초 실행) 기본 퀴즈 데이터로 시작하고, 파일은 있지만
        JSON 형식이 깨졌거나 스키마가 다르면 안내 후 기본 데이터로 초기화한다.
        """
        if not os.path.exists(STATE_FILE):
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            self.history = []
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data.get("best_score")
            self.history = data.get("history", [])
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            # JSONDecodeError: 문법이 깨짐 / KeyError,TypeError: 스키마가 다름 / OSError: 파일 접근 실패
            print("⚠️ 저장된 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            self.history = []

    def save_state(self):
        """현재 quizzes/best_score/history를 state.json 전체에 덮어쓴다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as error:
            # 디스크 공간 부족, 권한 문제 등 - 저장만 실패시키고 프로그램은 계속 진행
            print(f"⚠️ 데이터 저장 중 오류가 발생했습니다: {error}")
