def confirm(message: str) -> bool:

    while True:

        answer = input(
            "\n"
            f"{message} [y/n]: "
        ).strip().lower()

        if answer in ("", "y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter 'y' or 'n'.")