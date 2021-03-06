import tkinter, random, pickle
from tkinter import ttk



def run(mode):
    global clicked_currently_names, clicked_currently_shapes, pairs_current, pairs_count, names_called, shapes_called, winner_count_label_string, winner_count, losercount, popup_canvas, has_ran
    global names_canvases, names_text, names_boxes
    global shapes_canvases, shapes_boxes, shapes_shapes
    global popup_status,timer_count, timer_time, timer_gamestate, popup_canvas_window

    window = tkinter.Toplevel()
    window.title("Simpiley Shapeily - Game Panel")
    window.geometry("1280x720")
    window.resizable(0, 0)
    window.configure(background="white")

    popup_status = 0

    global_background = "#CBE0CF"
    shape_colour = "#347E8E"
    text_colour = "#347E8E"
    border_colour = "#695C60"
    fore_colour = "#DEDDA4"

    shapes_called = []
    clicked_currently_shapes = 0
    clicked_currently_names = 0
    pairs_current = {}
    pairs_count = 0
    names_called = None
    has_ran = None

    names_canvases = {}
    names_text = {}
    names_boxes = {}
    shapes_canvases = {}
    shapes_shapes = {}
    shapes_boxes = {}

    timer_count = 0
    timer_time = 1000
    timer_gamestate = "stopped"

    # Canvas for connecting lines
    line_canvas = tkinter.Canvas(window, width=1280, height=720, bg=global_background)
    line_canvas.pack()

    # Frames storage
    shapes_frame = tkinter.Frame(window, bg=global_background)
    names_frame = tkinter.Frame(window, bg=global_background)
    popup_frame = tkinter.Frame(window, bg="white", height="5")
    winner_frame = tkinter.Frame(window, bg=global_background)

    # Win Count setup
    winner_count = 0
    winner_count_label_string = tkinter.StringVar()
    winner_count_label_string.set("Wins: 0")
    winner_count_label = tkinter.Label(winner_frame, textvariable=winner_count_label_string, fg=text_colour, background=global_background, font=("MyriadPro-Regular", 15)).grid(column=2)

    popup_canvas = tkinter.Canvas(popup_frame, width=500, height=300, bg="white", highlightthickness=1, highlightbackground=border_colour)
    popup_canvas_background = tkinter.PhotoImage(file='resources\\background.gif')
    popup_canvas.create_image(0, 0, image=popup_canvas_background, anchor="nw")
    popup_canvas.pack()


    def update_leaderboard(count):
        file = "resources/leaderboard.db"
        leaderboard_dict = pickle.load(open(file, "rb"))
        if "Empty" in leaderboard_dict:
            leaderboard_dict = {}
        leaderboard_add = popup_window_entry.get()
        if leaderboard_add == "":
            get_reset()
            return()

        leaderboard_dict[leaderboard_add] = count
        pickle.dump(leaderboard_dict, open(file, "wb"))
        get_reset()

    def init_timer():
        global shapes_canvases, shapes_shapes, timer_count, timer_time, winner_count, timer_gamestate


        if timer_count % 2 == 0:
            fill = "#695C60"

        else:
            fill = "#347E8E"

        if timer_time <= 0 and timer_gamestate == "running":
            change_fill("red")

            get_popup("loose", winner_count)
            winner_count = 0

            timer_time = 1000
            timer_count = 0

            return

        elif timer_gamestate == "running":
            if winner_count == 0:
                reduceby = 10

            elif winner_count < 6:
                reduceby = 20 * winner_count

            elif winner_count > 5:
                reduceby = 5 * winner_count

            timer_time = timer_time - reduceby
            
            window.after(timer_time, lambda: change_fill(fill))
            window.after(timer_time, lambda: init_timer())
            timer_count+= 1

    def change_fill(fill):
        if timer_gamestate != "running":
            return()

        for i in shapes_shapes:
            shapes_canvases[i].itemconfig(shapes_shapes[i], fill=fill)

    def get_popup(outcome, count):
        global popup_canvas, popup_canvas_text, popup_canvas_count, has_ran, popup_status, timer_gamestate, popup_canvas_window, popup_window_entry, popup_canvas_instruction

        popup_button = ttk.Button(popup_frame, text="Restart", command=lambda: get_reset())
        popup_button.place(rely=0.9, relx=.5,anchor="center")

        popup_status = 1

        timer_gamestate = "stopped"

        if outcome == "loose":
            if has_ran == True:
                popup_canvas.delete(popup_canvas_text)
                popup_canvas.delete(popup_canvas_count)
                try:
                    popup_canvas.delete(popup_window_entry)

                except:
                    print("l")

                try:
                    popup_canvas.delete(popup_canvas_instruction)

                except:
                    print("l")


            popup_frame.lift()
            popup_canvas_text = popup_canvas.create_text(250, 100, text="Sorry, you lost!",
                                                         font=("MyriadPro-Regular", 20))
            popup_canvas_count = popup_canvas.create_text(250, 140, text="Rounds Won: " + str(count),
                                                         font=("MyriadPro-Regular", 15))
            popup_canvas_instruction = popup_canvas.create_text(250,180, text="Enter your name", font=("MyriadPro-Regular", 12))

            popup_window_entry = tkinter.Entry(window, text="Name")
            popup_window_entry.configure(width = 10)

            popup_canvas_window = popup_canvas.create_window(250, 200, window=popup_window_entry)

            winner_count_label_string.set("Wins: 0")

            popup_button.config(text="Reset", command=lambda: update_leaderboard(count))
        elif outcome == "win":
            if has_ran == True:
                popup_canvas.delete(popup_canvas_text)
                popup_canvas.delete(popup_canvas_count)
                try:
                    popup_canvas.delete(popup_window_entry)

                except:
                    print("l")

                try:
                    popup_canvas.delete(popup_canvas_instruction)

                except:
                    print("l")

            popup_frame.lift()
            popup_canvas_text = popup_canvas.create_text(250, 100, text="Congratulations, you won!",
                                                         font=("MyriadPro-Regular", 20))
            popup_canvas_count = popup_canvas.create_text(250, 180, text="Rounds Won so far: " + str(count),
                                                         font=("MyriadPro-Regular", 15))
            popup_button.config(text="Continue")

    def check_pairs():
        global clicked_currently_shapes, clicked_currently_names, pairs_current, pairs_count, names_called, shapes_called, winner_count, timer_gamestate

        if clicked_currently_shapes and clicked_currently_names is not 0:
            pairs_current[clicked_currently_names] = clicked_currently_shapes

            Coord_X = [270, 640, 1010]
            Coord_YS = 383
            Coord_YN = 180

            shape_pos = shapes_called.index(clicked_currently_shapes)
            name_pos = names_called.index(clicked_currently_names)

            if name_pos == shape_pos:
                line_canvas.create_line(Coord_X[name_pos], Coord_YN, Coord_X[name_pos], Coord_YS, fill=border_colour)

            elif name_pos < shape_pos:
                line_canvas.create_line(Coord_X[name_pos], Coord_YN, Coord_X[name_pos], Coord_YN + 40, fill=border_colour) # Down
                line_canvas.create_line(Coord_X[name_pos], Coord_YN + 40, Coord_X[name_pos] + 150, Coord_YN + 40, fill=border_colour) # Across
                line_canvas.create_line(Coord_X[name_pos] + 150, Coord_YN + 40, Coord_X[name_pos] + 150, Coord_YS - 40, fill=border_colour) # Down
                line_canvas.create_line(Coord_X[name_pos] + 150, Coord_YS - 40, Coord_X[shape_pos], Coord_YS - 40, fill=border_colour)  # Across
                line_canvas.create_line(Coord_X[shape_pos], Coord_YS - 40, Coord_X[shape_pos],Coord_YS, fill=border_colour)  # Down

            elif name_pos > shape_pos:
                line_canvas.create_line(Coord_X[name_pos], Coord_YN, Coord_X[name_pos], Coord_YN + 70, fill=border_colour)  # Down
                line_canvas.create_line(Coord_X[name_pos], Coord_YN + 70, Coord_X[name_pos] - 150, Coord_YN + 70, fill=border_colour)  # Across
                line_canvas.create_line(Coord_X[name_pos] - 150, Coord_YN + 70, Coord_X[name_pos] - 150, Coord_YS - 70, fill=border_colour)  # Down
                line_canvas.create_line(Coord_X[name_pos] - 150, Coord_YS - 70, Coord_X[shape_pos], Coord_YS - 70, fill=border_colour)  # Across
                line_canvas.create_line(Coord_X[shape_pos], Coord_YS - 70, Coord_X[shape_pos], Coord_YS, fill=border_colour)  # Down


            clicked_currently_shapes = 0
            clicked_currently_names = 0
            pairs_count = pairs_count + 1

        if pairs_count == 3:
            matches = 0
            for key, value in pairs_current.items():
                if key == value:
                    matches = matches + 1

                else:
                    get_popup("loose", winner_count)
                    winner_count = 0
                    break

            if matches == 3:
                winner_count+=1
                get_popup("win", winner_count)
                winner_count_label_string.set("Wins: " + str(winner_count))
                timer_gamestate = "stopped"

    def get_shapes(x):
        global shapes_called
        global shapes_canvases, shapes_shapes
        global timer_gamestate

        if mode == "timed":
            timer_gamestate = "running"
            init_timer()

        shapes_list = ['square', 'triangle', 'circle', 'diamond', 'pentagon', 'hexagon', 'trapezium']
        count = 0
        shapes_called = []
        shape_padx = 100

        while count < 3: # How many shapes to display
            shape = random.choice(shapes_list)
            while shape in shapes_called: # Get unique shape (gets rid of duplicates)
                shape = random.choice(shapes_list)


            shapes_canvases[shape] = tkinter.Canvas(shapes_frame, width=170, height=170, bg=global_background, bd=0,
                                                    highlightthickness=0, relief="ridge")
            shapes_canvases[shape].grid(row=1, column=count, padx=shape_padx)


            if shape == "square":
                shapes_shapes[shape] = (shapes_canvases[shape].create_rectangle(10, 10, 160, 160, fill=shape_colour,
                                                                                outline=global_background))  # Square
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "square"))

            elif shape == "triangle":
                shapes_shapes[shape] = (shapes_canvases[shape].create_polygon(10, 160, 85, 10, 160, 160, fill=shape_colour,
                                                                              outline=global_background))
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "triangle"))

            elif shape == "circle":
                shapes_shapes[shape] = (shapes_canvases[shape].create_oval(10, 10, 160, 160, fill=shape_colour,
                                                                           outline=global_background))
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "circle"))

            elif shape == "diamond":
                shapes_shapes[shape] = (shapes_canvases[shape].create_polygon(10, 85, 85, 10, 160, 85, 85, 160, fill=shape_colour,
                                                                              outline=global_background))  # Diamond
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "diamond"))

            elif shape == "pentagon":
                shapes_shapes[shape] = (shapes_canvases[shape].create_polygon(85, 0, 4, 59, 35, 154, 135, 154, 166, 59, fill=shape_colour,
                                                                              outline=global_background))  # Pentagon
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "pentagon"))

            elif shape == "hexagon":
                shapes_shapes[shape] = (shapes_canvases[shape].create_polygon(128, 11, 42, 11, 0, 85, 43, 159, 127, 159, 170, 85, fill=shape_colour,
                                                                              outline=global_background))  # Hexagon
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "hexagon"))

            elif shape == "trapezium":
                shapes_shapes[shape] = (shapes_canvases[shape].create_polygon(128, 51, 42, 51, 0, 134.3, 170, 134.3, fill=shape_colour,
                                                                              outline=global_background))  # Trapezium
                shapes_canvases[shape].bind("<ButtonPress-1>", lambda x: on_click("shape", "trapezium"))

            shapes_called.append(shape)

            count += 1

        get_names(shapes_called)

    def get_names(shapes_called):
        global names_called
        global names_canvases, names_text
        names_called = []
        count = 0
        padx = 125

        for i in shapes_called:
            count = count + 1
            name = random.choice(shapes_called)
            while name in names_called:
                name = random.choice(shapes_called)

            names_called.append(name)
            names_canvases[name] = tkinter.Canvas(names_frame, width=120, height=75, bg=global_background, bd=0,
                                                      highlightthickness=0, relief="ridge")
            names_canvases[name].grid(column=count, row=1, padx=padx)
            names_text[name] = names_canvases[name].create_text(60, 37.5, text=name.title())
            names_canvases[name].itemconfig(names_text[name], font=("MyriadPro-Regular", 20), fill=text_colour)
            names_canvases[name].bind("<ButtonPress-1>", lambda event,name=name: on_click("name", name))

    def on_click(type, input_shape):
        global clicked_currently_names, clicked_currently_shapes, names_boxes, names_canvases, shapes_shapes, shapes_canvases, shapes_boxes

        if popup_status == 1:
            return

        if type == "name":

            if input_shape in pairs_current:
                return

            if clicked_currently_names == 0:
                clicked_currently_names = input_shape
                names_boxes[input_shape] = names_canvases[input_shape].create_rectangle(0, 0, 119, 74, fill="", outline=border_colour)
                names_boxes[input_shape] = names_canvases[input_shape].create_rectangle(55, 65, 65, 75, fill=fore_colour, outline=border_colour)

        elif type == "shape":
            if clicked_currently_names == 0:
                return()

            if clicked_currently_shapes  == 0:
                clicked_currently_shapes = input_shape
                shapes_boxes[input_shape] = shapes_canvases[input_shape].create_rectangle(0, 0, 169, 169, fill="", outline=border_colour)
                check_pairs()

    def get_reset():
        global pairs_count, pairs_current, winner_count_label_string, winner_count, popup_canvas, has_ran, popup_status, timer_count, timer_time, popup_canvas_window

        pairs_count = 0
        pairs_current.clear()
        line_canvas.delete("all")

        popup_frame.lower()
        has_ran = True
        get_shapes(3)

        timer_count = 0
        timer_time = 1000

        popup_status = 0
        try:
            popup_canvas.delete(popup_canvas_window)
        except:
            print(" ")

        

    get_shapes(3)

    shapes_frame.place(relx=.5, rely=.65, anchor="center")
    names_frame.place(relx=.5, rely=.2, anchor="center")
    winner_frame.place(relx=.05, rely=.05, anchor="center")
    popup_frame.place(relx=.5, rely=.5, anchor="center")
    popup_frame.lower()

    window.mainloop()
