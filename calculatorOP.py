import customtkinter as ctk
import math

window = ctk.CTk()
window.title("Calculator for Mathematicians")
window.geometry("700x700")  # Reduced height since we removed the mode selection
window.configure(fg_color="#1e1e1e")

# --- Screen ---
screen = ctk.CTkEntry(
    window,
    font=("Arial", 36),
    width=660,
    height=80,
    justify="right",
    placeholder_text="0",
    corner_radius=12
)
screen.grid(row=0, column=0, columnspan=7, padx=15, pady=15)

# Make sure the screen can receive keyboard focus
screen.focus_set()

# --- Functions ---
def convert_angle(angle_value):
    """Convert angle from degrees to radians"""
    return math.radians(angle_value)

def delete_character():
    """Delete the last character from the screen"""
    current = screen.get()
    if current and current != "0" and current != "Error":
        if len(current) == 1:
            screen.delete(0, "end")
            screen.insert(0, "0")
        else:
            screen.delete(len(current)-1, "end")
    elif current == "Error":
        screen.delete(0, "end")
        screen.insert(0, "0")

def button_click(value):
    current = screen.get()
    if current == "0" or current == "Error":
        screen.delete(0, "end")
    
    # Handle special math functions
    if value == "Cos":
        screen.insert("end", "math.cos(convert_angle(")
    elif value == "Sin":
        screen.insert("end", "math.sin(convert_angle(")
    elif value == "Tan":
        screen.insert("end", "math.tan(convert_angle(")
    elif value == "Log":   # log base 10
        screen.insert("end", "math.log10(")
    elif value == "ln":    # natural log
        screen.insert("end", "math.log(")
    elif value == "π":
        screen.insert("end", "math.pi")
    elif value == "e":
        screen.insert("end", "math.e")
    elif value == "x^y":
        screen.insert("end", "**")
    elif value == "x!":
        # Check if there's a number before the factorial
        if current and current[-1].isdigit():
            screen.insert("end", "math.factorial(")
        else:
            # If no number before, insert factorial function with placeholder
            screen.insert("end", "math.factorial(")
    else:
        screen.insert("end", value)

def clear():
    screen.delete(0, "end")
    screen.insert(0, "0") 

def calculate():
    try:
        expression = screen.get()
        
        # Handle factorial separately as it requires integer input
        if "math.factorial(" in expression:
            # Extract the argument for factorial
            start_idx = expression.find("math.factorial(") + len("math.factorial(")
            # Find matching closing parenthesis
            paren_count = 1
            end_idx = start_idx
            while end_idx < len(expression) and paren_count > 0:
                if expression[end_idx] == '(':
                    paren_count += 1
                elif expression[end_idx] == ')':
                    paren_count -= 1
                end_idx += 1
            
            if paren_count == 0:
                # We found the complete factorial expression
                factorial_arg = expression[start_idx:end_idx-1]
                try:
                    # Evaluate the argument first
                    arg_value = eval(factorial_arg, {'math': math, 'convert_angle': convert_angle, '__builtins__': {}})
                    if arg_value >= 0 and arg_value == int(arg_value):
                        result = math.factorial(int(arg_value))
                        # Replace the factorial expression with its result
                        new_expression = expression[:expression.find("math.factorial(")] + str(result) + expression[end_idx:]
                        result = eval(new_expression, {'math': math, 'convert_angle': convert_angle, '__builtins__': {}})
                    else:
                        result = "Error"
                except:
                    result = "Error"
            else:
                result = "Error"
        else:
            # For degree mode, automatically add closing parentheses for convert_angle
            temp_expression = expression
            
            # Add closing parentheses for convert_angle functions
            convert_angle_count = temp_expression.count('convert_angle(')
            closing_count = temp_expression.count(')')
            
            # Add missing closing parentheses for convert_angle
            if convert_angle_count > 0:
                missing_parentheses = convert_angle_count - (closing_count - temp_expression.count('math.'))
                for _ in range(missing_parentheses):
                    temp_expression += ')'
            
            expression = temp_expression
            
            # Create a safe environment for evaluation
            safe_dict = {
                'math': math,
                'convert_angle': convert_angle,
                '__builtins__': {}
            }
            
            result = eval(expression, safe_dict)
        
        screen.delete(0, "end")
        
        # Format the result
        if isinstance(result, float):
            if result == int(result):
                screen.insert(0, str(int(result)))
            else:
                # Format to avoid floating point precision issues
                formatted = f"{result:.10f}".rstrip('0').rstrip('.')
                screen.insert(0, formatted)
        else:
            screen.insert(0, str(result))
            
    except Exception as e:
        screen.delete(0, "end")
        screen.insert(0, "Error")

