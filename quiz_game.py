import json
import os
import random

from data import DEFAULT_QUIZZES
from quiz import Quiz

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


class QuizGame:
    """퀴즈 게임 전체 흐름을 관리하는 클래스."""

    MENU_MIN = 1
    MENU_MAX = 5
    HINT_PENALTY = 5

    def __init__(self):
        self.quizzes = []
        self.best_score = None
        self.load_state()

    # ---------- 메뉴 ----------
    def print_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def get_menu_choice(self):
        return self._get_int_input("선택: ", self.MENU_MIN, self.MENU_MAX)

    def _get_int_input(self, prompt, min_value, max_value):
        while True:
            try:
                raw = input(prompt)
            except EOFError:
                self._handle_eof()
            text = raw.strip()

            if text == "":
                print(f"⚠️ 입력이 없습니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            if not text.lstrip("-").isdigit():
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            value = int(text)
            if value < min_value or value > max_value:
                print(f"⚠️ 잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
                continue

            return value

    def run(self):
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
                self.save_state()
                print("게임을 종료합니다. 안녕히 가세요!")
                break
            else:
                print(f"[{choice}] 기능은 아직 구현되지 않았습니다.")

    # ---------- 퀴즈 풀기 ----------
    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        available = len(self.quizzes)
        if available == 1:
            total = 1
        else:
            total = self._get_int_input(
                f"\n몇 문제를 풀까요? (1-{available}): ", 1, available
            )

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
        self.save_state()

    def _play_single_quiz(self, quiz, index):
        quiz.display(index)
        used_hint = False
        while True:
            answer = self._get_int_input(
                "\n정답 입력 (힌트 보기: 0): ", 0, len(quiz.choices)
            )
            if answer == 0:
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
        pass  # 히스토리 기능은 이후 커밋에서 구현 예정

    # ---------- 퀴즈 추가 ----------
    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._get_text_input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choices.append(self._get_text_input(f"선택지 {i}: "))

        answer = self._get_int_input("정답 번호 (1-4): ", 1, 4)
        hint = self._get_optional_text_input("힌트 (선택 사항, 없으면 Enter): ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def _get_text_input(self, prompt):
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
        try:
            raw = input(prompt)
        except EOFError:
            self._handle_eof()
        text = raw.strip()
        return text if text else None

    def _handle_eof(self):
        print("\n⚠️ 입력 스트림이 종료되었습니다. 게임을 저장하고 종료합니다.")
        self.save_state()
        raise SystemExit(0)

    # ---------- 퀴즈 목록 ----------
    def list_quizzes(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40)

    # ---------- 점수 확인 ----------
    def show_best_score(self):
        if self.best_score is None:
            print("\n⚠️ 아직 퀴즈를 풀지 않았습니다. 먼저 퀴즈를 풀어보세요.")
            return

        b = self.best_score
        print(f"\n🏆 최고 점수: {b['score']}점 ({b['total']}문제 중 {b['correct']}문제 정답)")

    # ---------- 파일 저장/불러오기 ----------
    def load_state(self):
        if not os.path.exists(STATE_FILE):
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None
            return

        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.quizzes = [Quiz.from_dict(q) for q in data["quizzes"]]
            self.best_score = data.get("best_score")
        except (json.JSONDecodeError, KeyError, TypeError, OSError):
            print("⚠️ 저장된 데이터 파일이 손상되어 기본 퀴즈 데이터로 초기화합니다.")
            self.quizzes = list(DEFAULT_QUIZZES)
            self.best_score = None

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"⚠️ 데이터 저장 중 오류가 발생했습니다: {error}")
