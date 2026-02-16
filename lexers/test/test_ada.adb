-- Ada test file for lexer testing.
-- This file contains various Ada constructs to test syntax highlighting.

with Ada.Text_IO;
with Ada.Integer_Text_IO;
with Ada.Float_Text_IO;

procedure Main is

   -- Types
   type Day is (Mon, Tue, Wed, Thu, Fri, Sat, Sun);
   
   type Vector is array (Positive range <>) of Integer;
   
   type Matrix is array (Positive range <>, Positive range <>) of Float;
   
   type Person is record
      Name : String(1..50);
      Age : Natural;
      Email : String(1..100);
   end record;
   
   -- Variables
   Counter : Integer := 0;
   Name : String(1..50);
   
   -- Subprograms
   function Add(A, B : Integer) return Integer is
   begin
      return A + B;
   end Add;
   
   function Fibonacci(N : Positive) return Natural is
   begin
      if N = 1 or N = 2 then
         return 1;
      else
         return Fibonacci(N-1) + Fibonacci(N-2);
      end if;
   end Fibonacci;
   
   procedure Swap(A, B : in out Integer) is
      Temp : Integer;
   begin
      Temp := A;
      A := B;
      B := Temp;
   end Swap;
   
begin
   -- Simple statements
   Counter := Counter + 1;
   Ada.Text_IO.Put_Line("Hello, World!");
   
   -- If statement
   if Counter > 10 then
      Ada.Text_IO.Put_Line("Counter is greater than 10");
   elsif Counter > 5 then
      Ada.Text_IO.Put_Line("Counter is greater than 5");
   else
      Ada.Text_IO.Put_Line("Counter is 5 or less");
   end if;
   
   -- Case statement
   case Counter is
      when 1 => Ada.Text_IO.Put_Line("One");
      when 2 => Ada.Text_IO.Put_Line("Two");
      when others => Ada.Text_IO.Put_Line("Other");
   end case;
   
   -- Loop statements
   for I in 1..10 loop
      Ada.Integer_Text_IO.Put(I);
      Ada.Text_IO.New_Line;
   end loop;
   
   while Counter < 100 loop
      Counter := Counter + 1;
   end loop;
   
   -- Arrays
   declare
      Arr : Vector(1..5) := (1, 2, 3, 4, 5);
   begin
      for I in Arr'Range loop
         Ada.Integer_Text_IO.Put(Arr(I));
      end loop;
   end;
   
   -- Records
   declare
      P : Person;
   begin
      P.Name := "John Doe              ";
      P.Age := 30;
      P.Email := "john@example.com     ";
   end;
   
   -- Exception handling
   begin
      Ada.Text_IO.Put_Line("Trying something...");
   exception
      when Constraint_Error =>
         Ada.Text_IO.Put_Line("Constraint error!");
      when others =>
         Ada.Text_IO.Put_Line("Some error!");
   end;
   
   -- Subprograms
   declare
      Result : Integer;
   begin
      Result := Add(5, 10);
      Ada.Integer_Text_IO.Put(Result);
   end;
   
   -- Function call
   Ada.Integer_Text_IO.Put(Fibonacci(10));
   
   -- Tagged types
   declare
      type Shape is tagged record
         X, Y : Float;
      end record;
      
      type Circle is new Shape with record
         Radius : Float;
      end record;
      
      C : Circle;
   begin
      C.X := 10.0;
      C.Y := 20.0;
      C.Radius := 5.0;
   end;
   
   -- Generics
   declare
      generic
         type Element is private;
      procedure Swap_Generic(A, B : in out Element);
      
      procedure Swap_Generic(A, B : in out Element) is
         Temp : Element;
      begin
         Temp := A;
         A := B;
         B := Temp;
      end Swap_Generic;
   begin
      null;
   end Main;
