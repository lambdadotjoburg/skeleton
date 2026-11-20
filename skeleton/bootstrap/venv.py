# .venv detection heuristic!
def in_virtual_environment() -> bool:

    import sys

    return sys.prefix != sys.base_prefix
