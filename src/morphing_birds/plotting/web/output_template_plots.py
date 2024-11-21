import pathlib

import numpy as np
from jinja2 import Template

from morphing_birds import Hawk3D, animate_plotly, plot_plotly

# get directory of file using pathlib
script_dir = pathlib.Path(__file__).parent.absolute()

hawk3d = Hawk3D(script_dir.parents[3] / "data/mean_hawk_shape.csv")
static_bird_plot = plot_plotly(hawk3d)
hawk3d.reset_transformation()
hawk3d.restore_keypoints_to_average()
fake_keypoints = np.random.normal(0, 0.01, (100,8,3)) + hawk3d.markers
animated_bird_plot = animate_plotly(hawk3d, fake_keypoints)
plotly_jinja_data = {"static_bird_plot":static_bird_plot.to_html(full_html=False, include_plotlyjs=False),
                     "animated_bird_plot":animated_bird_plot.to_html(full_html=False, include_plotlyjs=False)
                     }
# Save the figure as an HTML file
with (script_dir /"index.html").open("w", encoding="utf-8") as output_file, \
     (script_dir / "template.html").open() as template_file:
    j2_template = Template(template_file.read())
    output_file.write(j2_template.render(plotly_jinja_data))
