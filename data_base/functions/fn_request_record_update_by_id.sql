CREATE OR REPLACE FUNCTION fn_request_record_update_by_id(p_record_id UUID, p_status_id INT)
RETURNS VOID
AS $$
DECLARE 
    date_current TIMESTAMP := NOW();
    v_request_id UUID;
BEGIN

    v_request_id := (SELECT request_id FROM compensation_request_records WHERE record_id = p_record_id);

    UPDATE compensation_request_records
    SET status_id = p_status_id,
        updated_date = date_current
    WHERE record_id = p_record_id;

    WITH record_statuses AS (
        SELECT 
            cr.request_id,
            ARRAY_AGG(DISTINCT cs.status_name) AS status_list
        FROM compensation_request_records cr
        JOIN compensation_status cs ON cr.status_id = cs.status_id
        WHERE cr.request_id = v_request_id
        GROUP BY cr.request_id
    ),
    status_updates AS (
        SELECT 
            request_id,
            CASE 
                WHEN ARRAY['open', 'exceeded_limit'] && status_list THEN 'open'
                WHEN 'waiting_for_clarification' = ANY(status_list) THEN 'waiting_for_clarification'
                WHEN status_list <@ ARRAY['approved', 'declined', 'cancelled'] THEN 'processed'
                ELSE NULL 
            END AS new_status
        FROM record_statuses
    )
    UPDATE employee_compensation_request ecr
    SET status_id = cs.status_id
    FROM status_updates su
    JOIN compensation_status cs 
        ON su.new_status = cs.status_name
    WHERE ecr.request_id = su.request_id
    AND su.new_status IS NOT NULL; 

END;
$$ LANGUAGE plpgsql;
