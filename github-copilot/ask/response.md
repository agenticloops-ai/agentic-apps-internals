Here's a simple calculator in Python with a corresponding README.

````python
# filepath: /Users/smith/Downloads/vs-test/calculator.py

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def main():
    print("Simple Calculator")
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter choice (1/2/3/4): ")

    if choice not in ('1', '2', '3', '4'):
        print("Invalid input")
        return

    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid number input.")
        return

    if choice == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice == '3':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice == '4':
        try:
            result = divide(num1, num2)
            print(f"{num1} / {num2} = {result}")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
````

````markdown
# filepath: /Users/smith/Downloads/vs-test/README.md

# Simple Python Calculator

This is a simple command-line calculator written in Python.

## Features

- Addition
- Subtraction
- Multiplication
- Division (with zero division handling)

## Usage

1. Make sure you have Python 3 installed.
2. Run the calculator:

   ```sh
   python calculator.py
   ```

3. Follow the on-screen prompts to perform calculations.

## Example

```
Simple Calculator
Select operation:
1. Add
2. Subtract
3. Multiply
4. Divide
Enter choice (1/2/3/4): 1
Enter first number: 5
Enter second number: 3
5.0 + 3.0 = 8.0
```
````
