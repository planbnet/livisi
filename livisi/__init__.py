# __init__.py

# Import key classes, constants, and exceptions

# livisi_connector.py
from .livisi_connector import LivisiConnection, connect

# livisi_const.py
from .livisi_const import (
    BATTERY_LOW,
    CLASSIC_WEBSOCKET_PORT,
    COMMAND_RESTART,
    CONTROLLER_DEVICE_TYPES,
    EVENT_BUTTON_LONG_PRESSED,
    EVENT_BUTTON_PRESSED,
    EVENT_MOTION_DETECTED,
    IS_REACHABLE,
    LIVISI_EVENT_BUTTON_PRESSED,
    LIVISI_EVENT_MOTION_DETECTED,
    LIVISI_EVENT_STATE_CHANGED,
    LOGGER,
    REQUEST_TIMEOUT,
    UPDATE_AVAILABLE,
    V1_NAME,
    V2_NAME,
    V2_WEBSOCKET_PORT,
    WEBSERVICE_PORT,
)

# livisi_controller.py
from .livisi_controller import LivisiController

# livisi_device.py
from .livisi_device import LivisiDevice

# livisi_errors.py
from .livisi_errors import (
    ERROR_CODES,
    ErrorCodeException,
    IncorrectIpAddressException,
    LivisiException,
    ShcUnreachableException,
    WrongCredentialException,
)

# livisi_websocket.py
from .livisi_websocket import LivisiWebsocket

# livisi_websocket_event.py
from .livisi_websocket_event import LivisiWebsocketEvent

# Define __all__ to specify what is exported when using 'from livisi import *'
__all__ = [
    "BATTERY_LOW",
    "CLASSIC_WEBSOCKET_PORT",
    "COMMAND_RESTART",
    "CONTROLLER_DEVICE_TYPES",
    "ERROR_CODES",
    "EVENT_BUTTON_LONG_PRESSED",
    "EVENT_BUTTON_PRESSED",
    "EVENT_MOTION_DETECTED",
    "IS_REACHABLE",
    "LIVISI_EVENT_BUTTON_PRESSED",
    "LIVISI_EVENT_MOTION_DETECTED",
    "LIVISI_EVENT_STATE_CHANGED",
    # From livisi_const.py
    "LOGGER",
    "REQUEST_TIMEOUT",
    "UPDATE_AVAILABLE",
    "V1_NAME",
    "V2_NAME",
    "V2_WEBSOCKET_PORT",
    "WEBSERVICE_PORT",
    "ErrorCodeException",
    "IncorrectIpAddressException",
    # From livisi_connector.py
    "LivisiConnection",
    # From livisi_controller.py
    "LivisiController",
    # From livisi_device.py
    "LivisiDevice",
    # From livisi_errors.py
    "LivisiException",
    # From livisi_websocket.py
    "LivisiWebsocket",
    # From livisi_websocket_event.py
    "LivisiWebsocketEvent",
    "ShcUnreachableException",
    "WrongCredentialException",
    "connect",
]
