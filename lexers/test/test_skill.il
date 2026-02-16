; SKILL test file for lexer testing

; Variables
name = "John"
age = 30

; Functions
procedure(add(a b)
  a + b
)

procedure(fibonacci(n)
  if n <= 1
    then n
    else fibonacci(n-1) + fibonacci(n-2)
  )
)

; Lists
myList = list(1 2 3 4 5)
car(myList)
cdr(myList)
cons(0 myList)

; Strings
str = "Hello World"
strcat("Hello " "World")
strlen(str)
substring(str 1 5)

; Conditionals
if age > 18
  then printf("Adult\n")
  else printf("Minor\n")
)

; Loops
for i 1 10
  printf("%d\n" i)
)

; Symbols
symbol = 'mySymbol
quote(symbol)

; Procedures
procedure(myFunc(x)
  printf("Value: %L\n" x)
)

; Lambda
lambda(x x+1)

; Comments
;; This is a comment
