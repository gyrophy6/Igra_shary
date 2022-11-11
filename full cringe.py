import pygame
from pygame.draw import *
from math import hypot, cos, sin, pi
from random import randint, uniform

#У любой уважающей себя игры (кроме дс-ок) должна быть возмонжсоть выбрать сложность (вдруг игрок захочет больше
#внимания уделить сюжету, нежели геймплею)
print("Введите уровень сложности от 1 до 10")
N = int(input())

#А это релевантная привязка к нынешним обстоятельствам
print("Введите '1', чтобы активировать support Ukraine mode (иначе введите '0')")
U_MODE = int(input())


#Задаем основные необходимые величины. Из цветов и типов делаем списки,
#чтобы в дальнейшем с помощью Бога рандома выбирать рандомные элементы из них
FPS = 60
COLOR1 = (0, 0, 0)
COLOR2 = (255, 0, 0)
COLOR3 = (0, 255, 0)
COLOR4 = (0, 0, 255)
COLOR5 = (255, 255, 0)
COLOR6 = (255, 0, 255)
COLOR7 = (0, 255, 255)
COLOR8 = (150, 90, 255)
COLOR9 = (70, 200, 120)
COLOR10 = (255, 255, 255)
colors = [COLOR2,COLOR3,COLOR4,COLOR5,COLOR6,COLOR7,COLOR8,COLOR9,COLOR10]
x_range = 1200
y_range = 900
screen_size = (x_range, y_range)
targets_a_sec = (N+1/3)
full_target = (3*N)
types = ["rect", "crl"]
interval = (N/5)




class Target:

#Что бы это ни значило, инициализируем объект (slef -- ссылка на него)

    def __init__(self, position, velocity, r, color, type):

        self.type = type
        self.color = color
        self.r = r
        self.position = list(position)
        self.velocity = list(velocity)


#Рисуем таргет (target) на скрине (ekrane)
    def draw(self, screen):

#Рисуем бортики (они подогнаны, да, и что? Они же есть!)
        line(screen, (255, 255, 255), (0, 0), (x_range,0), 10)
        line(screen, (255, 255, 255), (0, 0), (0, y_range), 10)
        line(screen, (255, 255, 255), (x_range, 0), (x_range, y_range), 10)
        line(screen, (255, 255, 255), (0, y_range), (x_range, y_range), 10)
#Ну а это та самая релевантная привязка
        if U_MODE == 1:
            polygon(screen, (0, 0, 255), [(0, 0), (0, 0.5*y_range), (x_range, 0.5*y_range), (x_range, 0)]),
            polygon(screen, (255, 255, 0), [(0, 0.5*y_range), (x_range, 0.5*y_range), (x_range, y_range), (0, y_range)])

#Дальше относим к разным фигурам их параметры
        match self.type:
            case "crl":
                circle(screen, self.color, self.position, self.r)
            case "rect":
                rect(screen, self.color, (self.position[0] - self.r, self.position[1] - self.r, 2 * self.r, 2 * self.r))
#А тут вводим функцию проверки того, где находится какая-то точка (дальнейшем точка нажатия) относительно фигуры
    def is_inside(self, point):
        match self.type:
            case "crl":
                return hypot(point[0] - self.position[0], point[1] - self.position[1]) <= self.r
            case "rect":
                return abs(point[0] - self.position[0]) <= self.r or (point[1] - self.position[1]) <= self.r

#Ну а теперь можно подрубить счетчик очков (не воды с электричеством, как можно было бы подумать)
class Counter():

    def __init__(self):
        self._value = 0

    def increase(self):
        self._value += 1
#Ссылка на телегу мистера Пропера
    @property
    def value(self):

        return self._value
#Ну и теперь счетчик умеет прибавлять баллы и возвращать результат

#Сделаем пустой список объектов и будем добавлять в него рандомные
pygame.init()
screen = pygame.display.set_mode(screen_size)
points = []
SCOREBOBA = Counter()
ABOBA = Counter()

