# Nim test file for lexer testing.
# This file contains various Nim constructs to test syntax highlighting.

import std/[strutils, sequtils, algorithm]

type
  Person = object
    name*: string
    age*: int
    email*: string

proc newPerson(name: string, age: int, email: string = ""): Person =
  Person(name: name, age: age, email: email)

proc greet(p: Person): string =
  result = "Hello, " & p.name & "!"

proc fibonacci(n: int): int =
  if n <= 1:
    return n
  return fibonacci(n - 1) + fibonacci(n - 2)

proc add*(a, b: int): int =
  a + b

template unless*(condition: bool, body: untyped) =
  if not condition:
    body

macro unless*(condition: bool, body: untyped): untyped =
  quote:
    if not `condition`:
      `body`

type
  Animal = object of RootObj
  Dog = object of Animal
    breed*: string
  Cat = object of Animal
    color*: string

method speak(a: Animal): string {.base.} = "..."
method speak(d: Dog): string = "Woof!"
method speak(c: Cat): string = "Meow!"

proc main() =
  # Variables
  var x = 5
  let y = 10
  const z = 15
  
  echo "Sum: ", x + y
  
  # Mutable
  x = 7
  echo "X: ", x
  
  # Object
  var person = Person(name: "John", age: 30, email: "john@example.com")
  echo greet(person)
  
  # Sequences
  var nums = @[1, 2, 3, 4, 5]
  nums.add(6)
  echo "Nums: ", nums
  
  # Arrays
  var arr = [1, 2, 3, 4, 5]
  echo "Arr: ", arr
  
  # Slices
  echo "Slice: ", arr[1..3]
  
  # Sets
  var s = {1, 2, 3}
  s.incl(4)
  echo "Set: ", s
  
  # Tables
  var table = {"key1": "value1", "key2": "value2"}.toTable
  echo "Table: ", table
  
  # Control flow
  if x > 10:
    echo "x > 10"
  elif x > 5:
    echo "x > 5"
  else:
    echo "x <= 5"
  
  # Case
  case x
  of 1: echo "One"
  of 2: echo "Two"
  else: echo "Other"
  
  # For loops
  for i in 0..5:
    echo "For: ", i
  
  for i in nums:
    echo "Nums: ", i
  
  # While
  var i = 0
  while i < 5:
    echo "While: ", i
    inc i
  
  # Iterators
  iterator countup2(a, b: int): int =
    var i = a
    while i <= b:
      yield i
      inc i
  
  for i in countup2(1, 5):
    echo "Iterator: ", i
  
  # Exceptions
  try:
    raise newException(ValueError, "Test error")
  except ValueError as e:
    echo "Error: ", e.msg
  finally:
    echo "Finally"
  
  # Procs
  echo "Add: ", add(3, 4)
  
  # Methods
  var dog = Dog(breed: "Golden Retriever")
  var cat = Cat(color: "Orange")
  echo dog.speak()
  echo cat.speak()
  
  # Generics
  proc max[T](a, b: T): T =
    if a > b: a else: b
  
  echo "Max: ", max(5, 10)
  echo "Max str: ", max("apple", "banana")
  
  # Templates
  unless x == 10:
    echo "x is not 10"
  
  # Macros
  # macro defined above
  
  # Closures
  let add5 = proc(x: int): int = x + 5
  echo "Closure: ", add5(10)
  
  # Functional
  let evens = filter(numbers, x => x mod 2 == 0)
  echo "Evens: ", evens
  
  let doubled = map(numbers, x => x * 2)
  echo "Doubled: ", doubled
  
  # Discriminated unions
  type
    Message = object
      case kind: string
      of "move":
        x, y: int
      of "write":
        text: string
      of "quit":
        discard
  
  var msg = Message(kind: "move", x: 10, y: 20)
  case msg.kind
  of "move":
    echo "Move to (", msg.x, ", ", msg.y, ")"
  of "write":
    echo "Write: ", msg.text
  of "quit":
    echo "Quit"
  
  # Tuples
  var t = (name: "John", age: 30)
  echo "Tuple: ", t
  
  # Enums
  type
    Color = enum
      Red, Green, Blue
  
  let c = Red
  echo "Color: ", c
  
  echo "Program completed!"

when isMainModule:
  main()
