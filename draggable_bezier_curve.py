import math
import numpy as np

from draggable_plot import DraggablePlotExample
from bezier import BezierCurve


class DraggableBezierCurve(DraggablePlotExample):
   
    def __init__(self, parent = None):
        self._bzr_line = None
        super().__init__(parent)
        
    def _update_plot(self):
        self._update_bezier()
        super()._update_plot()
    
    def _update_bezier(self):
        _, xdata, ydata = zip(*sorted(self._points, key=lambda point: point[0]))
        xs = [x for x in xdata[0:4]]
        ys = [y for y in ydata[0:4]]
        for i in range(3, len(self._points), 3):
            xs.extend([x for x in xdata[i:i + 4]])
            ys.extend([y for y in ydata[i:i + 4]])

        #segments = len(xs)// 4
        segments = len(self._points) // 4
        if segments < 1: 
            return
        ts = np.linspace(0, segments, 100, endpoint=True)
        #self.curve = BezierCurve([x for x in xs[:4 * segments]], [y for y in ys[:4 * segments]], segments)
        self.curve = BezierCurve(xdata, ydata, segments)
        spline = [self.curve.value(t) for t in ts]

        if not self._bzr_line:
            self._bzr_line, = self._axes.plot([pnt[0] for pnt in spline], [pnt[1] for pnt in spline], 'r')
        else:
            # Update current plot
            self._bzr_line.set_data([pnt[0] for pnt in spline], [pnt[1] for pnt in spline])


if __name__ == "__main__":
    plot = DraggableBezierCurve()
