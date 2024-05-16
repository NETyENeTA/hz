from ConfigSettings import pg, COLOR, vec2, MOUSE, h_rgb


class RectObject:
    def __init__(self, pos: vec2, wh: vec2, is_update: bool = False, surface: pg.surface.Surface = None):
        self.surface = surface

        self.pos = pos
        self.wH = wh
        self.hitbox = self.get_hitbox()
        self.isUpdate = is_update

    def get_hitbox(self) -> pg.Rect:
        return pg.Rect(self.pos, self.wH)


class Frame(RectObject):

    def __init__(self, pos: vec2, wh: vec2, is_update: bool = False, surface: pg.surface.Surface = None):
        super().__init__(pos, wh, is_update, surface)


class Button(RectObject):

    def __init__(self, pos: vec2, wh: vec2, color: tuple[int, int, int] | tuple[int, int, int, int],
                 is_update: bool = False,
                 surface: pg.surface.Surface = None,
                 function=None, args=None
                 ):
        super().__init__(pos, wh, is_update, surface)
        self.color = COLOR(*color)
        self.function = function
        self.args = args

    def update(self):
        if self.hitbox.collidepoint(pg.mouse.get_pos()):
            if self.function and pg.mouse.get_pressed()[0] and not MOUSE.isClick:
                MOUSE.isClick = True
                self.function(*self.args) if self.args else self.function()

    def draw(self):
        # pg.draw.rect(self.surface, self.color.get(), self.hitbox)
        pg.draw.rect(self.surface, (255, 0, 0), self.hitbox)


class ButtonImage:

    def __init__(self, pos, image: pg.surface.Surface = None, *, function=None, args=None,
                 surface: pg.surface.Surface = None):
        self.pos = pos
        self.image = image
        self.function = function
        self.args = args

        self.hitbox = self.get_rect_image()
        self.surface = surface

    def get_rect_image(self) -> pg.Rect:
        return pg.Rect(self.pos - vec2(self.image.get_width() / 2, 0), self.image.get_size())

    def update(self):
        if self.hitbox.collidepoint(pg.mouse.get_pos()):
            if self.function and pg.mouse.get_pressed()[0] and not MOUSE.isClick:
                MOUSE.isClick = True
                self.function(*self.args) if self.args else self.function()

    def draw(self, y=0):
        self.surface.blit(self.image, self.pos - vec2(self.image.get_width() / 2, 0) + vec2(0, y))
        # pg.draw.rect(self.surface, (255, 0, 0), self.hitbox)


class CIRCLE:

    def __init__(self, pos: vec2, radius: int, speed: int = 1, surface: pg.surface.Surface = None):
        self.pos = pos
        self.speed = speed
        self.radius = radius
        self.LifeRadius = 100

        self.surface = surface

    def update(self):
        self.radius += self.speed

    def draw(self):
        pg.draw.circle(self.surface, h_rgb('F9F9F9'), self.pos, self.radius)
