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

def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_file = os.path.join(current_dir, "data", "domain")
    p = Phaml(domain_file)
    p.solve()
    mesh_data = p.get_mesh()
    polygons, orders = convert_mesh(*mesh_data)
    import matplotlib
    matplotlib.use("Agg")
    f = plot_mesh_mpl(polygons, orders)
    f.savefig("a.png")

run()
