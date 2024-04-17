import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import ipywidgets as widgets
from IPython.display import display, clear_output
from matplotlib.animation import FuncAnimation
from sklearn.decomposition import PCA




# --- OLD CODE ---

# class HawkData:

#     def __init__(self, csv_path):
#         self.markers = self.load_marker_frames(csv_path)
        
#         self.load_frame_data(csv_path)

#         self.check_data()

#     def load_marker_frames(self, csv_path):
#         """Load the unilateral markers dataset.

#         Returns
#         -------
#         data : pandas.DataFrame
#             The data frame containing the unilateral markers dataset.
#         """
#         # Load the data
#         markers_csv = pd.read_csv(csv_path)

#         # Rename the columns
#         markers_csv.columns = markers_csv.columns.str.replace("_rot_xyz_1", "_x")
#         markers_csv.columns = markers_csv.columns.str.replace("_rot_xyz_2", "_y")
#         markers_csv.columns = markers_csv.columns.str.replace("_rot_xyz_3", "_z")

#         # Get the index of the columns that contain the markers
#         marker_index = markers_csv.columns[markers_csv.columns.str.contains('_x|_y|_z')]
#         markers_csv = markers_csv[marker_index]

#         # Save the cleaned up dataframe
#         self.dataframe = markers_csv

#         # Make a numpy array with the markers
#         unilateral_markers = markers_csv.to_numpy()

#         # Reshape to 3D
#         unilateral_markers = unilateral_markers.reshape(-1,4,3)
        
#         return unilateral_markers

#     def load_frame_data(self, csv_path):
#         """Load the frame info from the dataset.

#         Returns
#         -------
#         data : pandas.DataFrame
#             The data frame containing the unilateral markers dataset.
#         """
#         # Load the data
#         markers_csv = pd.read_csv(csv_path)

#         # Makes horizontal distance NEGATIVE
#         markers_csv['HorzDistance'] = -markers_csv['HorzDistance']
        
#         self.horzDist = markers_csv['HorzDistance'].to_numpy()
#         self.frameID = markers_csv['frameID']
#         self.leftBool = markers_csv['Left'].to_numpy()
#         self.body_pitch = markers_csv['body_pitch'].to_numpy()
#         self.obstacleBool = markers_csv['Obstacle'].to_numpy()
#         self.IMUBool = markers_csv['IMU'].to_numpy()
#         self.time = markers_csv['time'].to_numpy()

#         # Add variables to dataframe
#         self.dataframe['frameID'] = self.frameID
#         self.dataframe['time'] = self.time
#         self.dataframe['HorzDistance'] = self.horzDist
#         self.dataframe['body_pitch'] = self.body_pitch
#         self.dataframe['Obstacle'] = self.obstacleBool
#         self.dataframe['IMU'] = self.IMUBool
#         self.dataframe['Left'] = self.leftBool

#     def get_data_table(self):

#         # Create a dataframe with the data
#         data = pd.DataFrame(self.markers.reshape(-1,12), columns=self.marker_names)

#     def check_data(self):
#         """
#         Check that the data are the same length.
#         """

#         num_frames = self.markers.shape[0]

#         if self.horzDist.shape[0] != num_frames:
#             raise ValueError("horzDist must be the same length as keypoints_frames.")
        
#         if len(self.frameID) != num_frames:
#             raise ValueError("frameID must be the same length as keypoints_frames.")
        
#         if self.leftBool.shape[0] != num_frames:
#             raise ValueError("leftBool must be the same length as keypoints_frames.")
        
#         if self.body_pitch.shape[0] != num_frames:
#             raise ValueError("body_pitch must be the same length as keypoints_frames.")
        
#         if self.obstacleBool.shape[0] != num_frames:
#             raise ValueError("obstacleBool must be the same length as keypoints_frames.")
        
#         if self.IMUBool.shape[0] != num_frames:
#             raise ValueError("IMUBool must be the same length as keypoints_frames.")
        
#     def filter_by(self,
#                   hawk=None,
#                   perchDist=None, 
#                   obstacle=False, 
#                   year=None, 
#                   Left=None,
#                   IMU=False):
#         """
#         Returns boolean array of indices to filter the data.
#         """

#         def filter_by_bool(variable, bool_value):

#             if bool_value is None:
#                 # Simply return the full array bool mask if passed None
#                 is_selected = np.ones(variable.shape, dtype=bool)
#                 return is_selected
            
#             is_selected = variable == bool_value
#             return is_selected

