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

INSERT INTO requirement_type (code, description) VALUES
    ('min_age', 'Applicant must be at least a minimum age'),
    ('min_ownership', 'Applicant must own at least a minimum quantity of an asset'),
    ('has_certification', 'Applicant must hold a specific license'),
    ('prior_agency', 'Applicant must have worked for a specific agency'),
    ('min_experience', 'Applicant must have a minimum amount of work experience');

INSERT INTO person_certification (person_id, certification_id)
SELECT p.person_id, c.certification_id
FROM (
    SELECT CAST('Marisol Vega' AS CHAR(80)) AS full_name, CAST('Notary' AS CHAR(80)) AS cert_name
    UNION ALL SELECT 'Marisol Vega', 'First Aid'
    UNION ALL SELECT 'Marisol Vega', 'Confidential Clearance'
    UNION ALL SELECT 'Harold Quinn', 'Notary'
    UNION ALL SELECT 'Harold Quinn', 'Forklift'
    UNION ALL SELECT 'Harold Quinn', 'Stapler Safety'
    UNION ALL SELECT 'Harold Quinn', 'Confidential Clearance'
    UNION ALL SELECT 'Priya Nandakumar', 'Notary'
    UNION ALL SELECT 'Priya Nandakumar', 'First Aid'
    UNION ALL SELECT 'Priya Nandakumar', 'Coffee Handling'
    UNION ALL SELECT 'Ellis Ward', 'Confidential Clearance'
    UNION ALL SELECT 'Ellis Ward', 'Stapler Safety'
    UNION ALL SELECT 'Ellis Ward', 'Forklift'
    UNION ALL SELECT 'Naomi Okonkwo', 'Notary'
    UNION ALL SELECT 'Naomi Okonkwo', 'Confidential Clearance'
    UNION ALL SELECT 'Naomi Okonkwo', 'First Aid'
    UNION ALL SELECT 'Theo Lang', 'Forklift'
    UNION ALL SELECT 'Theo Lang', 'Stapler Safety'
    UNION ALL SELECT 'Theo Lang', 'Coffee Handling'
    UNION ALL SELECT 'Theo Lang', 'Notary'
    UNION ALL SELECT 'Carmen Duarte', 'First Aid'
    UNION ALL SELECT 'Carmen Duarte', 'Notary'
    UNION ALL SELECT 'Carmen Duarte', 'Confidential Clearance'
    UNION ALL SELECT 'Jonah Peck', 'Stapler Safety'
    UNION ALL SELECT 'Jonah Peck', 'Forklift'
    UNION ALL SELECT 'Jonah Peck', 'Notary'
    UNION ALL SELECT 'Aisha Rahman', 'Confidential Clearance'
    UNION ALL SELECT 'Aisha Rahman', 'First Aid'
    UNION ALL SELECT 'Aisha Rahman', 'Coffee Handling'
    UNION ALL SELECT 'Victor Hale', 'Notary'
    UNION ALL SELECT 'Victor Hale', 'Forklift'
    UNION ALL SELECT 'Victor Hale', 'Stapler Safety'
    UNION ALL SELECT 'Victor Hale', 'First Aid'
    UNION ALL SELECT 'Silas Grant', 'Notary'
    UNION ALL SELECT 'Silas Grant', 'Confidential Clearance'
    UNION ALL SELECT 'Silas Grant', 'Stapler Safety'
    UNION ALL SELECT 'Wesley Park', 'Forklift'
    UNION ALL SELECT 'Wesley Park', 'Notary'
    UNION ALL SELECT 'Wesley Park', 'First Aid'
    UNION ALL SELECT 'Wesley Park', 'Coffee Handling'
    UNION ALL SELECT 'Lena Cho', 'Notary'
    UNION ALL SELECT 'Mateo Ruiz', 'Forklift'
    UNION ALL SELECT 'June Hollis', 'First Aid'
    UNION ALL SELECT 'Samir Patel', 'Stapler Safety'
    UNION ALL SELECT 'Robin Hale', 'Coffee Handling'
    UNION ALL SELECT 'Ingrid Solberg', 'Confidential Clearance'
    UNION ALL SELECT 'Caleb Frost', 'Notary'
    UNION ALL SELECT 'Yara Mensah', 'First Aid'
    UNION ALL SELECT 'Daphne Cho', 'Forklift'
    UNION ALL SELECT 'Andre Blake', 'Stapler Safety'
    UNION ALL SELECT 'Beatrice Cole', 'Coffee Handling'
    UNION ALL SELECT 'Cyril Okoye', 'Confidential Clearance'
    UNION ALL SELECT 'Delia Frost', 'Notary'
    UNION ALL SELECT 'Zoe Hart', 'First Aid'
    UNION ALL SELECT 'Lila Bennett', 'Coffee Handling'
    UNION ALL SELECT 'Quinn Adler', 'Forklift'
    UNION ALL SELECT 'Nia Brooks', 'Stapler Safety'
) AS held
JOIN person p ON p.full_name = held.full_name
JOIN certification c ON c.name = held.cert_name;

