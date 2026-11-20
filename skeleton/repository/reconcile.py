def reconcile(
    existing: dict[str, dict[str, str]],
    configured: dict[str, dict[str, str]],
    remove: bool = True,
) -> dict[str, dict[str, str]]:

    result: dict[str, dict[str, str]] = {}

    for section in ("dependencies", "devDependencies"):

        existing_section = existing.get(section, {})
        configured_section = configured.get(section, {})

        reconciled: dict[str, str] = {}

        for name, version in existing_section.items():

            if name in configured_section:
                reconciled[name] = configured_section[name]

            elif not remove:
                reconciled[name] = version

        for name, version in configured_section.items():

            if name not in reconciled:
                reconciled[name] = version

        result[section] = reconciled

    return result