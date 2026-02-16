MODULE Main;

IMPORT Out, In;

TYPE
  Person* = POINTER TO PersonDesc;
  PersonDesc* = RECORD
    name*: ARRAY 50 OF CHAR;
    age*: INTEGER;
    email*: ARRAY 100 OF CHAR;
  END;

VAR
  counter*: INTEGER;

PROCEDURE Add*(a, b: INTEGER): INTEGER;
BEGIN
  RETURN a + b;
END Add;

PROCEDURE Fibonacci*(n: INTEGER): INTEGER;
BEGIN
  IF n <= 1 THEN
    RETURN n;
  ELSE
    RETURN Fibonacci(n-1) + Fibonacci(n-2);
  END;
END Fibonacci;

PROCEDURE Swap*(VAR a, b: INTEGER);
VAR
  temp: INTEGER;
BEGIN
  temp := a;
  a := b;
  b := temp;
END Swap;

PROCEDURE NewPerson(name: ARRAY OF CHAR; age: INTEGER): Person;
VAR
  p: Person;
BEGIN
  NEW(p);
  p.name := name;
  p.age := age;
  p.email := "";
  RETURN p;
END NewPerson;

PROCEDURE PrintPerson(p: Person);
BEGIN
  Out.String("Name: "); Out.String(p.name); Out.Ln;
  Out.String("Age: "); Out.Int(p.age, 0); Out.Ln;
  Out.String("Email: "); Out.String(p.email); Out.Ln;
END PrintPerson;

BEGIN
  counter := 0;
  counter := counter + 1;
  Out.Int(counter, 0); Out.Ln;
  
  (* If statement *)
  IF counter > 10 THEN
    Out.String("Greater than 10"); Out.Ln;
  ELSIF counter > 5 THEN
    Out.String("Greater than 5"); Out.Ln;
  ELSE
    Out.String("5 or less"); Out.Ln;
  END;
  
  (* Case statement *)
  CASE counter OF
    1: Out.String("One"); Out.Ln;
  | 2: Out.String("Two"); Out.Ln;
  ELSE
    Out.String("Other"); Out.Ln;
  END;
  
  (* For loop *)
  FOR counter := 0 TO 10 DO
    Out.Int(counter, 0);
  END;
  Out.Ln;
  
  (* While loop *)
  WHILE counter < 100 DO
    counter := counter + 1;
  END;
  
  (* Repeat loop *)
  REPEAT
    counter := counter - 1;
  UNTIL counter = 0;
  
  (* Arrays *)
  VAR
    arr: ARRAY 10 OF INTEGER;
    i: INTEGER;
  BEGIN
    FOR i := 0 TO 9 DO
      arr[i] := i;
    END;
    
    FOR i := 0 TO 9 DO
      Out.Int(arr[i], 0);
    END;
    Out.Ln;
  END;
  
  (* Records *)
  VAR
    p: Person;
  BEGIN
    p := NewPerson("John Doe", 30);
    PrintPerson(p);
  END;
  
  (* Pointers *)
  VAR
    ptr: POINTER TO INTEGER;
  BEGIN
    NEW(ptr);
    ptr^ := 42;
    Out.Int(ptr^, 0); Out.Ln;
  END;
  
  (* Procedures *)
  Out.Int(Add(5, 10), 0); Out.Ln;
  Out.Int(Fibonacci(10), 0); Out.Ln;
  
  Out.String("Program completed"); Out.Ln;
END Main.
