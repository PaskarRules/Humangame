import copy
import time
import random

from functools import wraps


def logged(time_format, name_prefix=""):
    def decorator(func):
        if hasattr(func, '_logged_decorator') and func._logged_decorator:
            return func

        @wraps(func)
        def decorated_func(*args, **kwargs):
            start_time = time.time()
            print("- Running '{}' on {} ".format(
                name_prefix + func.__name__,
                time.strftime(time_format)
            ))
            result = func(*args, **kwargs)
            end_time = time.time()
            print("- Finished '{}', execution time = {:0.3f}s ".format(
                name_prefix + func.__name__,
                end_time - start_time
            ))
            return result

        decorated_func._logged_decorator = True
        return decorated_func

    return decorator


def log_everything_metaclass(class_name, parents, attributes):
    myattributes = {}
    for name, attr in attributes.items():
        myattributes[name] = attr
        if hasattr(attr, '__call__'):
            myattributes[name] = logged(
                "%b %d %Y - %H:%M:%S", class_name + "."
            )(attr)
    return type(class_name, parents, myattributes)


class Human(metaclass=log_everything_metaclass):
    """Your human."""

    def __init__(self, name, surname, gender, age, city, country):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.age = age
        self.city = city
        self.country = country
        self.tommy_status = "Unhappy"
        self.status = "Nothing"
        self.__telephone = None

    def __call__(self, *args, **kwargs):
        return copy.copy(self)

    def __str__(self):
        return f"{self.name} {self.surname}({self.gender}) live in {self.country} {self.city}."

    def _check_telephone(func):
        def wrapper(self, *args, **kwargs):
            telephone = args[0]
            if "+380" in telephone:
                telephone = telephone[4:-1]

            if len(telephone) != 8:
                telephone = None

            func(self, "+380" + telephone)

        return wrapper

    def drink(self, drink):
        self.status = "Drinking"
        self.tommy_status = "Happy"
        return f"{self.name} drinks {drink}!"

    def eat(self, food):
        self.status = "Eating"
        self.tommy_status = "Happy"
        return f"{self.name} eats {food}!"

    def walk(self):
        self.status = "Walking"
        return f"{self.name} walks."

    def run(self):
        self.status = "Running"
        return f"{self.name} runs."

    def breed(self, another_human):
        return Child(
            self.name + another_human.name,
            self.surname + another_human.surname,
            random.choice(['boy', 'girl']),
            0,
            self.city,
            self.country
        )

    @property
    def telephone(self):
        return f"{self.__telephone}"

    @telephone.setter
    @_check_telephone
    def telephone(self, telephone):
        self.__telephone = telephone


class Child(Human):
    def __init__(self, name, surname, gender, age, city, country):
        super().__init__(name, surname, gender, age, city, country)

    def run(self):
        return f"Child can't run!"

    def breed(self, another_human):
        return f"Child can't breed!"