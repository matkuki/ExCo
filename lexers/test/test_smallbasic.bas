' SmallBasic test file for lexer testing

' Variables and assignment
name = "John"
age = 30
isActive = true

' Arrays
arr[0] = 1
arr[1] = 2
arr[2] = 3

' For loop
For i = 1 To 10
  Print i
Next

' While loop
While x < 100
  x = x + 1
Wend

' If statement
If age > 18 Then
  Print "Adult"
Else
  Print "Minor"
EndIf

' Subroutines
Sub SayHello()
  Print "Hello!"
EndSub

' Functions
Function Add(a, b)
  Return a + b
EndFunction

' Math
result = Add(5, 10)
Print result

' String operations
text = "Hello"
Print Upper(text)
Print Lower(text)

' Input
' Input "Enter your name: ", name

' Select case
Select Case age
Case 0..12
  Print "Child"
Case 13..19
  Print "Teen"
Case Else
  Print "Adult"
EndSelect

' Comments
' This is a comment

Print "Program completed"
