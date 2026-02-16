#!/usr/bin/env python3
"""
Python test file for lexer testing.
This file contains various Python constructs to test syntax highlighting.
"""

import os
import sys
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from functools import wraps


@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None


def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


class Animal:
    """Base class for animals."""

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    def speak(self) -> str:
        """Make a sound."""
        return "..."

    def __str__(self) -> str:
        return f"{self.name} ({self.species})"


class Dog(Animal):
    """Dog class inheriting from Animal."""

    def __init__(self, name: str, breed: str):
        super().__init__(name, "Canis familiaris")
        self.breed = breed

    def speak(self) -> str:
        return "Woof!"

    def fetch(self, item: str) -> str:
        return f"{self.name} fetches the {item}"


class Cat(Animal):
    """Cat class inheriting from Animal."""

    def __init__(self, name: str, color: str):
        super().__init__(name, "Felis catus")
        self.color = color

    def speak(self) -> str:
        return "Meow!"

    def purr(self) -> str:
        return f"{self.name} purrs contentedly"


def list_animals(animals: List[Animal]) -> None:
    """List all animals and their sounds."""
    for animal in animals:
        print(f"{animal}: {animal.speak()}")


def process_data(data: Dict[str, Any]) -> List[str]:
    """Process dictionary data and return formatted strings."""
    results = []
    for key, value in data.items():
        results.append(f"{key}: {value}")
    return results


def decorator_example(func):
    """Example decorator function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result

    return wrapper


@decorator_example
def example_function(x: int, y: int = 10) -> int:
    """Example function with decorator."""
    return x + y


def main():
    """Main function to demonstrate Python features."""
    # Create instances
    person = Person("John", 30, "john@example.com")
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers", "Orange")

    # Print information
    print(person)
    print(dog)
    print(cat)

    # Use list
    animals = [dog, cat]
    list_animals(animals)

    # Use dictionary
    data = {"name": "Test", "value": 42, "active": True, "items": [1, 2, 3]}
    results = process_data(data)
    for r in results:
        print(r)

    # Call decorated function
    result = example_function(5, 15)
    print(f"Result: {result}")

    # List comprehension
    squares = [x**2 for x in range(10)]
    print(f"Squares: {squares}")

    # Dictionary comprehension
    cube = {x: x**3 for x in range(5)}
    print(f"Cubes: {cube}")

    # Generator expression
    gen = (x**2 for x in range(5))
    print(f"Generator: {list(gen)}")

    # Exception handling
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")
    finally:
        print("Done")

    # With statement
    with open("test.txt", "w") as f:
        f.write("Hello, World!")

    # Lambda functions
    add = lambda a, b: a + b
    print(f"Lambda add: {add(3, 4)}")

    # Filter and map
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    doubled = list(map(lambda x: x * 2, numbers))
    print(f"Evens: {evens}")
    print(f"Doubled: {doubled}")


if __name__ == "__main__":
    main()
