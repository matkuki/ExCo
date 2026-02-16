-- Zig test file for lexer testing.
-- This file contains various Zig constructs to test syntax highlighting.

const std = @import("std");
const fmt = std.fmt;
const testing = std.testing;

const Person = struct {
    name: []const u8,
    age: u32,
    email: ?[]const u8,
};

fn greet(person: Person) void {
    std.debug.print("Hello, {}!\n", .{person.name});
}

fn fibonacci(n: u32) u32 {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

const Animal = union(enum) {
    Dog: Dog,
    Cat: Cat,
};

const Dog = struct {
    name: []const u8,
    breed: []const u8,
};

const Cat = struct {
    name: []const u8,
    color: []const u8,
};

fn speak(animal: Animal) []const u8 {
    switch (animal) {
        .Dog => |d| std.debug.print("{} says Woof!\n", .{d.name}),
        .Cat => |c| std.debug.print("{} says Meow!\n", .{c.name}),
    }
}

fn add(a: i32, b: i32) i32 {
    return a + b;
}

fn max(comptime T: type, a: T, b: T) T {
    if (a > b) {
        return a;
    }
    return b;
}

test "basic math" {
    try testing.expect(add(2, 2) == 4);
}

test "fibonacci" {
    try testing.expect(fibonacci(0) == 0);
    try testing.expect(fibonacci(1) == 1);
    try testing.expect(fibonacci(10) == 55);
}

pub fn main() void {
    // Variables
    var x: i32 = 5;
    const y: i32 = 10;
    const sum = x + y;
    std.debug.print("Sum: {}\n", .{sum});

    // Mutable
    x = 7;
    std.debug.print("X: {}\n", .{x});

    // Structs
    const person = Person{
        .name = "John",
        .age = 30,
        .email = "john@example.com",
    };
    greet(person);

    // Arrays
    const arr = [_]i32{ 1, 2, 3, 4, 5 };
    for (arr) |num| {
        std.debug.print("Number: {}\n", .{num});
    }

    // Slices
    const slice = arr[1..4];
    std.debug.print("Slice: {} {} {}\n", .{slice[0], slice[1], slice[2]});

    // Pointers
    var value: i32 = 42;
    const ptr = &value;
    std.debug.print("Pointer: {}\n", .{ptr.*});

    // Optionals
    var maybe: ?i32 = null;
    maybe = 42;
    if (maybe) |v| {
        std.debug.print("Value: {}\n", .{v});
    }

    // Error handling
    const result: anyerror!i32 = 42;
    result catch |err| {
        std.debug.print("Error: {!}\n", .{err});
    };

    // Switch
    const num: u32 = 3;
    switch (num) {
        1 => std.debug.print("One\n", .{}),
        2 => std.debug.print("Two\n", .{}),
        else => std.debug.print("Other\n", .{}),
    }

    // While
    var count: u32 = 0;
    while (count < 5) : (count += 1) {
        std.debug.print("Count: {}\n", .{count});
    }

    // For
    for (0..5) |i| {
        std.debug.print("I: {}\n", .{i});
    }

    // Enums
    const Color = enum {
        red,
        green,
        blue,
    };
    const color = Color.green;
    switch (color) {
        .red => std.debug.print("Red\n", .{}),
        .green => std.debug.print("Green\n", .{}),
        .blue => std.debug.print("Blue\n", .{}),
    }

    // Tagged union
    const Message = union(enum) {
        quit,
        move: struct { x: i32, y: i32 },
        write: []const u8,
    };
    const msg = Message{ .move = .{ .x = 10, .y = 20 } };
    switch (msg) {
        .quit => std.debug.print("Quit\n", .{}),
        .move => |m| std.debug.print("Move to ({}, {})\n", .{ m.x, m.y }),
        .write => |w| std.debug.print("Write: {}\n", .{w}),
    }

    // Comptime
    const computed = comptime fibonacci(10);
    std.debug.print("Computed: {}\n", .{computed});

    // Anonymous struct
    const Point = struct { x: f32, y: f32 };
    const point = Point{ .x = 1.5, .y = 2.5 };
    std.debug.print("Point: ({}, {})\n", .{ point.x, point.y });

    // Bit fields
    const Flags = packed struct {
        a: bool,
        b: bool,
        c: bool,
    };
    const flags = Flags{ .a = true, .b = false, .c = true };
    std.debug.print("Flags: {} {} {}\n", .{ flags.a, flags.b, flags.c });

    std.debug.print("Program completed!\n", .{});
}
