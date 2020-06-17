# -*- coding: utf-8 -*-

import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent


class DraggablePlotExample(object):
    u""" An example of plot with draggable markers """

    def __init__(self, parent = None):
        self._dragging_point = None
        self._figure, self._axes, self._line = None, None, None
        self._points = []
        self._init_plot(parent)
        
    def _init_plot(self, parent):
        if parent:
            self._figure, self._axes, self._line = parent, parent.gca(), parent.gca().lines[0]
            data = self._line.get_data()
            self._points = [(i, x, y) for i, x, y in zip(range(len(data[0])), *data)]
        else:
            self._figure = plt.figure("Example plot")
            axes = plt.subplot(1, 1, 1)
            axes.set_xlim(0, 1)
            axes.set_ylim(0, 1)
            axes.grid(which="both")
            self._axes = axes
        
        self.lines_count = len(self._axes.lines)
        self.cid1 = self._figure.canvas.mpl_connect('button_press_event', self._on_click)
        self.cid2 = self._figure.canvas.mpl_connect('button_release_event', self._on_release)
        self.cid3 = self._figure.canvas.mpl_connect('motion_notify_event', self._on_motion)
        if not parent:
            plt.show()

    def _update_plot(self):
        if not self._points:
            self._line.set_data([], [])
        else:
            _, x, y = zip(*sorted(self._points, key=lambda point: point[0]))
            # Add new plot
            if not self._line:
                self._line, = self._axes.plot(x, y, "bo--", markersize=3)
            # Update current plot
            else:
                self._line.set_data(x, y)
        self._figure.canvas.draw()

    def _add_point(self, x, y=None, i=None):
        if isinstance(x, MouseEvent):
            i, x, y = len(self._points) + 1, x.xdata, x.ydata
        self._points.append((i, x, y))
        return i, x, y

    def _remove_point(self, point):
        if point in self._points:
            self._points.remove(point)

    def _find_neighbor_point(self, event):
        u""" Find point around mouse position

        :rtype: ((int, float, float)|None)
        :return: (x, y) if there are any point around mouse else None
        """
        distance_threshold = 0.05
        nearest_point = None
        min_distance = math.sqrt(2 * (100 ** 2))
        for i, x, y in self._points:
            distance = math.hypot(event.xdata - x, event.ydata - y)
            if distance < min_distance:
                min_distance = distance
                nearest_point = (i, x, y)
        if min_distance < distance_threshold:
            return nearest_point
        return None

    def _on_click(self, event):
        u""" callback method for mouse click event

        :type event: MouseEvent
        """
        # left click
        if event.button == 1 and event.inaxes in [self._axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._dragging_point = point
            else:
                self._add_point(event)
            self._update_plot()
        # right click
        elif event.button == 3 and event.inaxes in [self._axes]:
            point = self._find_neighbor_point(event)
            if point:
                self._remove_point(point)
                self._update_plot()

    def _on_release(self, event):
        u""" callback method for mouse release event

        :type event: MouseEvent
        """
        if event.button == 1 and event.inaxes in [self._axes] and self._dragging_point:
            self._dragging_point = None
            self._update_plot()

    def _on_motion(self, event):
        u""" callback method for mouse motion event

        :type event: MouseEvent
        """
        if not self._dragging_point:
            return
        if event.xdata is None or event.ydata is None:
            return
        self._remove_point(self._dragging_point)
        self._dragging_point = self._add_point(event.xdata, event.ydata, self._dragging_point[0])
        self._update_plot()
    
    def set_drag_line(self, index):
        self._line = self._axes.lines[index]
        data = self._line.get_data()
        self._points = [(i, x, y) for i, x, y in zip(range(len(data[0])), *data)]
        self._update_plot()

if __name__ == "__main__":
    plot = DraggablePlotExample()
