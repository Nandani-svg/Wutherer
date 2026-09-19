from __future__ import annotations

from typing import Optional, Any, Coroutine, Union
import asyncio
import string

import discord
from discord.ext import commands
from utils.emoji import TARGET
from utils.emoji import TARGET

from ..battleship import (
 BattleShip,
 SHIPS,
 Ship,
 Board,
)

from .wordle_buttons import WordInputButton
from ..utils import DiscordColor, DEFAULT_COLOR, BaseView


class Player:
def __init__(self, player: discord.User, *, game: BetaBattleShip) -> None:
self.game = game
self.player = player

self.embed = discord.Embed(title="Log", description="```\n\u200b\n```")

self.logs: list[str] = []
self.log: str = ""

self.approves_cancel: bool = False

def update_log(self, log: str) -> None:
self._logs.append(log)
log_str = "\n\n".join(self._logs[-self.game.max_log_size :])

if len(self.logs) > self.game.max_log_size:
log_str = "...\n\n" + log_str

self.embed.description = f"```diff\n{log_str}\n```"

def __getattribute__(self, name: str) -> Any:
try:
    return super().__getattribute__(name)
except AttributeError:
    return self.player.__getattribute__(name)


class  BattleshipInput(discord.ui.Modal, title="Input a coordinate"):
def __init__(self, view: BattleshipView) -> None:
super().__init__()
self.view = view

self.coord = discord.ui.TextInput(
label="Enter your target coordinate"
placeholder="ex: a8"
style=discord.TextStyle.short,
required=True,
min_length = 2,
max_length = 3,
)