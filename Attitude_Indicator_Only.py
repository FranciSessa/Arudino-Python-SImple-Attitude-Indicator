# Code by Francesco Sessa
import tkinter as tk
import math

# -------some utility functions-------
def rotate_point(x, y, angle_deg, cx, cy):
    #Rotate a point around (cx, cy) by angle_deg degrees clockwise.
    angle_rad = math.radians(angle_deg)
    dx = x - cx
    dy = y - cy
    xr = dx * math.cos(angle_rad) - dy * math.sin(angle_rad) + cx
    yr = dx * math.sin(angle_rad) + dy * math.cos(angle_rad) + cy
    return xr, yr

def translate_point(x, y, dx, dy):
    #Translate a point by (dx, dy).
    return x + dx, y + dy

# -------create the root window-------
root = tk.Tk() # create the root window, every tkinter program must have exactly one root window
root.title('Indicatore di Assetto') # set the title of the root window
root.geometry('850x600+300+50') # set the size of the root window, width x height + x_offset + y_offset (position on the screen)
root.configure(bg='darkgrey') # set the background color of the root window
root.resizable(False,False) # set the root window to not be resizable

# -------create the widgets-------
title = tk.Label(root,text='Indicatore di Assetto',font=('Arial 24 bold'),fg='red',bg='darkgrey') # create a label for the title of the window
# roll (it should be between -180 and 180 degrees)
roll_value_var = tk.StringVar() # create a string variable to hold the roll value
roll_value_var.set('0') # set the initial value of the roll variable
roll_inp= tk.Entry(root,textvariable=roll_value_var,font=('Arial 20 bold'),fg='blue',justify='left',bg='lightgrey') # create an entry widget for the roll input
roll_inp_label = tk.Label(root,text='Roll:',font=('Arial 20 bold'),fg='blue',anchor='w',justify='left',bg='darkgrey') # create a label for the roll
# pitch (it should be between -90 and 90 degrees)
pitch_value_var = tk.StringVar() # create a string variable to hold the roll value
pitch_value_var.set('0') # set the initial value of the pitch variable
pitch_inp= tk.Entry(root,textvariable=pitch_value_var,font=('Arial 20 bold'),fg='orange',justify='left',bg='lightgrey') # create an entry widget for the pitch input
pitch_inp_label = tk.Label(root,text='Pitch:',font=('Arial 20 bold'),fg='orange',anchor='w',justify='left',bg='darkgrey') # create a label for the pitch
# heading (it should be between 0 and 360 degrees)
heading_value_var = tk.StringVar() # create a string variable to hold the heading value
heading_value_var.set('0') # set the initial value of the heading variable
heading_inp= tk.Entry(root,textvariable=heading_value_var,font=('Arial 20 bold'),fg='purple',justify='left',bg='lightgrey') # create an entry widget for the heading input
heading_inp_label = tk.Label(root,text='Heading:',font=('Arial 20 bold'),fg='purple',anchor='w',justify='left',bg='darkgrey') # create a label for the heading

