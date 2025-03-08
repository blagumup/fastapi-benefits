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
		ecr.compensation_sum_usd,
		null AS total_used,
		ecr.email_subject,
		ecr.email_body
	FROM employee_compensation_request ecr
	JOIN employee e
		ON e.employee_id = ecr.employee_id
	JOIN compensation_status cs 
		ON ecr.status_id = cs.status_id;

END;
$$ LANGUAGE plpgsql;