CREATE OR REPLACE FUNCTION fn_employees_get_all()
RETURNS SETOF employee AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM employee;
END;
$$ LANGUAGE plpgsql;