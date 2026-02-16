// Rust test file for lexer testing.
// This file contains various Rust constructs to test syntax highlighting.

use std::collections::HashMap;
use std::fmt;
use std::io::{self, Read};

struct Person {
    name: String,
    age: u32,
    email: Option<String>,
}

impl Person {
    fn new(name: &str, age: u32) -> Self {
        Person {
            name: name.to_string(),
            age,
            email: None,
        }
    }

    fn with_email(mut self, email: &str) -> Self {
        self.email = Some(email.to_string());
        self
    }

    fn greet(&self) -> String {
        match &self.email {
            Some(email) => format!("Hello, {}! Email: {}", self.name, email),
            None => format!("Hello, {}!", self.name),
        }
    }
}

trait Animal {
    fn speak(&self) -> &str;
    fn name(&self) -> &str;
}

struct Dog {
    name: String,
    breed: String,
}

impl Dog {
    fn new(name: &str, breed: &str) -> Self {
        Dog {
            name: name.to_string(),
            breed: breed.to_string(),
        }
    }
}

impl Animal for Dog {
    fn speak(&self) -> &str {
        "Woof!"
    }

    fn name(&self) -> &str {
        &self.name
    }
}

struct Cat {
    name: String,
    color: String,
}

impl Cat {
    fn new(name: &str, color: &str) -> Self {
        Cat {
            name: name.to_string(),
            color: color.to_string(),
        }
    }
}

impl Animal for Cat {
    fn speak(&self) -> &str {
        "Meow!"
    }

    fn name(&self) -> &str {
        &self.name
    }
}

fn fibonacci(n: u32) -> u32 {
    match n {
        0 => 0,
        1 => 1,
        _ => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn factorial(n: u64) -> u64 {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}

fn process_data(data: &HashMap<String, i32>) -> Vec<String> {
    let mut results = Vec::new();
    for (key, value) in data.iter() {
        results.push(format!("{}: {}", key, value));
    }
    results
}

fn main() {
    // Variables and types
    let mut x = 5;
    let y = 10;
    let sum = x + y;
    println!("Sum: {}", sum);

    // Mutable variable
    x = 7;
    println!("X: {}", x);

    // Person struct
    let person = Person::new("John", 30).with_email("john@example.com");
    println!("{}", person.greet());

    // Animals
    let dog = Dog::new("Buddy", "Golden Retriever");
    let cat = Cat::new("Whiskers", "Orange");

    println!("{} says {}", dog.name(), dog.speak());
    println!("{} says {}", cat.name(), cat.speak());

    // Vector and iteration
    let numbers = vec![1, 2, 3, 4, 5];
    for num in &numbers {
        println!("Number: {}", num);
    }

    // HashMap
    let mut map = HashMap::new();
    map.insert("one".to_string(), 1);
    map.insert("two".to_string(), 2);
    map.insert("three".to_string(), 3);

    let results = process_data(&map);
    for r in results {
        println!("{}", r);
    }

    // Option and Result
    let some_value: Option<i32> = Some(42);
    let none_value: Option<i32> = None;

    match some_value {
        Some(v) => println!("Got value: {}", v),
        None => println!("No value"),
    }

    // Result
    let result: Result<i32, &str> = Ok(42);
    match result {
        Ok(v) => println!("Ok: {}", v),
        Err(e) => println!("Err: {}", e),
    }

    // Pattern matching
    let msg = match x {
        1 => "One",
        2 => "Two",
        n if n > 10 => "Greater than ten",
        _ => "Other",
    };
    println!("Message: {}", msg);

    // Closures
    let add = |a: i32, b: i32| a + b;
    println!("Add: {}", add(3, 4));

    let multiply = |a, b| a * b;
    println!("Multiply: {}", multiply(5, 6));

    // Iterators
    let nums = vec![1, 2, 3, 4, 5];
    let evens: Vec<_> = nums.iter().filter(|&&x| x % 2 == 0).collect();
    println!("Evens: {:?}", evens);

    let doubled: Vec<_> = nums.iter().map(|x| x * 2).collect();
    println!("Doubled: {:?}", doubled);

    // String operations
    let s1 = String::from("Hello");
    let s2 = String::from(" World");
    let s3 = s1 + &s2;
    println!("Concatenated: {}", s3);

    // Slices
    let arr = [1, 2, 3, 4, 5];
    let slice = &arr[1..4];
    println!("Slice: {:?}", slice);

    // Lifetimes
    fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
        if x.len() > y.len() {
            x
        } else {
            y
        }
    }

    let s1 = "hello";
    let s2 = "world!";
    println!("Longest: {}", longest(s1, s2));

    // Generics
    fn largest<T: PartialOrd>(list: &[T]) -> &T {
        let mut largest = &list[0];
        for item in list {
            if item > largest {
                largest = item;
            }
        }
        largest
    }

    let numbers = vec![34, 50, 25, 100, 65];
    let result = largest(&numbers);
    println!("Largest: {}", result);

    // Traits
    fn print_animal(animal: &impl Animal) {
        println!("{} says {}", animal.name(), animal.speak());
    }

    print_animal(&dog);
    print_animal(&cat);

    // Loops
    let mut count = 0;
    loop {
        count += 1;
        if count >= 5 {
            break;
        }
        println!("Count: {}", count);
    }

    // While
    let mut n = 0;
    while n < 3 {
        println!("N: {}", n);
        n += 1;
    }

    // For range
    for i in 0..5 {
        println!("I: {}", i);
    }

    // Enums
    enum Message {
        Quit,
        Move { x: i32, y: i32 },
        Write(String),
        ChangeColor(i32, i32, i32),
    }

    let msg = Message::Move { x: 10, y: 20 };
    match msg {
        Message::Quit => println!("Quit"),
        Message::Move { x, y } => println!("Move to ({}, {})", x, y),
        Message::Write(s) => println!("Write: {}", s),
        Message::ChangeColor(r, g, b) => println!("Color: {}, {}, {}", r, g, b),
    }

    // Error handling
    fn read_file(path: &str) -> Result<String, io::Error> {
        let mut file = std::fs::File::open(path)?;
        let mut contents = String::new();
        file.read_to_string(&mut contents)?;
        Ok(contents)
    }

    // Async (commented out as it requires async runtime)
    // async fn fetch_url(url: &str) -> Result<String, reqwest::Error> {
    //     reqwest::get(url).await?.text().await
    // }

    println!("Program completed!");
}
