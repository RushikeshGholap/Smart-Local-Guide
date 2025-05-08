INSERT INTO public.metadata_custom(gmap_id,totalreviews,tottallowratings,lowratingratio,
totalhighratings,highratingratio,
totalavgrating,avgratingratio)
select gmap_id, count(rating), 
count(CASE WHEN rating < 2 THEN 1 END),
cast(count(CASE WHEN rating < 2 THEN 1 END) as float)/cast(count(rating) as float),
count(CASE WHEN rating > 4 THEN 1 END), 
cast(count(CASE WHEN rating > 4 THEN 1 END) as float)/cast(count(rating) as float),
COUNT(CASE WHEN rating >= 2 and rating <=4 THEN 1 END),
cast(COUNT(CASE WHEN rating >= 2 and rating <=4 THEN 1 END) as float)/cast(count(rating) as float)

from public.main
group 
by gmap_id
;


update metadata_custom
set no_preferred_extreme = subquery.no_preferred_extreme,
avg_preferred_extreme = subquery.avg_preferred_extreme,
preferred_extreme = subquery.preferred_extreme
from (SELECT gmap_id,
CASE WHEN totalreviews > 10 and lowratingratio =1 and avgratingratio = 0 and highratingratio = 0
THEN True
ELSE False END as no_preferred_extreme,
CASE WHEN totalreviews > 10 and lowratingratio =0 and avgratingratio = 1 and highratingratio = 0
THEN True
ELSE False END as avg_preferred_extreme,
CASE WHEN totalreviews > 10 and lowratingratio =0 and avgratingratio = 0 and highratingratio = 1
THEN True
ELSE False END as preferred_extreme
from metadata_custom) as subquery
where metadata_custom.gmap_id= subquery.gmap_id;