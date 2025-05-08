update main set noise_indicator = result.noise
from(
select subquery.user_id, subquery.gmap_id,
CASE WHEN subquery.business_type = 0 and subquery.user_type = 0 and subquery.rating >=2 THEN TRUE 
WHEN subquery.business_type = 1 and subquery.user_type = 1 and (subquery.rating < 2 or subquery.rating > 4) THEN TRUE
WHEN subquery.business_type = 2 and subquery.user_type = 2 and subquery.rating <= 4 THEN TRUE
ELSE FALSE END as NOISE
from (select sub.user_id, sub.gmap_id, sub.business_type, uc.user_type, sub.rating from (select main.gmap_id,main.user_id, mc.business_type,main.rating from main join
metadata_custom_ext mc
on main.gmap_id = mc.gmap_id) sub join userdata_custom_ext uc
on sub.user_id = uc.user_id) as subquery) as result
where main.user_id = result.user_id and main.gmap_id = result.gmap_id;

