-- ============================================================
--  KADAL KANAKKU : Fish Catch, Auction & Sea-Safety Manager
--  Manavalakurichi Fish Landing Centre
--  CBSE Class XII Computer Science (083) Project 2026-27
--  Ryan, XII A
-- ============================================================
DROP DATABASE IF EXISTS kadal_kanakku;
CREATE DATABASE kadal_kanakku;
USE kadal_kanakku;

-- 1. BOATS registered at the landing centre
CREATE TABLE boats (
    boat_id      INT PRIMARY KEY,
    boat_name    VARCHAR(30) NOT NULL,
    reg_no       VARCHAR(20) NOT NULL UNIQUE,
    boat_type    VARCHAR(15) NOT NULL,      -- Kattumaram / Vallam / Fibre / Trawler
    owner_name   VARCHAR(30) NOT NULL,
    capacity_kg  INT
);

-- 2. FISHERMEN (each one works on one boat)
CREATE TABLE fishermen (
    fisher_id    INT PRIMARY KEY,
    fname        VARCHAR(30) NOT NULL,
    phone        CHAR(10) UNIQUE,
    village      VARCHAR(25),
    boat_id      INT,
    FOREIGN KEY (boat_id) REFERENCES boats(boat_id)
);

-- 3. TRIPS (one boat going to sea) + sea-safety status
CREATE TABLE trips (
    trip_id      INT PRIMARY KEY,
    boat_id      INT NOT NULL,
    trip_date    DATE NOT NULL,
    crew_count   INT,
    weather      VARCHAR(10),               -- CALM / MODERATE / ROUGH
    status       VARCHAR(10) DEFAULT 'AT SEA', -- AT SEA / RETURNED
    FOREIGN KEY (boat_id) REFERENCES boats(boat_id)
);

-- 4. BUYERS (merchants / exporters / local vendors)
CREATE TABLE buyers (
    buyer_id     INT PRIMARY KEY,
    bname        VARCHAR(30) NOT NULL,
    btype        VARCHAR(15),               -- Exporter / Wholesaler / Vendor
    town         VARCHAR(20),
    phone        CHAR(10)
);

-- 5. CATCHES (fish brought back in one trip, sold in auction)
CREATE TABLE catches (
    catch_id     INT PRIMARY KEY,
    trip_id      INT NOT NULL,
    species      VARCHAR(20) NOT NULL,
    weight_kg    FLOAT NOT NULL,
    buyer_id     INT,                        -- NULL = not yet auctioned
    rate_per_kg  FLOAT,                      -- NULL = not yet auctioned
    FOREIGN KEY (trip_id)  REFERENCES trips(trip_id),
    FOREIGN KEY (buyer_id) REFERENCES buyers(buyer_id)
);

INSERT INTO boats VALUES
(101,'St Antony','TN-15-MO-1021','Fibre','Arul Raj',800),
(102,'Kadal Rani','TN-15-MO-1187','Vallam','Selvin',600),
(103,'Arokia Matha','TN-15-MO-0954','Kattumaram','Jesudasan',250),
(104,'Sea Star','TN-15-MO-1342','Trawler','Benjamin',3000),
(105,'Velankanni','TN-15-MO-1209','Fibre','Michael Raj',900),
(106,'Alaigal','TN-15-MO-0877','Kattumaram','Antony Dhas',200),
(107,'Holy Cross','TN-15-MO-1455','Trawler','Xavier',3500),
(108,'Meenavan','TN-15-MO-1033','Vallam','Robert',650),
(109,'Muthu Kadal','TN-15-MO-1290','Fibre','Gnana Prakash',850),
(110,'Little Flower','TN-15-MO-0998','Vallam','Stephen',700),
(111,'Our Lady','TN-15-MO-1501','Trawler','Peter Raj',3200),
(112,'Thangam','TN-15-MO-1120','Kattumaram','Sahaya Raj',220);

