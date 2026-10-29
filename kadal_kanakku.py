# ==================================================================
#  KADAL KANAKKU  ("Sea Accounts")
#  Fish Catch, Auction & Sea-Safety Manager
#  for the Manavalakurichi Fish Landing Centre
#
#  CBSE Class XII Computer Science (083) Project, 2026-27
#  Student : Ryan, XII A, Roll No. 14
#  School  : St Joseph's School (CBSE), Manavalakurichi
#
#  Front end : Python 3 (menu driven console program)
#  Back end  : MySQL  (connected using mysql.connector)
# ==================================================================

import mysql.connector          # Python - MySQL connectivity
import csv                      # to export a report as a CSV file
from datetime import date       # to get today's date

# ---------------- database login details --------------------------
HOST = "localhost"
USER = "root"
PASSWORD = "root"               # <-- change to YOUR MySQL password
DATABASE = "kadal_kanakku"

BOAT_TYPES = ("KATTUMARAM", "VALLAM", "FIBRE", "TRAWLER")
WEATHER = ("CALM", "MODERATE", "ROUGH")

con = None                      # global connection object
cur = None                      # global cursor object


# ================== HELPER FUNCTIONS ==============================
def connect():
    """Connect to MySQL and create the global cursor."""
    global con, cur
    con = mysql.connector.connect(host=HOST, user=USER,
                                  passwd=PASSWORD, database=DATABASE,
                                  charset="utf8mb4",
                                  collation="utf8mb4_general_ci")  # works on MySQL & MariaDB
    cur = con.cursor()


def read_int(msg, low=None, high=None):
    """Keep asking until the user types a valid whole number."""
    while True:
        try:
            n = int(input(msg))
            if (low is not None and n < low) or (high is not None and n > high):
                print("  ! Number must be between", low, "and", high)
            else:
                return n
        except ValueError:
            print("  ! Please enter a whole number.")


def read_float(msg):
    """Keep asking until the user types a positive number."""
    while True:
        try:
            x = float(input(msg))
            if x > 0:
                return x
            print("  ! Value must be greater than 0.")
        except ValueError:
            print("  ! Please enter a number (e.g. 150 or 72.5).")


def read_text(msg):
    """Read a non-empty string."""
    while True:
        s = input(msg).strip()
        if s != "":
            return s
        print("  ! This field cannot be empty.")


def read_date(msg):
    """Read a date in YYYY-MM-DD form. Empty input = today."""
    while True:
        s = input(msg + " (YYYY-MM-DD, Enter = today): ").strip()
        if s == "":
            return str(date.today())
        try:
            y, m, d = s.split("-")
            date(int(y), int(m), int(d))    # raises error if invalid
            return s
        except ValueError:
            print("  ! Invalid date. Example: 2026-10-24")


def read_choice(msg, options):
    """Read one value from a tuple of allowed options."""
    while True:
        s = input(msg + " " + str(options) + ": ").strip().upper()
        if s in options:
            return s
        print("  ! Choose one of", options)


def exists(table, column, value):
    """Return True if a row with column = value exists in table."""
    cur.execute("SELECT COUNT(*) FROM " + table + " WHERE " + column + " = %s",
                (value,))
    return cur.fetchone()[0] > 0


def show(headings, rows):
    """Print rows as a neat table using plain string formatting."""
    if len(rows) == 0:
        print("  (no records found)")
        return
    # width of each column = longest value in that column
    widths = [len(h) for h in headings]
    for r in rows:
        for i in range(len(r)):
            widths[i] = max(widths[i], len(str(r[i])))
    line = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(line)
    print("| " + " | ".join(headings[i].ljust(widths[i])
                            for i in range(len(headings))) + " |")
    print(line)
    for r in rows:
        print("| " + " | ".join(str(r[i]).ljust(widths[i])
                                for i in range(len(r))) + " |")
    print(line)
    print("  ", len(rows), "row(s)")


def run(query, values=()):
    """Run INSERT / UPDATE / DELETE, commit and return rows affected."""
    try:
        cur.execute(query, values)
        con.commit()
        return cur.rowcount
    except mysql.connector.Error as e:
        con.rollback()
        print("  ! Database error:", e.msg)
        return 0


