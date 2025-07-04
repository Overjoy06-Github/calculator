from customtkinter import *
from PIL import Image
import pywinstyles

app = CTk()
width = 500
height = 700
app.geometry(f"{width}x{height}")
app.resizable(False, False)
FontManager.load_font("font/Dosis-ExtraLight.ttf")

bg_image = CTkImage(Image.open("images/background.png"), size=(width, height))
bg_label = CTkLabel(app, image=bg_image, text="")
bg_label.place(relwidth=1, relheight=1)

calculator_frame = CTkFrame(app, width=width-100, height=height-100, corner_radius=15, bg_color="#59599B")
calculator_frame.place(relx=0.5, rely=0.5, anchor="center")
pywinstyles.set_opacity(calculator_frame, value=0.5, color="#59599B")

entry_var = StringVar(value="0")
current_value = ""
operator = None
operand1 = None
history_var = StringVar(value="")
history_label = CTkEntry(
    app,
    textvariable=history_var,
    font=("Dosis", 20),
    width=350,
    height=30,
    border_width=0,
    corner_radius=0,
    fg_color="#000001",
    text_color="#000000",
    justify="right",
    state="readonly"
)
pywinstyles.set_opacity(history_label, value=0.9, color="#000001")
history_label.place(x=75, y=50)

screen = CTkEntry(app, textvariable=entry_var, justify="right", width=350, height=100, corner_radius=15, state="readonly", font=("Dosis", 55), bg_color="#000001", border_color="#FFFFFF")
pywinstyles.set_opacity(screen, value=0.9, color="#000001")
screen.place(x=75, y=75)


def clear_all():
    global current_value
    entry_var.set("0")
    current_value = ""
    history_var.set("")
    

def set_operator(op):
    global operator, operand1, current_value
    try:
        operand1 = float(current_value.replace(",", ""))
    except ValueError:
        operand1 = 0

    if operand1 == int(operand1):
        operand1 = int(operand1)

    formatted_op1 = f"{operand1:,}"
    if len(formatted_op1) > 10:
        formatted_op1 = f"{operand1:.6e}"

    operator = op
    history_var.set(f"{formatted_op1} {op}")
    current_value = ""
    entry_var.set("")


def add_value(num):
    global current_value
    num = str(num)

    if len(current_value) >= 10:
        return

    if entry_var.get() == "0":
        current_value = num
    else:
        current_value += num

    try:
        value = float(current_value) if '.' in current_value else int(current_value)
        entry_var.set(f"{value:,}")
    except ValueError:
        entry_var.set(current_value)


def calculate_result():
    global operator, operand1, current_value
    try:
        operand2 = float(current_value.replace(",", ""))
    except ValueError:
        operand2 = 0

    result = 0
    if operator == "+":
        result = operand1 + operand2
    elif operator == "-":
        result = operand1 - operand2
    elif operator == "*":
        result = operand1 * operand2
    elif operator == "/":
        result = operand1 / operand2 if operand2 != 0 else "Error"

    if isinstance(result, (int, float)) and result != "Error":
        if result == int(result):
            result = int(result)

        formatted_result = f"{result:,}"
        if len(formatted_result) > 10:
            formatted_result = f"{result:.6e}"

        entry_var.set(formatted_result)
        current_value = str(result)

        formatted_op1 = f"{operand1:,}"
        formatted_op2 = f"{operand2:,}"
        if len(formatted_op1) > 10:
            formatted_op1 = f"{operand1:.6e}"
        if len(formatted_op2) > 10:
            formatted_op2 = f"{operand2:.6e}"

        history_var.set(f"{formatted_op1} {operator} {formatted_op2} = ")
    else:
        entry_var.set("Error")
        history_var.set(f"{operand1} {operator} {operand2} = Error")
        current_value = ""

    operator = None
    operand1 = None


def delete_last():
    global current_value
    current_value = current_value[:-1]
    if not current_value:
        current_value = "0"

    try:
        value = float(current_value) if '.' in current_value else int(current_value)
        entry_var.set(f"{value:,}")
    except ValueError:
        entry_var.set(current_value)


