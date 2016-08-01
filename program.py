import sys


class Encoder:
    species = 'Homo Sapiens'

    def __init__(self):
        self.name = 'neelava'
        self.age = '29'

    def print_name(self):
        print(self.name)

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age


e = Encoder()
e.print_name()
#e.age=5
print(e.age)
print(type(e))
