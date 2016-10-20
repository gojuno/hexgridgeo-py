HexGridGeo
==========

Basics
------

GEO wrapper for `HexGrid <https://github.com/gojuno/hexgrid-py>`_

Example
-------

.. code-block:: python

    import hexgrid
    import hexgridgeo
    import morton

    grid = hexgridgeo.Grid(
        hexgrid.OrientationFlat, hexgrid.Point(500, 500),
        hexgridgeo.ProjectionSM)
    hex = grid.hex_at(hexgridgeo.Point(-73.5, 40.3))
    code = grid.hex_to_code(hex)
    restored_hex = grid.hex_from_code(code)
    neighbors = grid.hex_neighbors(hex, 2)
    points = [
        hexgridgeo.Point(-73.0, 40.0), hexgridgeo.Point(-74.0, 40.0),
        hexgridgeo.Point(-74.0, 41.0), hexgridgeo.Point(-73.0, 41.0)
    ]
    region = grid.make_region(points)
    hexes_in_region = region.hexes
