from typing import Tuple

class Rect():

    x: int
    y: int
    top: int
    left: int
    bottom: int
    right: int
    topleft: Tuple[int, int]
    bottomleft: Tuple[int, int]
    topright: Tuple[int, int]
    bottomright: Tuple[int, int]
    midtop: Tuple[int, int]
    midleft: Tuple[int, int]
    midbottom: Tuple[int, int]
    midright: Tuple[int, int]
    center: Tuple[int, int]
    centerx: int
    centery: int
    size: Tuple[int, int]
    width: int
    height: int
    w: int
    h: int

    def __init__(self, left: float, top: float, width: float, height: float):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.w = self.width
        self.h = self.height
        self.x = self.left
        self.y = self.top
        self.right = self.x + self.width
        self.bottom = self.y + self.height
   

if __name__ == '__main__':
       r = Rect(10,11, 50, 51)
       print(r)
   