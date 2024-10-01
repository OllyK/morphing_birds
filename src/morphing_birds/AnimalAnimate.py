import numpy as np
from matplotlib.animation import FuncAnimation

from .AnimalPlotter import plot
from .PlotterHelpers import get_plot3d_view, plot_settings

def animate(animal3d_instance, 
                keypoints_frames, 
                fig=None, 
                ax=None, 
                rotation_type="static", 
                el=20, 
                az=60, 
                alpha=0.3, 
                colour=None, 
                horzDist_frames=None, 
                bodypitch_frames=None, 
                vertDist_frames=None):
        """
        Create an animated 3D plot of a hawk video.
        """
        
        # Check dimensions and mirror the keypoints if only the right is given.
        keypoints_frames = format_keypoint_frames(animal3d_instance,keypoints_frames)

        if keypoints_frames.shape[0] == 0:
            raise ValueError("No frames to animate. Check the keypoints_frames input.")

        # Find the number of frames 
        num_frames = keypoints_frames.shape[0]

        # Initialize figure and axes
        if ax is None or fig is None:
            fig, ax = get_plot3d_view(fig)
        print("Figure and axes initialized.")


        # Prepare camera angles
        el_frames, az_frames = get_camera_angles(num_frames=num_frames, 
                                                      rotation_type=rotation_type, 
                                                      el=el, 
                                                      az=az)
        
        # Check if the horzDist_frames is given, if so check it is the correct length
        # If none given, return a zero array of the correct length.
        horzDist_frames  = check_transformation_frames(num_frames, horzDist_frames)
        vertDist_frames  = check_transformation_frames(num_frames, vertDist_frames)
        bodypitch_frames = check_transformation_frames(num_frames, bodypitch_frames)

        # # Plot settings
        ax = plot_settings(ax, animal3d_instance.origin)

        
        
        def update_animated_plot(frame):
            """
            Function to update the animated plot.
            """
            
            ax.clear()

            # Update the keypoints for the current frame

            # Make sure the keypoints are restored to the default shape to remove any transformations
            animal3d_instance.reset_transformation()

            # Update the keypoints for the current frame
            animal3d_instance.update_keypoints(keypoints_frames[frame])

            
            # Transform the keypoints
            # If none provided, uses 0 to transform the keypoints
            animal3d_instance.transform_keypoints(bodypitch = bodypitch_frames[frame],
                                                horzDist  = horzDist_frames[frame],
                                                vertDist  = vertDist_frames[frame])
            
            # Then plot the current frame
            plot(animal3d_instance, 
                    ax=ax, 
                    el=el_frames[frame], 
                    az=az_frames[frame], 
                    alpha=alpha, 
                    colour=colour)
            
            # ax.set_title(f"Frame {frame+1}/{num_frames}")
            # ax.set_title(animal3d_instance.origin)
            plot_settings(ax, animal3d_instance.origin)

            return fig, ax
        # Make sure the keypoints are restored to the default shape to remove any transformations
        animal3d_instance.restore_keypoints_to_average()


        # Creating the animation
        animation = FuncAnimation(fig, update_animated_plot, 
                                  frames=num_frames, 
                                  interval=20, repeat=True)
        
        return animation


def animate_compare(animal3d_instance, 
                keypoints_frames_list, 
                fig=None, 
                ax=None, 
                rotation_type="static", 
                el=20, 
                az=60, 
                alpha=0.3, 
                colour=None, 
                horzDist_frames=None, 
                bodypitch_frames=None, 
                vertDist_frames=None):
     

        """
        Create an animated 3D plot of a hawk video.
        """
        formatted_keypoints_frames_list = []
        for keypoints_frames in keypoints_frames_list:
            # Check dimensions and mirror the keypoints if only the right is given.
            keypoints_frames = format_keypoint_frames(animal3d_instance,keypoints_frames)

            if keypoints_frames.shape[0] == 0:
                raise ValueError("No frames to animate. Check the keypoints_frames input.")

            # Find the number of frames 
            num_frames = keypoints_frames.shape[0]

            formatted_keypoints_frames_list.append(keypoints_frames)


        # Initialize figure and axes
        if ax is None or fig is None:
            fig, ax = get_plot3d_view(fig)
        print("Figure and axes initialized.")


        # Prepare camera angles
        el_frames, az_frames = get_camera_angles(num_frames=num_frames, 
                                                      rotation_type=rotation_type, 
                                                      el=el, 
                                                      az=az)
        
        # Check if the horzDist_frames is given, if so check it is the correct length
        # If none given, return a zero array of the correct length.
        horzDist_frames  = check_transformation_frames(num_frames, horzDist_frames)
        vertDist_frames  = check_transformation_frames(num_frames, vertDist_frames)
        bodypitch_frames = check_transformation_frames(num_frames, bodypitch_frames)

        # # Plot settings
        ax = plot_settings(ax, animal3d_instance.origin)

        
        
        def update_animated_plot(frame):
            """
            Function to update the animated plot.
            """
            
            ax.clear()

            # Update the keypoints for the current frame

            # If keypoints_frame is a list
            for ii, keypoints_frames in enumerate(formatted_keypoints_frames_list):
                
                # Get a colour from matplotlib Set 2 using ii
                colour = plt.cm.Set1(ii)

                # Make sure the keypoints are restored to the default shape to remove any transformations
                animal3d_instance.reset_transformation()

                # Update the keypoints for the current frame
                animal3d_instance.update_keypoints(keypoints_frames[frame])

                
                # Transform the keypoints
                # If none provided, uses 0 to transform the keypoints
                animal3d_instance.transform_keypoints(bodypitch = bodypitch_frames[frame],
                                                    horzDist  = horzDist_frames[frame],
                                                    vertDist  = vertDist_frames[frame])
                
                # Then plot the current frame
                plot(animal3d_instance, 
                        ax=ax, 
                        el=el_frames[frame], 
                        az=az_frames[frame], 
                        alpha=alpha, 
                        colour=colour)
                
            # ax.set_title(f"Frame {frame+1}/{num_frames}")
            # ax.set_title(animal3d_instance.origin)
            plot_settings(ax, animal3d_instance.origin)

            return fig, ax
        # Make sure the keypoints are restored to the default shape to remove any transformations
        animal3d_instance.restore_keypoints_to_average()


        # Creating the animation
        animation = FuncAnimation(fig, update_animated_plot, 
                                  frames=num_frames, 
                                  interval=20, repeat=True)
        
        return animation



