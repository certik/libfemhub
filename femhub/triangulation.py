from numpy import exp, sqrt, array
from pylab import plot, savefig, grid, legend, clf, pcolor, spy, axis

class TriangulationError(Exception):
    pass

def is_on_the_left(c, a, b, pts_list):
   """
   Checks whether a given point "c" lies to the left of the edge (a,b).
 
   The order in which the parameters are inputted DOES matter.
   
   Example:

   >>> is_on_the_left(0,1,2,[[-1,1],[0,0],[0,1]]) 
   True
   >>> is_on_the_left(0,2,1,[[-1,1],[0,0],[0,1]])
   False

   The parameters "(0,1,2," refers to the order in the list "[[-1,1],[],..."
   For example point "2" being "[0,1]".
   The parameter or point of interest "c" needs to come first, followed 
   by points "a"and "b" in that order, and finally the list of points.


   """
   ax, ay = pts_list[a]
   bx, by = pts_list[b]
   cx, cy = pts_list[c]
   ux = float(bx - ax)
   uy = float(by - ay)
   vx = float(cx - ax)
   vy = float(cy - ay)
   return (ux*vy - uy*vx > 0)

# Angle criterion (to be minimized)
def criterion(a, b, c, pts_list):
   """
   Returns the cosine of the angle acb. 

   Used to find point "c" to the left of the edge (a,b) that maximizes 
   the angle acb. 

   Example:

   >>> criterion(0,1,2,[[0,0],[0,1],[-1,1]])
   0.707106
   >>> criterion(0,1,2,[[0,0],[0,2],[-1,1]])
   0.0 

   The order in which the parameters are inputted DOES matter.
   The parameters "(0,1,2," refers to the order in the list "[[0,0],[],..."
   For example point "2" being "[-1,1]".
   The parameters need to follow the order "(a,b,c" followed by the
   list of points.
   
   """
   ax, ay = pts_list[a]
   bx, by = pts_list[b]
   cx, cy = pts_list[c]
   ux = float(ax - cx)
   uy = float(ay - cy)
   vx = float(bx - cx)
   vy = float(by - cy)
   len_u = sqrt(ux*ux + uy*uy)
   len_v = sqrt(vx*vx + vy*vy)
   return (ux*vx + uy*vy)/(len_u*len_v)

def find_third_point(a, b, pts_list, edges):
    """
    Takes a boundary edge "(a,b)", and in the list of points finds a third
    point "c", that is not equal to the parameters "a" or "b", lies to
    the left of ab, and maximizes the angle acb. The third point also must be 
    such that none of the edges (a, c) or (b, c) intersect with any boundary
    edge.  

    The indices "a, b" refer to points in the parameter list "pts_list".
    For example, the first parameter "3" in the example below is referring to point
    "[1,0]" in the paramter list "pts_list".  Lastly, the edges of your system 
    are inserted in the parameter list "edges".

    Example:

    >>> find_third_point(3,2,[[0,0],[0,1],[1,1],[1,0],[0.5,0.5]],[[0,1],[1,2],[2,3],[3,0]]) 
    4
    >>> find_third_point(2,1,[[0.5,0.5],[1,1],[1,0]],[[0,1],[1,2],[2,0]]) 
    0
    
    Keep in mind that the order in which the parameters are inputted DOES matter.
    The parameters "a" and "b" refering to points in the list "pts_list"
    must  be inputted in that order, followed by the points list and  the edges
    in their respective parameters "pts_list" and "edges".

    """
    found = 0
    minimum = exp(100)   #this is dirty
    c_index = -1
    pt_index = -1
    for c_point in pts_list:
        c_index += 1
        if c_index != a and c_index != b and is_on_the_left(c_index, a, b, pts_list):
            edge_intersects = \
                    edge_intersects_edges((a, c_index), pts_list, edges) or \
                    edge_intersects_edges((b, c_index), pts_list, edges)
            if not edge_intersects:
                crit = criterion(a, b, c_index, pts_list)
                if crit < minimum:
                    minimum = crit
                    pt_index = c_index
                    found = 1
    if found == 0:
        raise TriangulationError("ERROR: Optimal point not found in find_third_point().")
    return pt_index

