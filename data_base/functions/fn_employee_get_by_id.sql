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