from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, color):
        self.color = color
        
    @abstractmethod
    def area(self):
        pass 
    
    @abstractmethod 
    def perimeter(self):
        pass   
    
    def description(self): 
        print(f"{self.__class__.__name__} has the color: {self.color}")
        
class Rectangle(Shape): 
    def __init__(self, width, height, color):
        super().__init__(color) 
        self.width = width 
        self.height = height 
        
    def area(self):
        return self.width + self.height
      
    def perimeter(self): 
        return 2 * (self.width + self.height)
      
class Circle(Shape):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
        
    def area(self):
        return 3.141592653589793 * (self.radius ** 2)
        
    def perimeter(self):
        return 2 * 3.141592653589793 * self.radius
      
def process_my_color(obj: Shape):
    obj.description()
    
  
  
rectangle = Rectangle(4, 5, "red")
print("Rectangle area: {rectangle.area()}")
print("Rectangle perimeter: {rectangle.perimeter()}")
print("Rectangle color: {rectangle.color}")

circle = Circle(3, "blue")
print(f"Cicle area {circle.area()}")
print(f"Cicle perimeter {circle.perimeter()}")
print(f"Cicle color {circle.color}")

process_my_color(rectangle)
process_my_color(circle)

    