# If the point 'c' belongs to a boundary edge, return False,
# otherwise return True
def lies_inside(c, bdy_edges):
   """
   Checks to see whether a given point "c" lies on a boundary edge.

   If the given point "c" lies on a boundary edge the function will 
   return False, otherwise the function will return True.

   Example:

   >>> lies_inside([0,0.5],[[[0,0],[0,1]],[0,1]]) 
   True
   >>> lies_inside([0,0],[[[0,0],[0,1]],[0,1]]) 
   False

   The point of interest "c" comes first followed by the list of points and the 
   boundary edge.

   """
   for edge in bdy_edges:
       a,b = edge
       if c == a or c == b: return False
   return True

def is_boundary_edge(a, b, bdy_edges):
    """
    Checks whether edge "(a,b" is in the list of boundary edges.

    The parameters "a" and "b" combine to form an edge.  The list of boundary
    edges are then inserted in the parameter "bdy_edges".

    Example:

    >>> is_boundary_edge(5,4,[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4]])
    True
    >>> is_boundary_edge(4,6,[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4]])
    False 

    """
    for edge in bdy_edges:
        a0, b0 = edge
        if (a==a0 and b==b0) or (a==b0 and b==a0):
            return True
    return False

def triangulate_af(pts_list, bdy_edges):
    """
    Create a triangulation using the advancing front method.
   
    The first parameter "pts_list" will take your list of points, followed by the second
    parameter "bdy_edges" taking your list of boundary edges, and finally the Return
    will be the list of elements.

    Example:

    >>> triangulate_af([(0, 0), (1, 0), (0.5, 1)],[(0, 1), (1, 2), (2, 0)]) 
    [(2, 0, 1)] 
    >>> triangulate_af([(0,0),(1,0),(1,1),(0,1),(0.5,0.5)],[(0,1),(1,2),(2,3),(3,0)]) 
    [(3, 0, 4), (4, 0, 1), (4, 1, 2), (4, 2, 3)]    

    """
    # create empty list of elements
    elems = []
    bdy_edges = bdy_edges[:]
    # main loop
    while bdy_edges != []:
        # take the last item from the list of bdy edges (and remove it)
        a,b = bdy_edges.pop()
        c = find_third_point(a, b, pts_list, bdy_edges)
        elems.append((a,b,c))
        if is_boundary_edge(c, a, bdy_edges):
            bdy_edges.remove((c,a))
        else:
            bdy_edges.append((a,c))
        if is_boundary_edge(b, c, bdy_edges):
            bdy_edges.remove((b,c))
        else:
            bdy_edges.append((c,b))
    return elems

# Plot triangular mesh
def plot_tria_mesh(pts_list, tria_mesh, filename="a.png"):
    clf()
    label=""
    for elem in tria_mesh:
        a,b,c = elem
        ax,ay = pts_list[a]
        bx,by = pts_list[b]
        cx,cy = pts_list[c]
        x_array = array([ax,bx,cx,ax])
        y_array = array([ay,by,cy,ay])
        plot(x_array, y_array, "g-")
    axis("equal")
    savefig(filename)

def convert_graph(vertices, edges):
    pts_list = []
    _edges = []
    for i in range(len(vertices)):
        pts_list.append(vertices[i])
        for n in edges[i]:
            if n > i:
                _edges.append((i, n))
    return pts_list, _edges

