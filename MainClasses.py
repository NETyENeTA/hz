import sys

from ConfigSettings import *
from InterfaceElements import ButtonImage, Button


class _Interface:
    alphaSurface = None

    def __init__(self, screen, app):
        self.buttons = []
        self.sc = screen

        self.app = app

    def go_to(self, tag_window: str, surface: pg.Surface):

        _Interface.alphaSurface = surface.copy()
        _Interface.alphaSurface.set_alpha(255)

        match tag_window:
            case 'MaMe':
                self.app.On = False
            case 'Logo':
                self.app.Logo.run()
            case 'Shop':
                self.app.Shop.run()

            case 'TaskChoose':
                self.app.TaskChoose.run()

            case 'Back':
                self.app.On = False

            case 'TaskProgrammer':
                self.app.TaskProgrammer.run()

            case 'TaskDesigner':
                self.app.TaskDesigner.run()

    def update(self):
        [el.update() for el in self.buttons]

        if _Interface.alphaSurface and _Interface.alphaSurface.get_alpha() > 0:
            _Interface.alphaSurface.set_alpha(_Interface.alphaSurface.get_alpha() - 15)

    def display(self, y=0):
        [el.draw(y) for index, el in enumerate(self.buttons) if index not in [0, 1]]
        [el.draw() for index, el in enumerate(self.buttons) if index in [0, 1]]
        self.sc.blit(_Interface.alphaSurface, (0, 0)) if _Interface.alphaSurface else None


class InterfaceLogo(_Interface):

    def __init__(self, screen: pg.surface.Surface, game):
        super().__init__(screen, game)

        self.buttons = [
            ButtonImage(vec2(RES.x / 2, RES.y - 100), pg.image.load(paths['images'] + 'startBtn.png'), surface=screen,
                        function=self.go_to, args=['MaMe', self.sc]),
        ]


class InterfaceGame(_Interface):
    image_icHome = pg.image.load(paths['images'] + 'icHome.png')
    image_icCup = pg.image.load(paths['images'] + 'icCup.png')
    image_icMarket = pg.image.load(paths['images'] + 'icMarket.png')
    image_icSettings = pg.image.load(paths['images'] + 'icSettings.png')
    image_icList = pg.image.load(paths['images'] + 'icList.png')

    def __init__(self, screen, game):
        super().__init__(screen, game)

        image_btn = pg.image.load(paths['images'] + 'btn.png')

        self.buttons = [
            ButtonImage(vec2(RES.x / 2 + 10, RES.y - 138), image_btn, function=self.go_to,
                        args=['Shop', self.sc], surface=screen),

            ButtonImage(vec2(RES.x / 2 - 100, RES.y - 138), image_btn, function=self.go_to,
                        args=['Logo', self.sc], surface=screen),
            ButtonImage(vec2(RES.x / 2 + 125, RES.y - 138), image_btn, function=self.go_to,
                        args=['TaskChoose', self.sc], surface=screen),

            ButtonImage(vec2(RES.x / 2 - 45, RES.y - 70), image_btn, function=self.go_to,
                        args=['', self.sc], surface=screen),
            ButtonImage(vec2(RES.x / 2 + 70, RES.y - 70), image_btn, function=self.go_to,
                        args=['n5', self.sc], surface=screen),

            # Button(vec2(RES.x / 2 - 25, RES.y - 130), vec2(50, 50), (255, 0, 0), surface=screen),
            # Button(vec2(RES.x / 2 - 125, RES.y - 130), vec2(50, 50), (0, 255, 0), surface=screen),
            # Button(vec2(RES.x / 2 + 100, RES.y - 130), vec2(50, 50), (0, 0, 255), surface=screen),

            # Button(vec2(RES.x / 2 + 40, RES.y - 60), vec2(50, 50), (255, 255, 0), surface=screen),
            # Button(vec2(RES.x / 2 - 85, RES.y - 60), vec2(50, 50), (0, 255, 255), surface=screen),
        ]

        self.Texts = [
        ]

    def display(self):
        [el.draw() for el in self.buttons]
        [el.draw() for el in self.Texts]

        self.sc.blit(self.image_icHome, (RES.x / 2 - 117, RES.y - 125))
        self.sc.blit(self.image_icCup, (RES.x / 2 - 66, RES.y - 56))
        self.sc.blit(self.image_icMarket, (RES.x / 2 - 10, RES.y - 123))
        self.sc.blit(self.image_icSettings, (RES.x / 2 + 48, RES.y - 56))
        self.sc.blit(self.image_icList, (RES.x / 2 + 103, RES.y - 125))

        self.sc.blit(_Interface.alphaSurface, (0, 0)) if _Interface.alphaSurface else None

    def resize(self):
        self.__init__(self.sc, self.app)


