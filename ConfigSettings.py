from Constants import *


def h_rgb(hex_color: str):
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def offset_go(point1: vec2, point2: vec2, speed: vec2) -> vec2:
    if abs(point1.x - point2.x) > speed.x:
        if point1.x > point2.x:
            point1.x -= speed.x
        elif point1.x < point2.x:
            point1.x += speed.x

    if abs(point1.y - point2.y) > speed.y:
        if point1.y > point2.y:
            point1.y -= speed.y
        elif point1.y < point2.y:
            point1.y += speed.y

    return point1


class MOUSE:
    isClick = False


class OFFSET:

    def __init__(self, cur: vec2 = vec2(0, 0), need: vec2 = vec2(0, 0), speed: vec2 = vec2(1, 1)):
        self.cur = cur
        self.need = need
        self.speed = speed

    def update(self):
        self.cur = offset_go(self.cur, self.need, self.speed)


class COLOUR:

    def __init__(self, r: int, g: int, b: int, a: int):
        self.r, self.g, self.b, self.a = r, g, b, a

    def __iter__(self):
        return iter([self.r, self.g, self.b, self.a])

    def __str__(self):
        return f'RGB:A => {self.r} {self.g} {self.b} {self.a}'


class COLOR:

    def __init__(self, red: int = 0, green: int = 0, blue: int = 0, alpha: int = 255, time: int = 0,
                 value: int = -1, next_color: tuple = (0, 0, 0)):

        self.color = COLOUR(*(value, value, value, alpha) if value >= 0 else (red, green, blue, alpha))

        self.time = time
        self.timer = time

        self.colorNext = next_color

    def set_color_next(self, color: tuple = (0, 0, 0)):
        self.colorNext = color

    def update(self):
        _color = []
        for color, nextColor in zip(self.color, self.colorNext):
            if color > nextColor:
                color -= 1
            elif color < nextColor:
                color += 1
            _color.append(color)
        self.set_color(*_color)

    def randomize(self, with_alpha: bool = False):
        self.color = COLOUR(rnd(0, 256), rnd(0, 256), rnd(0, 256),
                            rnd(0, 256) if with_alpha else self.color.a)

    def randomize_color(self, with_alpha: bool = False):
        self.color = COLOUR(*(rnd(0, self.color.r), rnd(0, self.color.g), rnd(0, self.color.b),
                              rnd(0, self.color.a) if with_alpha else self.color.a))

    @staticmethod
    def randomized(with_alpha: bool = False):
        return (rnd(0, 256), rnd(0, 256), rnd(0, 256),
                rnd(0, 256) if with_alpha else 255)

    def set_color(self, red: int = 0, green: int = 0, blue: int = 0, alpha: int = 255):
        self.color = COLOUR(red, green, blue, alpha)

    def set_all_color(self, value, with_alpha: bool = True):
        self.color = COLOUR(value, value, value, value if with_alpha else self.color.a)

    def set_alpha(self, alpha):
        self.color.a = alpha

    def add_alpha(self, alpha):
        self.color.a += alpha

        if self.color.a > 255:
            self.color.a = 255
            return True
        elif self.color.a < 0:
            self.color.a = 0
            return True

        return False

    def get(self):
        return self.color.r, self.color.g, self.color.b

    def get_color(self):
        return self.color.r, self.color.g, self.color.b, self.color.a

    def get_alpha(self):
        return self.color.a


class TEXT:

    def __init__(self, text: str | int, font, size: int, *, surface: pg.surface.Surface, pos: vec2):
        self.text = str(text)
        self.font = font.get_font(size) if isinstance(font, FONT) else font

        self.color = COLOR(value=0).get_color()

        self.renderedText = self.rendered_text()

        self.surface = surface
        self.pos = pos

        self.size = size

    def resize(self, pos):
        self.__init__(self.text, self.font, self.size, surface=self.surface, pos=pos)

    def remove_text(self):
        self.text = ''
        self.render_text()

    def set_text(self, _text: str):
        self.text = _text
        self.render_text()

    def add_text(self, text: str):
        self.text += text
        self.render_text()

    def render_text(self):
        self.renderedText = self.rendered_text()

    def rendered_text(self, _text: str = '') -> pg.surface.Surface:
        return self.font.render(self.text, True, self.color)

    def draw(self):
        self.surface.blit(self.renderedText, self.pos)


class FONT:

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def get_font(self, size) -> pg.font.Font:
        return pg.font.Font(self.path + self.name + '.ttf', size)

    def render_text(self, text, size, color) -> pg.surface:
        return self.get_font(size).render(text, True, color)

    def __str__(self):
        return f'{self.name}, {self.path}'


class FONTS:

    def __init__(self):
        self.fonts = []

    def add(self, name, path):
        self.fonts.append(FONT(name, path))

    def get_font_full(self, name, size) -> pg.font.Font:
        return [font.get_font(size) for font in self.fonts if font.name == name][0]

    def get_font(self, name) -> FONT:
        return [font for font in self.fonts if font.name == name][0]

    def __str__(self):
        return f'{self.fonts}'


Fonts = FONTS()
Fonts.add('PoetsenOne', paths['fonts'])

CameraOffset = OFFSET(speed=vec2(10, 10))