# ================== 1. BOATS & FISHERMEN ==========================
def add_boat():
    bid = read_int("Boat ID      : ", 1)
    if exists("boats", "boat_id", bid):
        print("  ! Boat ID already exists.")
        return
    name = read_text("Boat name    : ")
    reg = read_text("Reg. number  : ").upper()
    btype = read_choice("Boat type   ", BOAT_TYPES).title()
    owner = read_text("Owner name   : ")
    cap = read_int("Capacity (kg): ", 50, 10000)
    if run("INSERT INTO boats VALUES (%s,%s,%s,%s,%s,%s)",
           (bid, name, reg, btype, owner, cap)):
        print("  Boat added successfully.")


def view_boats():
    cur.execute("SELECT * FROM boats ORDER BY boat_id")
    show(["ID", "Boat", "Reg No", "Type", "Owner", "Cap(kg)"], cur.fetchall())


def add_fisherman():
    fid = read_int("Fisherman ID : ", 1)
    if exists("fishermen", "fisher_id", fid):
        print("  ! Fisherman ID already exists.")
        return
    name = read_text("Name         : ")
    phone = read_text("Phone (10 digits): ")
    if not (phone.isdigit() and len(phone) == 10):
        print("  ! Phone must be exactly 10 digits.")
        return
    village = read_text("Village      : ")
    bid = read_int("Works on Boat ID: ")
    if not exists("boats", "boat_id", bid):
        print("  ! No such boat.")
        return
    if run("INSERT INTO fishermen VALUES (%s,%s,%s,%s,%s)",
           (fid, name, phone, village, bid)):
        print("  Fisherman added successfully.")


def view_crew():
    """JOIN: list fishermen together with their boat name."""
    cur.execute("""SELECT f.fisher_id, f.fname, f.phone, f.village, b.boat_name
                   FROM fishermen f, boats b
                   WHERE f.boat_id = b.boat_id
                   ORDER BY b.boat_name, f.fname""")
    show(["ID", "Name", "Phone", "Village", "Boat"], cur.fetchall())


def search_fisherman():
    """LIKE search on name or village."""
    word = read_text("Enter part of name / village: ")
    pat = "%" + word + "%"
    cur.execute("""SELECT f.fisher_id, f.fname, f.village, b.boat_name
                   FROM fishermen f JOIN boats b ON f.boat_id = b.boat_id
                   WHERE f.fname LIKE %s OR f.village LIKE %s""", (pat, pat))
    show(["ID", "Name", "Village", "Boat"], cur.fetchall())


def update_owner():
    bid = read_int("Boat ID: ")
    owner = read_text("New owner name: ")
    if run("UPDATE boats SET owner_name = %s WHERE boat_id = %s", (owner, bid)):
        print("  Owner updated.")
    else:
        print("  ! Boat not found.")


def delete_fisherman():
    fid = read_int("Fisherman ID to delete: ")
    if input("  Are you sure? (y/n): ").lower() == "y":
        if run("DELETE FROM fishermen WHERE fisher_id = %s", (fid,)):
            print("  Deleted.")
        else:
            print("  ! Fisherman not found.")


def boat_menu():
    while True:
        print("\n--- BOATS & FISHERMEN ---")
        print("1.Add boat  2.View boats  3.Add fisherman  4.View crew (join)")
        print("5.Search fisherman  6.Change boat owner  7.Delete fisherman  0.Back")
        ch = read_int("Choice: ", 0, 7)
        if ch == 0:
            break
        [None, add_boat, view_boats, add_fisherman, view_crew,
         search_fisherman, update_owner, delete_fisherman][ch]()