class _TaskProgrammer:
    image_bg = pg.image.load(paths['images'] + 'bgTasks.png')

    images_text = [pg.image.load(paths['images'] + 'textBlock' + f'{i}.png') for i in range(4)]

    images_smallBlocks = [pg.image.load(paths['images'] + 'smallBlock' + f'{i}.png') for i in range(3)]

    pos = [(OFFSET(speed=vec2(5, 5)), 150), (OFFSET(speed=vec2(5, 5)), 250), (OFFSET(speed=vec2(5, 5)), 350)]

    status_offset = {
        False: 0,
        True: 30,
    }

    def __init__(self, screen: pg.surface.Surface, player):

        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Interface = _Interface(screen, self)
        self.Player = player

        self.isAnimation = False

        self.Interface.buttons = [
            ButtonImage(vec2(60, 10), pg.image.load(paths['images'] + 'arrow.png'), function=self.Interface.go_to,
                        args=['Back', self.sc], surface=screen)
        ]

        self.Interface.buttons.extend(
            [ButtonImage(vec2(160, 80 + Y * 60), image, function=print, args=[], surface=screen) for Y, image in
             enumerate(self.images_text)])

        self.Interface.buttons[1].function = self.button_down

        self.On = True

    def button_down(self):
        self.isAnimation = not self.isAnimation
        CameraOffset.need.y = self.status_offset[self.isAnimation]

        if self.isAnimation:
            for offset, pos in self.pos:
                offset.need = vec2(0, pos)
        else:
            for offset, pos in self.pos:
                offset.need = vec2(0, 90)

    def update(self):
        while self.On:
            self.Interface.update()

            CameraOffset.update()

            for offset, pos in self.pos:
                offset.update()

            self.events()
            self.display()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(self.image_bg, (0, 0))

        # for image, offset in zip(self.images_smallBlocks, self.pos):
        #     self.sc.blit(image, (40, offset[0].cur.y))

        self.Player.draw_coins()
        self.Interface.display(CameraOffset.cur.y)

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.On = True
        self.update()


class _TaskDesigner:
    image_bg = pg.image.load(paths['images'] + 'bgTasks.png')

    def __init__(self, screen: pg.surface.Surface, player):

        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Interface = _Interface(screen, self)
        self.Player = player

        self.Interface.buttons = [
            ButtonImage(vec2(60, 10), pg.image.load(paths['images'] + 'arrow.png'), function=self.Interface.go_to,
                        args=['Back', self.sc], surface=screen)
        ]

        self.On = True

    def update(self):
        while self.On:
            self.Interface.update()

            self.events()
            self.display()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(self.image_bg, (0, 0))

        self.Player.draw_coins()
        self.Interface.display()

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.On = True
        self.update()


class _TaskChoose:
    image_bg = pg.image.load(paths['images'] + 'bgTask.png')

    def __init__(self, screen: pg.surface.Surface, player, interface):

        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Interface = _Interface(screen, self)
        self.Player = player

        self.Interface.buttons = [
            ButtonImage(vec2(60, 10), pg.image.load(paths['images'] + 'arrow.png'), function=self.Interface.go_to,
                        args=['Back', self.sc], surface=screen)
        ]

        self.buttons = [
            Button(vec2(10, 100), vec2(301, 170), (0, 0, 0), surface=screen, function=interface.go_to,
                   args=['TaskDesigner', self.sc]),
            Button(vec2(10, 298), vec2(301, 170), (0, 0, 0), surface=screen, function=interface.go_to,
                   args=['TaskProgrammer', self.sc]),
        ]

        self.On = True

    def update(self):
        while self.On:
            self.Interface.update()

            [el.update() for el in self.buttons]

            self.events()
            self.display()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(self.image_bg, (0, 0))

        self.Player.draw_coins()
        self.Interface.display()

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.On = True
        self.update()


