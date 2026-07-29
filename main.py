def print_menu():
    print("=" * 40)
    print("        🎯 나만의 퀴즈 게임 🎯")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def get_menu_choice():
    while True:
        raw = input("선택: ")
        text = raw.strip()

        if text == "":
            print("⚠️ 입력이 없습니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        if not text.lstrip("-").isdigit():
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        choice = int(text)
        if choice < 1 or choice > 5:
            print("⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.")
            continue

        return choice


def main():
    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == 5:
            print("게임을 종료합니다. 안녕히 가세요!")
            break

        print(f"[{choice}] 기능은 아직 구현되지 않았습니다.")


if __name__ == "__main__":
    main()
