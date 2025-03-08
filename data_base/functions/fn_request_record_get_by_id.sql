CREATE OR REPLACE FUNCTION fn_request_record_get_by_id(p_request_id UUID)
RETURNS TABLE (
	request_id UUID,
	record_id UUID,
	transactiondate TIMESTAMP,
	category_id INT,
	category TEXT,
	status_id INT,
	full_name TEXT,
	recipient TEXT,
	recipe_amount_local MONEY,
	recipe_currency TEXT,
	recuipe_amount_usd MONEY,
	recipe_status TEXT,
	attachment_id UUID,
	file_name TEXT,
	file_path TEXT
)	
AS $$
BEGIN

	RETURN QUERY
	SELECT 
		crr.request_id,
		crr.record_id,
		cra.document_date as transactionDate,
		crr.category_id,
		bc.category_name as category,
		crr.status_id,
		null::text as full_name,
		null::text as recipient,
		cra.document_sum as recipe_amount_local,
		cra.document_currency as recipe_currency,
		null::money as recuipe_amount_usd,
		cs.status_name as recipe_status,
		cra.attachment_id,
		cra.file_name,
		cra.file_path
	FROM compensation_request_records crr 
	join compensation_request_attachments cra  	
		ON crr.record_id  = cra.record_id
	join benefit_category bc 
		on bc.category_id = crr.category_id
	join compensation_status cs 
		on crr.status_id = cs.status_id	
	;

END;
$$ LANGUAGE plpgsql;