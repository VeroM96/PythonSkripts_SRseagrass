from schism_utils.f_find_hwlw import find_hwlw
from schism_utils.f_sort_files import sort_files
from schism_utils.f_concat_v4 import read_data
from schism_utils import tidal_ellipse
from schism_utils.f_find_closest_index import find_closest_index
import schism_utils.tol_colors

"""Draw windrose (also known as a polar rose plot)"""

from matplotlib.projections import register_projection

from .windrose import (
    D_KIND_PLOT,  # noqa
    DEFAULT_THETA_LABELS,  # noqa
    DPI_DEFAULT,  # noqa
    FIGSIZE_DEFAULT,  # noqa
    WindAxes,  # noqa
    WindAxesFactory,  # noqa
    WindroseAxes,  # noqa
    clean,  # noqa
    clean_df,  # noqa
    plot_windrose,  # noqa
    plot_windrose_df,  # noqa
    plot_windrose_np,  # noqa
    wrbar,  # noqa
    wrbox,  # noqa
    wrcontour,  # noqa
    wrcontourf,  # noqa
    wrpdf,  # noqa
    wrscatter,  # noqa
)

register_projection(WindroseAxes)

