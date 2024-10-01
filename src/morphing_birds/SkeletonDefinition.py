import numpy as np

class SkeletonDefinition:
    def __init__(self, marker_names: list, fixed_marker_names: list, body_sections: dict):
        """
        Initializes the SkeletonDefinition with marker names and body sections.

        Parameters:
        - csv_marker_names (list): List of all marker names from the CSV in correct order.
        - fixed_marker_names (list): List of fixed marker names.
        - body_sections (dict): Dictionary defining body sections with their respective marker names.
        """
        self.marker_names = marker_names
        self.fixed_marker_names = fixed_marker_names
        self.body_sections = body_sections

    def get_marker_indices(self, marker_subset: list, csv_marker_names: list) -> list:
        """
        Retrieves indices for a subset of markers based on csv_marker_names.

        Parameters:
        - marker_subset (list): Specific markers to retrieve indices for.
        - csv_marker_names (list): List of all marker names from the CSV in the correct order.

        Returns:
        - list: List of indices corresponding to the marker_subset.

        Raises:
        - ValueError: If any marker in the subset is not found in csv_marker_names.
        """
        indices = []
        for name in marker_subset:
            if name in csv_marker_names:
                index = csv_marker_names.index(name)
                indices.append(index)
            else:
                raise ValueError(f"Marker '{name}' not found in CSV marker names.")
        return indices
    
    def get_body_section_indices(self, csv_marker_names: list) -> dict:
        """
        Returns a dictionary mapping each body section to its respective marker indices.

        Parameters:
        - csv_marker_names (list): List of all marker names from the CSV in the correct order.

        Returns:
        - dict: Dictionary with body section names as keys and lists of marker indices as values.

        Raises:
        - ValueError: If any marker in a body section is not found in csv_marker_names.
        """
        section_indices = {}
        for section, markers in self.body_sections.items():
            section_indices[section] = self.get_marker_indices(markers, csv_marker_names)
        return section_indices
    
    def get_right_marker_names(self) -> list:
        """
        Returns a list of names for all right-side markers.
        """
        return [name for name in self.marker_names if name not in self.fixed_marker_names]

    def get_left_marker_names(self) -> list:
        """
        Returns a list of names for all left-side markers.
        """
        return [name for name in self.marker_names if name not in self.fixed_marker_names]

    def get_right_marker_indices(self) -> list:
        """
        Returns a list of indices for all right-side markers.
        """
        return self.get_marker_indices(self.get_right_marker_names())

    def get_left_marker_indices(self) -> list:
        """
        Returns a list of indices for all left-side markers.
        """
        return self.get_marker_indices(self.get_left_marker_names())
