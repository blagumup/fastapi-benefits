DROP FUNCTION IF EXISTS fn_benefit_categories_get_all();

CREATE OR REPLACE FUNCTION fn_benefit_categories_get_all()
RETURNS SETOF benefit_category AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM benefit_category;
END;
$$ LANGUAGE plpgsql;

--==================
DROP FUNCTION IF EXISTS fn_compensation_requests_get_all();

CREATE OR REPLACE FUNCTION fn_compensation_requests_get_all()
RETURNS TABLE (
	request_id UUID,
	employee_id UUID,
	full_name TEXT,
	email VARCHAR(256),
	request_date TIMESTAMP,
	updated_date TIMESTAMP,
	status_id INT,
	request_status VARCHAR(10),
	benefit_program TEXT,
	"location" TEXT,
	compensation_sum_usd MONEY,
	total_used MONEY,
	email_subject TEXT,
	email_body TEXT
)	
AS $$
BEGIN

	RETURN QUERY
	SELECT 
		ecr.request_id,
		ecr.employee_id,
		null AS full_name,
		e.email,
		ecr.created_date AS request_date,
		ecr.updated_date,
		cs.status_id,
		cs.status_name AS request_status,
		null AS benefit_program,
		null AS location,
		ecr.compensation_sum_usd::money as compensation_sum_usd,
		null::money AS total_used,
		ecr.email_subject,
		ecr.email_body
	FROM employee_compensation_request ecr
	JOIN employee e
		ON e.employee_id = ecr.employee_id
	JOIN compensation_status cs 
		ON ecr.status_id = cs.status_id;

END;
$$ LANGUAGE plpgsql;


--==================
DROP FUNCTION IF EXISTS fn_employee_get_by_id();

CREATE OR REPLACE FUNCTION fn_employee_get_by_id(
    IN p_employee_id UUID
)
RETURNS SETOF employee AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM employee
    WHERE employee_id = p_employee_id;
END;
$$ LANGUAGE plpgsql;

--==================
DROP FUNCTION IF EXISTS fn_employees_get_all();

CREATE OR REPLACE FUNCTION fn_employees_get_all()
RETURNS SETOF employee AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM employee;
END;
$$ LANGUAGE plpgsql;

--==================
DROP FUNCTION IF EXISTS fn_upload_request_data(p_request_id, p_employee_id, p_email_body, p_email_subject, p_document_data);

CREATE OR REPLACE FUNCTION fn_upload_request_data(
    p_request_id UUID,
    p_employee_id UUID,
    p_email_body TEXT,
    p_email_subject TEXT,
    p_document_data JSON
) RETURNS VOID AS $$
DECLARE 
    date_current TIMESTAMP := NOW();
    waiting_for_clarification_status_id INT;
    open_status_id INT;
BEGIN
    
    waiting_for_clarification_status_id := (SELECT status_id FROM compensation_status WHERE status_name = 'waiting_for_clarification');
    open_status_id := (SELECT status_id FROM compensation_status WHERE status_name = 'open');

    -- Insert mployee_compensation_request
    INSERT INTO employee_compensation_request (
        request_id, 
        employee_id,
        created_date,
        updated_date,
        status_id,
        compensation_sum_usd,
        email_subject,
        email_body
    ) 
    VALUES (
        p_request_id,
        p_employee_id,
        date_current,
        date_current,
        open_status_id,
        NULL,
        p_email_subject,
        p_email_body
    ) ON CONFLICT (request_id) DO NOTHING;

    -- Create temporary table to store parsed JSON
    CREATE TEMP TABLE temp_parsed_documents (
        attachment_id UUID DEFAULT gen_random_uuid(),
        record_id UUID DEFAULT gen_random_uuid(),
        request_id UUID,
        file_name TEXT,
        category_name TEXT,
        category_id INT,
		status_id INT,
        document_number VARCHAR(50),
        document_date TIMESTAMP,
        address TEXT,
        document_sum MONEY,
        document_currency VARCHAR(10),
        account_number TEXT,
        additional_info TEXT,
        document_data JSON
    ) ON COMMIT DROP;

    -- parse JSON data
    INSERT INTO temp_parsed_documents (
        request_id,
        file_name,
        category_name,
        status_id,
        document_number,
        document_date,
        address,
        document_sum,
        document_currency,
        account_number,
        additional_info,
        document_data
        )
    SELECT 
        p_request_id,
        doc->>'file_name',
        doc->>'category',
		(doc ->> 'status_id')::INT,
        doc->>'document_number',
        (doc->>'document_date')::TIMESTAMP,
        doc->>'address',
        (doc->>'document_sum')::MONEY,
        doc->>'document_currency',
        doc->>'account_number',
        doc->>'additional_info',
        doc
    FROM json_array_elements(p_document_data->'documents') AS doc;

    -- Update category_id
    UPDATE temp_parsed_documents tpd
        SET category_id = bc.category_id
    FROM benefit_category bc
    WHERE tpd.category_name = bc.category_name;

    -- Insert compensation_request_records
    INSERT INTO compensation_request_records (
        record_id,
        request_id,
        status_id,
        updated_date,
        category_id
    )
    SELECT 
        record_id,
        request_id,
        status_id,
        date_current,
        category_id
    FROM temp_parsed_documents;

    -- Insert compensation_request_attachments
    INSERT INTO compensation_request_attachments (
        attachment_id,
        record_id,
        file_name,
        document_date,
        document_number,
        address,
        document_sum,
        document_currency,
        account_number,
        additional_info,
        document_data
    )
    SELECT 
        attachment_id,
        record_id, file_name, document_date, document_number, address, document_sum, document_currency, account_number, additional_info, document_data
    FROM temp_parsed_documents;

    IF EXISTS (
                SELECT 1 
                FROM compensation_request_records 
                WHERE request_id = p_request_id 
                    AND status_id = waiting_for_clarification_status_id
                )
        THEN
            UPDATE employee_compensation_request
                SET status_id = waiting_for_clarification_status_id
            WHERE request_id = p_request_id;
    END IF;

END;
$$ LANGUAGE plpgsql;

--==================
DROP FUNCTION IF EXISTS fn_user_benefit_categories_get(p_employee_id);

CREATE OR REPLACE FUNCTION fn_user_benefit_categories_get(
    IN p_employee_id UUID
)
RETURNS TABLE (
    employee_id UUID,
    category_id INT,
    category_name VARCHAR(100),
    category_description TEXT,
    cover_amount MONEY,
    cover_size NUMERIC(3,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        eps.employee_id,
        bc.category_id, 
        bc.category_name, 
        bc.category_description,
        bc.cover_amount,
        bc.cover_size
    FROM employee_package_set eps
    JOIN benefit_category bc
        ON bc.category_id = eps.category_id
        AND eps.employee_id = p_employee_id
    ;
END;
$$ LANGUAGE plpgsql;