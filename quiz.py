class Quiz:
    """퀴즈 한 문제를 표현하는 클래스."""

    def __init__(self, question, choices, answer, hint=None):
        self.question = question
        self.choices = choices
        self.answer = answer  # 1~4 중 하나의 번호
        self.hint = hint  # 힌트 (없으면 None)

    def display(self, index):
        print(f"\n[문제 {index}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def show_hint(self):
        if self.hint:
            print(f"💡 힌트: {self.hint}")
        else:
            print("💡 이 문제에는 힌트가 없습니다.")

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"], data.get("hint"))