#         # Get frameID
#         frameID = self.frameID

#         # Initialise the filter
#         filter = np.ones(len(self.frameID), dtype=bool)

#         # Filter by hawk_ID
#         if hawk is not None:
#             filter = np.logical_and(filter, HawkData.filter_by_hawk_ID(frameID, hawk))

#         # Filter by perchDist
#         if perchDist is not None:
#             filter = np.logical_and(filter, HawkData.filter_by_perchDist(frameID, perchDist))

#         # Filter by obstacleToggle
#         # if obstacle is not None:
#         filter = np.logical_and(filter, filter_by_bool(self.obstacleBool, obstacle))

#         # Filter by IMUToggle
#         # if IMU is not None:
#         filter = np.logical_and(filter, filter_by_bool(self.IMUBool, IMU))

#         # Filter by Left
#         # if Left is not None:
#         filter = np.logical_and(filter, filter_by_bool(self.leftBool, Left))

#         # Filter by year
#         # if year is not None:
#         filter = np.logical_and(filter, HawkData.filter_by_year(frameID,year))
        
#         return filter

#     @staticmethod  
#     def filter_by_hawk_ID(frameID, hawk: str):

#         def get_hawkID(hawk_name):

#             if hawk_name.isdigit():
#                 # Transform the hawk_ID into a string with the correct format
#                 hawk_ID = str(hawk_name).zfill(2) + "_"
                
#             # The user may have provided the full name of the hawk, or just the first few letters
#             # And so returns the matching ID.

#             if "dr" in hawk_name.lower():
#                 hawk_ID = "01_"  
#             if "rh" in hawk_name.lower():
#                 hawk_ID = "02_"
#             if "ru" in hawk_name.lower():
#                 hawk_ID = "03_"  
#             if "to" in hawk_name.lower():
#                 hawk_ID = "04_"  
#             if "ch" in hawk_name.lower():
#                 hawk_ID = "05_"
            
#             return hawk_ID
        
#         if hawk is None:
#             is_selected = np.ones(len(frameID), dtype=bool)
#             return is_selected
#         else:
#             hawk_ID = get_hawkID(hawk)

#         is_selected = frameID.str.startswith(hawk_ID)

#         return is_selected
    
#     @staticmethod
#     def filter_by_perchDist(frameID, perchDist):

#         # If perchDist is None, return the full array bool mask
#         if perchDist is None:
#             is_selected = np.ones(frameID, dtype=bool)
#             return is_selected
        

#         # Get any number from the perchDist string. The user may have given 
#         # "12m" or "12 m" or "12"
#         if perchDist.isdigit():
#             perchDist = int(perchDist)
#         else:
#             perchDist = int(''.join(filter(str.isdigit, perchDist)))

#         # Build back up the string to search for
#         # Make sure the integer is padded such that it is 2 digits in length
#         perchDist_str = "_" + str(perchDist).zfill(2) + "_"
        
#         # Now looks for _05_ or _12_ etc in the frameID. Note, 05_09_ would be 
#         # charmander flying 9m so we need to make sure we don't select that by leading 
#         # and trailing _ . HawkID should always be found with "startswith". 

#         is_selected = frameID.str.contains(perchDist_str)
        
#         return is_selected

#     @staticmethod
#     def filter_by_year(frameID, year):
        
#         if year is None:
#             is_selected = np.ones(len(frameID), dtype=bool)
#             return is_selected

#         # Data from 2017 and 2020 have different frameID formats, 
#         # there's an extra _ in the frameID for 2020
#         if year == 2017:
#             is_selected = frameID.str.count('_') == 3
#         elif year == 2020:
#             is_selected = frameID.str.count('_') == 4
#         else:
#             raise ValueError("Year must be 2017 or 2020.")
        
#         return is_selected


# class KeypointManager:

#     right_marker_names = [
#         "right_wingtip", 
#         "right_primary", 
#         "right_secondary",
#         "right_tailtip"]
    
#     left_marker_names = [
#         "left_wingtip", 
#         "left_primary", 
#         "left_secondary",
#         "left_tailtip"]
    
#     marker_names = [
#         "left_wingtip",   "right_wingtip", 
#         "left_primary",   "right_primary", 
#         "left_secondary", "right_secondary", 
#         "left_tailtip",   "right_tailtip"]
    
#     fixed_marker_names = [
#         "left_shoulder", 
#         "left_tailbase", 
#         "right_tailbase", 
#         "right_shoulder",
#         "hood", 
#         "tailpack"
#     ]

