
CREATE OR REPLACE FUNCTION fn_upload_request_data(
    p_request_id UUID,
    p_employee_id UUID,
    p_email_body TEXT,
    p_email_subject TEXT,
    p_document_data JSON
) RETURNS VOID AS $$
DECLARE 
    date_current TIMESTAMP := NOW()
BEGIN
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
    ) VALUES (
        p_request_id,
        p_employee_id,
        date_current,
        date_current,
        NULL,
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
		doc ->> 'status_id',
        doc->>'document_number',
        (doc->>'document_date')::TIMESTAMP,
        doc->>'address',
        (doc->>'document_sum')::MONEY,
        doc->>'document_currency',
        doc->>'account_number',
        doc->>'additional_info',
        doc
    FROM jsonb_array_elements(p_document_data->'documents') AS doc;

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
    SELECT attachment_id, record_id, file_name, document_date, document_number, address, document_sum, document_currency, account_number, additional_info, document_data
    FROM temp_parsed_documents;

END;
$$ LANGUAGE plpgsql;
