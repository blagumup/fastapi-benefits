CREATE OR REPLACE FUNCTION fn_user_benefit_categories_get(
    IN employee_id UUID
)
RETURNS TABLE (
    employee_id UUID
    category_id UUID,
    category_name TEXT,
    category_description TEXT,
    cover_amount MONEY,
    cover_size NUMERIC(1,2)
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
        AND eps.employee_id = employee_id
    ;
END;
$$ LANGUAGE plpgsql;