import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from PIL import Image
import io

# ....... Helper Plot Functions ........

def plot_keypoints(ax,animal3d_instance, colour='k', alpha=1):

    # Only plot the non-fixed markers. 
    coords = animal3d_instance.current_shape[:,animal3d_instance.marker_index,:][0]

    # Plot the keypoints
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2],
                s = 5, c=colour, alpha=alpha)

    return ax

def plot_sections(ax, animal3d_instance, colour, alpha=1):

    # Plot each section
    for section in animal3d_instance.skeleton_definition.body_sections.keys():
        polygon = get_polygon(animal3d_instance, section, colour, alpha)
        ax.add_collection3d(polygon)

    return ax

def get_polygon(animal3d_instance, section_name, colour, alpha=1):
    """
    Returns the coordinates of the polygon representing the given section.
    """

    if section_name not in animal3d_instance.skeleton_definition.body_sections.keys():
        raise ValueError(f"Section name {section_name} not recognised.")

    colour = colour_polygon(section_name, colour)

    alpha = alpha_polygon(section_name, alpha)

    coords = animal3d_instance.get_polygon_coords(section_name)

    polygon = Poly3DCollection([coords],
                               alpha=alpha,
                               facecolor=colour,
                               edgecolor='k',
                               linewidths=0.5)
    return polygon

def alpha_polygon(section_name, alpha):

        # The alpha of the polygon is determined by whether the landmarks are
        # estimated or measured.
        if "handwing" in section_name or "tail" in section_name:
            alpha = alpha
        else:
            alpha = 0.3

        return alpha

def colour_polygon(section_name, colour):
    
        # The colour of the polygon is determined by whether the landmarks are
        # estimated or measured.
        if "handwing" in section_name or "tail" in section_name:
            colour = colour
        else:
            colour = np.array((0.5, 0.5, 0.5, 0.5))
    
        return colour

def plot_settings(ax,origin):
        """
        Plot settings & set the azimuth and elev. for camera view of 3D axis.
        """

        # --- Panel Shading
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = True
        ax.xaxis.pane.set_edgecolor('w')
        ax.yaxis.pane.set_edgecolor('w')
        ax.zaxis.pane.set_edgecolor('w')

        # Put a line in the back corner of the plot
        corner = 0.32
        # ax.plot([-corner,-corner], [-corner,-corner], [-corner,corner], color='grey', linestyle=':', linewidth=0.5, zorder = -10)

        # Grid colour
        ax.xaxis._axinfo['grid'].update(color = 'grey', linestyle = ':', linewidth = 0.5)
        ax.yaxis._axinfo['grid'].update(color = 'grey', linestyle = ':',linewidth = 0.5)
        ax.zaxis._axinfo['grid'].update(color = 'grey', linestyle = ':',linewidth = 0.5)

        # ax.set_xlim(-0.3, 0.3)
        # ax.set_ylim(-0.3, 0.3)
        # ax.set_zlim(-0.3, 0.3)

        ax.set_xlim(-0.04, 0.04)
        ax.set_ylim(-0.04, 0.04)
        ax.set_zlim(-0.04, 0.04)

        # --- Axis Limits
        # increment = 0.28
        increment = 0.02


        ax.auto_scale_xyz(  [origin[0]-increment, origin[0]+increment], 
                            [origin[1]-increment, origin[1]+increment],
                            [origin[2]-increment, origin[2]+increment])

        # --- Axis labels and Ticks
        ax.set_xlabel('x (m)', fontsize=12)
        ax.set_ylabel('y (m)', fontsize=12)
        ax.set_zlabel('z (m)', fontsize=12)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)

        # ax.set_xticks(np.linspace(-0.2, 0.2, 3))
        # ax.set_yticks(np.linspace(-0.2, 0.2, 3))
        # ax.set_zticks(np.linspace(-0.2, 0.2, 3))

        ax.set_xticks(np.linspace(-0.02, 0.02, 3))
        ax.set_yticks(np.linspace(-0.02, 0.02, 3))
        ax.set_zticks(np.linspace(-0.02, 0.02, 3))

        # --- Axis Equal
        ax.set_aspect('equal', 'box')
        return ax

    
def get_plot3d_view(fig=None, rows=1, cols=1, index=1):
        """
        From HumanPose by Kevin Schegel

        Convenience function to create 3d matplotlib axis object.
        Wraps figure creation if need be and add_subplot.
        Parameters
        ----------
        fig : matplotlib.figure object, optional
            For re-use of an existing figure object. A new one is created if
            not given.
        rows : int
            Number of subplot rows. Like fig.add_subplot
        cols : int
            Number of subplot cols. Like fig.add_subplot
        index : int
            Index of subplot to use. Like fig.add_subplot
        Returns
        -------
        (fig, ax)
            fig : matplotlib.figure object
            ax : matplotlib.Axes object
        """
        if fig is None:
            fig = plt.figure(figsize=(6,6))

        
        ax = fig.add_subplot(rows, cols, index, projection='3d')
        ax.set_xlabel('X')
        ax.set_ylabel('Z')
        ax.set_zlabel('Y')
        return fig, ax

def save_plot_as_image(fig, cut_off=0.2):
     
    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=500, bbox_inches='tight')
    buf.seek(0)  # Rewind the buffer

    # Load the image from the buffer using PIL
    img = Image.open(buf)


    # Crop the image: Define the left, top, right, and bottom pixel coordinates
    width, height = img.size
    left = width * cut_off
    right = width * (1-cut_off)
    top = 0
    bottom = height
    cropped_img = img.crop((left, top, right, bottom))

    # Close the buffer and the plot
    buf.close()
    plt.close(fig)

    return cropped_img