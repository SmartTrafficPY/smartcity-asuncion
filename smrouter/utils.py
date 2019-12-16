from django.db import connections


class Router:
    """Class that serves as API between Django apps and Pgrouting"""

    def dictfetchall(cursor):
        """Return all rows from a query cursor as a dict"""
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_nearest_node(cursor, longitude, latitude):
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

    def driver_path(self, origin, destination):
        """Returns the sequence of nodes that a driver has to go between origin an destination"""

        with connections["map"].cursor() as cursor:

            """Getting the ids of the nodes nearest to the origin and dstination"""
            node_id_origin = self.get_nearest_node(cursor, origin.x, origin.y)
            node_id_destination = self.get_nearest_node(cursor, destination.x, destination.y)

            query = """
            SELECT path.path_seq, nodes.lon, nodes.lat
            from pgr_dijkstra('SELECT gid AS id, source, target, cost FROM ways',
            {node_id_origin}, {node_id_destination}) as path
            INNER JOIN ways_vertices_pgr as nodes on nodes.id=path.node
            ORDER BY path.path_seq;
            """.format(
                node_id_origin=node_id_origin, node_id_destination=node_id_destination
            )

            cursor.execute(query)
            path = self.dictfetchall(cursor)

        return path

    def pedestrian_path(**params):
        """
        Returns the sequence of nodes that a pedestrian has to go between an origin an destination,
        taking into account POIs
        """
        pass
