CREATE TABLE employee (
    employee_id UUID PRIMARY KEY,
    email VARCHAR(256) NOT NULL UNIQUE
);

CREATE TABLE benefit_category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    cover_amount MONEY,
    cover_size NUMERIC(1,2)
);

CREATE TABLE compensation_status (
    status_id INT PRIMARY KEY,
    status_name VARCHAR(50) NOT NULL,
    is_global BOOLEAN NOT NULL
);

CREATE TABLE employee_package_set (
    employee_id UUID REFERENCES employee(employee_id) ON DELETE CASCADE,
    category_id INT REFERENCES benefit_category(category_id) ON DELETE CASCADE,
    is_active BOOLEAN NOT NULL,
    PRIMARY KEY (employee_id, category_id)
);

CREATE TABLE employee_compensation_request (
    request_id UUID PRIMARY KEY,
    employee_id UUID REFERENCES employee(employee_id) ON DELETE CASCADE,
    created_date TIMESTAMP NOT NULL,
    updated_date TIMESTAMP NOT NULL,
    status_id INT REFERENCES compensation_status(status_id) ON DELETE SET NULL,
    compensation_sum_usd MONEY NOT NULL
);

CREATE TABLE compensation_request_records (
    record_id UUID PRIMARY KEY,
    request_id UUID REFERENCES employee_compensation_request(request_id) ON DELETE CASCADE,
    status_id INT REFERENCES compensation_status(status_id) ON DELETE SET NULL,
    updated_date TIMESTAMP NOT NULL,
    updated_by UUID,
    category_id INT REFERENCES benefit_category(category_id) ON DELETE SET NULL
);

CREATE TABLE compensation_request_attachments (
    attachment_id UUID PRIMARY KEY,
    record_id UUID REFERENCES compensation_request_records(record_id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    file_path VARCHAR(256) NOT NULL,
    document_date TIMESTAMP NOT NULL,
    document_number VARCHAR(50),
    address TEXT,
    document_sum MONEY,
    document_currency VARCHAR(10),
    account_number VARCHAR(50),
    additional_info TEXT
);