INSERT INTO person_asset (person_id, asset_type_id, quantity)
SELECT p.person_id, a.asset_type_id, owned.quantity
FROM (
    SELECT CAST('Marisol Vega' AS CHAR(80)) AS full_name, CAST('Rubber Stamp' AS CHAR(80)) AS asset_name, CAST(3 AS SIGNED) AS quantity
    UNION ALL SELECT 'Marisol Vega', 'Filing Cabinet', 2
    UNION ALL SELECT 'Marisol Vega', 'Desk Lamp', 2
    UNION ALL SELECT 'Harold Quinn', 'Rubber Stamp', 4
    UNION ALL SELECT 'Harold Quinn', 'Parking Pass', 2
    UNION ALL SELECT 'Harold Quinn', 'Hole Punch', 2
    UNION ALL SELECT 'Priya Nandakumar', 'Company Mug', 3
    UNION ALL SELECT 'Priya Nandakumar', 'Desk Lamp', 2
    UNION ALL SELECT 'Priya Nandakumar', 'Filing Cabinet', 1
    UNION ALL SELECT 'Ellis Ward', 'Rubber Stamp', 2
    UNION ALL SELECT 'Ellis Ward', 'Parking Pass', 1
    UNION ALL SELECT 'Ellis Ward', 'Hole Punch', 3
    UNION ALL SELECT 'Naomi Okonkwo', 'Filing Cabinet', 3
    UNION ALL SELECT 'Naomi Okonkwo', 'Rubber Stamp', 2
    UNION ALL SELECT 'Naomi Okonkwo', 'Desk Lamp', 1
    UNION ALL SELECT 'Theo Lang', 'Company Mug', 4
    UNION ALL SELECT 'Theo Lang', 'Hole Punch', 2
    UNION ALL SELECT 'Theo Lang', 'Parking Pass', 2
    UNION ALL SELECT 'Carmen Duarte', 'Desk Lamp', 3
    UNION ALL SELECT 'Carmen Duarte', 'Filing Cabinet', 2
    UNION ALL SELECT 'Carmen Duarte', 'Rubber Stamp', 1
    UNION ALL SELECT 'Jonah Peck', 'Rubber Stamp', 5
    UNION ALL SELECT 'Jonah Peck', 'Hole Punch', 1
    UNION ALL SELECT 'Jonah Peck', 'Parking Pass', 1
    UNION ALL SELECT 'Aisha Rahman', 'Company Mug', 2
    UNION ALL SELECT 'Aisha Rahman', 'Desk Lamp', 2
    UNION ALL SELECT 'Aisha Rahman', 'Filing Cabinet', 2
    UNION ALL SELECT 'Victor Hale', 'Rubber Stamp', 3
    UNION ALL SELECT 'Victor Hale', 'Filing Cabinet', 4
    UNION ALL SELECT 'Victor Hale', 'Hole Punch', 2
    UNION ALL SELECT 'Silas Grant', 'Parking Pass', 3
    UNION ALL SELECT 'Silas Grant', 'Rubber Stamp', 2
    UNION ALL SELECT 'Silas Grant', 'Desk Lamp', 1
    UNION ALL SELECT 'Wesley Park', 'Company Mug', 2
    UNION ALL SELECT 'Wesley Park', 'Filing Cabinet', 3
    UNION ALL SELECT 'Wesley Park', 'Hole Punch', 3
    UNION ALL SELECT 'Lena Cho', 'Rubber Stamp', 1
    UNION ALL SELECT 'Mateo Ruiz', 'Parking Pass', 1
    UNION ALL SELECT 'June Hollis', 'Desk Lamp', 1
    UNION ALL SELECT 'Samir Patel', 'Hole Punch', 1
    UNION ALL SELECT 'Robin Hale', 'Company Mug', 1
    UNION ALL SELECT 'Ingrid Solberg', 'Filing Cabinet', 1
    UNION ALL SELECT 'Caleb Frost', 'Rubber Stamp', 2
    UNION ALL SELECT 'Yara Mensah', 'Desk Lamp', 2
    UNION ALL SELECT 'Daphne Cho', 'Parking Pass', 2
    UNION ALL SELECT 'Andre Blake', 'Hole Punch', 2
    UNION ALL SELECT 'Beatrice Cole', 'Company Mug', 2
    UNION ALL SELECT 'Cyril Okoye', 'Filing Cabinet', 1
    UNION ALL SELECT 'Delia Frost', 'Rubber Stamp', 1
    UNION ALL SELECT 'Zoe Hart', 'Desk Lamp', 1
    UNION ALL SELECT 'Omar Farouk', 'Company Mug', 1
    UNION ALL SELECT 'Rosa Kim', 'Hole Punch', 1
    UNION ALL SELECT 'Paul Ibarra', 'Desk Lamp', 1
) AS owned
JOIN person p ON p.full_name = owned.full_name
JOIN asset_type a ON a.name = owned.asset_name;

