from tkinter import *
import time
import json

root = Tk()
root.title("Stepper Motor")
root.resizable(width=False, height=False)

x, y, z = 0, 0, 0
colorx, colory, colorz = "green", "green", "green"
yes_button = False

def create_motor_frame(parent, motor, row):
    frame = Frame(parent, width=150)
    frame.grid(row=row, column=0, columnspan=2, sticky="ns")
    Label(frame, text=f'Motor {motor}').grid(row=0, column=0)

    Label(frame, text='Acceleration').grid(row=1, column=1)
    accel_var = IntVar()
    Spinbox(frame, from_=1, to=3000, textvariable=accel_var).grid(row=2, column=1)
    Label(frame, text='mm/s²').grid(row=2, column=2)

    Label(frame, text='Speed').grid(row=3, column=1)
    speed_var = IntVar()
    Spinbox(frame, from_=1, to=3000, textvariable=speed_var).grid(row=4, column=1)
    Label(frame, text='mm/s').grid(row=4, column=2)

    Label(frame, text='Steps/mm').grid(row=5, column=1)
    column_frame = Frame(frame, width=150)
    column_frame.grid(row=6, column=1, sticky="ns")
    steps_var = IntVar()
    Spinbox(column_frame, from_=1, to=3000, width=5, textvariable=steps_var).grid(row=0, column=1)
    Label(column_frame, text='/').grid(row=0, column=2)
    mm_var = IntVar()
    Spinbox(column_frame, from_=1, to=3000, width=5, textvariable=mm_var).grid(row=0, column=3)
    Label(column_frame, text='mm').grid(row=0, column=4, columnspan=2)

    return frame

def settings():
    global settings_window
    settings_window = Toplevel(root)
    settings_window.title("Settings")
    settings_window.resizable(width=False, height=False)
    settings_window.grab_set()
    
    motors = ['X', 'Y', 'Z']
    for i, motor in enumerate(motors):
        create_motor_frame(settings_window, motor, i)
    
    Button(settings_window, text='Save', command=settings_window.destroy).grid(row=3, column=0, columnspan=2)

positions_file = "config.json"

def load_positions():
    try:
        with open(positions_file, "r") as file:
            positions = json.load(file)
    except FileNotFoundError:
        positions = {}
    
    for i in range(1, 6 + 1):
        if str(i) not in positions:
            positions[str(i)] = (0, 0, 0)
    
    return positions

def save(positions):
    with open(positions_file, "w") as file:
        json.dump(positions, file)

def save_callback(button):
    global yes_button, save_window, x, y, z
    yes_button = not yes_button
    button.coordinates = (x, y, z)
    button.config(text=f'P{button.index}*')
    save_window.destroy()

    positions = load_positions()
    positions[str(button.index)] = button.coordinates 
    save(positions)

def save_position_window(button):
    global save_window
    save_window = Toplevel(root)
    save_window.title("Save")
    save_window.resizable(width=False, height=False)
    Label(save_window, text='Do you wish to save in that position?').grid(row=0, column=0)
    save = Frame(save_window, width=150)
    save.grid(row=1, column=0)
    Button(save, text='Yes', command=lambda: save_callback(button)).grid(row=0, column=0)
    Button(save, text='No', command=save_window.destroy).grid(row=0, column=1)
    save_window.grab_set()

def on_button_press(event, button):
    button.start_time = time.time()
    button.after_id = button.after(5000, lambda: check_button_press(button))

def check_button_press(button):
    elapsed_time = time.time() - button.start_time
    if elapsed_time >= 5:
        save_position_window(button)

def on_button_release(event, button):
    global x, y, z
    elapsed_time = time.time() - button.start_time
    button.after_cancel(button.after_id)
    if elapsed_time < 5:
        if hasattr(button, 'coordinates'):
            x, y, z = button.coordinates
            update_coordinates()

def create_position_button(parent, row, col, index, positions):
    button = Button(parent, text=f'P{index}', width=8, height=4)
    button.grid(row=row, column=col)
    button.index = index
    button.coordinates = positions.get(str(index), (0, 0, 0))
    button.bind("<ButtonPress>", lambda e, b=button: on_button_press(e, b))
    button.bind("<ButtonRelease>", lambda e, b=button: on_button_release(e, b))
    return button

positions = load_positions()