# create the canvas for the attitude indicator
attit_width = 400 # set the width of the roll indicator canvas
attit_height = 400 # set the height of the roll indicator canvas
attit_indicator = tk.Canvas(root,width=attit_width,height=attit_height,bg='white',highlightthickness=0) # create the canvas for the roll indicator
center_x_att = attit_width / 2
center_y_att = attit_height / 2 # a little shift due to the canva widget that add a bit of space under (at theta=90 must be all blue)
# Initial sky and ground as polygons (covering the whole canvas)
sky_coords = [
    (0, 0),
    (attit_width*1.5, 0),
    (attit_width*1.5, attit_height),
    (0, attit_height)
]
ground_coords = [
    (-attit_width, center_y_att),
    (attit_width*2, center_y_att),
    (attit_width*2, attit_height*2),
    (-attit_width, attit_height*2)
] # it has to be larger than the canvas to cover the whole ground area even when rotated
# Draw polygons and keep their IDs
sky_id = attit_indicator.create_polygon(*sum(sky_coords, ()), fill='lightblue', outline='')
ground_id = attit_indicator.create_polygon(*sum(ground_coords, ()), fill='brown', outline='')
midpoint_id=attit_indicator.create_oval(attit_width/2-2,center_y_att-2,attit_width/2+2,center_y_att+2,fill='red') # create a circle in the center of the canvas
# To flatten the list of pairs, the code uses sum(sky_coords, ()) and sum(ground_coords, ()). 
# Here, sum is called with an empty tuple as the starting value, which effectively concatenates 
# all the coordinate pairs into a single tuple. For example, sum([(1, 2), (3, 4)], ()) results 
# in (1, 2, 3, 4). The * operator then unpacks this tuple into individual arguments for create_polygon.
# draw the pitch and roll lines
line_roll_coords=[(center_x_att,center_y_att-170),(center_x_att,center_y_att-200)]
line_roll_id=attit_indicator.create_line(*sum(line_roll_coords, ()),fill='blue',width=3)
theta_line_coords = [(attit_width/4,center_y_att),(attit_width*3/8,center_y_att)]
theta_line_id=attit_indicator.create_line(*sum(theta_line_coords, ()),fill='orange',width=3)
# Draw the fixed lines and center dot
attit_indicator.create_line(attit_width/4,center_y_att,attit_width*3/4,center_y_att,fill='black',width=3) # create an horizontal line in the center of the canvas
attit_indicator.create_line(attit_width/2,center_y_att,attit_width/2,attit_height,fill='black',width=1) # create a vertical line in the center of the canvas
attit_indicator.create_oval(attit_width/2-5,center_y_att-5,attit_width/2+5,center_y_att+5,fill='black') # create a circle in the center of the canvas
attit_indicator.create_oval(-100,-100,attit_width+100,center_y_att*2+100,fill='',outline='darkgray',width=200)
attit_indicator.create_oval(1,1,attit_width-1,center_y_att*2-1,fill='',outline='black',width=3)
attit_indicator.create_line(*sum(line_roll_coords, ()),fill='black',width=3)

# create the canvas for the heading indicator
head_width = 400 # set the width of the heading indicator canvas
head_height = 400 # set the height of the heading indicator canvas
head_indicator = tk.Canvas(root,width=head_width,height=head_height,bg='darkgrey',highlightthickness=0) # create a canvas for the heading indicator
center_x_head = head_width / 2
center_y_head = head_height / 2
# Draw the heading indicator 
r_head = 190 # radius of the heading indicator circle
head_indicator.create_oval(center_x_head-r_head, center_y_head-r_head, center_x_head+r_head, center_y_head+r_head, fill='lightblue', outline='black', width=2) # create a circle in the center of the canvas
# Draw the heading lines
for angle in range(0, 360, 30): # draw lines every 30 degrees
    x1, y1 = rotate_point(center_x_head, center_y_head+(r_head-8), angle, center_x_head, center_y_head)
    x2, y2 = rotate_point(center_x_head, center_y_head+r_head, angle, center_x_head, center_y_head)
    head_indicator.create_line(x1, y1, x2, y2, fill='black', width=1) # create a line from the circle to the edge of the canvas
# Draw the heading text
for angle in range(0, 360, 30): # draw text every 30 degrees
    x, y = rotate_point(center_x_head, center_y_head+(r_head-20), 180-angle, center_x_head, center_y_head)
    head_indicator.create_text(x, y, text=str(angle), fill='black', font=('Arial', 10)) # create a text at the edge of the canvas
