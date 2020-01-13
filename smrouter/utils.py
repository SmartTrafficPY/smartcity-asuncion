from django.contrib.gis.geos import Point
from django.db import connections


class Router:
    """Class that serves as API between Django apps and Pgrouting"""

    def from_coordinates_to_point(latitude, longitude):
        return Point(float(longitude), float(latitude))

    def __singlefetch(self, cursor):
        """Returns a dictionary with columns as keys when only a single row is queried"""
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        return dict(zip(columns, row))

    def __columnarrayfetchall(self, cursor):
        """Return all columns as a dictionary with a key per column"""
        dictionary = {}
        columns = cursor.description
        for col in columns:
            dictionary[col.name] = []

        keys = list(dictionary.keys())
        for row in cursor.fetchall():
            for index, elem in enumerate(row):
                dictionary[keys[index]].append(elem)

        return dictionary

    def __dictfetchall(self, cursor):
        """Return all rows from a query cursor as a dict"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_nearest_node(self, cursor, longitude, latitude):
        """Getting the id of a node nearest to a geopoint"""

        query = """
            SELECT id FROM ways_vertices_pgr
            ORDER BY the_geom <-> ST_GeometryFromText('POINT({lon} {lat})',4326)
            LIMIT 1;
            """.format(
            lon=longitude, lat=latitude
        )

        cursor.execute(query)
        node_id = (cursor.fetchone())[0]

        return node_id

    def get_min_distance(self, point, path):
        """Returns the min distance from a point(latitude and longitude) to a path"""
        # TODO Temporal, hay algunos registros que no tienen path porque no se pudo computar con driver_path
        if not path:
            return {"cost": 99999999999}

        with connections["map"].cursor() as cursor:

            """Getting the ids of the nodes nearest to the origin and dstination"""
            node_id_origin = self.get_nearest_node(cursor, point.x, point.y)

            if node_id_origin in path:
                """The node is already in the path"""
                return {"start_vid": node_id_origin, "end_vid": node_id_origin, "cost": 0}

            """Getting all distances from the point to the path"""
            query = """
            SELECT path.start_vid, path.end_vid, path.agg_cost * 100000 as cost
            from pgr_dijkstraCost('SELECT gid AS id, source, target, cost, reverse_cost, x1, y1, x2, y2  FROM ways',
            {node_id_origin}, ARRAY{path}, directed:=false) as path
            ORDER BY path.agg_cost
            LIMIT 1;
            """.format(
                node_id_origin=node_id_origin, path=path
            )

            cursor.execute(query)
            try:
                if cursor.rowcount == 0:
                    return {"cost": 99999999999}
                min_distance = self.__singlefetch(cursor)
            except Exception:
                raise Exception("An exception occurred when querying: \n" + query)

            # The cost is in 10^5 meters
            return min_distance

    def driver_path(self, origin, destination):
        """Returns the sequence of nodes that a driver has to go between origin an destination"""

        with connections["map"].cursor() as cursor:

            """Getting the ids of the nodes nearest to the origin and dstination"""
            node_id_origin = self.get_nearest_node(cursor, origin.x, origin.y)
            node_id_destination = self.get_nearest_node(cursor, destination.x, destination.y)

            query = """
            SELECT nodes.id, agg_cost * 100000 as agg_cost
            from pgr_dijkstra('SELECT gid AS id, source, target, cost, reverse_cost, x1, y1, x2, y2  FROM ways',
            {node_id_origin}, {node_id_destination}) as path
            INNER JOIN ways_vertices_pgr as nodes on nodes.id=path.node
            ORDER BY path.path_seq;
            """.format(
                node_id_origin=node_id_origin, node_id_destination=node_id_destination
            )

            cursor.execute(query)

            try:
                path = self.__columnarrayfetchall(cursor)
            except Exception:
                raise Exception("An exception occurred when querying: \n" + query)

        return path

    def pedestrian_path(**params):
        """
        Returns the sequence of nodes that a pedestrian has to go between an origin an destination,
        taking into account POIs
        """
        pass