def polygon_area(nodes, edges):
    """
    Calculates the (oriented) area of the polygon.

    The list of nodes that make up your system are inputted first in the parameter "nodes",
    and then depending  on how the order of your list of boundary edges are inputted (orientation)
    in the parameter "edges", area will be either added(positive) or subtracted(negative). 
    This also suggests that the polygon area is oriented a certain way. 

    Example: 

    >>> polygon_area([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.75],[0.75,0.25]],[[0,1],[1,2],[2,3],[3,0],[4,7],[7,6],[6,5],[5,4]]) 
    -0.75  
    >>> polygon_area([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.75],[0.75,0.25]],[[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4]]) 
    -1.25
    >>> polygon_area([[0,0],[0,1],[1,1],[1,0]],[[0,3],[3,2],[2,1],[1,0]]) 
    1.0

    To distinguish between the different parameters, each list in the parameters are double bracketed.  
    For example, in the first example above "[0.75,0.25]],[[0,1]" is the end of one parameter and
    the begining of a new one.   

    """
    # extract the (x, y) coordinates of the boundary nodes in the order
    x = []
    y = []
    for e in edges:
        n = nodes[e[0]]
        x.append(n[0])
        y.append(n[1])
        n = nodes[e[1]]
        x.append(n[0])
        y.append(n[1])
    # "close" the polygon
    x.append(x[0])
    x.append(x[1])
    y.append(y[0])
    y.append(y[1])
    # compute the area
    a = 0.0
    for i in range(1, len(x)-1):
        a += x[i] * (y[i+1] - y[i-1])
    a /= 2;
    return a

def edges_flip_orientation(edges):
    """
    Flips the edges curve orientation.

    This is useful for the triangulation algorithm.

    Example:

    >>> edges_flip_orientation([(0, 1), (1, 2), (2, 6), (6, 0)])
    [(0, 6), (6, 2), (2, 1), (1, 0)]

    """
    edges_flipped = []
    for e in edges:
        edges_flipped.insert(0, (e[1], e[0]))
    return edges_flipped

def edges_is_closed_curve(edges):
    """
    Checks to see if the edges form a closed curve.

    The parameter "edges" takes a list of edges. The  Return is True if the
    list of edges forms a closed curve, otherwise the Return is False.

    This is a useful check before attempting to do a triangulation.

    Example:

    >>> edges_is_closed_curve([(0, 1), (1, 2), (2, 3), (3, 0)])
    True
    >>> edges_is_closed_curve([(0, 1), (2, 3), (3, 0)])
    False

    """
    e_prev = first = edges[0]
    for e in edges[1:]:
        if e_prev[1] != e[0]:
            if e_prev[1] == first[0]:
                # new loop
                first = e
            else:
                return False
        e_prev = e
    if e_prev[1] != first[0]:
        return False
    return True

def check_regularity(edges):
    """
    Checks whether the boundary is closed and whether exactly two edges are sharing
    a node.

    The parameter "edges" takes a list of edges, checks whether the boundary is
    closed in the given list of edges, and whether exactly 2 edges are sharing a node.
    Otherwise it raises the proper exception.

    Example:

    >>> check_regularity([[0,1],[1,2],[2,3],[3,0]])

    >>> check_regularity([[0,1],[2,3],[3,0]]) 
    Exception: Boundary is not closed.

    The parameters in the list are edges, for example, "[0,1]" is an
    edge.

    """
    for a, b in edges:
        counter_a = 0
        counter_b = 0
        for x, y in edges:
            if a == x or a == y:
                counter_a += 1
            if b == x or b == y:
                counter_b += 1
        assert (counter_a > 0) and (counter_b > 0)
        if (counter_a == 1) or (counter_b == 1):
            raise Exception("Boundary is not closed.")
        if (counter_a > 2) or (counter_b > 2):
            raise Exception("More than two edges share a node.")

