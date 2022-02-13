import unittest
import numpy as np
import os


class ImportTests(unittest.TestCase):
    def test_read_line(self):
        from import_gcode import read_line, init_mashine
        gcm = init_mashine()
        self.assertEqual([1, [-1.883, 61.665, 20.0]],
                         read_line("N31 G1 X-1.883 Y61.665 Z20 F1000 S24000 M3", gcm)[:2], )
        self.assertEqual([1000.0, 24000], read_line("N45 G1 X-2.025 Y68.54", gcm)[2:4])
        self.assertEqual([3, [-2.584, 68.623, 20.0], 1000.0, 24000, 0.4],
                         read_line("N47 G3 X-2.584 Y68.623 CR=0.4", gcm)[:5])


class cad_calcTests(unittest.TestCase):
    def test_placeholder(self):
        import cadquery as cq
        from cad_calc import draw_and_subtract, linear_milling_vol
        workpiece = cq.Workplane("front").lineTo(20, 0).lineTo(20, 20).lineTo(0, 20).close().extrude(-10)
        cut = linear_milling_vol(cq.Workplane("front"), [2, 0, -1], [1, 1, -1], 0.6)
        inter1, workpiece = draw_and_subtract([[[2, 0, -1], [1, 1, -1]], [[1, 1, -1], [1.9, 1.9, -1]]], workpiece, 0.6)
        inter2, workpiece = draw_and_subtract([[[1.1, 1.1, -1], [2, 2, -1]]], workpiece, 0.6)

        self.assertEqual(1.7246038825755226, inter1.val().Volume())
        self.assertEqual(0.08485281374238579, inter2.val().Volume())

if __name__ == '__main__':
    unittest.main()
