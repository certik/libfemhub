FEMhub Python Library (libfemhub)
=================================

This library (repository) contains all new code, that is part of FEMhub, and
that glues common packages together, as well as provides new functionality.

Currently, it contains a Domain() class and a Mesh() class, as well as a simple
triangulation algorithm.

Example of usage
----------------

::

    >>> import femhub
    >>> d = femhub.Domain([[0,0],[0,1],[1,1],[1,0],[0.25,0.25],[0.25,0.75],[0.75,0.5]],[[0,1],[3,2],[1,2],[3,0],[4,5],[5,6],[6,4]])
    >>> d.nodes
    [[0, 0], [0, 1], [1, 1], [1, 0], [0.25, 0.25], [0.25, 0.75], [0.75,
    0.5]]
    >>> d.edges
    [(0, 3), (3, 2), (2, 1), (1, 0), [4, 5], [5, 6], [6, 4]]

You can browse the docstrings of the ``femhub.Domain()`` class or the
``femhub.Mesh()`` class.