#     def __init__(self, filename):

#         # Get the keypoint data from file.
#         self.load_data(filename)
        
#     def load_data(self,filename):

#         # load the data
#         with open(filename, 'r') as file:
#             data = np.loadtxt(file, delimiter=',', skiprows=0, dtype='str')
        
#         # Get the marker names from the first row of the csv file, 
#         # get every 3rd name and remove the '_x' from the names
#         csv_keypoint_names = data[0].reshape(-1, 3)
#         csv_keypoint_names = list(np.char.strip(csv_keypoint_names[:, 0], '_x'))

#         # Save the keypoint names
#         self.csv_keypoint_names = csv_keypoint_names


#         # Load marker coordinates and reshape to [n,3] matrix where n is the
#         # number of markers
#         keypoints = data[1].astype(float)
#         keypoints = keypoints.reshape(-1, 3) # [n,3]

#         # Get the indices of the markers
#         self.right_marker_index = self.get_keypoint_indices(self.right_marker_names)
#         self.left_marker_index  = self.get_keypoint_indices(self.left_marker_names)
#         self.marker_index       = self.get_keypoint_indices(self.marker_names)
#         self.fixed_marker_index = self.get_keypoint_indices(self.fixed_marker_names)

#         # Save the keypoints, and a safe copy. 
#         self.keypoints_original = np.copy(keypoints)
#         self.keypoints = keypoints

#     def get_keypoint_indices(self,names_to_find=None):
#             """
#             Returns the indices of the keypoints with the given names.
#             """
#             csv_keypoint_names = self.csv_keypoint_names

#             # If no names are given, use all the marker names (not the fixed ones)
#             if names_to_find is None:
#                 names_to_find = self.marker_names

#             indices = [csv_keypoint_names.index(name) for name in names_to_find]

#             return indices
    
#     def validate_keypoints(self,keypoints):

#         # First check they are not empty
#         if self.is_empty_keypoints(keypoints):
#             raise ValueError("No keypoints given.")
        
#         # Check they are in 3D
#         if keypoints.shape[-1] != 3:
#             raise ValueError("Keypoints not in 3D.")
        
#         # If [4,3] or [8,3] is given, reshape to [1,4,3] or [1,8,3]
#         if len(np.shape(keypoints)) == 2:
#             keypoints = keypoints.reshape(1, -1, 3)

#         # If [1,4,3] is given, mirror it to make [1,8,3]
#         if keypoints.shape[1] == len(self.right_marker_names):
#             keypoints = self._mirror_keypoints(keypoints)

#         # Then check there are enough keypoints
#         if keypoints.shape[1] != len(self.marker_names):
#             raise ValueError("Keypoints missing.")
        
#         return keypoints
        
#     def update_keypoints(self,user_keypoints):
#         """ 
#         Assumes the keypoints from the user are in the same order as the
#         marker names.
#         State changes Hawk3D.keypoints. 
#         """


#         # First validate the keypoints. This will mirror them 
#         # if only the right side is given. Also checks they are in 3D and 
#         # will return [n,8,3]. 

#         user_keypoints = self.validate_keypoints(user_keypoints)

#         # Update the keypoints with the user marker info. 
#         self.keypoints[self.marker_index] = user_keypoints

#     def transform_keypoints(self,
#                             horzDist=None,
#                             bodypitch=None, 
#                             vertDist=None):
        
#         """
#         If any of the parameters are None, they are not applied. 
#         """
        
#         # Make an unaltered copy of the keypoints
#         if horzDist is not None or bodypitch is not None or vertDist is not None:
#             self.keypoints_no_translation = np.copy(self.keypoints)
#         else:
#             self.keypoints_no_translation = None
#             print("No transformation applied.")
#             return

#         if bodypitch is not None:
#             self.add_pitchRotation(bodypitch)
        
#         if horzDist is not None:
#             self.add_horzDist(horzDist)
#             # print("Horizontal translation applied.")

#         if vertDist is not None:
#             self.add_vertDist(vertDist)

#         return self.keypoints
    
#     def restore_keypoints(self):

#         """
#         Makes the keypoints return to the previous 
#         state with no translation or rotation.
#         """

#         if self.keypoints_no_translation is None:
#             print("No previous keypoints to restore.")
#             return
        
#         self.keypoints = self.keypoints_no_translation
#         self.keypoints_no_translation = None

#     def add_pitchRotation(self, bodypitch):

