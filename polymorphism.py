class Animal:
    def __init__(self, courseName):
        self._courseName = courseName

    @property
    def course(self):
        return self._courseName

    @course.setter
    def course(self, courseName):
        self._courseName = courseName

    def talk(self):
        print('baby')

class Cat (Animal):
    def talk(self):
        print("meow")

class Dog (Animal):
    def talk1(self):
        print("Woof")

cat = Cat("Red")
dog = Dog("Yellow")
cat.course = 'ran'

dog.talk()
print(cat.course)


class Test:

    def __init__(self):
        self.__color = "red"

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self,clr):
        self.__color = clr



t = Test()
t.color = "yellow"

print(t.color)