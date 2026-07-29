from data import DEFAULT_QUIZZES


class QuizGame:
    """퀴즈 게임 전체 흐름을 관리하는 클래스."""

    MENU_MIN = 1
    MENU_MAX = 5

    def __init__(self):
        self.quizzes = list(DEFAULT_QUIZZES)
        self.best_score = None

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
            raw = input(prompt)
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
        while True:
            self.print_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.play_quiz()
            elif choice == 5:
                print("게임을 종료합니다. 안녕히 가세요!")
                break
            else:
                print(f"[{choice}] 기능은 아직 구현되지 않았습니다.")

    # ---------- 퀴즈 풀기 ----------
    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct_count = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(index)
            answer = self._get_int_input("\n정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")

        score = round(correct_count / total * 100)
        print("\n" + "=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        if self.best_score is None or score > self.best_score["score"]:
            self.best_score = {"score": score, "correct": correct_count, "total": total}
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40)
