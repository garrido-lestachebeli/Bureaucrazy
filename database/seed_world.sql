-- Agencies, titles, licenses, assets, and applicants loaded before play.
-- Names are unique so later inserts can look rows up without depending on ids.

INSERT INTO organization (name) VALUES
    ('Bureau of Parking'),
    ('Office of Lost Staplers'),
    ('Department of Forms'),
    ('Ministry of Waiting Rooms'),
    ('Agency of Name Badges'),
    ('Commission on Coffee'),
    ('Registry of Rubber Stamps'),
    ('Office of Hallway Passes');

INSERT INTO role (title) VALUES
    ('Clerk'),
    ('Inspector'),
    ('Archivist'),
    ('Receptionist'),
    ('Auditor'),
    ('Permit Reviewer'),
    ('File Runner'),
    ('Night Watch');

INSERT INTO certification (name) VALUES
    ('Notary'),
    ('Forklift'),
    ('First Aid'),
    ('Stapler Safety'),
    ('Confidential Clearance'),
    ('Coffee Handling');

INSERT INTO asset_type (name) VALUES
    ('Rubber Stamp'),
    ('Filing Cabinet'),
    ('Parking Pass'),
    ('Desk Lamp'),
    ('Company Mug'),
    ('Hole Punch');

INSERT INTO person (full_name, age) VALUES
    ('Marisol Vega', 52),
    ('Harold Quinn', 61),
    ('Priya Nandakumar', 44),
    ('Ellis Ward', 38),
    ('Naomi Okonkwo', 47),
    ('Theo Lang', 55),
    ('Carmen Duarte', 41),
    ('Jonah Peck', 49),
    ('Aisha Rahman', 36),
    ('Victor Hale', 58),
    ('Silas Grant', 45),
    ('Wesley Park', 63),
    ('Lena Cho', 33),
    ('Mateo Ruiz', 29),
    ('June Hollis', 31),
    ('Samir Patel', 27),
    ('Robin Hale', 24),
    ('Ingrid Solberg', 26),
    ('Caleb Frost', 34),
    ('Yara Mensah', 28),
    ('Daphne Cho', 30),
    ('Andre Blake', 25),
    ('Beatrice Cole', 32),
    ('Cyril Okoye', 29),
    ('Delia Frost', 35),
    ('Zoe Hart', 27),
    ('Felix Navarro', 19),
    ('Hana Sato', 21),
    ('Miles Crowe', 18),
    ('Lila Bennett', 20),
    ('Omar Farouk', 23),
    ('Petra Novak', 19),
    ('Quinn Adler', 22),
    ('Rosa Kim', 18),
    ('Ximena Ortiz', 20),
    ('Yusuf Demir', 23),
    ('Evan Cho', 21),
    ('Nia Brooks', 19),
    ('Paul Ibarra', 22),
    ('Ruth Ellison', 18);