#         if bodypitch is None:
#             return
    
#         rotmat = R.from_euler('x', bodypitch, degrees=True)
#         rot_keypoints = rotmat.apply(self.keypoints)

        
#         self.keypoints = rot_keypoints
        
#     def add_horzDist(self, horzDist):
#         if horzDist is None:
#             return

#         self.keypoints[:,1] += horzDist
    
#     def add_vertDist(self, vertDist):
#         if vertDist is None:
#             return

#         self.keypoints[:,2] += vertDist
        
#     @staticmethod
#     def _mirror_keypoints(keypoints):
#         """
#         Mirrors keypoints across the y-axis.
#         """
#         mirrored = np.copy(keypoints)
#         mirrored[:, :, 0] *= -1

#         nFrames, nMarkers, nCoords = np.shape(keypoints)

#         # Create [n,8,3] array
#         new_keypoints = np.empty((nFrames, nMarkers * 2, nCoords),
#                                  dtype=keypoints.dtype)
        
#         new_keypoints[:, 0::2, :] = mirrored
#         new_keypoints[:, 1::2, :] = keypoints

#         return new_keypoints

#     @staticmethod
#     def is_empty_keypoints(keypoints):
#         if isinstance(keypoints, np.ndarray) and keypoints.size > 0:
#             return False
#         else:
#             return True
        
#     def validate_frames(self, keypoints_frames):
#         """
#         Validates the keypoints_frames and returns a list of keypoints for each frame.
#         """
#         if not isinstance(keypoints_frames, list):
#             keypoints_frames = [keypoints_frames]
#         for ii, keypoints in enumerate(keypoints_frames):

#             # The if statement is to ensure that all keypoint sequences have the same length
#             if ii > 0 and keypoints.shape[0] != keypoints_frames[ii - 1].shape[0]:
#                 raise ValueError("All keypoint sequences must have the same length")
            
#             keypoints_frames[ii] = self._validate_keypoints(keypoints)
#         return keypoints_frames
    

# class HawkAnimator:
#     def __init__(self, plotter):

#         """ 
#         Uses the HawkPlotter class to create an animated 3D plot of a hawk video.
        
#         """
#         self.plotter = plotter

#     def _format_keypoint_frames(self, keypoints_frames):

#         """
#         Formats the keypoints_frames to be [n,8,3] where n is the number of frames 
#         and 8 is the number of keypoints and 3 is the number of dimensions.
#         If just 4 keypoints are given, the function will mirror the keypoints to make the left side.
#         """

#         if len(np.shape(keypoints_frames)) == 2:
#             keypoints_frames = keypoints_frames.reshape(1, -1, 3)
#             print("Warning: Only one frame given.")

#     # Mirror the keypoints_frames if only the right is given. 
#         if keypoints_frames.shape[1] == len(self.plotter.keypoint_manager.names_right_keypoints):
#             keypoints_frames = self.plotter.keypoint_manager._mirror_keypoints(keypoints_frames)

#         return keypoints_frames
        
#     def animate(self, 
#                 keypoints_frames, 
#                 fig=None, 
#                 ax=None, 
#                 rotation_type="static", 
#                 el=20, 
#                 az=60, 
#                 alpha=0.3, 
#                 colour=None, 
#                 horzDist_frames=None, 
#                 bodypitch_frames=None):
#         """
#         Create an animated 3D plot of a hawk video.
#         """

#         # Mirror the keypoints if only the right is given.
#         keypoints_frames = self._format_keypoint_frames(keypoints_frames)

#         # Find the number of frames 
#         num_frames = keypoints_frames.shape[0]


#         # Initialize figure and axes
#         if ax is None:
#             fig, ax = self.plotter.get_plot3d_view(fig)

#         # Prepare camera angles
#         el_frames, az_frames = self.get_camera_angles(num_frames=num_frames, 
#                                                       rotation_type=rotation_type, 
#                                                       el=el, 
#                                                       az=az)
        
#         # Check if the horzDist_frames is given, if so check it is the correct length
#         if horzDist_frames is not None:
#             if len(horzDist_frames) != num_frames:
#                 raise ValueError("horzDist_frames must be the same length as keypoints_frames.")
            
#         # Check if the bodypitch_frames is given, if so check it is the correct length
#         if bodypitch_frames is not None:
#             if len(bodypitch_frames) != num_frames:
#                 raise ValueError("bodypitch_frames must be the same length as keypoints_frames.")
            
