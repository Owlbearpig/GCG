import numpy as np
from numpy import sqrt, round
from functions import speed, writeline, layer_transition, end, sign, start, move

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        x, y = round(self.x + other.x, 3), round(self.y + other.y, 3)
        return Point(x, y)

"""
1. do initial stuff
2. print frame
3. print single lines
4. do end stuff
"""

settings = {
    'material': 'COC',
    'thickness': 2,  # mm
    'layer_height': 0.2, # mm
    'extruder_temp': 220,
    'bed_temp': 100,
    'nozzle_Ø': 0.4,
}

material = settings['material']
thickness = settings['thickness']

filename = 'test' #f'{thickness}mm_{material}_plate'

dz0 = settings['layer_height']

layer_cnt = int(thickness / dz0)

dy0 = 48.459  # dy = 48.609
dx0 = settings['nozzle_Ø'] * 0.943 # need a bit of overlap.

# origin, upper left of frame
p0 = Point(175, 175)

with open(filename + '.gcode', 'a+', newline='') as gcode_output_file:
    # Header/start
    start(gcode_output_file, settings)
    move(gcode_output_file, p0, cur_layer_height=dz0)

    # make frame -> add bars -> restart
    for layer_idx in range(layer_cnt+1):
        prev_pos = p0
        cur_layer_height = round(dz0 + layer_idx * dz0, 3)

        dx, dy = 0, 100
        dp = prev_pos + Point(dx, dy)
        writeline(gcode_output_file, f'G1 X{dp.x} Y{dp.y} E{speed(prev_pos, dp)}')

    """
    for layer_idx in range(layer_cnt+1):
        # first layer height 0.200 set in header -> z offset
        cur_layer_height = round(layer_height+layer_idx*layer_height, 3)
        prev_pos = p0
        for line_idx in range(segment_cnt-1):
            dp = round(prev_pos + np.array([(line_idx%2)*dx, sign(line_idx)*dy]), 3)
            writeline(file, f'G1 X{dp[0]} Y{dp[1]} E{speed(prev_pos, dp)}')

            prev_pos = dp

            prog = 100*((layer_idx*segment_cnt+(line_idx+1))/total_segment_cnt)

            if (layer_idx*segment_cnt+line_idx) % 385 == 0:
                writeline(file, f'M73 P{int(round(prog))}')

        if layer_idx != layer_cnt-1:
            layer_transition(file, z, dp, p0)

    # end
    #end(gcode_output_file, z)
    """
    gcode_output_file.close()
