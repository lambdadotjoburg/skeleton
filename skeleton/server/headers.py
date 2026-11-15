# HTTP protocol:
# 
#   https://en.wikipedia.org/wiki/HTTP
# 
# See RFC 7230:
# 
#   proxy servers should not forward the following header data:
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade"
}