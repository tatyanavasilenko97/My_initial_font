#!/usr/bin/python3
#-*- coding: UTF-8 -*-
from font import Font
from font_renderer import FontRenderer
from draggable_bezier_curve import DraggableBezierCurve
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

import tkinter
import tkinter.ttk


class Application:
    def __init__(self, master):
        self.master = master
        self.fontRenderer = FontRenderer()
        
        self.radioBtnGroup = None
        frame = tkinter.Frame(master)
        self.paramText = tkinter.Text(master=frame, width=20, height=6)
        self.paramRenderBtn = tkinter.Button(frame, text='Отобразить', command=self._on_button_click)
        self.fileDialogBtn = tkinter.Button(frame, text='Загрузить', command=self._on_button_load_click)
        self.fileSaveBtn = tkinter.Button(frame, text='Сохранить', command=self._on_button_save_click)
        self.editBtn = tkinter.Button(frame, text='Редактировать', command=self._on_button_edit_click)
        
        frame.pack(side=tkinter.LEFT)
        self.paramText.pack(side=tkinter.TOP)
        self.paramRenderBtn.pack(side=tkinter.TOP)
        self.fileDialogBtn.pack(side=tkinter.TOP)
        self.fileSaveBtn.pack(side=tkinter.TOP)
        self.editBtn.pack(side=tkinter.TOP)
        
        #self.canvas = FigureCanvasTkAgg(plt.gcf(), master)
        #self.canvas.draw()
        #self.canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)

    def _on_button_click(self):
        #plt.gca().clear()
        self.render_text(self.paramText.get(1.0, tkinter.END))
        #self.canvas.draw()

    def _on_button_load_click(self):
        csvfile = tkinter.filedialog.askopenfile()
        if csvfile is not None:
            self.load_from_file(csvfile.name)

    def _on_button_save_click(self):
        csvfile = tkinter.filedialog.asksaveasfile()
        if csvfile is not None:
            self.save_to_file(csvfile.name)

    def _on_button_edit_click(self):
        self.window = tkinter.Toplevel(self.master)
        scrollbar = tkinter.Scrollbar(self.window)
        scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.mylist = tkinter.Listbox(self.window, selectmode=tkinter.SINGLE, yscrollcommand=scrollbar.set)
        self.mylist.bind('<<ListboxSelect>>', self._on_listbox_select)
        for font_char in self.font:
            self.mylist.insert(tkinter.END, font_char)
        self.mylist.pack()
        scrollbar.config(command=self.mylist.yview)
        saveBtn = tkinter.Button(self.window, text='Сохранить', command=self._on_button_save_symbol_click)
        saveBtn.pack()
    
    def _on_listbox_select(self, event):
        current_selection = self.mylist.get(self.mylist.curselection())
        self.r_var = tkinter.IntVar()
        self.r_var.set(0)
        if self.radioBtnGroup:
            for radioBtn in self.radioBtnGroup:
                radioBtn.destroy()

        self.radioBtnGroup = [tkinter.Radiobutton(self.window, text="%d" % curcuit, variable=self.r_var, value=curcuit, \
            command=lambda: self.draggable.set_drag_line(self.r_var.get())) \
            for curcuit in range(self.font[current_selection].curcuits_count)]
        for radioBtn in self.radioBtnGroup:
            radioBtn.pack()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.fontRenderer.render(fig, ax, self.font, current_selection, 'curcuit')
        self.draggable = DraggableBezierCurve(fig)
        self.draggable.set_drag_line(self.r_var.get())
        fig.show()
    
    def _on_button_save_symbol_click(self):
        for i in range(self.draggable.lines_count):
            self.draggable.set_drag_line(i)
            self.font[self.mylist.get(self.mylist.curselection())][i] = self.draggable.curve
        
    def load_from_file(self, font_filename):
        self.font = Font.load_from_file(font_filename)
        
    def save_to_file(self, font_filename):
        Font.save_to_file(self.font, font_filename)
     
    def render_text(self, text):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.fontRenderer.render(fig, ax, self.font, text)
        fig.show()

        
if __name__ == '__main__':
    tk_app = tkinter.Tk()
    app = Application(tk_app)
    app.load_from_file("font.json")

    tk_app.mainloop()
    #app.render_text("АБВГДЕ")
    #app.render_text("АБВГДЕЖЗИКЛ\nМНОПРСТУФХЦ\nЧШЩЪЫЬЭЮЯ")
    