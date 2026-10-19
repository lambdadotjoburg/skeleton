from subprocess import Popen

from skeleton.infrastructure.runners.src.command import Command

from skeleton.infrastructure.common.src.context import RuntimeContext

from typing import Callable

Hook = Callable[["ProcessManager"], None]

class ProcessManager:

    def __init__(self, context: RuntimeContext):

        self.context = context

        self.commands: list[Command] = []
        self.processes: list[Popen] = []

        self.before_start_hooks: list[Hook] = []
        self.after_start_hooks: list[Hook] = []
        self.on_shutdown_hooks: list[Hook] = []
    
    def register_hook(
        self, hook: Hook,
        phase: str = "before_start"
    ):
        if phase == "before_start":
            self.before_start_hooks.append(hook)
        elif phase == "after_start":
            self.after_start_hooks.append(hook)
        elif phase == "on_shutdown":
            self.on_shutdown_hooks.append(hook)

    def register(self, command: Command):
        self.commands.append(command)
    
    def spawn(self, command: Command):
        return Popen(
            command.args,
            cwd=command.cwd,
            env=self.context.env,
            shell=False,
        )
    
    def start(self):

        try:

            # BEFORE START HOOKS
            for hook in self.before_start_hooks:
                hook(self)

            # spawn processes
            for command in self.commands:
                self.processes.append(
                    self.spawn(command)
                )

            # AFTER START HOOKS
            for hook in self.after_start_hooks:
                hook(self)

            for p in self.processes:
                p.wait()
        
        # fix this issues => twice:
        # Terminate batch job (Y/N)?
        # issue seems to be coming from npm, npx, etc.
        except KeyboardInterrupt:

            # When ctrl + C for shutdown:
            
            # Exception ignored on threading shutdown:
            # Traceback (most recent call last):

            # File "C:\Users\Lambda\AppData\Local\Programs\Python\Python313\Lib\threading.py", line 1540, in _shutdown
            #     _thread_shutdown()

            print("INFO: shutting down services ...")

            # ON SHUTDOWN HOOKS!
            for hook in self.on_shutdown_hooks:
                hook(self)

            for p in self.processes:
                try:
                    p.terminate()
                except Exception:
                    pass

            for p in self.processes:
                try:
                    p.wait(timeout=3)
                except Exception:
                    try:
                        p.kill()
                    except Exception:
                        pass