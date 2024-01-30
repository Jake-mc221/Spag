import math
from abc import ABC, abstractmethod

from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image


class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm."""
    @abstractmethod
    def algo(self, img: Image):
        pass

class deepfry_strategy(Strategy):
    def algo(self, img: Image):
        img.sharpen(radius=8, sigma=4)
        img.modulate(100, 200)

        slope = math.tan((math.pi * (55 / 100.0 + 1.0) / 4.0))
        if slope < 0.0:
            slope = 0.0
        intercept = 15/100.0+((100-15)/200.0)*(1.0-slope)

        img.function("polynomial", [slope, intercept])
        img.evaluate(operator='gaussiannoise', value=0.05)


        return img

class implode_strategy(Strategy):
    def algo(self, img: Image):
        img.implode(amount=0.35)
        return img

class oilpaint_strategy(Strategy):
    def algo(self, img: Image):
        img.oil_paint(radius=5.0, sigma=0.0)
        return img

class fast_strategy(Strategy):
    def algo(self, img: Image):
        img.motion_blur(radius=16, sigma=8, angle=-45)
        return img


class sheer_strategy(Strategy):
    def algo(self, img: Image):
        img.shear('Red', 20, 30)
        return img


class swirl_strategy(Strategy):
    def algo(self, img: Image):
        img.swirl(degree=-90)
        return img


class blur_strategy(Strategy):
    def algo(self, img: Image):
        try:
            img.rotational_blur(angle=10)
        except Exception as e:
            print(e)
        return img

class meme_strategy(Strategy):
    def algo(selfslef, img: Image):
        with Drawing() as draw:
            draw.font = 'Arial'
            draw.font_size = 30
            draw.fill_color = Color('white')
            draw.text(50, 50, "Funny Text")
            draw(img)
        return img

class dis_strategy(Strategy):
    def algo(selfslef, img: Image):
        img.distort('barrel', (0.5, 0.8, 0.0, 1.0))
        img.save(filename='output_distorted.jpg')
        return img


class handler:
    @staticmethod
    def handle(choice) -> Strategy:
        if choice == "implode":
            return implode_strategy()
        elif choice == "sheer":
            return sheer_strategy()
        elif choice == "swirl":
            return swirl_strategy()
        elif choice == "blur":
            return blur_strategy()
        elif choice == "deepfry":
            return deepfry_strategy()
        elif choice == "fast":
            return fast_strategy()
        elif choice == "oilpaint":
            return oilpaint_strategy()
        elif choice == "meme":
            return meme_strategy()
        elif choice == "dis":
            return dis_strategy()
