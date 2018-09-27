from glob import glob


def SearchFile():
    paths = sorted(glob('/media/*.gcode'))
    if len(paths) > 0:
        return paths
    else:
        return False