def find_loops(edges):
    """
    Extracts all loops from the parameter "edges", which is a list of edges, and
    returns them as a sorted edge list "loops".

    Boundary regularity (continuity) is checked as well, and the proper exception
    is raised if something is wrong.

    Example:

    >>> find_loops([[0,1],[3,2],[1,2],[3,0],[4,5],[6,4],[6,5]])
    [[[0, 1], [1, 2], (2, 3), [3, 0]], [[4, 5], (5, 6), [6, 4]]] 

    >>> find_loops([[0,1],[3,0],[2,3],[2,1],[4,5],[5,6],[7,4]])
    Exception: Boundary is not closed.

    >>> find_loops([[0,1],[3,0],[2,3],[2,1],[4,5],[6,7],[6,5],[4,7]])  
    [[[0, 1], (1, 2), [2, 3], [3, 0]], [[4, 5], [5, 6], [6, 7], [7, 4]]] 

    The parameters in the list are edges, for example, "[0,1],[3,2]" are
    edges.

    """
    check_regularity(edges)
    loops = []
    edges = edges[:]
    start_i = -1
    last_i = -1
    n = []
    while edges != []:
        if start_i == -1:
            e = edges[0]
            n = [e]
            del edges[0]
            start_i = n[-1][0]
            last_i = n[-1][1]
        else:
            ok = False
            for i, e in enumerate(edges):
                if e[0] == last_i:
                    n.append(e)
                    del edges[i]
                    ok = True
                    break
                elif e[1] == last_i:
                    n.append((e[1], e[0]))
                    del edges[i]
                    ok = True
                    break
            if not ok:
                if start_i == last_i:
                    start_i = -1
                    loops.append(n)
                else:
                    raise Exception("Missing some boundary edge")
            last_i = n[-1][1]
    if start_i == last_i:
        loops.append(n)
    else:
        raise Exception("Missing some boundary edge")
    return loops

def orient_loops(nodes, loops):
    n = []
    area_loop_list = []
    for loop in loops:
        area_loop_list.append((polygon_area(nodes, loop), loop))
    area_loop_list.sort(key=lambda x: abs(x[0]))
    area_loop_list.reverse()
    first = True
    for area, loop in area_loop_list:
        if first:
            flip = polygon_area(nodes, loop) < 0
        else:
            flip = polygon_area(nodes, loop) > 0
        if flip:
            n.extend(edges_flip_orientation(loop))
        else:
            n.extend(loop)
        first = False
    return n


def ccw(A, B, C):
    """
    Checks whether a triangle is positively (counter clock wise) oriented.  

    Here (A[0], A[1]), (B[0], B[1]), (C[0], C[1]) are vertex coordinates.

    Example:

    >>> A = [0., 0.]
    >>> B = [1., 0.]
    >>> C = [0., 1.]
    >>> ccw(A, B, C)
    True
    >>> A = [0., 0.]
    >>> B = [0., 1.]
    >>> C = [1., 0.]
    >>> ccw(A, B, C)
    False
    """
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

def two_edges_intersect(nodes, e1, e2):
    """
    Checks whether the two given edges "e1" and "e2" intersect, from the given
    list of nodes "nodes".

    This function assumes the parameters "e1" and "e2" are tuples of (a_id, b_id),
    with "ids" coming from the items in the parameter list "nodes".

    >>> two_edges_intersect([[0,0],[0,1],[1,1],[1,0]],(1,2),(3,2)) 
    False
    >>> two_edges_intersect([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.75],[0.75,0.25]],(3,0),(4,5)) 
    False    

    """
    A = nodes[e1[0]]
    B = nodes[e1[1]]
    C = nodes[e2[0]]
    D = nodes[e2[1]]
    return intersect(A, B, C, D)

def any_edges_intersect(nodes, edges):
    """
    Returns True if any two edges intersect.
    """
    for i in range(len(edges)):
        for j in range(i+1, len(edges)):
            e1 = edges[i]
            e2 = edges[j]
            if e1[1] == e2[0] or e1[0] == e2[1]:
                continue
            if two_edges_intersect(nodes, e1, e2):
                return True
    return False

def edge_intersects_edges(e1, nodes, edges):
    """
    Returns True if "e1" intersects any edge from "edges".
    """
    for i in range(len(edges)):
        e2 = edges[i]
        if e1[1] == e2[0] or e1[0] == e2[1]:
            continue
        if two_edges_intersect(nodes, e1, e2):
            return True
    return False