def check_number():
    global x, y, z
    try:
        x = int(gotox.get())
    except ValueError:
        char_warning()
        x = 0
    try:
        y = int(gotoy.get())
    except ValueError:
        char_warning()
        y = 0
    try:
        z = int(gotoz.get())
    except ValueError:
        char_warning()
        z = 0
    update_coordinates()

def char_warning():
    warning = Toplevel(root)
    warning.resizable(width=False, height=False)
    Label(warning, text='The value is not a number! Try again.').grid(row=0, column=0)
    Button(warning, text='OK', command=warning.destroy).grid(row=1, column=0)
    warning.grab_set()

def check_limit():
    global x, y, z, colorx, colory, colorz
    limit = 3000

    if int(x) < limit:
        colorx = "green"
    else:
        x = limit
        colorx = "red"
        coordinatesx.config(text=str(x))
        limit_warning()
    checkLimitx.config(fg=colorx)

    if int(y) < limit:
        colory = "green"
    else:
        y = limit
        colory = "red"
        coordinatesy.config(text=str(y))
        limit_warning()
    checkLimity.config(fg=colory)

    if int(z) < limit:
        colorz = "green"
    else:
        z = limit
        colorz = "red"
        coordinatesz.config(text=str(z))
        limit_warning()
    checkLimitz.config(fg=colorz)

def homeMotor(x_target=None, y_target=None, z_target=None):
    global x, y, z
    x = x_target if x_target is not None else x
    y = y_target if y_target is not None else y
    z = z_target if z_target is not None else z
    update_coordinates()

def home_all():
    homeMotor(0, 0, 0)

def limit_warning():
    warning = Toplevel(root)
    warning.resizable(width=False, height=False)
    Label(warning, text='Limit Reached! Defaulting to 3000.').grid(row=0, column=0)
    Button(warning, text='OK', command=warning.destroy).grid(row=1, column=0)
    warning.grab_set()

def update_coordinates():
    global x, y, z    
    coordinatesx.config(text=str(x))
    coordinatesy.config(text=str(y))
    coordinatesz.config(text=str(z))
    check_limit()

def move_delta(dx=0, dy=0, dz=0):
    global x, y, z
    x += dx * int(jogxy.get())
    y += dy * int(jogxy.get())
    z += dz * int(jogz.get())
    update_coordinates()

def moveTo(_x=None, _y=None, _z=None):
    global x, y, z
    try:
        if _x is None and _y is None and _z is None:
            x = int(gotox.get())
            y = int(gotoy.get())
            z = int(gotoz.get())
        else:
            x = _x
            y = _y
            z = _z
    except ValueError:
        char_warning()
        x, y, z = 0, 0, 0
    check_number()

def move_up_left(): move_delta(-1, 1, 0)
def move_xy_up(): move_delta(0, 1, 0)
def move_up_right(): move_delta(1, 1, 0)
def move_left(): move_delta(-1, 0, 0)
def move_right(): move_delta(1, 0, 0)
def move_down_left(): move_delta(-1, -1, 0)
def move_xy_down(): move_delta(0, -1, 0)
def move_down_right(): move_delta(1, -1, 0)
def move_z_up(): move_delta(0, 0, 1)
def move_z_down(): move_delta(0, 0, -1)

columnleft = Frame(root, width=150)
columnleft.grid(row=0, column=0, columnspan=2, sticky="ns")

Button(columnleft, text='Go To', command=moveTo).grid(row=3, column=0)

Label(columnleft, text='X').grid(row=1, column=1)
Label(columnleft, text='Y').grid(row=1, column=2)
Label(columnleft, text='Z').grid(row=1, column=3)

columnx = Frame(columnleft, width=150)
columnx.grid(row=2, column=1, sticky="ns")
columny = Frame(columnleft, width=150)
columny.grid(row=2, column=2, sticky="ns")
columnz = Frame(columnleft, width=150)
columnz.grid(row=2, column=3, sticky="ns")

Button(columnx, text='🏠︎', width=4, command=lambda: homeMotor(0)).grid(row=2, column=1)
Button(columny, text='🏠︎', width=4, command=lambda: homeMotor(y_target=0)).grid(row=2, column=1)
Button(columnz, text='🏠︎', width=4, command=lambda: homeMotor(z_target=0)).grid(row=2, column=1)

