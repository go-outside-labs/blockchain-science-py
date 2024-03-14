# -*- encoding: utf-8 -*-
# src/utils/network.py
# author: Mia Stein
# Network utils methods.

import json
import websocket
import src.utils.os as utils


def on_ws_message(msg: dict) -> None:
    """Handle orderbook data from websocket."""

    utils.pprint(msg['data'])


def on_open_topic(ws, topic: str) -> None:
    """Open websocket topic."""

    ws.send(json.dumps({"op": "subscribe", "args": [topic]}))


def ws_connection(url, ping_interval, ping_timeout) -> None:
    """Connect to websocket."""

    ping_interval = ping_interval or 20
    ping_timeout = ping_timeout or 10

    ws = websocket.WebSocketApp(url, on_message=on_ws_message)
    ws.run_forever(ping_interval=ping_interval, ping_timeout=ping_timeout)

