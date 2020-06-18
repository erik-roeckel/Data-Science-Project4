from neo4j import GraphDatabase, basic_auth

#connection with authentication
# to run on local machine use this
#driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "project4"), encrypted=False)

#connection without authentication
driver = GraphDatabase.driver("bolt://localhost", encrypted=False)


session = driver.session()
transaction = session.begin_transaction()
output = ""

# Q1 All actors in descending order of number of films they acted in
output += "\n### Q1 ###\n"
result = transaction.run('''MATCH (a:Actor)-[:ACTS_IN]->(m:Movie) 
                        RETURN a.name AS actor_name, COUNT(distinct m) AS number_of_films_acted_in 
                        ORDER BY number_of_films_acted_in DESC 
                        LIMIT 20''')
for record in result:
   output += record['actor_name'] + ", " + str(record['number_of_films_acted_in']) + "\n"

# Q2 Movie with largest cast out of those that have been reviewed
output += "\n### Q2 ###\n"
result = transaction.run('''MATCH (p:Person)-[:ACTS_IN]->(m:Movie)<-[:RATED]-()
                        RETURN m.title as movie_title, COUNT(distinct p.name) AS number_of_cast_members 
                        ORDER BY number_of_cast_members DESC 
                        LIMIT 1''')
for record in result:
   output += str(record['movie_title']) + ", " + str(record['number_of_cast_members']) + "\n"

# Q3 Retrieves any director from graph that has directed 2 or more movie genres
output += "\n### Q3 ###\n"
result = transaction.run('''MATCH (d:Director)-[:DIRECTED]->(m:Movie)
                        WITH d, COUNT(distinct m.genre) AS number_of_genres
                        WHERE number_of_genres >= 2
                        RETURN d.name as director_name, number_of_genres''')
for record in result:
   output += record['director_name'] + ", " + str(record['number_of_genres']) + "\n"

# Q4 Retrieves all actors who have acted in a movie with another actor who acted in same movie as kevin bacon
output += "\n### Q4 ###\n"
result = transaction.run('''MATCH (bacon:Actor {name: "Kevin Bacon"})-[:ACTS_IN]->(same_movie:Movie)<-[:ACTS_IN]-(coactor:Actor)-[:ACTS_IN]->(diff_movie:Movie)<-[:ACTS_IN]-(b2:Actor)
                        RETURN b2.name AS actor_name''')
for record in result:
   output += record['actor_name'] + "\n"

# write output containing all four query results to output file
with open("output.txt", "w", encoding='utf-8') as output_file:
   output_file.write(output)

   
transaction.close()
session.close()