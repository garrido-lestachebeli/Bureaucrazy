-- World data is loaded before anyone plays.

CREATE TABLE organization (
    organization_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (organization_id),
    UNIQUE KEY uq_organization_name (name)
);

CREATE TABLE role (
    role_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    PRIMARY KEY (role_id),
    UNIQUE KEY uq_role_title (title)
);

CREATE TABLE person (
    person_id INT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(150) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (person_id),
    CONSTRAINT chk_person_age CHECK (age >= 0)
);

CREATE TABLE certification (
    certification_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (certification_id),
    UNIQUE KEY uq_certification_name (name)
);

CREATE TABLE asset_type (
    asset_type_id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY (asset_type_id),
    UNIQUE KEY uq_asset_type_name (name)
);

CREATE TABLE person_certification (
    person_id INT NOT NULL,
    certification_id INT NOT NULL,
    PRIMARY KEY (person_id, certification_id),
    CONSTRAINT fk_person_certification_person
        FOREIGN KEY (person_id) REFERENCES person (person_id),
    CONSTRAINT fk_person_certification_certification
        FOREIGN KEY (certification_id) REFERENCES certification (certification_id)
);

CREATE TABLE person_asset (
    person_id INT NOT NULL,
    asset_type_id INT NOT NULL,
    quantity INT NOT NULL,
    PRIMARY KEY (person_id, asset_type_id),
    CONSTRAINT chk_asset_quantity CHECK (quantity >= 0),
    CONSTRAINT fk_person_asset_person
        FOREIGN KEY (person_id) REFERENCES person (person_id),
    CONSTRAINT fk_person_asset_type
        FOREIGN KEY (asset_type_id) REFERENCES asset_type (asset_type_id)
);

CREATE TABLE employment_record (
    employment_id INT NOT NULL AUTO_INCREMENT,
    person_id INT NOT NULL,
    organization_id INT NOT NULL,
    role_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    PRIMARY KEY (employment_id),
    CONSTRAINT chk_employment_dates CHECK (end_date IS NULL OR end_date >= start_date),
    CONSTRAINT fk_employment_person
        FOREIGN KEY (person_id) REFERENCES person (person_id),
    CONSTRAINT fk_employment_organization
        FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT fk_employment_role
        FOREIGN KEY (role_id) REFERENCES role (role_id)
);
