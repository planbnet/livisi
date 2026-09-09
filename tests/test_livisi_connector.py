"""Tests for the LIVISI connector."""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from livisi import LivisiConnection, LivisiController, LivisiException


class TestLivisiConnection(IsolatedAsyncioTestCase):
    """Test the LIVISI connection lifecycle."""

    async def test_controller_failure_closes_connection(self) -> None:
        """Test controller discovery failure closes the owned session."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock()
        connection._websocket.disconnect = AsyncMock()

        with (
            patch.object(
                connection, "_create_web_session", return_value=web_session
            ),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(side_effect=LivisiException),
            ),
            self.assertRaises(LivisiException),
        ):
            await connection.connect("192.0.2.1", "password")

        web_session.close.assert_awaited_once_with()
        connection._websocket.disconnect.assert_awaited_once_with()
        self.assertIsNone(connection._web_session)

    async def test_session_replacement_failure_closes_connection(self) -> None:
        """Test Avatar session replacement failure closes the connection."""
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
                side_effect=(web_session, LivisiException()),
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

        self.assertEqual(web_session.close.await_count, 2)
        connection._websocket.disconnect.assert_awaited_once_with()
        self.assertIsNone(connection._web_session)

    async def test_cleanup_failure_preserves_connection_error(self) -> None:
        """Test cleanup failure does not replace the connection error."""
        connection = LivisiConnection()
        web_session = MagicMock()
        web_session.close = AsyncMock(side_effect=RuntimeError)
        connection._websocket.disconnect = AsyncMock()
        connection_error = LivisiException("controller failed")

        with (
            patch.object(
                connection, "_create_web_session", return_value=web_session
            ),
            patch.object(connection, "_async_retrieve_token", new=AsyncMock()),
            patch.object(
                connection,
                "_async_get_controller",
                new=AsyncMock(side_effect=connection_error),
            ),
            self.assertRaises(LivisiException) as raised,
        ):
            await connection.connect("192.0.2.1", "password")

        self.assertIs(raised.exception, connection_error)
        self.assertIsNone(connection._web_session)
        self.assertIsNone(connection.controller)
