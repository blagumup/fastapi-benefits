
-- Initialize PostgreSQL tables and insert predefined statuses

CREATE TABLE employee (
    employee_id UUID PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL
);

CREATE TABLE benefit_category (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    cover_amount MONEY,
    cover_size NUMERIC(1,2)
);

CREATE TABLE employee_package_set (
    employee_id UUID REFERENCES employee(employee_id),
    category_id INT REFERENCES benefit_category(category_id),
    PRIMARY KEY (employee_id, category_id)
);

CREATE TABLE compensation_status (
    status_id SERIAL PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL,
    is_global BOOLEAN NOT NULL
);

INSERT INTO compensation_status (status_name, is_global) VALUES
    ('open', TRUE),
    ('approved', FALSE),
    ('waiting_for_clarification', TRUE),
    ('declined', FALSE),
    ('cancelled', FALSE),
    ('exceeded_limit', FALSE),
    ('processed', TRUE);

CREATE TABLE employee_compensation_request (
    request_id UUID PRIMARY KEY,
    employee_id UUID REFERENCES employee(employee_id),
    created_date TIMESTAMP DEFAULT NOW(),
    updated_date TIMESTAMP DEFAULT NOW(),
    status_id INT REFERENCES compensation_status(status_id) ON DELETE SET NULL,
    compensation_sum_usd MONEY,
    email_subject TEXT,
    email_body TEXT
);

CREATE TABLE compensation_request_records (
    record_id UUID PRIMARY KEY,
    request_id UUID REFERENCES employee_compensation_request(request_id),
    status_id INT REFERENCES compensation_status(status_id) ON DELETE SET NULL,
    updated_date TIMESTAMP DEFAULT NOW(),
    updated_by UUID,
    category_id INT REFERENCES benefit_category(category_id) ON DELETE SET NULL,
    reason TEXT
);

CREATE TABLE compensation_request_attachments (
    attachment_id UUID PRIMARY KEY,
    record_id UUID REFERENCES compensation_request_records(record_id),
    file_name TEXT,
    file_path VARCHAR(256),
    document_date TIMESTAMP,
    document_number VARCHAR(50),
    address TEXT,
    document_sum MONEY,
    document_currency VARCHAR(10),
    account_number TEXT,
    additional_info TEXT,
    document_data JSON
);

