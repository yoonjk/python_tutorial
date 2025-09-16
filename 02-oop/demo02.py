from abc import ABC, abstractmethod 

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass 
      
    def description(self):
        print("test")
      
class Circle(Shape):
    def __init__(self, radius): 
        self.radius = radius 
        
    def area(self): 
        return 3.141592653589793 * self.radius
      
class Rectangle(Shape): 
    def __init__(self, width, height):
        self.width = width 
        self.height = height 
        
    def area(self):
        return self.width * self.height
      
class AreaCalculator:
    def area(self, shape):
      shape.description()
      return shape.area()
    
    
areaCalculator = AreaCalculator()
circle = Circle(5)
rectangle = Rectangle(5,5)

print(areaCalculator.area(circle))
print(areaCalculator.area(rectangle))

