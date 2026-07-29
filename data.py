from quiz import Quiz

# 기본 제공 퀴즈 (주제: IT/컴퓨터 상식)
DEFAULT_QUIZZES = [
    Quiz(
        "HTTP 상태 코드 중 '요청한 리소스를 찾을 수 없음'을 의미하는 코드는?",
        ["200", "301", "404", "500"],
        3,
    ),
    Quiz(
        "컴퓨터의 중앙처리장치를 가리키는 약자는?",
        ["RAM", "CPU", "GPU", "SSD"],
        2,
    ),
    Quiz(
        "1바이트(Byte)는 몇 비트(bit)로 이루어져 있는가?",
        ["4비트", "8비트", "16비트", "32비트"],
        2,
    ),
    Quiz(
        "다음 중 대표적인 관계형 데이터베이스 관리 시스템(RDBMS)이 아닌 것은?",
        ["MySQL", "PostgreSQL", "MongoDB", "Oracle"],
        3,
    ),
    Quiz(
        "Git에서 원격 저장소의 변경 사항을 내려받아 현재 브랜치에 병합까지 수행하는 명령어는?",
        ["fetch", "pull", "push", "clone"],
        2,
    ),
    Quiz(
        "다음 중 운영체제(OS)가 아닌 것을 고르시오.",
        ["Windows", "Linux", "Python", "macOS"],
        3,
    ),
]
