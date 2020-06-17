#!/usr/bin/python3
#-*- coding: UTF-8 -*-
import numpy as np
from matplotlib.patches import Polygon


class FontRenderer:
    def __init__(self):
        self.h_indent = 0.1
        self.h_padding = 0.1
        self.v_indent = 0.1
        self.v_padding = 0.1
        self.window_size_x = 1
        self.window_size_y = 1.2
        self.edgecolor = 'black'
        self.facecolor = (0.2, 0.2, 0.2)
        self.smooth_factor = 50
        
    def _render_control_points(self, ax, char, left_point):
        n_curcuits = char.curcuits_count
        x, y = left_point
        max_x = 0
        for i in range(n_curcuits):
            curve = char[i]
            xdata = []
            ydata = []
            for x_array, y_array in curve.control_points():
                xdata.extend(x_array)
                ydata.extend(y_array)
            ax.plot(xdata, ydata, 'o--')
            max_x = max(max_x, max(xdata))
        return (max_x, y)
        
    def _render_char(self, ax, font, char, left_point):
        n_curcuits = font[char].curcuits_count
        x, y = left_point
        max_x = 0
        for i in range(n_curcuits):
            curve = font[char][i]
            n_segments = curve.segments_count
            curve_param = np.linspace(0, n_segments, self.smooth_factor * n_segments)
            if i == 0: facecolor = self.facecolor
            else: facecolor = 'white'
            x_array, y_array = np.hsplit(np.array([curve.value(t) for t in curve_param]), 2)
            polygon = Polygon(np.column_stack([x_array + x, y_array + y]), True, edgecolor=self.edgecolor, facecolor=facecolor)
            ax.add_patch(polygon)
            max_x = max(max_x, max(x_array))
        
        for component in font[char].components:
            x, y = self._render_char(ax, font, component, left_point)
            max_x = max(x, max_x)
            
        return (max_x, y)
        
    def render(self, figure, ax, font, text, render_type='char'):
        right_point_x = 0
        last_point_x = 0
        last_point_y = 0
        for char in text:
            if char == '\n':
                right_point_x = max(right_point_x, last_point_x)
                last_point_x = 0
                last_point_y = last_point_y - self.v_indent - 1
            else: # regular char
                if render_type == 'char':
                    point = self._render_char(ax, font, char, (last_point_x, last_point_y))
                elif render_type == 'curcuit':
                    point = self._render_control_points(ax, font[char], (last_point_x, last_point_y))
                last_point_x += self.h_indent + point[0]
                right_point_x = max(right_point_x, last_point_x)
        
        #figure.set_size_inches((int(right_point_x) * self.window_size_x, max(1, abs(last_point_y) * self.window_size_y)))
        ax.set_xlim(0 - self.h_padding, right_point_x * self.window_size_x + self.h_padding)
        ax.set_ylim(0 - self.v_padding + last_point_y, 1 + self.v_padding)
        #ax.set_xlim(0, 1)
        #ax.set_ylim(0, 1)
        #plt.show()


if __name__ == "__main__":
    FontRenderer().render("АБВ", [(1, 1), (125, 125), (250, 0)])
