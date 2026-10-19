import time, threading

from skeleton.infrastructure.common.src.context import RuntimeContext
from skeleton.infrastructure.runners.src.browser import resolve_browser

def create_dev_portal(context: RuntimeContext):

    delay = 2.0
    servers = context.config.servers["servers"]

    gateway = servers["gateway"]
    backend = servers["backend"]

    gateway_host = gateway["host"]
    gateway_port = gateway["port"]
    gateway_url = f"http://{gateway_host}:{gateway_port}"

    # for opening backend documentation
    # valid options include "docs"/"redoc"
    docs = context.config.services["services"]["backend"]["docs"]
    
    backend_host = backend["host"]
    backend_port = backend["port"]
    backend_url = f"http://{backend_host}:{backend_port}/{docs}"
    
    opener = resolve_browser("system")

    urls = [
        gateway_url,
        backend_url,
    ]
    
    # self-object as first arg
    def hook(manager):
        
        if opener is None:
            return
        
        def _open():
            time.sleep(delay)

            for url in urls:
                opener.open(url)

        # When ctrl + C for shutdown:
        # Exception ignored on threading shutdown:
        # Traceback (most recent call last):
        # File "C:\Users\Lambda\AppData\Local\Programs\Python\Python313\Lib\threading.py", line 1540, in _shutdown
        #     _thread_shutdown()
        threading.Thread(target=_open, daemon=True).start()

    return hook

