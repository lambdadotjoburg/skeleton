# command line input received from
# subprocess call may look like:
# --mode prod --watch --open

# arguments are thus:
# ["--mode", "prod", "--watch", "--open"]
def parse(argv: list[str]) -> dict:

    options: dict[str, str | bool] = {
        "mode": "dev",
        "watch": False,
        "open": False,
    } # dev/prod

    i = 0

    while i < len(argv):

        arg = argv[i]

        if arg == "--mode":

            if i + 1 >= len(argv):
                raise ValueError("--mode requires a values to be specified")
            
            mode = argv[i + 1]

            if mode not in ["dev", "prod"]:
                raise ValueError(f"invalid mode: {mode}")
            
            options["mode"] = mode

            i += 2
            continue

        if arg == "--root":
    
            if i + 1 >= len(argv):
                raise ValueError("--root requires a values to be specified")
            
            root = argv[i + 1]
            options["root"] = root

            i += 2
            continue

        if arg == "--watch":
            options["watch"] = True
            i += 1
            continue

        if arg == "--open":
            options["open"] = True
            i += 1
            continue

        raise ValueError(f"Unknown option: {arg}")

    return options