class _Shop:
    image_cornerUp = pg.image.load(paths['images'] + 'cornerU.png')
    image_cornerDown = pg.image.load(paths['images'] + 'cornerD.png')
    image_bg = pg.image.load(paths['images'] + 'bg2.png')

    buttons_image = [
        pg.image.load(paths['images'] + 'btn0.png'),
        pg.image.load(paths['images'] + 'btn1.png'),
        pg.image.load(paths['images'] + 'btn2.png'),
        pg.image.load(paths['images'] + 'btn3.png'),
    ]

    shops = [
        (pg.image.load(paths['images'] + 'shop0.png'), 30),
        (pg.image.load(paths['images'] + 'shop1.png'), 30),
        (pg.image.load(paths['images'] + 'shop2.png'), 30),
        (pg.image.load(paths['images'] + 'shop3.png'), 30),

        (pg.image.load(paths['images'] + 'shop0.png'), -270, 0),
        (pg.image.load(paths['images'] + 'shop1.png'), -270, 0),
        (pg.image.load(paths['images'] + 'shop2.png'), -270, 0),
        (pg.image.load(paths['images'] + 'shop3.png'), -270, 0),

        (pg.image.load(paths['images'] + 'shop0.png'), RES.x, 0),
        (pg.image.load(paths['images'] + 'shop1.png'), RES.x, 0),
        (pg.image.load(paths['images'] + 'shop2.png'), RES.x, 0),
        (pg.image.load(paths['images'] + 'shop3.png'), RES.x, 0),
    ]

    items_buy = {
        'bg0': False,
        'bg1': False,
        'bg2': False,
        'bg3': False,
    }

    image_shopChooser = pg.image.load(paths['images'] + 'shopChooser.png')

    poses = {
        0: -292,
        1: 0,
        2: 294,
    }

    def __init__(self, screen: pg.surface.Surface, player):

        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Interface = _Interface(screen, self)
        self.Player = player

        self.Interface.buttons = [
            ButtonImage(vec2(60, 10), pg.image.load(paths['images'] + 'arrow.png'), function=self.Interface.go_to,
                        args=['Back', self.sc], surface=screen)
        ]

        self.Choose = 1

        self.buttons = [
            Button(vec2(245, 200), vec2(48, 48), (0, 0, 0), surface=screen, function=self.buy,
                   args=[999, pg.image.load(paths['images'] + 'bgGrey.png'), 'bg0']),
            Button(vec2(245, 260), vec2(48, 48), (0, 0, 0), surface=screen, function=self.buy,
                   args=[999, pg.image.load(paths['images'] + 'bgYellow.png'), 'bg1']),
            Button(vec2(245, 320), vec2(48, 48), (0, 0, 0), surface=screen, function=self.buy,
                   args=[999, pg.image.load(paths['images'] + 'bgGreen.png'), 'bg2']),
            Button(vec2(245, 380), vec2(48, 48), (0, 0, 0), surface=screen, function=self.buy,
                   args=[999, pg.image.load(paths['images'] + 'bgGrey.png'), 'bg3']),

            Button(vec2(40, 475), vec2(70, 60), (0, 0, 0), surface=screen, function=self.cam_offset_go, args=[-1]),
            Button(vec2(212, 475), vec2(70, 60), (0, 0, 0), surface=screen, function=self.cam_offset_go, args=[1]),
        ]

        self.On = True

    def cam_offset_go(self, value: int):
        self.Choose += value
        if self.Choose in [-1, 3]:
            self.Choose -= value
        CameraOffset.need.x = self.poses[self.Choose]

    def buy(self, money_remove: int, _bg: pg.surface.Surface, item_name: str):

        if self.Player.coins > money_remove:
            self.Player.images = _bg
            self.items_buy[item_name] = True
            self.Player.remove_money(money_remove)
        elif self.items_buy[item_name]:
            self.Player.images = _bg

    def update(self):
        while self.On:
            self.Interface.update()

            [el.update() for el in self.buttons]
            CameraOffset.update()

            self.events()
            self.display()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(self.image_bg, (0, 0))
        self.sc.blit(self.image_cornerUp, (0, 0))
        self.sc.blit(self.image_cornerDown, (0, RES.y - self.image_cornerDown.get_height()))

        self.sc.blit(self.buttons_image[0], (30, 50))
        self.sc.blit(self.buttons_image[1], (160, 50))
        self.sc.blit(self.buttons_image[2], (30, 120))
        self.sc.blit(self.buttons_image[3], (150, 120))

        for i, el in enumerate(self.shops):
            self.sc.blit(el[0], (el[1] + CameraOffset.cur.x, 200 + 60 * (i % 4)))

        self.sc.blit(self.image_shopChooser, (RES.x / 2 - self.image_shopChooser.get_width() / 2, RES.y - 100))

        self.Interface.display()
        self.Player.draw_coins()

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.On = True
        self.update()


