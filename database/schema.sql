-- World data is loaded before anyone plays.
-- A game owns its generated rules and the requests the player has judged.
-- open_case is the single request currently on the desk. It is not history:
-- reviewed_request requires both the player's decision and the real outcome.

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

CREATE TABLE game (
    game_id INT NOT NULL AUTO_INCREMENT,
    started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    current_day INT NOT NULL DEFAULT 1,
    status ENUM('active', 'won', 'lost') NOT NULL DEFAULT 'active',
    weight_qualified INT NOT NULL DEFAULT 60,
    weight_nearly INT NOT NULL DEFAULT 30,
    weight_not_close INT NOT NULL DEFAULT 10,
    mistakes_allowed INT NOT NULL DEFAULT 1,
    PRIMARY KEY (game_id),
    CONSTRAINT chk_game_day CHECK (current_day >= 1),
    CONSTRAINT chk_game_weights CHECK (
        weight_qualified >= 0
        AND weight_nearly >= 0
        AND weight_not_close >= 0
        AND weight_qualified + weight_nearly + weight_not_close = 100
    ),
    CONSTRAINT chk_mistakes_allowed CHECK (mistakes_allowed >= 0)
);

CREATE TABLE requirement_type (
    requirement_type_id INT NOT NULL AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL,
    description VARCHAR(255) NOT NULL,
    PRIMARY KEY (requirement_type_id),
    UNIQUE KEY uq_requirement_type_code (code)
);

CREATE TABLE requirement (
    requirement_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    organization_id INT NULL,
    role_id INT NULL,
    requirement_type_id INT NOT NULL,
    minimum_value INT NULL,
    asset_type_id INT NULL,
    certification_id INT NULL,
    history_organization_id INT NULL,
    detail VARCHAR(80) NULL,
    parent_requirement_id INT NULL,
    PRIMARY KEY (requirement_id),
    CONSTRAINT chk_requirement_one_owner CHECK (
        (organization_id IS NOT NULL AND role_id IS NULL)
        OR (organization_id IS NULL AND role_id IS NOT NULL)
    ),
    CONSTRAINT chk_requirement_minimum CHECK (minimum_value IS NULL OR minimum_value >= 0),
    CONSTRAINT fk_requirement_game
        FOREIGN KEY (game_id) REFERENCES game (game_id),
    CONSTRAINT fk_requirement_organization
        FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT fk_requirement_role
        FOREIGN KEY (role_id) REFERENCES role (role_id),
    CONSTRAINT fk_requirement_type
        FOREIGN KEY (requirement_type_id) REFERENCES requirement_type (requirement_type_id),
    CONSTRAINT fk_requirement_asset
        FOREIGN KEY (asset_type_id) REFERENCES asset_type (asset_type_id),
    CONSTRAINT fk_requirement_certification
        FOREIGN KEY (certification_id) REFERENCES certification (certification_id),
    CONSTRAINT fk_requirement_history_organization
        FOREIGN KEY (history_organization_id) REFERENCES organization (organization_id),
    CONSTRAINT fk_requirement_parent
        FOREIGN KEY (parent_requirement_id) REFERENCES requirement (requirement_id)
);

CREATE TABLE reviewed_request (
    request_id INT NOT NULL AUTO_INCREMENT,
    game_id INT NOT NULL,
    day_number INT NOT NULL,
    organization_id INT NOT NULL,
    role_id INT NOT NULL,
    person_id INT NOT NULL,
    selection_band ENUM('qualified', 'nearly', 'not_close') NOT NULL,
    player_decision ENUM('approve', 'deny', 'timeout') NOT NULL,
    actual_outcome ENUM('qualified', 'not_qualified') NOT NULL,
    decision_correct BOOLEAN NOT NULL,
    outcome_detail VARCHAR(500) NULL,
    reviewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (request_id),
    KEY idx_reviewed_game_day (game_id, day_number),
    CONSTRAINT fk_reviewed_game
        FOREIGN KEY (game_id) REFERENCES game (game_id),
    CONSTRAINT fk_reviewed_organization
        FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT fk_reviewed_role
        FOREIGN KEY (role_id) REFERENCES role (role_id),
    CONSTRAINT fk_reviewed_person
        FOREIGN KEY (person_id) REFERENCES person (person_id)
);

CREATE TABLE open_case (
    game_id INT NOT NULL,
    organization_id INT NOT NULL,
    role_id INT NOT NULL,
    person_id INT NOT NULL,
    selection_band ENUM('qualified', 'nearly', 'not_close') NOT NULL,
    drawn_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (game_id),
    CONSTRAINT fk_open_case_game
        FOREIGN KEY (game_id) REFERENCES game (game_id),
    CONSTRAINT fk_open_case_organization
        FOREIGN KEY (organization_id) REFERENCES organization (organization_id),
    CONSTRAINT fk_open_case_role
        FOREIGN KEY (role_id) REFERENCES role (role_id),
    CONSTRAINT fk_open_case_person
        FOREIGN KEY (person_id) REFERENCES person (person_id)
);
