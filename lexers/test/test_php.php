<?php
// PHP test file for lexer testing.
class Person {
    public string $name;
    public int $age;
    public ?string $email;
    
    public function __construct(string $name, int $age, ?string $email = null) {
        $this->name = $name;
        $this->age = $age;
        $this->email = $email;
    }
    
    public function greet(): string {
        return "Hello, {$this->name}!";
    }
    
    public static function create(string $name, int $age): self {
        return new self($name, $age);
    }
}

function add(int $a, int $b): int {
    return $a + $b;
}

$x = 5;
$y = 10;
$sum = $x + $y;
echo "Sum: $sum\n";

$arr = [1, 2, 3, 4, 5];
foreach ($arr as $value) {
    echo "Value: $value\n";
}

if ($x > 10) {
    echo "x > 10\n";
} elseif ($x > 5) {
    echo "x > 5\n";
} else {
    echo "x <= 5\n";
}

for ($i = 0; $i < 5; $i++) {
    echo "For: $i\n";
}

$add = function(int $a, int $b): int {
    return $a + $b;
};
echo $add(5, 10) . "\n";

$dog = new class implements Animal {
    public function speak(): string {
        return "Woof!";
    }
};

try {
    throw new Exception("Test error");
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
} finally {
    echo "Finally\n";
}

echo "Program completed!\n";
?>