# draw the fuselage, wing and tail
fus_ID= head_indicator.create_line(center_x_head, center_y_head+70, center_x_head, center_y_head-30, fill='darkgrey', width=16,capstyle='round') # create a vertical line in the center of the canvas
wing_length = 120
wing_ID= head_indicator.create_line(center_x_head-wing_length/2, center_y_head, center_x_head+wing_length/2, center_y_head, fill='grey', width=14,capstyle='round')
tail_length = 50
tail_ID = head_indicator.create_line(center_x_head-tail_length/2, center_y_head+60, center_x_head+tail_length/2, center_y_head+60, fill='grey', width=10,capstyle='round')
# Functions to update the attitude indicator and the heading indicator
def update_attitude(*args):
    try:
        phi = float(roll_value_var.get())
        theta = float(pitch_value_var.get())
    except ValueError:
        return
    # Rotate sky and ground polygons
    new_center_x, new_center_y = translate_point(center_x_att, center_y_att, 0, center_y_att*math.sin(math.radians(theta))) 
    traslated_ground_coords = [translate_point(x, y, 0, center_y_att*math.sin(math.radians(theta))) for x, y in ground_coords]
    new_ground = [rotate_point(x, y, -phi, new_center_x, new_center_y) for x, y in traslated_ground_coords]
    attit_indicator.coords(ground_id, *sum(new_ground, ()))
    #rotate roll line
    new_roll_line_coords = [rotate_point(x, y, -phi, center_x_att,center_y_att) for x, y in line_roll_coords]
    attit_indicator.coords(line_roll_id, *sum(new_roll_line_coords, ())) # update the roll line
    # translate pitch line
    new_theta_line_coords =[translate_point(x, y, 0, center_y_att*math.sin(math.radians(theta))) for x, y in theta_line_coords] 
    attit_indicator.coords(theta_line_id, *sum(new_theta_line_coords, ())) # update the theta line
def update_heading(*args):
    try:
        heading = float(heading_value_var.get())
    except ValueError:
        return
    # Calculate the fus coords
    x1, y1 = rotate_point(center_x_head, center_y_head -70, 180-heading, center_x_head, center_y_head) 
    x2, y2 = rotate_point(center_x_head, center_y_head +30, 180-heading, center_x_head, center_y_head) 
    # Calculate the wing coords
    wing_x1, wing_y1 = rotate_point(center_x_head-wing_length/2, center_y_head, 180-heading, center_x_head, center_y_head) # wing start pointù
    wing_x2, wing_y2 = rotate_point(center_x_head+wing_length/2, center_y_head, 180-heading, center_x_head, center_y_head) # wing end point
    # Calculate the tail coords
    tail_x1, tail_y1 = rotate_point(center_x_head-tail_length/2, center_y_head-60, 180-heading, center_x_head, center_y_head) # tail start point
    tail_x2, tail_y2 = rotate_point(center_x_head+tail_length/2, center_y_head-60, 180-heading, center_x_head, center_y_head) # tail end point
    # Update the fuselage, wing and tail lines
    head_indicator.coords(fus_ID, x1, y1, x2, y2) 
    head_indicator.coords(wing_ID, wing_x1, wing_y1, wing_x2, wing_y2) 
    head_indicator.coords(tail_ID, tail_x1, tail_y1, tail_x2, tail_y2) 

# Add a trace to the variables to update the attitude indicator when the value changes
roll_value_var.trace_add('write', update_attitude)
pitch_value_var.trace_add('write', update_attitude)
heading_value_var.trace_add('write', update_heading)

# -------pack the widgets-------
title.grid(row=0, column=0, columnspan=8, sticky='n')
roll_inp_label.grid(row=1, column=0, sticky='n')
roll_inp.grid(row=1, column=1, sticky='n')
pitch_inp_label.grid(row=2, column=0, sticky='n')
pitch_inp.grid(row=2, column=1, sticky='n')
attit_indicator.grid(row=4, column=0,padx=10)
heading_inp_label.grid(row=3, column=0, sticky='n')
heading_inp.grid(row=3, column=1, sticky='n')
head_indicator.grid(row=4, column=1)

# -------start the main loop-------
root.mainloop()