# ================== 2. TRIPS & SEA SAFETY =========================
def start_trip():
    """Log a boat leaving for sea, with a weather safety check."""
    bid = read_int("Boat ID: ")
    cur.execute("SELECT boat_name, boat_type FROM boats WHERE boat_id = %s", (bid,))
    row = cur.fetchone()
    if row is None:
        print("  ! No such boat.")
        return
    # a boat cannot go out again while it is still at sea
    cur.execute("SELECT COUNT(*) FROM trips WHERE boat_id=%s AND status='AT SEA'",
                (bid,))
    if cur.fetchone()[0] > 0:
        print("  !", row[0], "is already at sea.")
        return
    weather = read_choice("Weather", WEATHER)
    # SAFETY RULE: small country boats must not go out in rough sea
    if weather == "ROUGH" and row[1].upper() in ("KATTUMARAM", "VALLAM"):
        print("  *** SAFETY ALERT: Rough sea. A", row[1],
              "is NOT allowed to go out. Trip not logged. ***")
        return
    crew = read_int("Crew count: ", 1, 30)
    tdate = read_date("Trip date")
    cur.execute("SELECT IFNULL(MAX(trip_id),0) + 1 FROM trips")
    tid = cur.fetchone()[0]                 # auto next trip number
    if run("INSERT INTO trips VALUES (%s,%s,%s,%s,%s,'AT SEA')",
           (tid, bid, tdate, crew, weather)):
        print("  Trip", tid, "logged.", row[0], "is now AT SEA.")


def mark_returned():
    tid = read_int("Trip ID that returned: ")
    if run("UPDATE trips SET status='RETURNED' WHERE trip_id=%s AND status='AT SEA'",
           (tid,)):
        print("  Trip", tid, "marked RETURNED. Welcome back!")
    else:
        print("  ! Trip not found or already returned.")


def boats_at_sea():
    """Safety board: who is still at sea and how many people."""
    cur.execute("""SELECT t.trip_id, b.boat_name, b.boat_type, t.trip_date,
                          t.crew_count, t.weather
                   FROM trips t, boats b
                   WHERE t.boat_id = b.boat_id AND t.status = 'AT SEA'
                   ORDER BY t.trip_date""")
    rows = cur.fetchall()
    show(["Trip", "Boat", "Type", "Left On", "Crew", "Weather"], rows)
    total = sum(r[4] for r in rows)
    print("  >> Total people at sea now:", total)


def view_trips():
    cur.execute("""SELECT t.trip_id, t.trip_date, b.boat_name, t.crew_count,
                          t.weather, t.status
                   FROM trips t JOIN boats b ON t.boat_id = b.boat_id
                   ORDER BY t.trip_date DESC, t.trip_id DESC""")
    show(["Trip", "Date", "Boat", "Crew", "Weather", "Status"], cur.fetchall())


def trip_menu():
    while True:
        print("\n--- TRIPS & SEA SAFETY ---")
        print("1.Start trip  2.Mark returned  3.Boats at sea  4.All trips  0.Back")
        ch = read_int("Choice: ", 0, 4)
        if ch == 0:
            break
        [None, start_trip, mark_returned, boats_at_sea, view_trips][ch]()


# ================== 3. CATCH & AUCTION ============================
def record_catch():
    tid = read_int("Trip ID: ")
    cur.execute("SELECT status FROM trips WHERE trip_id = %s", (tid,))
    row = cur.fetchone()
    if row is None:
        print("  ! No such trip.")
        return
    if row[0] != "RETURNED":
        print("  ! Boat has not returned yet. Mark the trip returned first.")
        return
    species = read_text("Species (e.g. Tuna): ").title()
    kg = read_float("Weight in kg: ")
    cur.execute("SELECT IFNULL(MAX(catch_id),0) + 1 FROM catches")
    cid = cur.fetchone()[0]
    if run("INSERT INTO catches (catch_id, trip_id, species, weight_kg) "
           "VALUES (%s,%s,%s,%s)", (cid, tid, species, kg)):
        print("  Catch", cid, "recorded. Waiting for auction.")


def unsold_catches():
    cur.execute("""SELECT c.catch_id, b.boat_name, t.trip_date, c.species, c.weight_kg
                   FROM catches c, trips t, boats b
                   WHERE c.trip_id = t.trip_id AND t.boat_id = b.boat_id
                     AND c.buyer_id IS NULL
                   ORDER BY c.catch_id""")
    show(["Catch", "Boat", "Date", "Species", "Kg"], cur.fetchall())