#Добавляем в него рандомные
def new_ball():
    points.append(Target((randint(100, 700), randint(100, 500)), (randint(-40, 40), randint(-40, 40)), randint(30, 50),
                         colors[randint(0, 5)], types[randint(0, 1)]))

#Рисуем те самые рандомные
def draw_balls():
    for point in points:
        point.draw(screen)

#Эт
def quit_event_handler(event):
    pass
#Эта следит за нажатиями
def mousebuttondown_event_handler(event):

#Еслм точка, куда нажали мышкой, удовлятворяет той функции ис инсайд (дэд???), то счетчик прибавляет баллы
    def process_point(point):
        if point.is_inside(event.pos):
            SCOREBOBA.increase()
            points.remove(point)
            screen.fill(COLOR10)

 #А еще можно специально спамить объекты! Это же ещё круче!
    for point in points:
        process_point(point)
    if ABOBA.value / FPS * targets_a_sec > len(points) and full_target > len(points):
        new_ball()


#Зададим скорость. Все, что можно сказать, это то, что она не превосходит скорость света.
def move_points(time):
    def move_point(point, time):
        if point.type == "rect":
            point.velocity[0] -= int(time * 5 * (point.position[0] - screen_size[0] / 2) / screen_size[0])
            point.velocity[1] -= int(time * 5 * (point.position[1] - screen_size[1] / 2) / screen_size[1])
#Поставим скоростные ограничения (а если будут много превышать -- сделаем штрафы. Один из способов зарабатывать прогой)
            if point.velocity[0] > N*screen_size[0] / 15:
                point.velocity[0] = screen_size[0] / 15
            if point.velocity[1] > N*(screen_size[1]) / 15:
                point.velocity[1] = screen_size[1] / 15

#Это время (не собственное, просто время. Нермех ботать будем после лабы по проге)
        tx = ((screen_size[0] - point.r - point.position[0]) / point.velocity[0] if point.velocity[0] > 0 else \
                  -(point.position[0] - point.r) / point.velocity[0]) if point.velocity[0] != 0 else screen_size[0]
        ty = ((screen_size[1] - point.r - point.position[1]) / point.velocity[1] if point.velocity[1] > 0 else \
                  -(point.position[1] - point.r) / point.velocity[1]) if point.velocity[1] != 0 else screen_size[1]

#В случае, если квадрат (rect) не достигнет бордюров (не шутить про ССС не шутить про ССС)
        if tx > time and ty > time:
            for i in range(2):
                point.position[i] += time * point.velocity[i]
            return
#Позиция точки плюс равно время минус тэ. Тут вроде и так все ясно.
        t = tx if tx - ty < 0 else ty
        for i in range(2):
            point.position[i] += (time - t) * point.velocity[i]

#Бог рандома геометрии углов
        phi = uniform(0.1, pi - 0.1)
#В физике это называтся "ускорение"
        vel = hypot(*point.velocity)
#А это -- отражение
        if tx == min(tx, ty):
            point.velocity[0] = (-1 if point.position[0] > screen_size[0] / 2 else 1) * vel * sin(phi)
            point.velocity[1] = vel * cos(phi)
        else:
            point.velocity[1] = (-1 if point.position[1] > screen_size[1] / 2 else 1) * vel * sin(phi)
            point.velocity[0] = vel * cos(phi)

        move_point(point, time - t)

#Погнали
    for point in points:
        move_point(point, time)




pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    ABOBA.increase()
    for event in pygame.event.get():
#Вышли
        if event.type == pygame.QUIT:
            quit_event_handler(event)
            finished = True
#Нажатие мышки
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttondown_event_handler(event)

    move_points(interval)

# Необходимо обновить экран
    draw_balls()
    pygame.display.update()
    screen.fill(COLOR1)


pygame.quit()

#Cамая приятная счать

def out_red(text):
        print("\033[7m\033[30m\033[46m{}\033[0m".format(text))
out_red("Congratulations! Your total score:")

print(SCOREBOBA.value)

def out_red(text):
        print("\033[1m\033[30m\033[46m{}\033[0m".format(text))
out_red("Now go practice physics.")

### Э Т О  К О Н Е Ц ! ! ! ###