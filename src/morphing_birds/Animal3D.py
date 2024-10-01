import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import ipywidgets as widgets
from IPython.display import display, clear_output
from matplotlib.animation import FuncAnimation
from PIL import Image
import io

class Animal3D:
    """
    A class representing a 3D model of an animal.

    This class provides functionality to load, manipulate, and visualise
    3D keypoints representing a biomechanical shape ("skeleton"). It inherits from
    the HawkSkeletonDefinition class, which defines the basic outline structure.

    The Animal3D class allows users to:
    1. Load keypoint data from a CSV file
    2. Transform the keypoints (e.g., rotate, translate)
    3. Visualise the animal model in 3D
    4. Animate the model
    5. Run PCA on the keypoints and animate the principal components.


    Attributes:
        skeleton_definition (SkeletonDefinition): Defines the animal's outline (skeleton) structure
        right_marker_names (list): Names of markers on the right side of the animal
        left_marker_names (list): Names of markers on the left side of the animal
        csv_marker_names (list): Names of markers as they appear in the CSV file
        default_shape (numpy.ndarray): The original keypoint positions loaded from the CSV
        current_shape (numpy.ndarray): The current (possibly transformed) keypoint positions
        transformation_matrix (numpy.ndarray): 4x4 matrix representing current transformations
        origin (numpy.ndarray): The origin point for transformations
        untransformed_shape (numpy.ndarray): A copy of the original keypoint positions
    """
    def __init__(self, skeleton_definition):
        """
        Initializes the Animal3D class with the given CSV file path.

        Parameters:
        - csv_path (str): Path to the CSV file containing the animal's keypoints.
        """
        self.skeleton_definition = skeleton_definition

        # Initialize marker indices
        self.marker_index = []
        self.fixed_marker_index = []
        self.right_marker_index = []
        self.left_marker_index = []
        self.body_section_indices = {}
        self.polygons = {}

        # Initialize keypoints
        self.default_shape = None
        self.current_shape = None
        self.untransformed_shape = None

        # Transformation attributes
        self.transformation_matrix = np.identity(4)
        self.origin = np.zeros(3)


    def define_indices(self):
        """
        Defines and assigns marker indices for moving, fixed, right, and left markers based on csv_marker_names.
        """
        # Retrieve fixed and moving marker indices from SkeletonDefinition
        self.marker_index = self.skeleton_definition.get_marker_indices(
            self.skeleton_definition.marker_names,
            self.csv_marker_names
        )
        self.fixed_marker_index= self.skeleton_definition.get_marker_indices(
            self.skeleton_definition.fixed_marker_names,
            self.csv_marker_names
        )

        # Retrieve right and left marker indices
        self.right_marker_index = self.skeleton_definition.get_marker_indices(
            self.skeleton_definition.get_right_marker_names(),
            self.csv_marker_names
        )
        self.left_marker_index = self.skeleton_definition.get_marker_indices(
            self.skeleton_definition.get_left_marker_names(),
            self.csv_marker_names
        )

    def init_polygons(self):
        """
        Initializes polygon definitions based on body sections and their corresponding marker indices.
        """
        self.polygons = {}
        for section, indices in self.body_section_indices.items():
            self.polygons[section] = indices

    def get_polygon_coords(self, section_name: str) -> np.ndarray:
        """
        Retrieves the coordinates for a specific body section.

        Parameters:
        - section_name (str): Name of the body section.

        Returns:
        - numpy.ndarray: Coordinates of the polygon's keypoints.

        Raises:
        - ValueError: If the section name is not recognized.
        """
        if section_name not in self.polygons:
            raise ValueError(f"Section name '{section_name}' not recognized.")

        indices = self.polygons[section_name]
        coords = self.current_shape[0,indices, :]
        return coords

    def validate_keypoints(self, keypoints):
        """
        Validates the keypoints, ensuring they are three-dimensional and reshapes/mirrors them if necessary.

        Parameters:
        - keypoints (numpy.ndarray): The keypoints array to validate.

        Returns:
        - numpy.ndarray: The validated and potentially reshaped and mirrored keypoints.
        """

        if keypoints.size == 0:
            raise ValueError("No keypoints provided.")
        
        # Check they are in 3D
        if keypoints.shape[-1] != 3:
            raise ValueError("Keypoints must be in 3D space.")
        
        expected_markers = len(self.skeleton_definition.marker_names) + len(self.skeleton_definition.fixed_marker_names)
        if keypoints.shape[0] != expected_markers:
            raise ValueError(f"Expected {expected_markers} markers, but got {keypoints.shape[0]}.")

        # If [4,3] or [8,3] is given, reshape to [1,4,3] or [1,8,3]
        if len(np.shape(keypoints)) == 2:
            keypoints = keypoints.reshape(1, -1, 3)

        # If [1,4,3] is given, mirror it to make [1,8,3]
        if keypoints.shape[1] == len(self.right_marker_names):
            keypoints = self.mirror_keypoints(keypoints)

        return keypoints

    def mirror_keypoints(self,keypoints):
        """
        Mirrors keypoints across the y-axis to create a symmetrical set.

        Parameters:
        - keypoints (numpy.ndarray): Keypoints in shape [1, n, 3].

        Returns:
        - numpy.ndarray: Mirrored keypoints array in shape [1, 2*n, 3].
        """
        mirrored = np.copy(keypoints)
        mirrored[:, :, 0] *= -1

        nFrames, nMarkers, nCoords = np.shape(keypoints)

        # Create [n,8,3] array
        new_keypoints = np.empty((nFrames, nMarkers * 2, nCoords),
                                 dtype=keypoints.dtype)
        
        new_keypoints[:, 0::2, :] = mirrored
        new_keypoints[:, 1::2, :] = keypoints

        return new_keypoints

    def update_keypoints(self,user_keypoints):
        """
        Updates the keypoints based on user-provided data. Resets to default if no keypoints are provided.
        Validates and mirrors the keypoints if necessary, and applies transformations.

        Parameters:
        - user_keypoints (numpy.ndarray or None): Array of keypoints provided by the user. 
        If None, resets to the default keypoints setup.
        """

        # Make sure the current_shape starts as default to reset it
        if user_keypoints is None:
            # Reset to default shape if no user keypoints are provided
            self.restore_keypoints_to_average()
            return

        # First validate the keypoints. This will mirror them 
        # if only the right side is given. Also checks they are in 3D and 
        # will return [n,8,3]. 

        # Validate and possibly mirror the user keypoints -- returns [n,8,3] 
        # If only the right side is given, the left side is created by mirroring.
        # Also checks in 3D space. 
        validated_keypoints = self.validate_keypoints(user_keypoints)


        # Update the keypoints with the user marker info. 
        # Only non fixed markers are updated.
        self.current_shape[:,self.marker_index,:] = validated_keypoints      

        # Save the untransformed shape
        self.untransformed_shape = self.current_shape.copy()

        # Apply transformations
        self.apply_transformation()

    def transform_keypoints(self, bodypitch=0, horzDist=0, vertDist=0, yaw=0):
        """
        Transforms the keypoints by rotating them around the body pitch, 
        and translating them by the horizontal and vertical distances.
        """

        # Reset the transformation matrix
        self.reset_transformation()

        # Apply any translations
        self.update_translation(horzDist, vertDist)

        # Apply any rotations
        self.update_rotation(bodypitch)

        self.update_rotation(yaw, which='z')

        # Apply the transformation
        self.apply_transformation()

    def update_rotation(self, degrees=0, which='x'):
        """
        Updates the transformation matrix with a rotation around the x-axis.
        """
        radians = np.deg2rad(degrees)
        if which == "x":
            rotation_matrix = np.array([
                [1,0,0,0],
                [0, np.cos(radians), -np.sin(radians), 0],
                [0, np.sin(radians),  np.cos(radians), 0],
                [0,0,0,1]
            ])
        elif which == "y":
            rotation_matrix = np.array([
                [np.cos(radians), 0, np.sin(radians), 0],
                [0,1,0,0],
                [-np.sin(radians), 0, np.cos(radians), 0],
                [0,0,0,1]
            ])
        elif which == "z":
            rotation_matrix = np.array([
                [np.cos(radians), -np.sin(radians), 0, 0],
                [np.sin(radians),  np.cos(radians), 0, 0],
                [0,0,1,0],
                [0,0,0,1]
            ])

        # rotation_matrix = np.array([
        #     [1,0,0,0],
        #     [0, np.cos(radians), -np.sin(radians), 0],
        #     [0, np.sin(radians),  np.cos(radians), 0],
        #     [0,0,0,1]
        # ])

        self.transformation_matrix = self.transformation_matrix @ rotation_matrix



    def update_translation(self,horzDist=0, vertDist=0):
        """
        Updates the transformation matrix with horizontal and vertical translations.
        """
        translation_matrix = np.array([
            [1,0,0,0],
            [0,1,0,horzDist],
            [0,0,1,vertDist],
            [0,0,0,1]
        ])
        self.transformation_matrix = self.transformation_matrix @ translation_matrix

        # Update origin
        self.origin = [0, horzDist, vertDist]

    def apply_transformation(self):

        """
        Applies the current transformation matrix to the keypoints.
        """
        # Adding a homogeneous coordinate directly to the current_shape
        homogeneous_keypoints = np.hstack((self.current_shape.reshape(-1, 3), np.ones((self.current_shape.shape[1], 1))))
        
        transformed_keypoints = np.dot(homogeneous_keypoints, self.transformation_matrix.T)
        
        self.current_shape = transformed_keypoints[:, :3].reshape(1, -1, 3)

    def reset_transformation(self):
        self.transformation_matrix = np.eye(4)
        self.current_shape = self.untransformed_shape

        # Also reset the origin
        self.origin = np.array([0,0,0])

    def restore_keypoints_to_average(self):
        """
        Restores the keypoints and origin to the default shape.
        """
        self.current_shape = self.default_shape.copy()
        self.untransformed_shape = self.current_shape.copy()

        # Also update the origin
        self.origin = np.array([0,0,0])

    @property
    def markers(self):
        """
        Returns the non-fixed markers.
        """
        
        marker_index = self.marker_index
        
        return self.current_shape[:,marker_index,:]

    @property
    def right_markers(self):
        """
        Returns the right side markers.
        """
        
        right_marker_index = self.right_marker_index
        
        return self.current_shape[:,right_marker_index,:]
    
    @property
    def default_markers(self):
        """
        Returns the default markers.
        """
        
        marker_index = self.marker_index
        
        return self.default_shape[:,marker_index,:]

    @property
    def default_right_markers(self):
        """
        Returns the right side markers.
        """
        
        right_marker_index = self.right_marker_index
        
        return self.default_shape[:,right_marker_index,:]



     

# ----- Plot Functions -----
 