#         # Plot settings
#         self.plotter._plot_settings(ax, horzDist=0 if horzDist_frames is None else horzDist_frames)

        
#         def update_animated_plot(frame, *fargs):
#             """
#             Function to update the animated plot.
#             """

#             fig, ax, keypoints, el_frames, az_frames, alpha, colour, horzDist_frames, bodypitch_frames = fargs
#             ax.clear()
#             # Here, you need to adjust how keypoints for the current frame are passed to plot
#             self.plotter.plot(keypoints=keypoints[frame], 
#                               fig=fig, 
#                               ax=ax, 
#                               el=el_frames[frame], 
#                               az=az_frames[frame], 
#                               alpha=alpha, 
#                               colour=colour, 
#                               horzDist=horzDist_frames[frame] if horzDist_frames else None, 
#                               bodypitch=bodypitch_frames[frame] if bodypitch_frames else None)
#             return fig, ax

#         # Creating the animation
#         animation = FuncAnimation(fig, update_animated_plot, 
#                                   frames=num_frames, 
#                                   fargs=(fig, ax, keypoints_frames, el_frames, az_frames, alpha, colour, horzDist_frames, bodypitch_frames), 
#                                   interval=20, repeat=True)
        
#         return animation

#     def get_camera_angles(self,num_frames, rotation_type, el=20, az=60):
#         """
#         Creates two arrays of camera angles for the length of the animation.

#         "static" -- the angles do not change in the animation, set using el, az.

#         "dynamic" -- fast rotations

#         "slow" -- slow rotations

#         Used in: Creates inputs for plot_hawk3D_frame
#         """

#         if el is None or az is None:
#             return [None, None]

#         def linspacer(number_array, firstValue, endValue, nFrames):
#             """
#             Function to make linearly spaced numbers between two values of a
#             given length.
#             """

#             number_array = np.append(
#                 number_array, np.linspace(firstValue, endValue, nFrames))
#             return number_array

#         if "dynamic" in rotation_type:

#             tenthFrames = round(num_frames * 0.1)
#             remainderFrames = num_frames - (tenthFrames * 9)

#             az_frames = np.linspace(40, 40, tenthFrames)
#             az_frames = linspacer(az_frames, 40, 10, tenthFrames)
#             az_frames = linspacer(az_frames, 10, 10, tenthFrames)
#             az_frames = linspacer(az_frames, 10, 90, tenthFrames)
#             az_frames = linspacer(az_frames, 90, 90, tenthFrames * 2)
#             az_frames = linspacer(az_frames, 90, -90, tenthFrames)
#             az_frames = linspacer(az_frames, -90, -90, tenthFrames)
#             az_frames = linspacer(az_frames, -90, 40, tenthFrames)
#             az_frames = linspacer(az_frames, 40, 40, remainderFrames)

#             el_frames = np.linspace(20, 20, tenthFrames)
#             el_frames = linspacer(el_frames, 20, 15, tenthFrames)
#             el_frames = linspacer(el_frames, 15, 0, tenthFrames)
#             el_frames = linspacer(el_frames, 0, 0, tenthFrames)
#             el_frames = linspacer(el_frames, 0, 80, tenthFrames)
#             el_frames = linspacer(el_frames, 80, 80, tenthFrames)
#             el_frames = linspacer(el_frames, 80, 15, tenthFrames)
#             el_frames = linspacer(el_frames, 15, 15, tenthFrames)
#             el_frames = linspacer(el_frames, 15, 20, tenthFrames)
#             el_frames = linspacer(el_frames, 20, 20, remainderFrames)

#         elif "slow" in rotation_type:

#             halfFrames = round(num_frames * 0.5)
#             tenthFrames = round(num_frames * 0.1)
#             remainderFrames = num_frames - (halfFrames + (tenthFrames * 2) +
#                                             tenthFrames + tenthFrames)

#             az_frames = np.linspace(90, 90, halfFrames)
#             az_frames = linspacer(az_frames, 90, -90,
#                                   tenthFrames)  # Switch to back
#             az_frames = linspacer(az_frames, -90, -90, tenthFrames * 2)
#             az_frames = linspacer(az_frames, -90, 90,
#                                   tenthFrames)  # Switch to front
#             az_frames = linspacer(az_frames, 90, 90, remainderFrames)

#             remainderFrames = num_frames - (tenthFrames * 9)

