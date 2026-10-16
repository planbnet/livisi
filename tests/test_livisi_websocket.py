"""Tests for the LIVISI websocket."""

import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from livisi import LivisiWebsocket


class _BlockingWebsocket:
    """Fake websocket connection that waits for messages forever."""

    def __init__(self, started: asyncio.Event) -> None:
        self._started = started

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args) -> None:
        return None

    def __aiter__(self):
        return self

    async def __anext__(self):
        self._started.set()
        await asyncio.Event().wait()


class TestLivisiWebsocket(IsolatedAsyncioTestCase):
    """Test the LIVISI websocket lifecycle."""

    async def test_cancellation_is_propagated(self) -> None:
        """Cancelling the listener must stop it instead of reporting a close."""
        aiolivisi = MagicMock()
        aiolivisi.controller.is_v2 = False
        aiolivisi.token = "token"
        aiolivisi.host = "192.0.2.1"
        websocket = LivisiWebsocket(aiolivisi)
        on_close = AsyncMock()
        started = asyncio.Event()

        with patch(
            "livisi.livisi_websocket.websockets.client.connect",
            return_value=_BlockingWebsocket(started),
        ):
            task = asyncio.create_task(websocket.connect(MagicMock(), on_close))
            await started.wait()
            self.assertTrue(websocket.is_connected())
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task

        self.assertFalse(websocket.is_connected())
        on_close.assert_not_awaited()
