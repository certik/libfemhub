"""
Python version of the example "simple".
"""
import os

from numpy import array

from phaml import Phaml
from femhub.plot import plot_mesh_mpl

def convert_mesh(x, y, elems, elems_orders):
    """
    Convert the mesh from Phaml representation to femhub representation.
    """
    polygons = {}
    for n, elem in enumerate(elems):
        polygons[n] = array([ [x[i-1], y[i-1]] for i in elem ])
    orders = {}
    for n, order in enumerate(elems_orders):
        orders[n] = order
    return polygons, orders

def get_solution_points(polygons, orders):
    """
    Returns a list of x and y points for the values of the solution.
    """
    x = []
    y = []
    for e_id in polygons:
        e_x = list(polygons[e_id][:, 0])
        e_y = list(polygons[e_id][:, 1])
        x.extend(e_x)
        y.extend(e_y)
    return array(x), array(y)

def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_file = os.path.join(current_dir, "data", "domain")
    p = Phaml(domain_file)
    p.solve()
    mesh_data = p.get_mesh()
    polygons, orders = convert_mesh(*mesh_data)
    x, y = get_solution_points(polygons, orders)
    # --------------
    # Call phaml here:
    from numpy import sin, cos
    values = sin(x)*cos(y)
    # up to here
    # --------------
    import matplotlib
    matplotlib.use("Agg")
    f = plot_mesh_mpl(polygons, orders)
    f.savefig("mesh.png")


run()
