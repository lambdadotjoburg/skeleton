def resolve_component(
    current: int,
    value: bool | str,
) -> int:

    if value is True:
        return current + 1

    if isinstance(value, str):

        number = int(value)

        if number < 0:
            return max(0, current + number)

        return number

    return current

def resolve_version(
    current: tuple[int, int, int],
    *,
    major: bool | str = False,
    minor: bool | str = False,
    patch: bool | str = False,
) -> tuple[int, int, int]:

    major_version, minor_version, patch_version = current

    major_changed = major is True or isinstance(major, str)
    minor_changed = minor is True or isinstance(minor, str)

    major_version = resolve_component(major_version, major)
    minor_version = resolve_component(minor_version, minor)
    patch_version = resolve_component(patch_version, patch)

    if major_changed and minor is False:
        minor_version = 0

    if (major_changed or minor_changed) and patch is False:
        patch_version = 0

    return (
        major_version,
        minor_version,
        patch_version,
    )