from dataclasses import dataclass

from fastapi import Request

@dataclass(frozen=True, kw_only=True)
class RouteContext:
    prefix: str # /api or /ws or /
    target: str # frontend/backend
    strip: bool # weather to strip prefixes
    protocol: str # http or ws

@dataclass(frozen=True, kw_only=True)
class UpstreamContext:
    path: str # composed path/...
    target: str # resolved
    protocol: str # http or ws

@dataclass(frozen=True, kw_only=True)
class UpstreamRequest:
    target: str
    request: Request
