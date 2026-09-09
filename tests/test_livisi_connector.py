"""Tests for the LIVISI connector."""

import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, call, patch

from aiohttp import ServerDisconnectedError

from livisi import (
    LivisiConnection,
    LivisiController,
    LivisiException,
    ShcUnreachableException,
    WrongCredentialException,
)


class TestLivisiConnection(IsolatedAsyncioTestCase):
    """Test the LIVISI connection lifecycle and request handling."""

    async def test_controller_failure_closes_connection(self) -> None:
        """Test controller discovery failure closes all resources."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock()
        connection._websocket.disconnect = AsyncMock()
        connect_error = LivisiException("controller failed")

        with (
            patch.object(connection, "_create_web_session", return_value=web_session),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(side_effect=connect_error),
            ),
            self.assertRaises(LivisiException) as raised,
        ):
            await connection.connect("192.0.2.1", "password")

        self.assertIs(raised.exception, connect_error)
        web_session.close.assert_awaited_once_with()
        connection._websocket.disconnect.assert_awaited_once_with()
        self.assertIsNone(connection._web_session)
        self.assertIsNone(connection.controller)

    async def test_avatar_session_replacement_failure_cleans_up(self) -> None:
        """Test a failed Avatar session replacement leaves no open session."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock()
        connection._websocket.disconnect = AsyncMock()
        controller = LivisiController(
            controller_type="Avatar",
            serial_number="1234",
            os_version="1.0",
            is_v2=True,
            is_v1=False,
        )

        with (
            patch.object(
                connection,
                "_create_web_session",
                side_effect=(web_session, LivisiException("replacement failed")),
            ),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(return_value=controller),
            ),
            self.assertRaises(LivisiException),
        ):
            await connection.connect("192.0.2.1", "password")

        web_session.close.assert_awaited_once_with()
        connection._websocket.disconnect.assert_awaited_once_with()
        self.assertIsNone(connection._web_session)
        self.assertIsNone(connection.controller)

    async def test_cleanup_failure_preserves_connection_error(self) -> None:
        """Test cleanup failure does not mask the original connection error."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock(side_effect=RuntimeError("close failed"))
        connection._websocket.disconnect = AsyncMock()
        connect_error = LivisiException("controller failed")

        with (
            patch.object(connection, "_create_web_session", return_value=web_session),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(side_effect=connect_error),
            ),
            self.assertRaises(LivisiException) as raised,
        ):
            await connection.connect("192.0.2.1", "password")

        self.assertIs(raised.exception, connect_error)
        connection._websocket.disconnect.assert_awaited_once_with()
        self.assertIsNone(connection._web_session)

    async def test_unexpected_controller_error_is_wrapped(self) -> None:
        """Test unexpected controller parsing errors follow the exception contract."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock()
        connection._websocket.disconnect = AsyncMock()

        with (
            patch.object(connection, "_create_web_session", return_value=web_session),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(side_effect=ValueError("invalid response")),
            ),
            self.assertRaises(LivisiException) as raised,
        ):
            await connection.connect("192.0.2.1", "password")

        self.assertIsInstance(raised.exception.__cause__, ValueError)
        web_session.close.assert_awaited_once_with()
        connection._websocket.disconnect.assert_awaited_once_with()

    async def test_wrong_credentials_keep_specific_exception(self) -> None:
        """Test a login error is not wrapped in the generic exception."""
        connection = LivisiConnection()
        connection.host = "192.0.2.1"
        connection._password = "wrong"
        connection._async_send_request = AsyncMock(
            return_value={"errorcode": 2009, "description": "invalid credentials"}
        )

        with self.assertRaises(WrongCredentialException):
            await connection._async_retrieve_token()

    async def test_state_transport_error_is_wrapped(self) -> None:
        """Test state transport failures use the library exception contract."""
        connection = LivisiConnection()
        connection.host = "192.0.2.1"
        connection.token = "token"
        connection._async_send_request = AsyncMock(
            side_effect=ServerDisconnectedError()
        )

        with self.assertRaises(ShcUnreachableException):
            await connection.async_get_value("capability-id", "onState")

    async def test_unexpected_state_error_is_wrapped(self) -> None:
        """Test unexpected state-read errors follow the exception contract."""
        connection = LivisiConnection()
        connection.async_send_authorized_request = AsyncMock(
            side_effect=RuntimeError("response failed")
        )

        with self.assertRaises(LivisiException) as raised:
            await connection.async_get_value("capability-id", "onState")

        self.assertIsInstance(raised.exception.__cause__, RuntimeError)

    async def test_invalid_json_is_wrapped(self) -> None:
        """Test malformed response JSON raises LivisiException."""
        connection = LivisiConnection()
        response = MagicMock(status=200, reason="OK")
        response.json = AsyncMock(
            side_effect=json.JSONDecodeError("invalid", "not-json", 0)
        )
        response_context = AsyncMock()
        response_context.__aenter__.return_value = response
        web_session = MagicMock()
        web_session.request.return_value = response_context
        connection._web_session = web_session

        with self.assertRaises(LivisiException):
            await connection._async_send_request("get", "http://example.test")

    async def test_token_retry_uses_refreshed_authorization_header(self) -> None:
        """Test a token refresh replaces the Authorization header for the retry."""
        connection = LivisiConnection()
        connection.host = "192.0.2.1"
        connection.token = "expired-token"
        connection._async_send_request = AsyncMock(
            side_effect=({"errorcode": 2007}, {"result": "ok"})
        )

        async def refresh_token() -> None:
            connection.token = "fresh-token"

        connection._async_refresh_token = AsyncMock(side_effect=refresh_token)

        response = await connection.async_send_authorized_request("get", "status")

        self.assertEqual(response, {"result": "ok"})
        self.assertEqual(
            connection._async_send_request.await_args_list,
            [
                call(
                    "get",
                    "http://192.0.2.1:8080/status",
                    None,
                    {
                        "authorization": "Bearer expired-token",
                        "Content-type": "application/json",
                        "Accept": "*/*",
                    },
                ),
                call(
                    "get",
                    "http://192.0.2.1:8080/status",
                    None,
                    {
                        "authorization": "Bearer fresh-token",
                        "Content-type": "application/json",
                        "Accept": "*/*",
                    },
                ),
            ],
        )

    async def test_controller_state_failure_uses_empty_state(self) -> None:
        """Test optional controller state failure does not break device loading."""
        connection = LivisiConnection()
        connection.controller = LivisiController(
            controller_type="Classic",
            serial_number="1234",
            os_version="1.0",
            is_v2=False,
            is_v1=True,
        )

        async def request(_method: str, path: str, payload=None):
            responses = {
                "message": [],
                "device": [
                    {
                        "id": "controller-id",
                        "type": "SHC",
                        "tags": {},
                        "config": {"name": "Controller"},
                    }
                ],
                "capability": [],
                "location": [],
            }
            if path == "device/controller-id/state":
                raise LivisiException("state unavailable")
            return responses[path]

        connection.async_send_authorized_request = AsyncMock(side_effect=request)

        devices = await connection.async_get_devices()

        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0].state, {})

    def test_non_dict_messages_are_ignored(self) -> None:
        """Test non-dict messages do not break device polling."""
        connection = LivisiConnection()

        parsed = connection.parse_messages([None, "invalid", {}])

        self.assertEqual(parsed, (set(), set(), set(), set()))

    def test_message_with_invalid_timestamp_is_still_processed(self) -> None:
        """A malformed timestamp must not discard the whole message."""
        connection = LivisiConnection()

        parsed = connection.parse_messages(
            [
                {
                    "type": "DeviceLowBattery",
                    "timestamp": "bad",
                    "devices": ["/device/123"],
                }
            ]
        )

        # low_battery_devices contains the id despite the bad timestamp.
        self.assertEqual(
            parsed, ({"123"}, set(), set(), set())
        )
