import numpy as np
from numpy import sqrt, round
from functions import speed, writeline, layer_transition, end, sign, start

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
}

material = settings['material']
thickness = settings['thickness']

filename = 'test' #f'{thickness}mm_{material}_plate'

layer_height = settings['layer_height']

layer_cnt = int(thickness / layer_height)

dy = 48.459 #dy = 48.609
dx = 0.377
center_width = 149.413-100.587
horiz_segment_cnt = int(center_width / dx)
segment_cnt = 2*horiz_segment_cnt # vertical line + horiz line gives one dx of total width.

total_segment_cnt = layer_cnt*segment_cnt

# origin, upper left of frame
p0 = np.array([100.973, 129.300])

with open(filename + '.gcode', 'a+', newline='') as gcode_output_file:
    # Header/start
    start(gcode_output_file, settings)

    for layer_idx in range(1, layer_cnt+1):
        # first layer height 0.200 set in header -> z offset
        cur_layer_height = round(layer_height+(layer_idx)*layer_height, 3)
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

    gcode_output_file.close()
