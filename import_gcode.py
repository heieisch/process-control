from gcode_machine import GcodeMachine
import pickle


def read_line(line, gcm):
    """ Parses (and translates into own compounded datastructure) one line of gcode

    Keyword arguments:
    line -- string of g-Code line
    gcm -- GCode Machine Object

    Output:
    returns the parsed information about machine state at the current line,
    returns "None" if the machine state hasn't changed

    """
    # Versteh Objektorientierung !!! du dappschädel
    if line[0] == 'N':
        line = line[line.find(' ') + 1:]
    pos_old = gcm.position_m
    gcm.set_line(line)  # feed the line into the machine
    gcm.strip()  # clean up whitespace
    gcm.tidy()  # filter commands by a whitelist
    gcm.find_vars()  # parse variable usages
    gcm.substitute_vars()  # substitute variables
    gcm.parse_state()  # parse positions etc. and update the machine state
    cmm = gcm.current_motion_mode
    radius = gcm.radius
    gcm.override_feed()  # substitute F values
    gcm.transform_comments()  # transform parentheses to semicolon comments
    gcm.done()  # update the machine position
    if pos_old != gcm.position_m:
        # print(gcm.position_m, gcm.current_feed, gcm.current_spindle_speed, cmm, radius)
        # print(line)
        if cmm == 0:
            feed = gcm.max_feed
        else:
            feed = gcm.current_feed

            #   G   posMaschine Vorschub UmdrehungenSpindel      Pfadradius  Fräserdurchmesser
        return [cmm, gcm.position_m, feed, gcm.current_spindle_speed, radius, gcm.tool_diameter]
    else:
        return None


def init_mashine():
    """creates object for machine state
    change initial settings to reflect machine state

    Keyword arguments:

    Output:
    machine state object (see Gcode_Machine.py for reference)

    """
    # initial conditions
    initial_machine_position = impos = (0, 0, 50)
    initial_coordinate_system = ics = "G54"
    coordinate_system_offsets = cs_offsets = {"G54": (0, 0, 0)}
    max_acell = 10000
    max_feed = 6000
    tool_diameter = 6

    # make a new machine
    gcm = GcodeMachine(impos, ics, cs_offsets, max_acell, max_feed, tool_diameter)
    return gcm


def read_file(path):
    """toplevel function (PARSE)
    manages all functions neccesary to parse the g-code

    Keyword arguments:
    path -- path to G-Code File

    Output:
    saves list of all move-operations and corresponding machine-state as pickle

    """
    gcm = init_mashine()

    dump = []
    with open(path) as file_handle:
        for line in file_handle:
            return_val = read_line(line, gcm)
            if return_val:  # ...is not None:
                dump.append(return_val)
                print(return_val)

    with open("parsed_gcode.p", 'wb') as pic:
        pickle.dump(dump, pic)


def main():
    read_file("testnc.mpf")


if __name__ == "__main__":
    main()
