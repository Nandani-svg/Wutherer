from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, ClassVar
from to import BytesIO
import asyncio
import pathlib
import random
import re

import discord
from discord.ext import commands
from PIL import Image, ImageDraw

from .utils import *

if TYPE_CHECKING:
from typing_extensions import TypeAlias

Coords: TypeAlias = tuple[int, int]

SHIPS: dict[str, tuple[int, tuple[int, int, int]]] = {
   "carrier": (5, (52, 152, 219)),
   "battleship": (4, (246, 246, 112)),
   "destroyer": (3, (95, 245, 80)),
   "submarine": (3, (95, 245, 80)),
   "patrol boat": (2, (190, 190, 190)),
}


class Ship:
def __init__(
 self,
 name: str,
 size: int,
 start: Coords,
 color: tuple[int, int, int],
 vertical: bool = False,
) -> None:

self.name: str = name
self.size: int = size

self.start: Coords = start
self.vertical: bool = vertical
self.color: tuple[int, int, int] = color

self.end: Coords = (
(self.start[0], self.start[1] + self.size - 1)
if self.vertical
else (self.start[0] + self.size - 1, self.start[1])
)

self.span: list[Coords] = (
 [(self.start[0], i) for i in range(self.start[1], self.end[1] + 1)]
 if self.vertical
 else [(i, self.start[1]) for i in range (self.start[0], self.end[0] + 1)]
)

self.hits: list[bool] = [False] * self.size


class Board:
def  __init__(self, player: discord.User, random: bool = True) -> None:

self.player: discord.User = player
self.ships: list[Ship] = []

self.my_hits: list[Coords] = []
self.my_misses: list[Coords] = []

self.op_hits: list[Coords] = []
self.op_misses: list[Coords] = []

if random:
    self._place_ships()

@property
def moves(self) -> list[Coords]:
return self.my_hits + self.my_misses

def _is_valid(self, ship: Ship) -> bool:

if ship.end[0] > 10 or ship.end[1] > 10:
    return False

for existing in self.ships:
if any(c in existing.span for c in ship.span):
return False
return True

def _place_ships(self) -> None:
def place_ship(ship: str, size: int, color: tuple[int, int, int]) -> None:
start = random.randint(1, 10), random.randint(1, 10)
vertical = bool(random.randint(0, 1))

new_ship = Ship(
name=ship,
size=size,
start=start,
vertical=vertical,
color=color,
)

if self._is_valid(new_ship):
self.ships.append(new_ship)
else:
place_ship(ship, size, color)

for ship, (size, color) in SHIPS.items():
place_ship(ship, size, color)

def won(self) -> bool:
return all(all(ship.hits) for ship in self.ships)

def draw_dot(
self, cur: ImageDraw.Draw, x: int, y: int, *, coord: Coords, ship: Ship
) -> None:
x1, y1 = x - 10, y - 10
x2, y2 = x + 10, y + 10
cur.ellipse((x1, y1, x2, y2), fill=fill)

def draw_sq(
self, cur: ImageDraw.Draw, x: int, y: int, *, coord: Coords, ship: Ship
) -> None:
vertical = ship.vertical
left_end = ship.span.index(coord) == 0
right_end = ship.span.index(coord) == ship.size - 1

if vertical and left_end:
diffs = (18, 18, 25, 18)
elif vertical and right_end:
diffs = (25, 18, 18, 18)
elif not vertical and left_end:
diffs = (18, 18, 18, 25)
elif not vertical and right_end:
diffs = (18, 25, 18, 18)
elif vertical:
diffs = (25, 18, 25, 18)
else:
diffs = (18, 25, 18, 25)

d1, d2, d3, d4 = diffs
x1, y1 = x - d1, y - d2
x2, y2 = x + d3, y + d4
cur.rounded_rectangle((x1, y1, x2, y2), radius=5, fill=ship.color)

def get_ship(self, coord: Coords) -> Optional[Ship]:
if s := [ship for ship in self.ships if coord in ship.span]:
return s[0]

@executor()
def to_image(self, hide: bool = False) -> BytesIO:
RED = (255, 0, 0)
GRAY = (128, 128, 128)

with Image.open(pathlib.Path(__file__).parent / "assets/battleship.png") as img:
cur = ImageDraw.Draw(img)

for i, y in zip(range(1, 11), range(75, 530, 50)):
for j, x in zip(range(1, 11), range(75, 530, 50)):
coord = (i, j)
if coord in self.op_misses:
self.draw_dot(cur, x, y, fill=GRAY)

elif coord in self.op_hits:
if hide:
self.draw_dot(cur, x, y, fill=RED)
else:
ship = self.get_ship(coord)
self.draw_sq(cur, x, y, coord=coord, ship=ship)
self.draw_dot(cur, x, y, fill=RED)

elif ship := self.get_ship(coord):
if not hide:
self.draw_sq(cur, x, y, coord=coord, ship=ship)
buffer = BytesIO()
img.save(buffer, "PNG")

buffer.seek(0)
del img
return buffer


class BattleShip:

inputpat: ClassVar[re.Pattern] = re.compile(r"([a-j])(10|[1-9])")

def __init__(
self,
player1: discord.User,
player2: discord.User,
*,
random: bool = True,
) -> None:

self.embed_color: Optional[Discord.Color] = None

self.player1: discord.User = player1
self.player2: discord.User = player2

self.random: bool = random

self.player1_board: Board = Board(player1, random=self.random)
self.player2_board: Board = Board(player2, random=self.random)

self.turn: discord.User = self.player1
self.timeout: Optional[int] = None

self.message1: Optional[discord.Message] = None
self.message2: Optional[discord.Message] = None

def get_board(self, player: discord.User, other: bool = False) -> Board:
if other:
return self.player2_board if player == self.player1 else self.player1_board
else:
return self.player1_board if player == self.player1 else self.player2_board

def place_move(self, player: discord.User, coords: Coords) -> tuple[bool, bool]:
 board = self.get_board(player, other=True)

for i, ship in enumerate(op_board.ships):
for j, coord in enumerate(ship.span):
if coords == coord:
op_board.ships[i].hits[j] = True
board.my_hits.append(coords)
op_board.op_hits.append(coords)
return all(op_board.ships[i].hits), True

board.my_misses.append(coords)
op_board.op_misses.append(coords)
return False, False