#             el_frames = np.linspace(80, 80, tenthFrames * 2)
#             el_frames = linspacer(el_frames, 80, 20,
#                                   tenthFrames)  # Transition to lower
#             el_frames = linspacer(el_frames, 20, 20, tenthFrames * 2)
#             el_frames = linspacer(el_frames, 20, 10,
#                                   tenthFrames)  # Switch to back
#             el_frames = linspacer(el_frames, 10, 10, tenthFrames * 3)
#             el_frames = linspacer(el_frames, 10, 80,
#                                   remainderFrames)  # Switch to front

#         else:
#             el_frames = np.linspace(el, el, num_frames)
#             az_frames = np.linspace(az, az, num_frames)

#         return el_frames, az_frames



# class HawkPCA_OLD:

#     """
#     Class to run PCA on the Hawk3D data.
#     """
    
#     def __init__(self, HawkData, KeypointManager):
#         self.data = HawkData
#         self.mu = KeypointManager.right_keypoints

#         # Make the dimensions fit for PCA
#         self.mu = self.mu.reshape(1,12)

#     def get_input(self, data=None):

#         if data is None:
#             data = self.data.markers

#         # The data is in the shape (n_frames, n_markers*n_dimensions)
#         pca_input = data.reshape(-1,12)

#         return pca_input
    
#     def run_PCA(self, data=None):

#         pca_input = self.get_input(data)
       
#         pca = PCA()
#         pca_output = pca.fit(pca_input)

#         self.pca_input = pca_input

#         # Another word for eigenvectors is components.
#         self.principal_components = pca_output.components_

#         # Another word for scores is projections.
#         self.scores = pca_output.transform(pca_input)

#     def get_score_range(self, num_frames=30):

#         num_components = self.scores.shape[1]

#         min_score = np.mean(self.scores, axis=0) - (2 * np.std(self.scores, axis=0))
#         max_score = np.mean(self.scores, axis=0) + (2 * np.std(self.scores, axis=0))

#         half_length = num_frames // 2 + 1

#         # Initialize score_frames with the shape [n, 12]
#         self.score_frames = np.zeros([num_frames, num_components])


#         for ii in range(num_components):
        
#             # Create forward and backward ranges for each component using np.linspace
#             forward = np.linspace(min_score[ii], max_score[ii], num=half_length)
            
#             # # If num_frames is odd, we add an extra element to 'forward'
#             # if num_frames % 2 != 0:
#             #     forward = np.append(forward, max_score[ii])
            
#             backward = forward[::-1]  # Reverse the forward range

#             # Combine forward and backward, and assign to the i-th column
#             self.score_frames[:, ii] = np.concatenate((forward, backward[:num_frames - half_length]))

#     def select_components(self, components_list):

#         selected_components = self.principal_components[:,components_list]
        
#         return selected_components

#     def reconstruct(self,components_list=None, score_frames=None):

#         if components_list is None:
#             components_list = range(12)
        
#         if score_frames is None:
#             score_frames = self.score_frames
#         else:

#             # Check score_frames are a numpy array
#             if not isinstance(score_frames, np.ndarray):
#                 raise TypeError("score_frames must be a numpy array.")

#             # Check the score_frames are the right shape
#             if score_frames.shape[1] != self.principal_components.shape[0]:
#                 raise ValueError("score_frames must have the same number of columns as components_list.")
            
#             if len(score_frames.shape) != 2:
#                 raise ValueError("score_frames must be 2d.")
            

#         selected_PCs = self.principal_components[components_list]
#         selected_scores = score_frames[:,components_list]

        
#         num_frames = score_frames.shape[0]
#         reconstructed_frames = np.empty((0,4,3))


#         selected_PCs = selected_PCs.reshape(1, -1, 4, 3)  # [1, nPCs, 4, 3]
#         selected_scores = selected_scores.reshape(num_frames, -1, 1, 1)  # [n, nPCs, 1, 1]
#         mu = self.mu.reshape(1, 4, 3)  # [1, 4, 3]

#         reconstructed_frames = mu + np.sum(selected_scores * selected_PCs, axis=1)

#         return reconstructed_frames

#     def get_results_table(self,filter=None):


#         # Using the original dataframe from the csv, concat the PCA scores
#         # Filter makes sure the data is the same size as the PCA input. 
#         self.results_table = self.concat_scores(filter)

#         # Add a bins column based on the horizontal distance
#         self.bin_by_horz_distance()

#         return self.results_table

#     def concat_scores(self, filter=None):

#         """
#         Returns a pandas dataframe with the scores added to the original data.
#         """

