from numpy import sqrt
from consts import mask_dir

def sign(i):
    if i % 4 == 0:
        return -1
    if i % 4 == 2:
        return 1
    return 0

def writeline(open_file, s):
    open_file.write('\n'+s)


def speed(p1, p2):
    c = 0.028206675277192242  # extrusion speed: E'distance*c' (number from slicer for hips) TODO: filament specific?

    return round(sqrt((p1.x-p2.x)**2+(p1.y-p2.y)**2)*c, 3)


def start(gcode_output_file, settings):
    """
    Initial commands, not sure what they all do ...
    :param gcode_output_file:
    :param settings: general print settings dict
    :return: None
    """
    header_file = open(mask_dir / 'header', 'r')
    for line in header_file.readlines():
        line = line.replace('ExtT', str(settings['extruder_temp']))
        line = line.replace('BedT', str(settings['bed_temp']))
        line = line.replace('LH', str(settings['layer_height']))

        gcode_output_file.write(line)


def move(gcode_output_file, p, cur_layer_height):
    """
    Retracts filament -> move up above print (0.6mm above) -> move to p -> put filament at E0 again
    :param gcode_output_file: some time make it into class maybe : )
    :param p: target point (x, y)
    :param cur_layer_height: height to set nozzle after move
    :return: None
    """
    move_file = open(mask_dir / 'move', 'r')
    for line in move_file.readlines():
        line = line.replace('target', f'X{p.x} Y{p.y}')
        line = line.replace('z', str(cur_layer_height))
        line = line.replace('above', str(cur_layer_height+0.6))

        gcode_output_file.write(line)

def layer_transition(open_file, z, cur_pos, start_pos):
    """
    TODO same as move ??
    :param open_file:
    :param z:
    :param cur_pos:
    :param start_pos:
    :return:
    """
    layer_transition = open('layer_transition', 'r')
    z, h = str(z), str(round(z+0.800, 3))
    for line in layer_transition:
        line = line.replace('z', z)
        line = line.replace('h', h)

        line = line.replace('cur_pos', f'X{cur_pos[0]} Y{cur_pos[1]}')
        line = line.replace('start_pos', f'X{start_pos[0]} Y{start_pos[1]}')

        open_file.write(line)


def end(open_file, z):
    end = open('end', 'r')
    z = round(z+0.600, 3)
    for line in end:
        line = line.replace('z', f'{z}')

        open_file.write(line)
