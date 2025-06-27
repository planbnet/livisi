# __init__.py

# Import key classes, constants, and exceptions

# livisi_connector.py
from .livisi_connector import LivisiConnection, connect

# livisi_controller.py
from .livisi_controller import LivisiController

# livisi_device.py
from .livisi_device import LivisiDevice

# livisi_websocket.py
from .livisi_websocket import LivisiWebsocket

# livisi_websocket_event.py
from .livisi_websocket_event import LivisiWebsocketEvent

# livisi_const.py
from .livisi_const import (
    LOGGER,
    V2_NAME,
    V1_NAME,
    V2_WEBSOCKET_PORT,
    CLASSIC_WEBSOCKET_PORT,
    WEBSERVICE_PORT,
    REQUEST_TIMEOUT,
    CONTROLLER_DEVICE_TYPES,
    BATTERY_LOW,
    UPDATE_AVAILABLE,
    LIVISI_EVENT_STATE_CHANGED,
    LIVISI_EVENT_BUTTON_PRESSED,
    LIVISI_EVENT_MOTION_DETECTED,
    IS_REACHABLE,
    EVENT_BUTTON_PRESSED,
    EVENT_BUTTON_LONG_PRESSED,
    EVENT_MOTION_DETECTED,
    COMMAND_RESTART,
)

# livisi_errors.py
from .livisi_errors import (
    LivisiException,
    ShcUnreachableException,
    WrongCredentialException,
    IncorrectIpAddressException,
    ErrorCodeException,
    ERROR_CODES,
)

# Define __all__ to specify what is exported when using 'from livisi import *'
__all__ = [
    # From livisi_connector.py
    "LivisiConnection",
    "connect",
    # From livisi_controller.py
    "LivisiController",
    # From livisi_device.py
    "LivisiDevice",
    # From livisi_websocket.py
    "LivisiWebsocket",
    # From livisi_websocket_event.py
    "LivisiWebsocketEvent",
    # From livisi_const.py
    "LOGGER",
    "V2_NAME",
    "V1_NAME",
    "V2_WEBSOCKET_PORT",
    "CLASSIC_WEBSOCKET_PORT",
    "WEBSERVICE_PORT",
    "REQUEST_TIMEOUT",
    "CONTROLLER_DEVICE_TYPES",
    "BATTERY_LOW",
    "UPDATE_AVAILABLE",
    "LIVISI_EVENT_STATE_CHANGED",
    "LIVISI_EVENT_BUTTON_PRESSED",
    "LIVISI_EVENT_MOTION_DETECTED",
    "IS_REACHABLE",
    "EVENT_BUTTON_PRESSED",
    "EVENT_BUTTON_LONG_PRESSED",
    "EVENT_MOTION_DETECTED",
    "COMMAND_RESTART",
    # From livisi_errors.py
    "LivisiException",
    "ShcUnreachableException",
    "WrongCredentialException",
    "IncorrectIpAddressException",
    "ErrorCodeException",
    "ERROR_CODES",
]