#         # If filter is None, check the input is the same
#         # size as the original data and warn the user.
#         if filter is None:
#             if self.data.markers.shape[0] != self.scores.shape[0]:
#                 raise ValueError("Please input the filter you used to run the PCA.")

#         # Get the data pandas dataframe, just the useful columns
#         col_names = ['frameID','time','HorzDistance','body_pitch','Obstacle','IMU','Left']
#         data = self.data.dataframe[col_names]

#         # Apply the filter if given
#         if filter is not None:
#             data = data[filter]
#         else:
#             data = data

#         num_components = self.scores.shape[1]

#         # Add the scores to the dataframe. Give the column the name 'PC1' etc.
#         PC_names = ["PC" + str(i) for i in range(1, num_components+1)]

#         score_df = pd.DataFrame(self.scores, columns=PC_names)

#         data = pd.concat([data, score_df], axis=1)

#         return data
    
#     def bin_by_horz_distance(self, size_bin=0.05):

#         """
#         Bin the horizontal distance into bins of size size_bin.
#         Using the HawkPCA results dataframe.
#         """

#         bins = np.arange(-12.2,0.2, size_bin)
#         bins = np.around(bins, 3)
#         labels = bins.astype(str).tolist()
#         # make label one smaller
#         labels.pop(0)

#         self.results_table['bins'] = pd.cut(self.results_table['HorzDistance'], 
#                                        bins, 
#                                        right=False, 
#                                        labels = labels, 
#                                        include_lowest=True)
    
#     def filter_results_by(self,
#                   hawk=None,
#                   perchDist=None, 
#                   obstacle=False, 
#                   year=None, 
#                   Left=None,
#                   IMU=False):
#         """
#         Returns boolean array of indices to filter the data.
#         Somewhat of a repeat of HawkData.filter_by but that is not compatible with
#         pandas, maybe refactor it there.
#         """

#         # Get the data pandas dataframe
#         data = self.results_table
#         frameID = data.frameID

#         # Initialise the filter
#         filter = np.ones(len(frameID), dtype=bool)

#         # Filter by hawk
#         if hawk is not None:
#             filter = np.logical_and(filter, HawkData.filter_by_hawk_ID(frameID, hawk))

#         # Filter by perchDist
#         if perchDist is not None:
#             filter = np.logical_and(filter, HawkData.filter_by_perchDist(frameID, perchDist))

#         # Filter by year
#         if year is not None:
#             filter = np.logical_and(filter, HawkData.filter_by_year(frameID,year))

#         # Filter by obstacle
#         if obstacle is not None:
#             filter = np.logical_and(filter, data.Obstacle==obstacle)
            
#         # Filter by Left
#         if Left is not None:
#             filter = np.logical_and(filter, data.Left==Left)
            
#         # Filter by IMU
#         if IMU is not None:
#             filter = np.logical_and(filter, data.IMU==IMU)
        
#         return data[filter]
         
#     def binned_results(self, results_table=None):
 
#         """
#         Returns a dataframe with the mean scores and std scores for each bin, plus 
#         the mean for horizontal distance, time and body pitch.
#         """

#         def mean_score_by_bin(results_table):

#             # Get the PC names
#             PC_columns = results_table.filter(like='PC')

#             # observed=True is to prevent a warning about future behaviour. 
#             # See https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-specify
#             # It will only group by the bins that are present in the data, 
#             # so in this case it is irelevant.
            
#             mean_scores = PC_columns.groupby(results_table['bins'], observed=True).mean()

#             return mean_scores
        
#         def std_score_by_bin(results_table):

#             # Get the PC names
#             PC_columns = results_table.filter(like='PC')

#             # observed=True is to prevent a warning about future behaviour. 
#             # See https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html#groupby-specify
            
#             std_scores = PC_columns.groupby(results_table['bins'], observed=True).mean()

#             return std_scores
        
#         def mean_col_by_bin(results_table,column_name):
            
#             mean_column = results_table.groupby('bins', observed=True)[column_name].mean()

#             return mean_column


#         if results_table is None:
#             results_table = self.results_table
#             print("Binning full data, no filters applied.")


#         binned_means_scores = mean_score_by_bin(results_table)
#         binned_std_scores = std_score_by_bin(results_table)

#         # Concatenate HorzDist means etc to the binned_means_scores dataframe
#         col_names = ["HorzDistance","time","body_pitch"]