INSERT INTO employment_record (person_id, organization_id, role_id, start_date, end_date)
SELECT p.person_id, o.organization_id, r.role_id, job.start_date, job.end_date
FROM (
    SELECT CAST('Marisol Vega' AS CHAR(80)) AS full_name, CAST('Bureau of Parking' AS CHAR(80)) AS org_name, CAST('Clerk' AS CHAR(80)) AS role_title, CAST('2010-03-01' AS DATE) AS start_date, CAST('2016-06-30' AS DATE) AS end_date
    UNION ALL SELECT 'Marisol Vega', 'Department of Forms', 'Archivist', '2016-07-01', NULL
    UNION ALL SELECT 'Harold Quinn', 'Office of Lost Staplers', 'Inspector', '2008-02-01', '2015-11-30'
    UNION ALL SELECT 'Harold Quinn', 'Registry of Rubber Stamps', 'Auditor', '2015-12-01', NULL
    UNION ALL SELECT 'Priya Nandakumar', 'Commission on Coffee', 'Receptionist', '2014-04-01', '2019-08-31'
    UNION ALL SELECT 'Priya Nandakumar', 'Ministry of Waiting Rooms', 'Clerk', '2019-09-01', NULL
    UNION ALL SELECT 'Ellis Ward', 'Agency of Name Badges', 'File Runner', '2015-01-15', '2020-05-31'
    UNION ALL SELECT 'Ellis Ward', 'Bureau of Parking', 'Night Watch', '2020-06-01', NULL
    UNION ALL SELECT 'Naomi Okonkwo', 'Department of Forms', 'Auditor', '2011-06-01', '2018-03-31'
    UNION ALL SELECT 'Naomi Okonkwo', 'Office of Hallway Passes', 'Permit Reviewer', '2018-04-01', NULL
    UNION ALL SELECT 'Theo Lang', 'Commission on Coffee', 'Night Watch', '2009-09-01', '2016-09-30'
    UNION ALL SELECT 'Theo Lang', 'Office of Lost Staplers', 'Inspector', '2016-10-01', NULL
    UNION ALL SELECT 'Carmen Duarte', 'Ministry of Waiting Rooms', 'Receptionist', '2013-02-01', '2019-01-31'
    UNION ALL SELECT 'Carmen Duarte', 'Agency of Name Badges', 'Clerk', '2019-02-01', NULL
    UNION ALL SELECT 'Jonah Peck', 'Registry of Rubber Stamps', 'Archivist', '2012-05-01', '2018-07-31'
    UNION ALL SELECT 'Jonah Peck', 'Bureau of Parking', 'Inspector', '2018-08-01', NULL
    UNION ALL SELECT 'Aisha Rahman', 'Department of Forms', 'Auditor', '2016-03-01', '2021-04-30'
    UNION ALL SELECT 'Aisha Rahman', 'Commission on Coffee', 'Permit Reviewer', '2021-05-01', NULL
    UNION ALL SELECT 'Victor Hale', 'Office of Hallway Passes', 'Night Watch', '2006-01-10', '2014-12-31'
    UNION ALL SELECT 'Victor Hale', 'Office of Lost Staplers', 'File Runner', '2015-01-15', NULL
    UNION ALL SELECT 'Silas Grant', 'Bureau of Parking', 'Clerk', '2014-07-01', '2020-02-28'
    UNION ALL SELECT 'Silas Grant', 'Department of Forms', 'Archivist', '2020-03-01', NULL
    UNION ALL SELECT 'Wesley Park', 'Ministry of Waiting Rooms', 'Inspector', '2004-11-01', '2012-10-31'
    UNION ALL SELECT 'Wesley Park', 'Registry of Rubber Stamps', 'Auditor', '2012-11-01', NULL
    UNION ALL SELECT 'Lena Cho', 'Bureau of Parking', 'Clerk', '2023-01-09', '2025-08-15'
    UNION ALL SELECT 'Mateo Ruiz', 'Office of Lost Staplers', 'File Runner', '2024-01-08', NULL
    UNION ALL SELECT 'June Hollis', 'Department of Forms', 'Receptionist', '2022-06-01', '2025-01-31'
    UNION ALL SELECT 'Samir Patel', 'Ministry of Waiting Rooms', 'Night Watch', '2023-03-01', NULL
    UNION ALL SELECT 'Robin Hale', 'Commission on Coffee', 'Clerk', '2024-06-03', NULL
    UNION ALL SELECT 'Ingrid Solberg', 'Agency of Name Badges', 'Auditor', '2023-09-01', NULL
    UNION ALL SELECT 'Caleb Frost', 'Office of Hallway Passes', 'Permit Reviewer', '2021-01-04', '2024-01-31'
    UNION ALL SELECT 'Yara Mensah', 'Bureau of Parking', 'Inspector', '2024-02-12', NULL
    UNION ALL SELECT 'Daphne Cho', 'Department of Forms', 'Archivist', '2023-01-16', '2026-01-15'
    UNION ALL SELECT 'Andre Blake', 'Registry of Rubber Stamps', 'File Runner', '2025-01-20', NULL
    UNION ALL SELECT 'Beatrice Cole', 'Commission on Coffee', 'Receptionist', '2022-01-10', NULL
    UNION ALL SELECT 'Cyril Okoye', 'Ministry of Waiting Rooms', 'Clerk', '2024-04-01', NULL
    UNION ALL SELECT 'Delia Frost', 'Agency of Name Badges', 'Inspector', '2020-05-01', '2023-05-31'
    UNION ALL SELECT 'Zoe Hart', 'Office of Hallway Passes', 'Night Watch', '2025-03-03', NULL
    UNION ALL SELECT 'Hana Sato', 'Commission on Coffee', 'Clerk', '2026-08-03', NULL
    UNION ALL SELECT 'Ximena Ortiz', 'Bureau of Parking', 'Receptionist', '2026-09-01', NULL
) AS job
JOIN person p ON p.full_name = job.full_name
JOIN organization o ON o.name = job.org_name
JOIN role r ON r.title = job.role_title;
