# AWK test file for lexer testing.
# This file contains various AWK constructs to test syntax highlighting.

BEGIN {
    print "AWK Test Program"
    x = 10
    y = 20
    sum = x + y
    print "Sum:", sum
}

# Function definition
function add(a, b) {
    return a + b
}

function multiply(a, b) {
    return a * b
}

function fibonacci(n) {
    if (n <= 1) {
        return n
    }
    return fibonacci(n-1) + fibonacci(n-2)
}

# Arrays
BEGIN {
    arr[0] = "zero"
    arr[1] = "one"
    arr[2] = "two"
    
    # Array iteration
    for (i in arr) {
        print "arr[" i "] =", arr[i]
    }
    
    # Associative arrays
    scores["Alice"] = 95
    scores["Bob"] = 87
    scores["Charlie"] = 92
    
    for (name in scores) {
        print name, "=>", scores[name]
    }
}

# Pattern matching
BEGIN {
    text = "Hello World"
    
    # String functions
    print length(text)
    print toupper(text)
    print tolower(text)
    print substr(text, 1, 5)
    print index(text, "World")
    
    # Regular expressions
    if (text ~ /Hello/) {
        print "Found Hello"
    }
    
    if (text !~ /Goodbye/) {
        print "No Goodbye"
    }
}

# Control flow
BEGIN {
    x = 5
    
    if (x > 10) {
        print "x > 10"
    } else if (x > 5) {
        print "x > 5"
    } else {
        print "x <= 5"
    }
    
    # While loop
    i = 0
    while (i < 5) {
        print i
        i++
    }
    
    # Do-while
    i = 0
    do {
        print "do:", i
        i++
    } while (i < 3)
    
    # For loop
    for (i = 0; i < 5; i++) {
        print "for:", i
    }
}

# Built-in variables
BEGIN {
    # Field separator
    FS = ","
    
    # Output field separator
    OFS = " - "
    
    # Number of fields
    print "NF:", NF
    
    # Record number
    print "NR:", NR
    
    # File name
    print "FILENAME:", FILENAME
}

# Math functions
BEGIN {
    print sqrt(16)
    print exp(1)
    print log(10)
    print sin(0)
    print cos(0)
    print int(3.7)
    print rand()
    srand(12345)
}

# String functions
BEGIN {
    s = "hello,world"
    n = split(s, parts, ",")
    print "parts:", n
    
    gsub(/o/, "0", s)
    print "gsub:", s
    
    sub(/h/, "H", s)
    print "sub:", s
    
    match(s, /l+/)
    print "match:", RSTART, RLENGTH
    
    sprintf("%.2f", 3.14159)
}

# User input
# This would require interactive input
# line = getline

END {
    print "Program finished"
    print "Total records:", NR
}