#         for col_name in col_names:
#             binned_means_scores[col_name] = mean_col_by_bin(results_table,col_name)
            
#         # Remove rows with NaN values
#         binned_means_scores = binned_means_scores.dropna(axis=0, how='any')
#         binned_std_scores = binned_std_scores.dropna(axis=0, how='any')

#         return binned_means_scores, binned_std_scores

#     def reconstruct_reduced_dims(self, binned_means_scores, selected_PCs=None):
        
#         # Make a numpy array with binned scores. 
#         # This will be the input to the reconstruction.

#         # Get the PC names
#         PC_columns = binned_means_scores.filter(like='PC')

#         # Transform to numpy array
#         score_frames = PC_columns.to_numpy()

#         reconstructed_frames = self.reconstruct(selected_PCs, score_frames)


#         return reconstructed_frames



# class Hawk3D:
#     def __init__(self, filename):

#         # As an explanation, anything within KeypointManager can be found by calling
#         # Hawk3D.keypoint_manager. For example, Hawk3D.keypoint_manager.keypoints
#         # will return the keypoints. 
        
#         self.keypoint_manager = KeypointManager(filename)
#         self.plotter = HawkPlotter(self.keypoint_manager)
#         self.animator = HawkAnimator(self.plotter)

#         self.keypoint_manager.keypoints_no_translation = None

#     def get_data(self, csv_path):
        
#         """
#         Loads the data from the csv file.
#         """

#         self.frames = HawkData(csv_path)
#         self.markers = self.frames.markers
#         self.horzDist = self.frames.horzDist

#         self.PCA = HawkPCA(self.frames, self.keypoint_manager)

#     def display_hawk(self, 
#                      user_keypoints=None, 
#                      el = 20, 
#                      az = 60, 
#                      alpha = 0.3, 
#                      colour = None,
#                      horzDist = None, 
#                      bodypitch = None, 
#                      vertDist = None):
        
#         """
#         Displays the hawk using either the default keypoints or user-provided keypoints.

#         Parameters:
#         user_keypoints (numpy.ndarray, optional): An array of keypoints provided by the user.
#                                                     Expected shape is [1, 4, 3].
#         """

#         if user_keypoints is not None:
#             self.keypoint_manager.update_keypoints(user_keypoints)

#         # Transforms the keypoints if horzdist or bodypitch is given
#         # Saves a copy of the untransformed keypoints to restore later
#         self.keypoint_manager.keypoints = self.keypoint_manager.transform_keypoints(horzDist=horzDist, 
#                                                     bodypitch=bodypitch, 
#                                                     vertDist=vertDist)
        
#         # Use the plotter to display the hawk with the current keypoints. Average from file by default.
#         self.plotter.interactive_plot(el=el, 
#                                       az=az, 
#                                       alpha=alpha, 
#                                       colour=colour,
#                                       horzDist=horzDist)
#         # 2024-01-04 22:49 SERIOUSLY CAN'T UNDERSTAND WHY THIS WON'T WORK
#         # The keypoints are not updating when I call the function again.
#         # And the keypoints won't rotate.

#     def animate_hawk(self, keypoint_sequence,
#                 rotation_type="static", 
#                 el=20, 
#                 az=60, 
#                 alpha=0.3, 
#                 colour=None, 
#                 horzDist_frames=None, 
#                 bodypitch_frames=None):
#         """
#         Animates the hawk using a sequence of keypoints.

#         Parameters:
#         keypoint_sequence (numpy.ndarray): An array of keypoints for each frame.
#                                            Expected shape is [n, 4, 3], where n is the number of frames.
#         """
            
#         # Use the animator to animate the hawk with the given keypoints.
#         self.animation = self.animator.animate(keypoint_sequence,
#                                                rotation_type=rotation_type, 
#                                                el=el, 
#                                                az=az, 
#                                                alpha=alpha, 
#                                                colour=colour, 
#                                                horzDist_frames=horzDist_frames, 
#                                                bodypitch_frames=bodypitch_frames)

       

#     def quick_PCA(self, selected_PCs=0,num_frames=30):
        
#         """
#         Quick PCA reconstruction of the hawk using the given number of principal components.
#         Animates the hawk using the reconstructed frames. Default first PCs. 
#         """

#         self.PCA.run_PCA()
#         self.PCA.get_score_range(num_frames)
#         frames = self.PCA.reconstruct(selected_PCs)

#         self.animate_hawk(frames)


def main():
    pass


if __name__ == "__main__":
    main()


    