from django.db import connections


class Router:
    """Class that serves as API between Django apps and Pgrouting"""

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
                print(elem)

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

    def get_points_from_nearest_edge(self, cursor, point_location):
        query = """
            select x1,y1,x2,y2
            from ways
            ORDER BY ways.the_geom <-> ST_GeogFromText('{point_location}') LIMIT 1
        """.format(
            point_location=point_location
        )
        cursor.execute(query)

        point = ()
        for elem1, elem2, elem3, elem4 in cursor.fetchall():
            point = (elem1, elem2, elem3, elem4)
        return point

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
            path = self.__dictfetchall(cursor)

        return path

    def get_point_projected_to_location(self, point_location):

        with connections["map"].cursor() as cursor:
            edge_points = {}
            edge_points = self.get_points_from_nearest_edge(cursor, point_location)
            query = """
                WITH data AS (
                SELECT 'LINESTRING ({x1} {y1}, {x2} {y2})' AS road,
                'POINT({x} {y})' AS poi)
                SELECT ST_AsText(
                ST_Line_Interpolate_Point(road, ST_Line_Locate_Point(road, poi))) AS projected_poi
                FROM data;
             """.format(
                x1=edge_points[0],
                y1=edge_points[1],
                x2=edge_points[2],
                y2=edge_points[3],
                x=point_location.x,
                y=point_location.y,
            )
            cursor.execute(query)
            point = (cursor.fetchone())[0]

        return point

    def get_nearest_edge(textgeometry):

        with connections["map"].cursor() as cursor:
            query = """
                select gid
                from ways
                ORDER BY ways.the_geom <-> '{textgeometry}' LIMIT 1
                """.format(
                textgeometry=textgeometry
            )

            cursor.execute(query)
            node_id = (cursor.fetchone())[0]
        return node_id

    def gid_severe_light(self, report_type_severe, report_type_light, user):

        with connections["default"].cursor() as cursor:
            query = """
                create or replace view table_costt{user} as (SELECT table_severe.gid, (CASE when sum(new_cost) is null
                THEN 0 ELSE sum(new_cost) end)
                + (CASE when sum(new_cost1) is null then 0 ELSE sum(new_cost1) end) as cost FROM
                (SELECT gid, count(gid)*0.002 as new_cost
                FROM smreports_report
                WHERE report_type_id in ({report_type_severe}) and status != 'R'
                GROUP BY gid )as table_severe
                LEFT JOIN (SELECT gid, count(gid)*0.0001 as new_cost1
                FROM smreports_report
                WHERE report_type_id in ({report_type_light}) and status !='R'
                GROUP BY gid) as table_light
                ON table_severe.gid = table_light.gid
                GROUP BY table_severe.gid
                UNION ALL
                SELECT  table_light.gid, (CASE when  sum(new_cost) is null
                THEN 0 ELSE sum(new_cost) end) +
                (CASE when sum(new_cost1) is null then 0 ELSE sum(new_cost1) end) as cost FROM
                (SELECT gid, count(gid)*0.002 as new_cost
                FROM smreports_report
                WHERE report_type_id  in ({report_type_severe}) and status != 'R'
                GROUP BY gid )as table_severe
                FULL OUTER JOIN (SELECT gid ,count(gid)*0.0001 as new_cost1
                FROM smreports_report
                WHERE report_type_id in ({report_type_light}) and status != 'R'
                GROUP BY gid) as table_light
                ON table_severe.gid = table_light.gid WHERE table_severe.gid is null
                GROUP BY table_light.gid);
                Select * from table_costt{user};
            """.format(
                report_type_severe=report_type_severe, report_type_light=report_type_light, user=user
            )
            cursor.execute(query)
            with connections["map"].cursor() as cursorr:
                query = """
                CREATE TABLE IF NOT EXISTS costt(
                gid BIGINT NOT NULL,
                cost DOUBLE PRECISION
                );
                create or replace view cost{user} as (select * from costt);
                """.format(
                    user=user
                )
                cursorr.execute(query)
            for elem, elem1 in cursor.fetchall():
                with connections["map"].cursor() as cursor1:
                    query = """
                        insert into cost{user} (gid, cost)
                        values ({elem},{elem1});
                    """.format(
                        elem=elem, elem1=elem1, user=user
                    )
                    cursor1.execute(query)

        pass

    def init_path(self, origin, destination, user):

        with connections["map"].cursor() as cursor:
            node_id_origin = self.get_nearest_node(cursor, origin.x, origin.y)
            node_id_destination = self.get_nearest_node(cursor, destination.x, destination.y)

            query = """
                select q.*, the_geom from(select
                nextval('osm_nodes_node_id_seq') as seq, j.node
                from (
                select c.*,case when c.path_seq = 1 then 0 else
                sum(c.new_plus_cost) OVER (PARTITION BY c.path_id
                ORDER BY c.seq) - c.new_plus_cost end as new_agg_cost
                from
                (select a.* , (CASE when  a.edge=  b.gid THEN sum(b.cost) + sum(a.cost)
                else sum(a.cost) end) as new_plus_cost
                from (SELECT * FROM pgr_ksp('SELECT gid as id, source, target, cost, reverse_cost FROM ways',
                {node_id_origin}, {node_id_destination}, 3, directed:=false)) a
                left join (select * from cost{user}) b
                on a.edge=b.gid
                group by a.edge, a.seq, a.path_id, a.path_seq, a.node, a.cost, a.agg_cost, b.gid, b.cost
                order by seq) as c
                ) as j
                left join (
                select x.path_id, sum(x.new_plus_cost) as total from
                (select c.*,case when c.path_seq = 1 then 0 else
                sum(c.new_plus_cost) OVER (PARTITION BY c.path_id
                ORDER BY c.seq) - c.new_plus_cost end as new_agg_cost
                from
                (select a.*, (CASE when a.edge=b.gid THEN sum(b.cost) + sum(a.cost)
                else sum(a.cost) end) as new_plus_cost
                from (SELECT * FROM pgr_ksp('SELECT gid as id, source, target, cost, reverse_cost FROM ways',
                {node_id_origin}, {node_id_destination}, 3, directed:=false)) a
                left join (select * from cost{user}) b
                on a.edge=b.gid
                group by a.edge, a.seq, a.path_id, a.path_seq, a.node, a.cost, a.agg_cost, b.gid, b.cost
                order by seq) as c) as x
                group by x.path_id
                ) as p on j.path_id=p.path_id
                order by p.total, j.path_seq) as q, ways_vertices_pgr where id = q.node order by q.seq;
            """.format(
                node_id_origin=node_id_origin, node_id_destination=node_id_destination, user=user
            )
            cursor.execute(query)
            path = self.__dictfetchall(cursor)

        return path

    def pedestrian_path(self, origin, destination, report_types_severe, report_type_light, user):
        self.gid_severe_light(report_types_severe, report_type_light, user)
        path = self.init_path(origin, destination, user)

        with connections["map"].cursor() as cursor:
            query = """
                    DROP VIEW cost{user};
                """.format(
                user=user
            )
            cursor.execute(query)
        with connections["default"].cursor() as cursor:
            query = """
                    DROP VIEW table_costt{user};
                """.format(
                user=user
            )
            cursor.execute(query)

        return path
