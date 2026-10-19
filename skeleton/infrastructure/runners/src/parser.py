from skeleton.infrastructure.runners.src.actions import ACTIONS

# command line input may look like:
# python run.py --start frontend gateway --watch --open
# python run.py --start --watch --open

# arguments are thus:
# ["--start", "frontend", "gateway", "--watch", "--open"]

def parse(argv: list[str]) -> dict:

    action = "start" # default

    targets: list[str] = [] # frontend, gateway, packages

    options: dict[str, str | bool] = {
        "mode": "dev",
        "watch": False,
        "open": False,
    } # dev/prod
    
    if argv and argv[0] in ACTIONS:
        action = ACTIONS[argv[0]]
        i = 1
    else:
        i = 0

    while i < len(argv):

        arg = argv[i]

        if arg.startswith("--"):
            break

        targets.append(arg)
        i += 1

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

    return {
        "action": action,
        "targets": targets,
        "options": options
    }