def auction_catch():
    """Sell an unsold catch to the highest bidder."""
    unsold_catches()
    cid = read_int("Catch ID to auction: ")
    cur.execute("SELECT species, weight_kg FROM catches "
                "WHERE catch_id=%s AND buyer_id IS NULL", (cid,))
    row = cur.fetchone()
    if row is None:
        print("  ! Not found or already sold.")
        return
    bid = read_int("Winning Buyer ID: ")
    if not exists("buyers", "buyer_id", bid):
        print("  ! No such buyer.")
        return
    rate = read_float("Final bid rate (Rs per kg): ")
    if run("UPDATE catches SET buyer_id=%s, rate_per_kg=%s WHERE catch_id=%s",
           (bid, rate, cid)):
        print("  SOLD!", row[1], "kg of", row[0], "@ Rs", rate,
              "= Rs", round(row[1] * rate, 2))


def view_sales():
    cur.execute("""SELECT c.catch_id, t.trip_date, bo.boat_name, c.species,
                          c.weight_kg, c.rate_per_kg,
                          c.weight_kg * c.rate_per_kg, bu.bname
                   FROM catches c
                   JOIN trips t   ON c.trip_id = t.trip_id
                   JOIN boats bo  ON t.boat_id = bo.boat_id
                   JOIN buyers bu ON c.buyer_id = bu.buyer_id
                   ORDER BY t.trip_date, c.catch_id""")
    show(["Catch", "Date", "Boat", "Species", "Kg", "Rate", "Amount", "Buyer"],
         cur.fetchall())


def delete_catch():
    cid = read_int("Catch ID to delete (wrong entry): ")
    if run("DELETE FROM catches WHERE catch_id = %s", (cid,)):
        print("  Deleted.")
    else:
        print("  ! Catch not found.")


def catch_menu():
    while True:
        print("\n--- CATCH & AUCTION ---")
        print("1.Record catch  2.Unsold catches  3.Auction a catch")
        print("4.View all sales  5.Delete catch  0.Back")
        ch = read_int("Choice: ", 0, 5)
        if ch == 0:
            break
        [None, record_catch, unsold_catches, auction_catch,
         view_sales, delete_catch][ch]()


# ================== 4. BUYERS =====================================
def add_buyer():
    bid = read_int("Buyer ID: ", 1)
    if exists("buyers", "buyer_id", bid):
        print("  ! Buyer ID already exists.")
        return
    name = read_text("Name: ")
    btype = read_choice("Type", ("EXPORTER", "WHOLESALER", "VENDOR")).title()
    town = read_text("Town: ")
    phone = read_text("Phone: ")
    if run("INSERT INTO buyers VALUES (%s,%s,%s,%s,%s)",
           (bid, name, btype, town, phone)):
        print("  Buyer added.")


def view_buyers():
    cur.execute("SELECT * FROM buyers ORDER BY btype, bname")
    show(["ID", "Name", "Type", "Town", "Phone"], cur.fetchall())


def buyer_menu():
    while True:
        print("\n--- BUYERS ---")
        print("1.Add buyer  2.View buyers  0.Back")
        ch = read_int("Choice: ", 0, 2)
        if ch == 0:
            break
        [None, add_buyer, view_buyers][ch]()


# ================== 5. REPORTS ====================================
def daily_report():
    d = read_date("Report date")
    cur.execute("""SELECT c.species, SUM(c.weight_kg), SUM(c.weight_kg*c.rate_per_kg)
                   FROM catches c JOIN trips t ON c.trip_id = t.trip_id
                   WHERE t.trip_date = %s AND c.buyer_id IS NOT NULL
                   GROUP BY c.species ORDER BY 3 DESC""", (d,))
    rows = cur.fetchall()
    show(["Species", "Total Kg", "Revenue (Rs)"], rows)
    print("  >> Total auction revenue on", d, ": Rs", sum(r[2] for r in rows))


def species_report():
    """GROUP BY species with aggregate functions. Returns rows for CSV."""
    cur.execute("""SELECT species, COUNT(*), SUM(weight_kg),
                          ROUND(AVG(rate_per_kg),2), MAX(rate_per_kg),
                          SUM(weight_kg*rate_per_kg)
                   FROM catches WHERE buyer_id IS NOT NULL
                   GROUP BY species ORDER BY SUM(weight_kg*rate_per_kg) DESC""")
    rows = cur.fetchall()
    show(["Species", "Lots", "Total Kg", "Avg Rate", "Max Rate", "Revenue"], rows)
    return rows


