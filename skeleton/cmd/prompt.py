def prompt(
    name: str,
    current: str,
    choices: list[str] | None = None,
) -> str:

    while True:

        suffix = (
            f" ({' | '.join(choices)})"
            if choices
            else ""
        )

        answer = input(
            f"{name} [{current}]{suffix}: "
        ).strip()

        if not answer:
            return current

        if choices and answer not in choices:
            print(f"Please choose one of: {' | '.join(choices)}")
            continue

        return answer