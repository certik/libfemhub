"""
Python version of the example "simple".
"""
import os

from numpy import array

from phaml import Phaml
from femhub.plot import plot_mesh_mpl

def run():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    domain_file = os.path.join(current_dir, "data", "domain")
    p = Phaml(domain_file)
    p.solve()
    x, y, _elems, _orders = p.get_mesh()
    polygons = {}
    for n, elem in enumerate(_elems):
        polygons[n] = array([ [x[i-1], y[i-1]] for i in elem ])
    print polygons
    orders = {}
    for n, order in enumerate(_orders):
        orders[n] = order
    import matplotlib
    matplotlib.use("Agg")
    f = plot_mesh_mpl(polygons, orders)
    f.savefig("a.png")

run()
