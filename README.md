# Calculator for Mathematicians

A dark, modern scientific calculator built with CustomTkinter for precise math work. Supports degree-based trigonometry, factorials, logarithms, constants, keyboard input, and formatted results — designed for mathematicians, students, and power users. 🎯🔢

## Features
- Degree-mode trig: Sin, Cos, Tan (automatically converts degrees → radians) 🔁
- Constants: π, e
- Factorial with integer validation: `x!` → `math.factorial` 🧮
- Logarithms: `Log` (base 10), `ln` (natural log)
- Exponentiation (`x^y` → `**`), percent, parentheses
- Big entry screen, responsive button grid, Clear (C), Delete (DEL), and large `=` button
- Keyboard support: numbers, operators, Enter (evaluate), Backspace (delete), Escape/C to clear ⌨️
- Safer evaluation environment and formatted numeric output (trims floating-point noise) 🔒

## Requirements
- Python 3.8+
- customtkinter
- (standard library: `math`)

Install dependency:
```bash
pip install customtkinter
```

CustomTkinter docs: [CustomTkinter GitHub](https://github.com/TomSchimansky/CustomTkinter)

## Usage
1. Clone or copy the script into a file, e.g. `calculator.py`.
2. Install dependencies (see above).
3. Run:
```bash
python calculator.py
```

Enter expressions using buttons or keyboard. Examples:
- `Sin(30)` → `math.sin(convert_angle(30))`
- `5x!` → `5math.factorial(…)` (use buttons to build factorial)
- `ln(2.718281828)` → natural log

If evaluation fails, the screen shows `Error`. Check for mismatched parentheses or invalid factorial inputs (factorial requires non-negative integers).

## Keyboard Shortcuts
- Numbers: `0`–`9`
- Operators: `+`, `-`, `*`, `/`, `.`
- Parentheses: `(`, `)`
- Enter / Numpad Enter: evaluate
- Backspace / `d` / `D`: delete last character
- Escape / `c` / `C`: clear

## Security & Limitations
The app uses a restricted `eval` environment exposing only `math` and `convert_angle`. Still avoid entering untrusted code. Factorial handling validates integer input before computing. Complex expressions relying on arbitrary builtins are not allowed.

## Contributing
Contributions, bug reports, and feature requests are welcome. Please open issues or PRs if hosting in a repository.

## License
MIT License — feel free to reuse and adapt.