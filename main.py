from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Ctrl+C가 감지되었습니다. 게임을 저장하고 종료합니다.")
        game.save_state()


if __name__ == "__main__":
    main()
