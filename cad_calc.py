import cadquery as cq
import numpy as np
from OCP.Standard import Standard_ConstructionError


def linear_milling_vol(cut, start_point, end_point, mill_diameter):
    """creates the volume that gets milled from linear move

    Keyword arguments:
    start_point -- [x,y,z] toolcentrepoint mm
    end_point -- [x,y,z] toolcentrepoint mm
    mill_diameter -- tooldiameter mm

    Output:
    CADquery Object

    """

    assert (start_point[2] == end_point[2] != 0)
    alpha = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])

    points = [[start_point[0] + mill_diameter / 2 * np.cos(alpha + np.pi / 2),
               start_point[1] + mill_diameter / 2 * np.sin(alpha + np.pi / 2)],
              [start_point[0] + mill_diameter / 2 * np.cos(alpha + np.pi),
               start_point[1] + mill_diameter / 2 * np.sin(alpha + np.pi)],
              [start_point[0] + mill_diameter / 2 * np.cos(alpha - np.pi / 2),
               start_point[1] + mill_diameter / 2 * np.sin(alpha - np.pi / 2)],
              [end_point[0] + mill_diameter / 2 * np.cos(alpha - np.pi / 2),
               end_point[1] + mill_diameter / 2 * np.sin(alpha - np.pi / 2)],
              [end_point[0] + mill_diameter / 2 * np.cos(alpha), end_point[1] + mill_diameter / 2 * np.sin(alpha)],
              [end_point[0] + mill_diameter / 2 * np.cos(alpha + np.pi / 2),
               end_point[1] + mill_diameter / 2 * np.sin(alpha + np.pi / 2)]]

    cut = cut.moveTo(points[0][0], points[0][1]).threePointArc(points[1], points[2]).lineTo(points[3][0], points[3][1]) \
        .threePointArc(points[4], points[5]).close().extrude(end_point[2])

    return cut


def circular_milling_vol(cut, start_point, end_point, mill_diameter, arc_centre):
    """creates the volume that gets milled from circular move

    Keyword arguments:
    start_point -- [x,y,z] toolcentrepoint mm
    end_point -- [x,y,z] toolcentrepoint mm
    mill_diameter -- tooldiameter mm
    arc_centre -- !!! noch nicht sicher!!! entweder radius oder kreismittelpunkt

    Output:
    CADquery Object

    """
    pass  # weil grade noch leer, dann löahen
    # ...


def draw_and_subtract(moves, workpiece, mill_diameter):
    """gets moves of one timestep

    Keyword arguments:
    moves -- moves of current timestep
    workpiece -- current workpiece
    mill_diameter -- Mill Diameter

    Output:
    intersection -- virtual chip (spahn)
    workpiece -- updated workpiece
    """
    cut = cq.Workplane("front")
    for move in moves:
        if len(move) == 2:
            cut = linear_milling_vol(cut, move[0], move[1], mill_diameter)
        else:
            cut = circular_milling_vol(cut, move[0], move[1], move[2], mill_diameter)
    try:
        intersection = workpiece.intersect(cut)
        intersection.largestDimension()
    except Standard_ConstructionError:
        intersection = None
    if intersection is not None:
        wp = workpiece.cut(cut)
    return intersection, wp


def get_param_for_neural_net(moves, workpiece, mill_diameter):
    """appends cutting-simulation-parameters line at csv list

    Keyword arguments:
    moves -- moves of current timestep
    workpiece -- current workpiece
    mill_diameter -- Mill Diameter

    Output:
    compounded_move -- is move compounded (zusammengestzt)
    alpha -- direction angle of movement
    b_box -- boundingbox of virtual chip, corresponds to Umschlingungswinkel
    vol -- volume of virtual chip
    z_hight -- z-hight-information, noch unklar
    """
    # inter = intersection
    inter, workpiece = draw_and_subtract(moves, workpiece, mill_diameter)
    compounded_move = len(moves) - 1  # zum Abfangen wenn stückechen zusammengestzt
    # Umschlingungswinkel -in Fahrtrichtung drehen: alpha
    alpha = np.arctan2(moves[-1][1][1] - moves[0][0][1], moves[-1][1][0] - moves[0][0][0])
    shape = inter.val().rotate((0, 0, 0), (0, 0, 1), alpha)
    vol = shape.Volume()
    b_box = shape.BoundingBox()  # ähnlich zu Umschlingungswinkel -> =Umschlingungswinkel
    z_hight = moves[0][0][2]  # noch unklar
    return [compounded_move, alpha, b_box, vol, z_hight]
