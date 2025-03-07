CREATE OR REPLACE FUNCTION fn_compensation_requests_get_all()
RETURNS SETOF compensation_request_records AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM compensation_request_records;
END;
$$ LANGUAGE plpgsql;