class LOGO:
    image_logo = pg.image.load(paths['images'] + 'logo.png')

    def __init__(self, screen: pg.surface.Surface):
        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Interface = InterfaceLogo(screen, self)

        self.On = True

    def update(self):
        while self.On:
            self.Interface.update()

            self.events()
            self.display()

    def events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.On = False
            elif event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(LOGO.image_logo, (0, 45))

        self.Interface.display()

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.On = True
        self.update()


class APP:
    bgColor = COLOR(*h_rgb('F9F9F9')).get_color()

    def __init__(self):
        self.sc = pg.display.set_mode(RES, pg.RESIZABLE)

        pg.display.set_caption('Look Up!')

        self.Game = Game(self.sc)

    def start(self):
        self.Game.run()


class Player:
    rang_level = {}
    for key, value in zip(range(RANGS), sorted(list(range(KOEF1, RANGS * KOEF1, KOEF1)) * KOEF2)):
        rang_level[key] = value

    image_borderLevel = pg.image.load(paths['images'] + 'notFilledLevel.png')
    image_filledLevel = pg.image.load(paths['images'] + 'FilledLevel.png')

    image_coin = pg.image.load(paths['images'] + 'coin.png')

    def __init__(self, surface: pg.surface.Surface):
        self.images = pg.image.load(paths['images'] + 'people.png')  # todo: add images!
        self.levelSkill = 0
        self.rang = 1
        self.coins = 0

        self.textRang = TEXT(f'{self.rang} lvl', Fonts.get_font('PoetsenOne'), 18, surface=surface,
                             pos=vec2(41, 2))

        self.textRang.color = COLOR(value=0).get_color()

        self.textLevel = TEXT(self.levelSkill, Fonts.get_font('PoetsenOne'), 18, surface=surface,
                              pos=vec2(10, RES.y - 120))

        self.textCoins = TEXT(f'{self.coins}', Fonts.get_font('PoetsenOne'), 18, surface=surface,
                              pos=vec2(RES.x - 70, 2))

        self.surface = surface
        self.pos = vec2(RES.x / 2 - 50, RES.y - 350)

        self.percentLevel = 0

    def resize(self):
        self.__init__(self.surface)

    def remove_level_skill(self, value: int):

        if type(value) is str:
            value = int(value)

    def remove_money(self, value: int):
        self.coins -= value
        self.textCoins.set_text(f'{self.coins}')
        self.textCoins.pos.x = (RES.x - 70) - 10 * (len(str(self.coins)) - 1)

    def add_money(self, value: int):

        if type(value) is str:
            value = int(value)

        self.coins += value
        self.textCoins.set_text(f'{self.coins}')
        self.textCoins.pos.x = (RES.x - 70) - 10 * (len(str(self.coins)) - 1)

    def add_level_skill(self, value: int):

        if type(value) is str:
            value = int(value)

        self.levelSkill += value

        print('LEVEL', self.levelSkill, 'RANG', self.rang, 'from')

        for i in range(self.levelSkill // Player.rang_level[self.rang]):
            self.levelSkill -= Player.rang_level[self.rang]
            self.rang += 1

        self.textLevel.set_text(f'{self.levelSkill}')
        self.textRang.set_text(f'{self.rang} lvl')

        self.percentLevel = self.levelSkill / Player.rang_level[self.rang]

        print('LEVEL', self.levelSkill, 'RANG', self.rang, 'to')

    def draw_coins(self):

        self.surface.blit(Player.image_coin, (RES.x - 52, 2))
        self.textCoins.draw()

    def draw(self):
        pg.draw.rect(self.surface, COLOR(value=150).get_color(), (self.pos, (100, 100)))

        self.surface.blit(Player.image_borderLevel, (80, 8))
        self.surface.blit(Player.image_filledLevel.subsurface(((0, 0), (
            Player.image_filledLevel.get_width() * self.percentLevel, Player.image_filledLevel.get_height()))), (80, 8))
        self.surface.blit(Player.image_coin, (RES.x - 52, 2))

        self.surface.blit(self.images, (25, 25))

        self.textCoins.draw()
        self.textRang.draw()


class Game:
    image_bg = pg.image.load(paths['images'] + 'bg.png')

    image_cUR = pg.image.load(paths['images'] + 'cornerUR.png')
    image_cDL = pg.image.load(paths['images'] + 'cornerDL.png')

    def __init__(self, screen):
        self.sc = screen
        self.Clock = pg.time.Clock()

        self.Logo = LOGO(screen)
        self.Player = Player(screen)
        self.Interface = InterfaceGame(screen, self)

        self.Shop = _Shop(screen, self.Player)
        self.TaskChoose = _TaskChoose(screen, self.Player, self.Interface)
        self.TaskDesigner = _TaskDesigner(screen, self.Player)
        self.TaskProgrammer = _TaskProgrammer(screen, self.Player)

        self.On = True
        self.isCommandRun = False
        self.function = None
        self.args = None

        self.hesh = TEXT('', Fonts.get_font('PoetsenOne'), 18, surface=screen, pos=vec2(10, RES.y - 120))
        self._command_text = TEXT('', Fonts.get_font('PoetsenOne'), 18, surface=screen, pos=vec2(10, RES.y - 120))
        self._command_text.color = COLOR(value=150).get_color()

        self.heshes = {
            'add_lvl': (self.Player.add_level_skill, [5]),
            'remove_lvl': (self.Player.remove_level_skill, [5]),
            'am': (self.Player.add_money, [5]),
            'rm': (self.Player.remove_money, [5]),
        }

    def hesh_commands(self):

        for hesh, hesh_word, temp in zip([self.hesh.text] * len(self.heshes), self.heshes.keys(),
                                         self.heshes.values()):
            if hesh in hesh_word and len(hesh) > 0:
                self._command_text.set_text(hesh_word)
            elif len(hesh) == 0:
                self._command_text.remove_text()

            if hesh == hesh_word:
                self.isCommandRun = True
                self.function = temp[0]
                self.args = temp[1]

        if not any([hesh in hesh_word for hesh, hesh_word in zip([self.hesh.text] * len(self.heshes), self.heshes)]):
            self.hesh.remove_text()

    def update(self):
        while self.On:
            self.Interface.update()

            # print(self.Player.levelSkill, self.hesh.text)

            if not self.isCommandRun:
                self.hesh_commands()

            self.events()
            self.display()

    def events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:

                if event.key == pg.K_TAB and self._command_text.text:
                    self.hesh.set_text(self._command_text.text)

                if event.key not in [pg.K_RETURN, pg.K_TAB]:
                    self.hesh.add_text('_' if event.unicode in [' '] else event.unicode)

                if event.key == pg.K_RETURN:
                    self.isCommandRun = False
                    temp = self.hesh.text.split('/')
                    self.args = temp[1:] if len(temp) > 1 else self.args
                    self.function(*self.args) if self.args else self.function()
                    self.hesh.remove_text()

            elif event.type == pg.MOUSEBUTTONUP:
                MOUSE.isClick = False

            elif event.type == pg.VIDEORESIZE:

                RES.x = event.w
                RES.y = event.h
                self.Interface.resize()
                self.Player.resize()
                self.hesh.resize(vec2(10, RES.y - 120))
                self._command_text.resize(vec2(10, RES.y - 120))

    def display(self):
        self.sc.fill(APP.bgColor)

        self.sc.blit(Game.image_cDL, (0, RES.y - Game.image_cDL.get_height()))
        self.sc.blit(Game.image_cUR, (21, -7))
        self.sc.blit(Game.image_bg, (0, 0))

        self.Player.draw()
        self.Interface.display()
        self._command_text.draw()
        self.hesh.draw()

        pg.display.flip()
        self.Clock.tick(FPS)

    def run(self):
        self.Logo.run()
        self.update()
