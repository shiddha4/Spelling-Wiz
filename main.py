# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
#


class Person:
    def __init__(self, name, age):
        self.age = age
        self.name = name
    def __init__(self,name,age,sex):
        self.age=age
        self.name=name
        self.sex = sex


    def info(self):
        return (f'{self.name} is {self.age} years old')



p1=Person('suren',2)
print(p1.info())












