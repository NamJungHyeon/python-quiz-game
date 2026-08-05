class Quiz:
    """퀴즈 한 문제를 표현하는 클래스.

    문제/선택지/정답/힌트라는 데이터와, 그 데이터를 출력하고 채점하는 동작을
    한 곳에 묶어둔다. 게임 진행이나 파일 저장 방식은 전혀 알지 못한다.
    """

    def __init__(self, question, choices, answer, hint=None):
        self.question = question    # 문제 텍스트
        self.choices = choices      # 선택지 4개 (리스트)
        self.answer = answer  # 정답 번호: 1~4 중 하나
        self.hint = hint  # 힌트 문자열 (없으면 None)

    def display(self, index):
        """문제 번호와 함께 문제/선택지를 화면에 출력한다."""
        print(f"\n[문제 {index}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답 번호와 같은지 비교한다."""
        return user_answer == self.answer

    def show_hint(self):
        """힌트가 있으면 힌트를, 없으면 안내 메시지를 출력한다."""
        if self.hint:
            print(f"💡 힌트: {self.hint}")
        else:
            print("💡 이 문제에는 힌트가 없습니다.")

    def to_dict(self):
        """state.json에 저장할 수 있도록 이 퀴즈를 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽은 딕셔너리로부터 Quiz 인스턴스를 복원한다."""
        return cls(data["question"], data["choices"], data["answer"], data.get("hint"))
