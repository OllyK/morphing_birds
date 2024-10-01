import unittest
import numpy as np
from morphing_birds import Hawk3D

class TestHawk3D(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Path to the test CSV file
        cls.csv_path = "tests/test_mean_hawk_shape.csv"
        cls.hawk3d = Hawk3D(cls.csv_path)

    def test_load_keypoints(self):
        # Test if keypoints are loaded correctly
        self.assertIsNotNone(self.hawk3d.default_shape)
        self.assertEqual(self.hawk3d.default_shape.shape[1], len(self.hawk3d.skeleton_definition.get_all_marker_names()))

    def test_define_indices(self):
        # Test if indices are defined correctly
        self.assertEqual(len(self.hawk3d.right_marker_index), len(self.hawk3d.skeleton_definition.get_right_marker_names()), "Right marker indices are not defined correctly")
        self.assertEqual(len(self.hawk3d.left_marker_index), len(self.hawk3d.skeleton_definition.get_left_marker_names()), "Left marker indices are not defined correctly")
        self.assertEqual(len(self.hawk3d.fixed_marker_index), len(self.hawk3d.skeleton_definition.fixed_marker_names), "Fixed marker indices are not defined correctly")

    def test_init_polygons(self):
        # Test if polygons are initialized correctly
        for section, markers in self.hawk3d.skeleton_definition.body_sections.items():
            indices = self.hawk3d.polygons[section]
            expected_indices = self.hawk3d.skeleton_definition.get_marker_indices(markers, self.hawk3d.csv_marker_names)
            self.assertEqual(indices, expected_indices)

    def test_get_polygon_coords(self):
        # Test if polygon coordinates are correct
        for section in self.hawk3d.skeleton_definition.body_sections.keys():
            coords = self.hawk3d.get_polygon_coords(section)
            indices = self.hawk3d.polygons[section]
            expected_coords = self.hawk3d.current_shape[0, indices, :]
            np.testing.assert_array_equal(coords, expected_coords)


    def test_polygon_shape(self):
        
        self.hawk3d.validate_polygon_shape()
if __name__ == '__main__':
    unittest.main()

