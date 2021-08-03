# dtype: ignore
from typing import Tuple, List
import math

class Point():
    # x: float
    # y: float
    # top: float
    # left: float
    # center: Tuple[float, float]

    def __init__(self, left: float = 0.0, top: float = 0.0): 
        self._left = float(left)
        self._top = float(top)

    @property
    def left(self)->float:  
        return self._left

    @left.setter
    def left(self, value: float):
        self._left = float(value)

    @property
    def top(self)->float: 
        return self._top

    @top.setter
    def top(self, value: float):
        self._top = float(value)

    @property
    def x(self)->float: 
        return self.left

    @x.setter
    def x(self, value: float):
        self.left = value

    @property
    def y(self)->float: 
        return self.top

    @y.setter
    def y(self, value: float):
        self.top = value

    @property
    def center(self)->Tuple[float,float]:
        return (self.left, self.top)

    @center.setter
    def topleft(self, value:Tuple[float,float]):
        self.left = value[0]
        self.top = value[1]

    def __getitem__(self, i):
        return self.topleft[i]

    def __copy__(self):
        return Point(self.left, self.top)

    def __deepcopy__(self):
        return Point(self.left, self.top)

    ###############
    def distanceTo(self, point)->float:
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt((dx*dx)+(dy*dy))

    def rotateAround(self, angle, point):
        ang = math.radians(angle)
        c = math.cos(ang)
        s = math.sin(ang)
        px = self.x - point[0]
        py = self.y - point[1]

        xnew = px * c - py * s
        ynew = px * s + py * c

        self.x = xnew + point[0]
        self.y = ynew + point[1]

class Rect():
    # x: float
    # y: float
    # top: float
    # left: float
    # bottom: float
    # right: float
    # topleft: Tuple[float, float]
    # bottomleft: Tuple[float, float]
    # topright: Tuple[float, float]
    # bottomright: Tuple[float, float]
    # size: Tuple[float, float]

    # midtop: Tuple[float, float]
    # midleft: Tuple[float, float]
    # midbottom: Tuple[float, float]
    # midright: Tuple[float, float]
    # center: Tuple[float, float]
    # centerx: float
    # centery: float

    # width: float
    # height: float
    # w: float
    # h: float

    # noqa
    def __init__(self, left: float = 0.0, top: float = 0.0, width: float = 0.0, height: float = 0.0): # noqa
        self._left = float(left)
        self._top = float(top)
        self._width = float(width)
        self._height = float(height)

    @property
    def left(self)->float:  
        return self._left

    @left.setter
    def left(self, value: float):
        self._left = float(value)

    @property
    def top(self)->float: 
        return self._top

    @top.setter
    def top(self, value: float):
        self._top = float(value)

    @property
    def width(self)->float: 
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = float(value)

    @property
    def height(self)->float: 
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = float(value)


    #####################################


    @property
    def w(self)->float: 
        return self.width

    @w.setter
    def w(self, value: float):
        self.width = value

    @property
    def h(self)->float: 
        return self.height

    @h.setter
    def h(self, value: float):
        self.height = value

    @property
    def x(self)->float: 
        return self.left

    @x.setter
    def x(self, value: float):
        self.left = value

    @property
    def y(self)->float: 
        return self.top

    @y.setter
    def y(self, value: float):
        self.top = value

    @property
    def right(self)->float: 
        return self.left + self.width

    @right.setter
    def right(self, value: float):
        self.width = value - self.left

    @property
    def bottom(self)->float: 
        return self.top + self.height

    @bottom.setter
    def bottom(self, value: float):
        self.height = value - self.top

    #######################

    @property
    def topleft(self)->Tuple[float,float]:
        return (self.left, self.top)

    @topleft.setter
    def topleft(self, value:Tuple[float,float]):
        self.left = value[0]
        self.top = value[1]

    @property
    def bottomleft(self)->Tuple[float,float]:
        return (self.left, self.bottom)

    @bottomleft.setter
    def bottomleft(self, value:Tuple[float,float]):
        self.left = value[0]
        self.bottom = value[1]

    @property
    def topright(self)->Tuple[float,float]:
        return (self.right, self.top)

    @topright.setter
    def topright(self, value:Tuple[float,float]):
        self.right = value[0]
        self.top = value[1]

    @property
    def bottomright(self)->Tuple[float,float]:
        return (self.right, self.bottom)

    @bottomright.setter
    def bottomright(self, value:Tuple[float,float]):
        self.right = value[0]
        self.bottom = value[1]

    @property
    def size(self)->Tuple[float,float]:
        return (self.width, self.height)

    @size.setter
    def size(self, value:Tuple[float,float]):
        self.width = value[0]
        self.height = value[1]

    #######
    def __getitem__(self, i):
        return self.topleft[i]

    def __copy__(self):
        return Rect(self.left, self.top, self.width, self.height)

    def __deepcopy__(self):
        return Rect(self.left, self.top, self.width, self.height)

    #######

    def collideRect(self, rect)->bool:
        ret = False

        if self.left < rect.right and \
            self.right > rect.left and \
            self.top < rect.bottom and \
            self.bottom > rect.top :
                ret = True

        return ret

    def containsRect(self, rect)->bool:
        ret = False

        if self.left < rect.left and \
            self.right > rect.right and \
            self.top < rect.top and \
            self.bottom > rect.bottom :
                ret = True

        return ret
        

    # def collideRectList(self, list)->int:
    #     ret = -1
    #     for i, rect in enumerate(list):
    #         rect: Rect
    #         if rect.collideRect(rect):
    #             return i

    #     return ret

    # def containRect(self, items):
    #     pass

    def collidePoint(self, point: Point):
        ret = False

        if self.left < point.x and \
            self.right > point.x and \
            self.top < point.y and \
            self.right  > point.y :
                ret = True

        return ret


