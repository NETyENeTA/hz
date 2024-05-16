import pygame as pg
from random import randrange as rnd

vec2 = pg.math.Vector2
RES = vec2(320, 568)
FPS = 90
ALPHA = 120

RANGS = 999
KOEF1 = 5  # (level skill)
KOEF2 = 5  # 0 -> ? +KOEF1 (level skill)

AndroidPath = '/data/data/keycap.tst.lookup/files/app/'

paths = {
    'fonts': AndroidPath + 'assets/fonts/',
    'images': AndroidPath + 'assets/images/',
}

pg.init()
