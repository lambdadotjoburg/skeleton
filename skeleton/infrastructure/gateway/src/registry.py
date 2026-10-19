import asyncio

from skeleton.infrastructure.gateway.src.service import Service

# service config manager!
class Registry:

    def __init__(self) -> None:
        self.services: dict[str, Service] = {}

    def regsiter(self, service: Service) -> None:
        self.services[service.config.id] = service

    async def start_all(self) -> None:
        await asyncio.gather(
            *[
                service.run()
                for service
                in self.services.values()
            ]
        )

    async def stop_all(self) -> None:

        print("INFO:     Gracefully shutting down all services ...")
        for service in self.services.values():
            await service.shutdown()

    def get(self, name) -> Service:
        return self.services[name]