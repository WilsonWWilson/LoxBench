from enum import IntEnum


class HttpStatusCode(IntEnum):
    MISSING_CREDS = 0
    OK = 200
    CODE_IN_USE = 201               # custom lx status code.
    SERIAL_NO_CHANGED = 301
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    API_REQUEST_NOT_ALLOWED = 401
    BLOCKED_TEMP = 403
    NOT_FOUND = 404
    SOCKET_FAILED = 418
    FORBIDDEN = 423                 # used e.g. for nfc code touch if an output cannot be controlled
    MS_UPDATE_REQUIRED = 426
    INVALID_TOKEN = 477             # Like an 401 but that when the token is no longer valid.
    SECURED_CMD_FAILED = 500
    MS_OUT_OF_SERVICE = 503
    WAITING_FOR_NW = 601
    CLOUDDNS_ERROR = 700            # > 700 = CloudDNS Errors
    CLOUDDNS_NOT_REGISTERED = 701   # starting 1.1.2015
    CLOUDDNS_NOT_CONFIGURED = 702
    CLOUDDNS_PORT_CLOSED = 703
    CLOUDDNS_SECURE_PWD_REQUIRED = 704
    CLOUDDNS_DENIED_CUSTOM_MESSAGE = 705
    REQUEST_TIMEOUT = -1


WS_CLOSE_CODE = {
    "BLOCKED": 4003  # temporarily blocked
}
