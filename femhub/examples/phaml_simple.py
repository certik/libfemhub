"""
Python version of the example "simple".
"""
import os

from numpy import array

from phaml import Phaml
from femhub.plot import plot_mesh_mpl, plot_sln_mayavi

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

# This function is not used anywhere yet
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

    import matplotlib
    matplotlib.use("Agg")
    f = plot_mesh_mpl(polygons, orders)
    f.savefig("mesh.png")

    x, y, mesh, _ = mesh_data
    values = p.get_solution_values(x, y)

    mesh = [elem-1 for elem in mesh]
    f = plot_sln_mayavi(x, y, mesh, values)
    f.savefig("sln.png")