division_img = CTkImage(light_image=Image.open("images/division.png"), size=(35, 35))
multiplication_img = CTkImage(light_image=Image.open("images/multiplication.png"), size=(35, 35))
addition_img = CTkImage(light_image=Image.open("images/addition.png"), size=(35, 35))
subtraction_img = CTkImage(light_image=Image.open("images/subtraction.png"), size=(35, 35))
equal_img = CTkImage(light_image=Image.open("images/equal.png"), size=(35, 35))

arithmetic_buttons = [
    {
        "text": "C", "x": 75, "y": 200, "width": 150, "command": clear_all
    },
    {
        "text": "DEL", "x": 260, "y": 200, "width": 1, "command": delete_last
    },
    {
        "text": "", "x": 356, "y": 200, "width": 1, "image": division_img, "fg_color": "#ff5757", "command": lambda: set_operator("/")
    },
    {
        "text": "", "x": 356, "y": 285, "width": 1, "image": multiplication_img, "fg_color": "#ff5757", "command": lambda: set_operator("*")
    },
    {
        "text": "", "x": 356, "y": 370, "width": 1, "image": subtraction_img, "fg_color": "#ff5757", "command": lambda: set_operator("-")
    },
    {
        "text": "", "x": 356, "y": 455, "width": 1, "image": addition_img, "fg_color": "#ff5757", "command": lambda: set_operator("+")
    },
    {
        "text": "", "x": 356, "y": 540, "width": 1, "image": equal_img, "fg_color": "#ff5757", "command": calculate_result
    },
    {
        "text": "0", "x": 75, "y": 540, "width": 150, "command": lambda: add_value(0)
    },
]

base_style = {
    "height": 50,
    "corner_radius": 15,
    "bg_color": "#000001",
    "border_color": "#FFFFFF",
    "font": ("Dosis", 35),
    "fg_color": "#FFFFFF",
    "text_color": "#000000"
}

for config in arithmetic_buttons:
    style = base_style.copy()
    style.update({
        "text": config.get("text", ""),
        "width": config.get("width", 1),
        "image": config.get("image", None),
        "fg_color": config.get("fg_color", base_style["fg_color"]),
        "command": config.get("command", lambda: None)
    })
    btn = CTkButton(app, **style)
    btn.place(x=config["x"], y=config["y"])
    pywinstyles.set_opacity(btn, value=0.9, color="#000001")
    
buttons_data = [
    {"value": 1, "x": 75,  "y": 455},
    {"value": 2, "x": 176, "y": 455},
    {"value": 3, "x": 275, "y": 455},
    {"value": 4, "x": 75,  "y": 370},
    {"value": 5, "x": 176, "y": 370},
    {"value": 6, "x": 275, "y": 370},
    {"value": 7, "x": 75,  "y": 285},
    {"value": 8, "x": 176, "y": 285},
    {"value": 9, "x": 275, "y": 285},
    {"value": ".", "x": 275, "y": 540}
]

button_style = {
    "width": 50,
    "height": 50,
    "corner_radius": 15,
    "bg_color": "#000001",
    "border_color": "#FFFFFF",
    "font": ("Dosis", 35),
    "fg_color": "#FFFFFF",
    "text_color": "#000000"
}

for data in buttons_data:
    btn = CTkButton(app,
                    text=str(data["value"]),
                    command=lambda v=data["value"]: add_value(v),
                    **button_style)
    btn.place(x=data["x"], y=data["y"])
    pywinstyles.set_opacity(btn, value=0.9, color="#000001")


def handle_keypress(event):
    key = event.char
    keysym = event.keysym

    if key == "":
        return

    if key.isdigit():
        add_value(key)
    elif key == ".":
        add_value(".")
    elif key in "+-*/":
        set_operator(key)
    elif keysym in ("Return", "Equal"):
        calculate_result()
    elif keysym == "BackSpace":
        delete_last()
    elif keysym in ("Escape", "Delete", "c", "C"):
        clear_all()

app.bind("<Key>", handle_keypress)

app.mainloop()