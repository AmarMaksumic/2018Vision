from Tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Scale

class Controls:

    def __init__(self, master, profile):

        self.profile = profile
        self.master = master
        master.title("Controls")

        rgb_red_min = Scale(master, from_=0, to=255, background="red")
        rgb_red_max = Scale(master, from_=0, to=255, background="red")

        rgb_green_min = Scale(master, from_=0, to=255, background="green")
        rgb_green_max = Scale(master, from_=0, to=255, background="green")

        rgb_blue_min = Scale(master, from_=0, to=255, background="blue")
        rgb_blue_max = Scale(master, from_=0, to=255, background="blue")

        rgb_red_min.set(profile.red[0])
        rgb_red_max.set(profile.red[1])

        rgb_green_min.set(profile.green[0])
        rgb_green_max.set(profile.green[1])

        rgb_blue_min.set(profile.blue[0])
        rgb_blue_max.set(profile.blue[1])


        hsv_hue = Scale(master, from_=0, to=255 , label="hue")
        hsv_sat = Scale(master, from_=0, to=255 , label="sat")
        hsv_val = Scale(master, from_=0, to=255, label="val" )

        self.total = 0
        self.entered_number = 0

        self.total_label_text = IntVar()
        self.total_label_text.set(self.total)
        self.total_label = Label(master, textvariable=self.total_label_text)

        self.label = Label(master, text="Total:", )

        vcmd = master.register(self.validate) # we have to wrap the command
        self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.add_button = Button(master, text="+", command=lambda: self.update("add"))
        self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))

        # LAYOUT
        rgb_red_min.grid(row=0, column=0)
        rgb_red_max.grid(row=0, column=1)

        rgb_green_min.grid(row=0, column=2)
        rgb_green_max.grid(row=0, column=3)

        rgb_blue_min.grid(row=0, column=4)
        rgb_blue_max.grid(row=0, column=5)
        #
        # hsv_hue.grid(row=1, column=0)
        # hsv_sat.grid(row=1, column=1)
        # hsv_val.grid(row=1, column=2)


        # self.label.grid(row=0, column=0, sticky=W)
        # self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
        #
        # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
        #
        # self.add_button.grid(row=2, column=0)
        # self.subtract_button.grid(row=2, column=1)
        # self.reset_button.grid(row=2, column=2, sticky=W+E)

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.entered_number = 0
            return True

        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False

    def update(self, method):
        if method == "add":
            self.total += self.entered_number
        elif method == "subtract":
            self.total -= self.entered_number
        else: # reset
            self.total = 0

        self.total_label_text.set(self.total)
        self.entry.delete(0, END)

