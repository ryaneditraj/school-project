# Viva Q&A – Kadal Kanakku (Ryan, XII A, Roll 14)

1. **What is your project?** A menu-driven Python + MySQL program for the Manavalakurichi fish landing centre. It records boats, fishermen, sea trips (with a weather safety check), catches, auctions to buyers, and prints revenue reports.
2. **Why this topic?** Manavalakurichi is a fishing village; auctions are recorded on paper, and nobody can quickly tell who is still at sea. It is a real local problem, not a generic library/bank project.
3. **Front end and back end?** Front end: Python 3 console. Back end: MySQL database `kadal_kanakku`.
4. **Which module connects Python with MySQL?** `mysql.connector`, using `connect(host, user, passwd, database)`.
5. **What is a cursor?** An object created by `con.cursor()` that executes SQL (`execute()`) and fetches results (`fetchone()`, `fetchall()`).
6. **Why `commit()`?** INSERT/UPDATE/DELETE changes are only saved permanently after `con.commit()`. On error I call `rollback()`.
7. **What is `rowcount`?** Number of rows affected by the last query. I use it to know whether an UPDATE/DELETE actually found the record.
8. **How many tables? Keys?** Five: boats (PK boat_id), fishermen (PK fisher_id, FK boat_id), trips (PK trip_id, FK boat_id), buyers (PK buyer_id), catches (PK catch_id, FK trip_id, FK buyer_id).
9. **Primary key vs foreign key?** PK uniquely identifies each row and cannot be NULL. FK is a column that refers to a PK of another table, linking the tables.
10. **Candidate/alternate key example?** In boats, both boat_id and reg_no are unique → candidate keys. boat_id is primary, reg_no is the alternate key (UNIQUE).
11. **Degree and cardinality of boats?** Degree = 6 columns; cardinality = 12 rows of sample data.
12. **Where did you use a join?** View crew (fishermen + boats), view sales (catches + trips + boats + buyers), boats at sea, top boats report.
13. **Where GROUP BY and HAVING?** Species report groups by species with COUNT, SUM, AVG, MAX. Buyer report uses HAVING SUM(weight*rate) > amount (HAVING filters groups; WHERE filters rows).
14. **Why `%s` placeholders instead of joining strings?** Values are passed separately, so quotes in input don't break the query and it prevents SQL injection.
15. **How does the safety check work?** In start_trip, if weather is ROUGH and the boat is a Kattumaram or Vallam, the trip is refused. Also a boat already AT SEA cannot start another trip. "Boats at sea" shows total people at sea.
16. **How is an unsold catch represented?** buyer_id and rate_per_kg are NULL; I find them with `WHERE buyer_id IS NULL`.
17. **How did you handle wrong input?** Helper functions (read_int, read_float, read_date, read_choice) loop with try–except ValueError until valid. Database errors are caught with `except mysql.connector.Error`; `finally` closes the connection.
18. **How is CSV used?** Reports → 6 writes the species report using `csv.writer`, `writerow`, `writerows`, then reads it back with `csv.reader`.
19. **What does LIKE do in your project?** Search fisherman: `fname LIKE '%bosco%'` finds partial matches.
20. **Limitations / future scope?** Single user, no login, console only; future: GUI or web/mobile app, live weather API alerts, SMS to families, Tamil language interface, fish price trend graphs.
