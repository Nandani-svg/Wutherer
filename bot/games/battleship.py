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