# ....... Helper Animation Functions ........

def format_keypoint_frames(animal3d_instance, keypoints_frames):

        """
        Formats the keypoints_frames to be [n,8,3] where n is the number of frames 
        and 8 is the number of keypoints and 3 is the number of dimensions.
        If just 4 keypoints are given, the function will mirror the keypoints to make the left side.
        """

        if len(np.shape(keypoints_frames)) == 2:
            keypoints_frames = keypoints_frames.reshape(1, -1, 3)
            print("Warning: Only one frame given.")

    # Mirror the keypoints_frames if only the right is given. 
        if keypoints_frames.shape[1] == len(animal3d_instance.right_marker_names):
            keypoints_frames = animal3d_instance.mirror_keypoints(keypoints_frames)

        return keypoints_frames

def check_transformation_frames(num_frames, transformation_frames):

        """
        Checks that the transformation frames are the same length as the keypoints frames.
        If passed None, create an array of zeros for the transformation.
        """

        if transformation_frames is None:
            transformation_frames = np.zeros(num_frames)
        
        if len(transformation_frames) != num_frames:
            raise ValueError("Transformation frames must be the same length as keypoints_frames.")
        
        
        return transformation_frames

def get_camera_angles(num_frames, rotation_type, el=20, az=60):
        """
        Creates two arrays of camera angles for the length of the animation.

        "static" -- the angles do not change in the animation, set using el, az.

        "dynamic" -- fast rotations

        "slow" -- slow rotations

        Used in: Creates inputs for plot_hawk3D_frame
        """

        if el is None or az is None:
            return [None, None]

        def linspacer(number_array, firstValue, endValue, nFrames):
            """
            Function to make linearly spaced numbers between two values of a
            given length.
            """

            number_array = np.append(
                number_array, np.linspace(firstValue, endValue, nFrames))
            return number_array

        if "dynamic" in rotation_type:

            tenthFrames = round(num_frames * 0.1)
            remainderFrames = num_frames - (tenthFrames * 9)

            az_frames = np.linspace(40, 40, tenthFrames)
            az_frames = linspacer(az_frames, 40, 10, tenthFrames)
            az_frames = linspacer(az_frames, 10, 10, tenthFrames)
            az_frames = linspacer(az_frames, 10, 90, tenthFrames)
            az_frames = linspacer(az_frames, 90, 90, tenthFrames * 2)
            az_frames = linspacer(az_frames, 90, -90, tenthFrames)
            az_frames = linspacer(az_frames, -90, -90, tenthFrames)
            az_frames = linspacer(az_frames, -90, 40, tenthFrames)
            az_frames = linspacer(az_frames, 40, 40, remainderFrames)

            el_frames = np.linspace(20, 20, tenthFrames)
            el_frames = linspacer(el_frames, 20, 15, tenthFrames)
            el_frames = linspacer(el_frames, 15, 0, tenthFrames)
            el_frames = linspacer(el_frames, 0, 0, tenthFrames)
            el_frames = linspacer(el_frames, 0, 80, tenthFrames)
            el_frames = linspacer(el_frames, 80, 80, tenthFrames)
            el_frames = linspacer(el_frames, 80, 15, tenthFrames)
            el_frames = linspacer(el_frames, 15, 15, tenthFrames)
            el_frames = linspacer(el_frames, 15, 20, tenthFrames)
            el_frames = linspacer(el_frames, 20, 20, remainderFrames)

        elif "slow" in rotation_type:

            halfFrames = round(num_frames * 0.5)
            tenthFrames = round(num_frames * 0.1)
            remainderFrames = num_frames - (halfFrames + (tenthFrames * 2) +
                                            tenthFrames + tenthFrames)

            az_frames = np.linspace(90, 90, halfFrames)
            az_frames = linspacer(az_frames, 90, -90,
                                  tenthFrames)  # Switch to back
            az_frames = linspacer(az_frames, -90, -90, tenthFrames * 2)
            az_frames = linspacer(az_frames, -90, 90,
                                  tenthFrames)  # Switch to front
            az_frames = linspacer(az_frames, 90, 90, remainderFrames)

            remainderFrames = num_frames - (tenthFrames * 9)

            el_frames = np.linspace(80, 80, tenthFrames * 2)
            el_frames = linspacer(el_frames, 80, 20,
                                  tenthFrames)  # Transition to lower
            el_frames = linspacer(el_frames, 20, 20, tenthFrames * 2)
            el_frames = linspacer(el_frames, 20, 10,
                                  tenthFrames)  # Switch to back
            el_frames = linspacer(el_frames, 10, 10, tenthFrames * 3)
            el_frames = linspacer(el_frames, 10, 80,
                                  remainderFrames)  # Switch to front

        else:
            el_frames = np.linspace(el, el, num_frames)
            az_frames = np.linspace(az, az, num_frames)

        return el_frames, az_frames


