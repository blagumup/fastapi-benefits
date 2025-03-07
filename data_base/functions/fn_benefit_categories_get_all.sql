CREATE OR REPLACE FUNCTION fn_benefit_categories_get_all()
RETURNS SETOF benefit_category AS $$
BEGIN
	RETURN QUERY
	SELECT *
	FROM benefit_category;
END;
$$ LANGUAGE plpgsql;