INSERT INTO fishermen VALUES
(1,'Arul Raj','9443100011','Manavalakurichi',101),
(2,'Selvin','9443100012','Manavalakurichi',102),
(3,'Jesudasan','9443100013','Kadiapattinam',103),
(4,'Benjamin','9443100014','Colachel',104),
(5,'Michael Raj','9443100015','Manavalakurichi',105),
(6,'Antony Dhas','9443100016','Muttom',106),
(7,'Xavier','9443100017','Colachel',107),
(8,'Robert','9443100018','Manavalakurichi',108),
(9,'Gnana Prakash','9443100019','Kadiapattinam',109),
(10,'Stephen','9443100020','Manavalakurichi',110),
(11,'Peter Raj','9443100021','Muttom',111),
(12,'Sahaya Raj','9443100022','Manavalakurichi',112),
(13,'John Bosco','9443100023','Manavalakurichi',101),
(14,'Vincent','9443100024','Colachel',104),
(15,'Ravi','9443100025','Kadiapattinam',107);

INSERT INTO trips VALUES
(1,101,'2026-10-20',4,'CALM','RETURNED'),
(2,102,'2026-10-20',3,'CALM','RETURNED'),
(3,104,'2026-10-20',8,'MODERATE','RETURNED'),
(4,103,'2026-10-21',2,'CALM','RETURNED'),
(5,105,'2026-10-21',4,'MODERATE','RETURNED'),
(6,107,'2026-10-21',9,'MODERATE','RETURNED'),
(7,106,'2026-10-22',2,'CALM','RETURNED'),
(8,108,'2026-10-22',3,'CALM','RETURNED'),
(9,109,'2026-10-22',4,'CALM','RETURNED'),
(10,111,'2026-10-23',8,'MODERATE','RETURNED'),
(11,110,'2026-10-23',3,'CALM','RETURNED'),
(12,101,'2026-10-24',4,'CALM','RETURNED'),
(13,104,'2026-10-24',8,'CALM','RETURNED'),
(14,112,'2026-10-25',2,'MODERATE','AT SEA'),
(15,107,'2026-10-25',9,'MODERATE','AT SEA');

INSERT INTO buyers VALUES
(1,'Kanyakumari Sea Exports','Exporter','Colachel','9842200001'),
(2,'Mary Fish Traders','Wholesaler','Nagercoil','9842200002'),
(3,'Selvi','Vendor','Manavalakurichi','9842200003'),
(4,'Kerala Marine Foods','Exporter','Thiruvananthapuram','9842200004'),
(5,'Jeya Fish Stall','Vendor','Thuckalay','9842200005'),
(6,'Ocean Fresh Agency','Wholesaler','Marthandam','9842200006'),
(7,'Lourdu Mary','Vendor','Kadiapattinam','9842200007'),
(8,'Cape Seafoods','Exporter','Tuticorin','9842200008'),
(9,'Raja Dry Fish','Wholesaler','Colachel','9842200009'),
(10,'Pushpa','Vendor','Muttom','9842200010');

INSERT INTO catches VALUES
(1,1,'Seer Fish',120,1,620),
(2,1,'Mackerel',200,2,140),
(3,2,'Sardine',350,6,60),
(4,3,'Tuna',900,4,210),
(5,3,'Squid',300,1,280),
(6,3,'Prawn',150,8,450),
(7,4,'Anchovy',80,3,90),
(8,5,'Seer Fish',140,8,600),
(9,5,'Pomfret',60,2,520),
(10,6,'Tuna',1100,1,200),
(11,6,'Squid',250,4,290),
(12,7,'Sardine',90,5,70),
(13,8,'Mackerel',260,6,150),
(14,9,'Prawn',110,4,470),
(15,10,'Tuna',800,8,205),
(16,10,'Crab',70,2,380),
(17,11,'Sardine',400,9,55),
(18,12,'Seer Fish',100,1,640),
(19,13,'Squid',320,NULL,NULL),
(20,13,'Anchovy',500,NULL,NULL);
