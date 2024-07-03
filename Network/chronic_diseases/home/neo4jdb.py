from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_trackable_stats(self, trackable_name):
        with self.driver.session() as session:
            query = """
                MATCH (u:User)-[:TRACKS]->(t:Trackable)
                WHERE t.trackable_name = $trackable_name
                RETURN u.sex AS Gender, COUNT(u) AS Count
            """
            result = session.run(query, trackable_name=trackable_name)
            return list(result)
        
    def get_treatments(self, trackable_name):
        with self.driver.session() as session:
            query = """
            MATCH (u:User)-[:TRACKS]->(disease:Trackable {trackable_name: $trackable_name, trackable_type: "Symptom"}),
            (u)-[:TRACKS]->(treatment:Trackable {trackable_type: "Treatment"})
            RETURN treatment.trackable_name AS Treatment, COUNT(treatment) AS UsageCount
            ORDER BY UsageCount DESC
            """
            result = session.run(query, trackable_name=trackable_name)
            return list(result)
        
    def get_weather(self, trackable_name):
        with self.driver.session() as session:
            query = """
            MATCH (u:User)-[r:TRACKS]->(t:Trackable {trackable_name: $trackable_name}),
            (u)-[r2:TRACKS]->(w:Trackable {trackable_type: "Weather"})
            WHERE t.trackable_name = $trackable_name
            RETURN w.trackable_name AS WeatherCondition, COUNT(*) AS Count ORDER BY Count DESC
            """
            result = session.run(query, trackable_name=trackable_name)
            return list(result)
    def get_tag(self, trackable_name):
        with self.driver.session() as session:
            query = """
            MATCH (u:User)-[r:TRACKS]->(t:Trackable {trackable_name: $trackable_name}),
            (u)-[r2:TRACKS]->(tag:Trackable {trackable_type: "Tag"})
            RETURN tag.trackable_name AS Tag, COUNT(*) AS Count
            ORDER BY Count DESC
            """
            result = session.run(query, trackable_name=trackable_name)
            return list(result)
        
    def get_condition(self, trackable_name):
        with self.driver.session() as session:
            query = """           
            MATCH (u:User)-[r:TRACKS]->(headache:Trackable {trackable_name: $trackable_name}),
            (u)-[r2:TRACKS]->(condition:Trackable {trackable_type: "Condition"})
            WHERE NOT condition.trackable_name = $trackable_name
            RETURN condition.trackable_name AS Condition, COUNT(*) AS Count
            ORDER BY Count DESC

            """
            result = session.run(query, trackable_name=trackable_name)
            return list(result)  