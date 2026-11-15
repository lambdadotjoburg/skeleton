import webbrowser

from urllib.parse import urljoin

from ..layout.engine import EngineLayout

def open_portal(*, engine: EngineLayout) -> None:

    portal = engine.server.portal
    layout = engine.server

    destinations: list[str] = []

    from ..runtime.server import ServerName

    for name, service in portal.services.items():

        server = layout.server(name)

        base = f"http://{server.host}:{server.port}/"

        if service.open:
            destinations.append(
                base.rstrip("/")
            )

        doc = service.docs

        if doc is None:
            continue

        if name == ServerName.GATEWAY and not doc.enabled:
            continue

        if doc.open:
            destinations.append(
                urljoin(
                    base,
                    doc.url.lstrip("/")
                )
            )

    if not destinations:
        return

    if portal.browser == "default":
        browser = webbrowser.get()
    else:
        browser = webbrowser.BackgroundBrowser(portal.browser)

    for url in destinations:
        browser.open(url, new=2)