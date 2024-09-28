import numpy as np

class SkeletonDefinition:
    def __init__(self, marker_names, fixed_marker_names, body_sections):
        self.marker_names = marker_names
        self.fixed_marker_names = fixed_marker_names
        self.body_sections = body_sections

    def get_keypoint_indices(self, section_name):
        return [self.marker_names.index(marker) for marker in self.body_sections[section_name]]

    def get_marker_index(self, marker_name):
        return self.all_marker_names.index(marker_name)

    def get_section_markers(self, section_name):
        return self.body_sections[section_name]    