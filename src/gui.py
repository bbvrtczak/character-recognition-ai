from tkinter import *
import customtkinter as ctk
from PIL import Image, ImageDraw
import PIL
import converter

WIDTH = 1400  # canvas size
HEIGHT = 1400  # canvas size
CENTER = WIDTH // 2
WHITE = 1
BLACK = 0
PIXEL_SIZE = 50  # how many pixels per 1 output image pixel
OUTPUT_SIZE = 28


class DrawGUI:

    def __init__(self):
        self.__root = ctk.CTk()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.__root.title("OCR Letter Recognition")
        self.__root.iconbitmap("../res/window_icon.ico")
        #self.__root.resizable(False, False)

        # window size and position
        sc_width = self.__root.winfo_screenwidth()
        sc_height = self.__root.winfo_screenheight()
        x = (sc_width / 2) - 600
        y = (sc_height / 2) - 325
        self.__root.geometry("%dx%d+%d+%d" % (1200, 650, x, y))

        self.__brush_width = 1
        self.__color = "#FFFFFF"
        self.__brush_type = 1

        # canvas and image
        self.__cnv = Canvas(self.__root, width=WIDTH, height=HEIGHT, bg="black", highlightthickness=0, cursor="pencil")
        self.__cnv.place(relx=0.05, rely=0.1)
        self.__cnv.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
        self.scale_factor = 2.0
        self.__cnv.scale('all', 0, 0, self.scale_factor, self.scale_factor)
        self.__cnv.bind("<B1-Motion>", self.paint)

        self.__image = PIL.Image.new("1", (WIDTH, HEIGHT), 0)
        self.__draw = ImageDraw.Draw(self.__image)

        # process button
        self.__process_btn = ctk.CTkButton(master=self.__root, text="Process", font=("Open Sans", -32, "bold"),
                                           width=240, height=100, compound="left", corner_radius=15,
                                           text_color="#f5f5f5",
                                           hover_color="#2463a6", cursor="hand2", command=self.process)
        self.__process_btn.place(relx=0.55, rely=0.35)

        # clear button
        self.__clear_btn = ctk.CTkButton(master=self.__root, text="Clear", font=("Open Sans", -32, "bold"),
                                         width=240, height=100, compound="left", corner_radius=15, text_color="#f5f5f5",
                                         hover_color="#2463a6", cursor="hand2", command=self.clear)
        self.__clear_btn.place(relx=0.55, rely=0.5)

        # change brush button
        #self.__change_br = ctk.CTkButton(master=self.__root, text="✏", font=("Open Sans", -32),
                                         #width=30, height=50, compound="left", corner_radius=15, text_color="#f5f5f5",
                                         #hover_color="#2463a6", cursor="hand2", command=self.change_brush)
        #self.__change_br.place(relx=0.53, rely=0.84)

        # predicted result box and label
        self.__result = ctk.CTkTextbox(master=self.__root, width=250, height=250, corner_radius=15,
                                       font=("Open Sans", -172, "bold"), state="disabled", cursor="")
        self.__result.place(relx=0.77, rely=0.14)

        self.__result_label = ctk.CTkLabel(self.__root, text="Predicted output", fg_color="transparent",
                                           font=("Open Sans", -32, "bold"))
        self.__result_label.place(relx=0.773, rely=0.07)

        # second guess box and label
        self.__second = ctk.CTkTextbox(master=self.__root, width=250, height=250, corner_radius=15,
                                       font=("Open Sans", -172, "bold"), state="disabled", cursor="")
        self.__second.place(relx=0.768, rely=0.54)

        self.__second_label = ctk.CTkLabel(self.__root, text="Second guess", fg_color="transparent",
                                           font=("Open Sans", -32, "bold"))
        self.__second_label.place(relx=0.78, rely=0.47)

        self.__root.mainloop()

    def paint(self, event):
        # getting position in 28x28 grid
        x_grid_pixel = self.get_grid_position(event.x)
        y_grid_pixel = self.get_grid_position(event.y)

        # calculating corner pixels for rectangle
        if self.__brush_type == 0:
            x1, y1 = (x_grid_pixel - 1) * PIXEL_SIZE, (y_grid_pixel - 1) * PIXEL_SIZE
            x2, y2 = x_grid_pixel * PIXEL_SIZE, y_grid_pixel * PIXEL_SIZE
        elif self.__brush_type == 1:
            x1, y1 = (x_grid_pixel - 2) * PIXEL_SIZE, (y_grid_pixel - 2) * PIXEL_SIZE
            x2, y2 = (x_grid_pixel + 1) * PIXEL_SIZE, (y_grid_pixel + 1) * PIXEL_SIZE

        self.__cnv.create_rectangle(x1, y1, x2, y2, outline=self.__color, fill=self.__color, width=self.__brush_width)
        self.__draw.rectangle([x1, y1, x2 + self.__brush_width, y2 + self.__brush_width],
                              outline=self.__color, fill=self.__color, width=self.__brush_width)

    def clear(self):
        self.__cnv.delete("all")
        self.__draw.rectangle([0, 0, 1000, 1000], fill="black")

        self.__result.configure(state="normal")
        self.__result.delete('1.0', END)
        self.__result.configure(state="disabled")

        self.__second.configure(state="normal")
        self.__second.delete('1.0', END)
        self.__second.configure(state="disabled")

    def process(self):
        output_image = self.__image.copy()
        output_image = output_image.resize((OUTPUT_SIZE, OUTPUT_SIZE), Image.LANCZOS)

        processed_output, second_guess = converter.get_model_output(output_image)

        if processed_output == "i":
            processed_output = " i"
        if second_guess == "i":
            second_guess = " i"


        self.put_output_text(processed_output, second_guess)

    def get_grid_position(self, pos):
        grid_pos = 0
        tmp_var = 0
        while tmp_var < pos:
            tmp_var += PIXEL_SIZE
            grid_pos += 1

        return grid_pos

    def put_output_text(self, output, second):
        prediction = " " + output
        self.__result.configure(state="normal")
        self.__result.delete('1.0', END)
        self.__result.insert("1.0", prediction)
        self.__result.configure(state="disabled")

        second_guess = " " + second
        self.__second.configure(state="normal")
        self.__second.delete('1.0', END)
        self.__second.insert("1.0", second_guess)
        self.__second.configure(state="disabled")

    def change_brush(self):
        if self.__brush_type == 0:
            self.__brush_type = 1
            self.__change_br.configure(font=("Open Sans", -32, "bold"))
        else:
            self.__brush_type = 0
            self.__change_br.configure(font=("Open Sans", -32))


DrawGUI()