def top_boats():
    cur.execute("""SELECT b.boat_name, b.boat_type, COUNT(DISTINCT t.trip_id),
                          SUM(c.weight_kg), SUM(c.weight_kg*c.rate_per_kg)
                   FROM boats b, trips t, catches c
                   WHERE b.boat_id = t.boat_id AND t.trip_id = c.trip_id
                     AND c.buyer_id IS NOT NULL
                   GROUP BY b.boat_id, b.boat_name, b.boat_type
                   ORDER BY 5 DESC LIMIT 5""")
    rows = cur.fetchall()
    show(["Boat", "Type", "Trips", "Kg", "Earnings (Rs)"], rows)
    if rows:
        print("  >> TOP BOAT:", rows[0][0])


def buyer_report():
    """GROUP BY + HAVING: buyers who spent more than a given amount."""
    amt = read_float("Show buyers who spent more than Rs: ")
    cur.execute("""SELECT bu.bname, bu.btype, COUNT(*),
                          SUM(c.weight_kg*c.rate_per_kg)
                   FROM buyers bu, catches c
                   WHERE bu.buyer_id = c.buyer_id
                   GROUP BY bu.buyer_id, bu.bname, bu.btype
                   HAVING SUM(c.weight_kg*c.rate_per_kg) > %s
                   ORDER BY 4 DESC""", (amt,))
    show(["Buyer", "Type", "Lots", "Spent (Rs)"], cur.fetchall())


def period_report():
    d1 = read_date("From date")
    d2 = read_date("To date  ")
    cur.execute("""SELECT t.trip_date, COUNT(DISTINCT t.trip_id),
                          SUM(c.weight_kg), SUM(c.weight_kg*c.rate_per_kg)
                   FROM trips t JOIN catches c ON t.trip_id = c.trip_id
                   WHERE t.trip_date BETWEEN %s AND %s AND c.buyer_id IS NOT NULL
                   GROUP BY t.trip_date ORDER BY t.trip_date""", (d1, d2))
    show(["Date", "Trips", "Kg", "Revenue (Rs)"], cur.fetchall())


def export_csv():
    """Write the species report into a CSV file using the csv module."""
    rows = species_report()
    fname = "species_report.csv"
    try:
        with open(fname, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Species", "Lots", "Total_Kg", "Avg_Rate",
                        "Max_Rate", "Revenue"])
            w.writerows(rows)
        print("  Report saved to", fname)
        # read it back to prove it worked
        with open(fname, "r") as f:
            print("  First 3 lines of the file:")
            for i, line in enumerate(csv.reader(f)):
                if i == 3:
                    break
                print("   ", line)
    except IOError:
        print("  ! Could not write the file.")


def report_menu():
    while True:
        print("\n--- REPORTS ---")
        print("1.Daily revenue  2.Species-wise totals  3.Top 5 boats")
        print("4.Buyer spending (HAVING)  5.Revenue between dates")
        print("6.Export species report to CSV  0.Back")
        ch = read_int("Choice: ", 0, 6)
        if ch == 0:
            break
        [None, daily_report, species_report, top_boats,
         buyer_report, period_report, export_csv][ch]()


# ================== MAIN PROGRAM ==================================
def main():
    print("=" * 60)
    print("   KADAL KANAKKU - Fish Catch, Auction & Sea-Safety Manager")
    print("        Manavalakurichi Fish Landing Centre")
    print("=" * 60)
    try:
        connect()
    except mysql.connector.Error as e:
        print("Cannot connect to MySQL:", e.msg)
        print("Check that MySQL is running, schema.sql is loaded and")
        print("PASSWORD at the top of this file is correct.")
        return
    try:
        while True:
            print("\n========= MAIN MENU =========")
            print("1. Boats & Fishermen")
            print("2. Trips & Sea Safety")
            print("3. Catch & Auction")
            print("4. Buyers")
            print("5. Reports")
            print("0. Exit")
            ch = read_int("Enter choice: ", 0, 5)
            if ch == 0:
                break
            [None, boat_menu, trip_menu, catch_menu, buyer_menu, report_menu][ch]()
    finally:
        con.close()                 # always close the connection
        print("\nConnection closed. Nanri! (Thank you)")


if __name__ == "__main__":
    main()
