import webbrowser

class BrowserOpener():
    def open(self, url: str):
        raise NotImplementedError(
            f"No browser opener implemented!"
        )

class SystemBrowserOpener(BrowserOpener):
    def open(self, url: str) -> None:
        webbrowser.open(url)

def resolve_browser(
    choice: str
) -> BrowserOpener | None:
    if choice == "system":
        return SystemBrowserOpener()
    return None