# --- Button Layout ---
button_texts = [
    "π", "Cos", "7", "8", "9", "/", "(",
    "e", "Sin", "4", "5", "6", "*", ")",
    "x^y", "Tan", "1", "2", "3", "-", "%",
    "ln", "Log", "0", ".", "DEL", "+", "x!"
]

# --- Grid Settings ---
for i in range(7):
    window.grid_columnconfigure(i, weight=1)
for j in range(1, 8):  # Adjusted rows since we removed mode selection
    window.grid_rowconfigure(j, weight=1)

row = 1  # Start from row 1 now (0=screen)
col = 0

# --- Create Buttons ---
for text in button_texts:
    if text == "C":
        cmd = clear
        color = "#d9534f"  # Red color for Clear
    elif text == "DEL":
        cmd = delete_character
        color = "#f0ad4e"  # Orange color for Delete
    elif text == "=":
        cmd = calculate
        color = "#5cb85c"  # Green color for Equal
    else:
        cmd = lambda x=text: button_click(x)
        color = "#333333"  # Dark gray for regular buttons

    ctk.CTkButton(
        window,
        text=text,
        fg_color=color,
        font=("Arial", 20),
        corner_radius=30,
        width=80,
        height=70,
        hover_color="#444444",
        command=cmd
    ).grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

    col += 1
    if col > 6:
        col = 0
        row += 1

# --- Equal button at bottom ---
equal_btn = ctk.CTkButton(
    window,
    text="=",
    fg_color="#5cb85c",
    hover_color="#4cae4c",
    font=("Arial", 26, "bold"),
    corner_radius=20,
    width=660,
    height=70,
    command=calculate
)
equal_btn.grid(row=row, column=0, columnspan=7, padx=10, pady=(8, 15))

# --- Clear button next to Equal ---
clear_btn= ctk.CTkButton(
    window,
    text="C",
    fg_color="#d9534f",
    hover_color="#c9302c",
    font=("Arial", 20, "bold"),
    corner_radius=20,
    width=100,
    height=50,
    command=clear
)
clear_btn.grid(row=row+1, column=6, padx=10, pady=(0, 15))

# --- Degree Mode Label ---
degree_label = ctk.CTkLabel(
    window,
    text="Calculator is in DEGREE mode",
    font=("Arial", 16, "bold"),
    text_color="#5cb85c"
)
degree_label.grid(row=row+1, column=0, columnspan=7, pady=(0, 10))

# --- Keyboard Functionality ---
def key_press(event):
    key = event.keysym
    
    # Handle numbers and operators
    if key in "0123456789":
        button_click(key)
    elif key in ("plus", "KP_Add"):
        button_click("+")
    elif key in ("minus", "KP_Subtract"):
        button_click("-")
    elif key in ("asterisk", "KP_Multiply"):
        button_click("*")
    elif key in ("slash", "KP_Divide"):
        button_click("/")
    elif key == "period":
        button_click(".")
    elif key == "parenleft":
        button_click("(")
    elif key == "parenright":
        button_click(")")
    elif key in ("Return", "KP_Enter"):  # Enter key
        calculate()
    elif key == "BackSpace":
        delete_character()
    elif key == "Escape":
        clear()
    elif key == "c" or key == "C":
        clear()
    elif key == "d" or key == "D":
        delete_character()
    
    # Prevent the default behavior for these keys
    if key in ["Return", "KP_Enter", "BackSpace", "Escape"]:
        return "break"

# Bind the key events
window.bind("<Key>", key_press)
# Also bind to the screen specifically
screen.bind("<Key>", key_press)

window.mainloop()
