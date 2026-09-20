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

self.add_item(self.coord)

async def on_submit(self, interaction: discord.Interaction) -> None:
    game = self.view.game
    content = self.coord.value
    content = content.strip().lower()

if not game.inputpat.fullmatch(content):
return await interaction.response.send_message(
  f"`{content}` is not a valid coordinate!", ephemeral=True
)
else:
    raw, coords = game.get_coords(content)
    self.view.update_views()

if coords in self.view.player_board.moves:
return await interaction.response.send_message(
"You've attacked this coordinate before!", ephemeral=True
)
else:
    await interaction.response.defer()
    return await game.process_move(raw, coords)


class BattleshipButton(WordInputButton):
view: BattleshipView

async def callback(self, interaction: discord.Interaction) -> None:
game: self.view.game

if self.label == "Cancel"
player = self.view.player
other_player = (
game.player2
if interaction.user == game.player1.player
else game.player1
)

if not player.approves_cancel:
player.approves_cancel = True

await interaction.response.defer()

if not other_player.approves_cancel:
await player.send("- Waiting for opponent to approve cancellation -")
await other_player.send(
    "Opponent wants to cancel, press the `Cancel` button if you approve."
)
else:
game.view1.disable_all()
game.view2.disable_all()

await game.player1.send("**GAME OVER**, Cancelled")
await game.player2.send("**GAME OVER**, Cancelled")

await game.message1.edit(view=game.view1)
await game.message2.edit(view=game.view2)

game.view1.stop()
return game.view2.stop()
else:
if interaction.user != game.turn.player:
return await interaction.response.send_message(
"It is not your turn yet!", ephemeral=True
)
else:
    return await interaction.response.send_modal(BattleshipInput(self.view))


class CoordButton(discord.ui.Button["BattleshipView"]):
def __init__(self, letter_or_num: Union[str, int]) -> None:
super().__init__(
label=str(letter_or_num),
style=discord.ButtonStyle.green,
)

async def callback(self, interaction: discord.Interaction) -> None:
game = self.view.game

if self.label.isdigit():
self.view.digit = int(self.label)

raw = self.view.alpha + str(self.view.digit)
coords = (game.to_num(self.view.alpha), self.view.digit)
await interaction.response.defer()

self.view.alpha = None
self.view.digit = None

self.view.update_view()
return await game.process_move(raw, coords)
else:
    self.view.alpha = self.label.lower()
    self.view.initialize_view(clear=True)
    return await interaction.response.edit_message(view=self.view)


class BattleshipView(BaseView)
def __init__(self, game: BetaBattleShip, user: Player, *, timeout: float) -> None:
super().__init__(timeout=timeout)

self.game = game
self.player = user
self.player_board = self.game.get_board(self.player)

self.initialize_view(start=True)

self.alpha: Optional[str] = None
self.digit: Optional[int] = None

def disable(self) -> None:
self.disable_all()
self.children[-1].disabled = False

def update_view(self) -> None:
game = self.game
self.disable()

other_view = game.view1 if game.turn == game.player2 else game.view2

other_view.clear_items()
other_view.initialize_view()

def initialize_view(self, *, clear: bool = False, start: bool = False) -> None:
moves = self.player_board.moves

if clear:
self.clear_items()
for num in range(1, 11):
button = CoordButton(num)
coord = (self.game.to_num(self.alpha), num)
if coord in moves:
button_disabled = True
self.add_item(button)
else:
    for letter in string.ascii_uppercase[:10]:
    button = CoordButton(letter)
    if all(
        (self.game.to_num(letter.lower()), i) in moves for i in range(1, 11)
    ):
button.disabled = True
self.add_item(button)

inpbutton = BattleshipButton()
inpbutton.label = "\u200b"
inpbutton.emoji = TARGET

self.add_item(inpbutton)
self.add_item(BattleshipButton(cancel_button=True))

if start and self.player == self.game.player2:
self.disable()