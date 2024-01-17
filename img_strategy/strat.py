from abc import ABC, abstractmethod
from wand.image import Image

class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """

    @abstractmethod
    def algo(self,img: Image):
        pass
class implode_strategy(Strategy):
    def algo(self, img: Image):
        img.implode(amount=0.35)
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
        img.rotational_blur(angle=10)
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



