from quiz import Quiz

# 기본 제공 퀴즈 (주제: IT/컴퓨터 상식)
DEFAULT_QUIZZES = [
    Quiz(
        "HTTP 상태 코드 중 '요청한 리소스를 찾을 수 없음'을 의미하는 코드는?",
        ["200", "301", "404", "500"],
        3,
        hint="흔히 '페이지를 찾을 수 없습니다' 에러 화면에서 보게 되는 숫자입니다.",
    ),
    Quiz(
        "컴퓨터의 중앙처리장치를 가리키는 약자는?",
        ["RAM", "CPU", "GPU", "SSD"],
        2,
        hint="컴퓨터의 '두뇌'라고 불리는 장치입니다.",
    ),
    Quiz(
        "1바이트(Byte)는 몇 비트(bit)로 이루어져 있는가?",
        ["4비트", "8비트", "16비트", "32비트"],
        2,
        hint="2의 3제곱입니다.",
    ),
    Quiz(
        "다음 중 대표적인 관계형 데이터베이스 관리 시스템(RDBMS)이 아닌 것은?",
        ["MySQL", "PostgreSQL", "MongoDB", "Oracle"],
        3,
        hint="이 항목은 문서(document) 지향 NoSQL 데이터베이스입니다.",
    ),
    Quiz(
        "Git에서 원격 저장소의 변경 사항을 내려받아 현재 브랜치에 병합까지 수행하는 명령어는?",
        ["fetch", "pull", "push", "clone"],
        2,
        hint="'fetch'와 'merge'를 한 번에 수행하는 명령어입니다.",
    ),
    Quiz(
        "다음 중 운영체제(OS)가 아닌 것을 고르시오.",
        ["Windows", "Linux", "Python", "macOS"],
        3,
        hint="이것은 프로그래밍 언어입니다.",
    ),
]
