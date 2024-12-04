import pathlib

import numpy as np
import plotly.graph_objects as go
from jinja2 import Template
from scipy.stats import ortho_group

from morphing_birds import (
    Hawk3D,
    animate_plotly,
    plot_keypoints_plotly,
    plot_plotly,
    plot_sections_plotly,
    plot_settings_animateplotly,
)

# get directory of file using pathlib
SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

hawk3d = Hawk3D(SCRIPT_DIR.parents[3] / "data/mean_hawk_shape.csv")
static_bird_plot = plot_plotly(hawk3d)
hawk3d.reset_transformation()
hawk3d.restore_keypoints_to_average()
fake_keypoints = np.random.normal(0, 0.01, (100, 8, 3)) + hawk3d.markers
animated_bird_plot = animate_plotly(hawk3d, fake_keypoints)


def create_fake_pca_data(hawk3d, n_samples=25, n_components=12, n_markers=4, n_dims=3):
    # Simulate the mean shape of the hawk (mu)
    mu = hawk3d.left_markers.copy()

    # Generate an orthogonal matrix for principal components
    principal_components = ortho_group.rvs(dim=n_markers * n_dims)

    # Simulate decreasing variances for principal components
    explained_variance = np.linspace(2, 0.1, n_components)

    # Adjust principal components by the square root of variances
    principal_components = principal_components[:n_components] * np.sqrt(
        explained_variance[:, np.newaxis]
    )

    # Simulate score frames with temporal dynamics
    time = np.linspace(0, 4 * np.pi, n_samples)
    score_frames = np.zeros((n_samples, n_components))

    for i in range(n_components):
        amplitude = np.exp(
            -i / n_components
        )  # Decreasing amplitude for higher components
        frequency = i + 1
        score_frames[:, i] = amplitude * np.sin(frequency * time)

    # Reconstruct frames using the simulated principal components and scores
    components_list = list(range(n_components))  # Use all components or a subset
    selected_PCs = principal_components[components_list, :]
    selected_scores = score_frames[:, components_list]

    reconstruction = np.dot(selected_scores, selected_PCs)
    reconstruction = reconstruction.reshape(-1, n_markers, n_dims)
    reconstructed_frames = mu + reconstruction

    return reconstructed_frames, principal_components, score_frames


# Call the function to create fake PCA data
reconstructed_frames, principal_components, score_frames = create_fake_pca_data(hawk3d)


def reconstruct_frames(
    selected_components,
    n_frames,
    mu,
    principal_components,
    score_frames,
):
    if not selected_components:
        # If no components are selected, use the mean shape for all frames
        reconstructed = np.repeat(mu, n_frames, axis=0)
    else:
        selected_PCs = principal_components[selected_components, :]
        selected_scores = score_frames[:, selected_components]
        reconstruction = np.dot(selected_scores, selected_PCs)
        reconstruction = reconstruction.reshape(-1, n_markers, n_dims)
        reconstructed = mu + reconstruction
    return reconstructed


# Create a plot that allows selecting principal components
# Parameters
alpha = 0.3
colour = "lightblue"
n_frames = 25
n_markers = 4  # Define the number of markers
n_dims = 3  # Define the number of dimensions
# Define the predefined combinations
predefined_combinations = [
    {"label": "PC 1", "components": [0]},
    {"label": "PC 2", "components": [1]},
    {"label": "PC 3", "components": [2]},
    {"label": "PC 4", "components": [3]},
    {"label": "PC 5", "components": [4]},
    {"label": "PC 6", "components": [5]},
    {"label": "PC 7", "components": [6]},
    {"label": "PC 8", "components": [7]},
    {"label": "PC 9", "components": [8]},
    {"label": "PC 10", "components": [9]},
    {"label": "PC 11", "components": [10]},
    {"label": "PC 12", "components": [11]},
]


def create_create_components_plot(
    hawk3d,
    predefined_combinations,
    principal_components,
    score_frames,
    n_frames=25,
    alpha=0.3,
    colour="lightblue",
):
    all_frames = []
    for combo in predefined_combinations:
        components_list = combo["components"]
        reconstructed_frames = reconstruct_frames(
            components_list,
            n_frames,
            hawk3d.left_markers.copy(),
            principal_components,
            score_frames,
        )
        frames = []
        for i in range(n_frames):
            hawk3d.reset_transformation()
            hawk3d.update_keypoints(reconstructed_frames[i])
            fig = go.Figure()
            fig = plot_sections_plotly(fig, hawk3d, colour=colour, alpha=alpha)
            fig = plot_keypoints_plotly(fig, hawk3d, colour=colour, alpha=1)
            fig = plot_settings_animateplotly(fig, hawk3d)
            frames.append(
                go.Frame(
                    data=fig.data, layout=fig.layout, name=f"{combo['label']}_frame_{i}"
                )
            )
        all_frames.extend(frames)

    initial_combo_name = predefined_combinations[0]["label"]
    initial_frames = [
        frame for frame in all_frames if frame.name.startswith(f"{initial_combo_name}_")
    ]

    initial_fig = go.Figure(data=initial_frames[0].data)
    initial_fig.frames = all_frames

    buttons = []
    for combo in predefined_combinations:
        frame_names = [f"{combo['label']}_frame_{i}" for i in range(n_frames)]
        button = {
            "label": combo["label"],
            "method": "animate",
            "args": [
                frame_names,
                {
                    "frame": {"duration": 50, "redraw": True},
                    "mode": "immediate",
                    "transition": {"duration": 0},
                    "fromcurrent": True,
                },
            ],
        }
        buttons.append(button)

    initial_fig.update_layout(
        updatemenus=[
            {
                "type": "buttons",
                "buttons": buttons,
                "x": 0,
                "y": 1.15,
                "showactive": True,
            }
        ]
    )

    return initial_fig


# Call the function to create the animated figure
components_plot = create_create_components_plot(
    hawk3d, predefined_combinations, principal_components, score_frames
)

plotly_jinja_data = {
    "static_bird_plot": static_bird_plot.to_html(
        full_html=False, include_plotlyjs=False
    ),
    "animated_bird_plot": animated_bird_plot.to_html(
        full_html=False, include_plotlyjs=False
    ),
     "components_plot": components_plot.to_html(
          full_html=False, include_plotlyjs=False
     ),
}
# Save the figure as an HTML file
with (SCRIPT_DIR / "index.html").open("w", encoding="utf-8") as output_file, (
    SCRIPT_DIR / "template.html"
).open() as template_file:
    j2_template = Template(template_file.read())
    output_file.write(j2_template.render(plotly_jinja_data))
