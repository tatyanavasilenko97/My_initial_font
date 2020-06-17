#!/usr/bin/python3
#-*- coding: UTF-8 -*-
import json
import numpy as np
from bezier import BezierCurve


class FontChar:
    def __init__(self, symbol, curcuits_count, curves, components):
        self._symbol = symbol
        self._curcuits_count = curcuits_count
        self._curves = curves
        self._components = components

    @property
    def curcuits_count(self):
        return self._curcuits_count

    @property
    def symbol(self):
        return self._symbol
        
    @property
    def components(self):
        return self._components
        
    def __getitem__(self, curcuit_index):
        return self._curves[curcuit_index]
        
    def __iter__(self):
        return iter(self._curves)
        
    def __setitem__(self, key, value):
        self._curves[key] = value


class Font:
    def __init__(self, font_name, symbols_map):
        self._font_name = font_name
        self._symbols = symbols_map

    def __getitem__(self, key):
        return self._symbols[key]

    def __iter__(self):
        return iter(self._symbols)
        
    @property
    def font_name(self):
        return self._font_name

    @staticmethod
    def load_from_file(fname):
        with open(fname, encoding="utf-8") as json_file:
            data = json.load(json_file)
            font_name = data["fontName"]
            symbols_map = dict()
            for symbol in data["symbols"]:
                character = symbol["character"]
                curcuit_count = 0
                curcuits = []
                components = []
                curcuit_count = symbol["curcuitCount"]
                for curcuit in symbol["curcuits"]:
                    x_array = [point["x"] for curve in curcuit["curves"] for point in curve.values()]
                    y_array = [point["y"] for curve in curcuit["curves"] for point in curve.values()]
                    segments_count = curcuit["curvesCount"]
                    bzr = BezierCurve(x_array, y_array, segments_count)
                    curcuits.append(bzr)
                components = symbol["components"]
                symbols_map[character] = FontChar(character, curcuit_count, curcuits, components)
                
            return Font(font_name, symbols_map)
        return None
    
    @staticmethod
    def save_to_file(font, fname):
        with open(fname, "w", encoding="utf-8") as json_file:
            font_name = font.font_name
            symbols = []
            for symbol in font:
                character = font[symbol]
                curcuits = []
                components = font[symbol].components
                for curcuit in character:
                    segments_count = curcuit.segments_count
                    curves = []
                    for x_array, y_array in curcuit.control_points():
                        curve = {}
                        curve["p0"] = dict(x=x_array[0],y=y_array[0])
                        curve["p1"] = dict(x=x_array[1],y=y_array[1])
                        curve["p2"] = dict(x=x_array[2],y=y_array[2])
                        curve["p3"] = dict(x=x_array[3],y=y_array[3])
                        curves.append(curve)
                    curcuits.append({"curvesCount": segments_count, "curves": curves})
                symbols.append({"character": character.symbol, "curcuits": curcuits, "curcuitCount": len(curcuits), "components": components})
            json.dump({"fontName": font_name, "symbols": symbols}, json_file)


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon
    x = np.linspace(0, 11)
    font = Font.load_from_file("font.txt")
    ax = plt.gca()
    ax.add_patch(Polygon([font["К"][0].value(i) for i in x], True, edgecolor='black'))
    font["К"][0].control_points()
    plt.show()