checkLimitx = Label(columnx, text='⦿', fg=colorx, width=4)
checkLimitx.grid(row=2, column=2)
checkLimity = Label(columny, text='⦿', fg=colory, width=4)
checkLimity.grid(row=2, column=2)
checkLimitz = Label(columnz, text='⦿', fg=colorz, width=4)
checkLimitz.grid(row=2, column=2)

gotox = Spinbox(columnleft, from_=0, to=3000, textvariable=IntVar())
gotox.grid(row=3, column=1)
gotoy = Spinbox(columnleft, from_=0, to=3000, textvariable=IntVar())
gotoy.grid(row=3, column=2)
gotoz = Spinbox(columnleft, from_=0, to=3000, textvariable=IntVar())
gotoz.grid(row=3, column=3)

joystickxy = Frame(columnleft, width=150)
joystickxy.grid(row=4, column=1, columnspan=2)

Button(joystickxy, text='◤', width=10, height=5, command=move_up_left).grid(row=0, column=0)
Button(joystickxy, text='▲', width=10, height=5, command=move_xy_up).grid(row=0, column=1)
Button(joystickxy, text='◥', width=10, height=5, command=move_up_right).grid(row=0, column=2)
Button(joystickxy, text='◀', width=10, height=5, command=move_left).grid(row=1, column=0)
Label(joystickxy, text='XY', width=10, height=5).grid(row=1, column=1)
Button(joystickxy, text='▶', width=10, height=5, command=move_right).grid(row=1, column=2)
Button(joystickxy, text='◣', width=10, height=5, command=move_down_left).grid(row=2, column=0)
Button(joystickxy, text='▼', width=10, height=5, command=move_xy_down).grid(row=2, column=1)
Button(joystickxy, text='◢', width=10, height=5, command=move_down_right).grid(row=2, column=2)

joystickz = Frame(columnleft, width=150)
joystickz.grid(row=4, column=3, columnspan=2)

Button(joystickz, text='▲', width=10, height=5, command=move_z_up).grid(row=0, column=0)
Label(joystickz, text='Z', width=10, height=5).grid(row=1, column=0)
Button(joystickz, text='▼', width=10, height=5, command=move_z_down).grid(row=2, column=0)

Label(columnleft, text='Speed').grid(row=7, column=1)
Label(columnleft, text='Jog Distance').grid(row=8, column=1)
speedxy = Spinbox(columnleft, from_=1, to=1000, width=9, textvariable=IntVar())
speedxy.grid(row=7, column=1, columnspan=2)
jogxy = Spinbox(columnleft, from_=1, to=1000, width=9, textvariable=IntVar())
jogxy.grid(row=8, column=1, columnspan=2)
speedz = Spinbox(columnleft, from_=1, to=1000, textvariable=IntVar())
speedz.grid(row=7, column=3)
jogz = Spinbox(columnleft, from_=1, to=1000, textvariable=IntVar())
jogz.grid(row=8, column=3)
Label(columnleft, text='mm/s').grid(row=7, column=2)
Label(columnleft, text='mm').grid(row=8, column=2)

columnright = Frame(root, width=150)
columnright.grid(row=0, column=2, columnspan=2, sticky="ns")

Label(columnright, text='Coordinates', font=('TkDefaultFont', 12)).grid(row=0, column=0, columnspan=2)
Label(columnright, text='X', font=('TkDefaultFont', 10)).grid(row=1, column=0)
Label(columnright, text='Y', font=('TkDefaultFont', 10)).grid(row=2, column=0)
Label(columnright, text='Z', font=('TkDefaultFont', 10)).grid(row=3, column=0)
coordinatesx = Label(columnright, text=int(x), font=('TkDefaultFont', 10, 'bold'))
coordinatesx.grid(row=1, column=1)
coordinatesy = Label(columnright, text=int(y), font=('TkDefaultFont', 10, 'bold'))
coordinatesy.grid(row=2, column=1)
coordinatesz = Label(columnright, text=int(z), font=('TkDefaultFont', 10, 'bold'))
coordinatesz.grid(row=3, column=1)

for i in range(1, 7):
    create_position_button(columnright, 4 + (i-1)//2, (i-1) % 2, i, positions=positions)

Button(columnright, text='Home All', width=18, height=3, command=home_all).grid(row=7, column=0, columnspan=2)
Button(columnright, text='Settings', width=18, height=3, command=settings).grid(row=8, column=0, columnspan=2)

root.mainloop()
