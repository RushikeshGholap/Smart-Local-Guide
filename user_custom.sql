
INSERT INTO public.user_custom(user_id,totalreviews,totallowratings,lowratingratio,
totalhighratings,highratingratio,
totalavgrating,avgratingratio)
select user_id, count(rating), 
count(CASE WHEN rating < 2 THEN 1 END),
cast(count(CASE WHEN rating < 2 THEN 1 END) as float)/cast(count(rating) as float),
count(CASE WHEN rating > 4 THEN 1 END), 
cast(count(CASE WHEN rating > 4 THEN 1 END) as float)/cast(count(rating) as float),
COUNT(CASE WHEN rating >= 2 and rating <=4 THEN 1 END),
cast(COUNT(CASE WHEN rating >= 2 and rating <=4 THEN 1 END) as float)/cast(count(rating) as float)

from public.main
group 
by user_id
;


update user_custom
set negativeextreme = subquery.negativeextreme,
positiveextreme = subquery.highextreme,
averageextreme = subquery.avgextreme
from (SELECT user_id,
CASE WHEN totalreviews > 10 and lowratingratio =1 and avgratingratio = 0 and highratingratio = 0
THEN True
ELSE False END as negativeextreme,
CASE WHEN totalreviews > 10 and lowratingratio =0 and avgratingratio = 1 and highratingratio = 0
THEN True
ELSE False END as avgextreme,
CASE WHEN totalreviews > 10 and lowratingratio =0 and avgratingratio = 0 and highratingratio = 1
THEN True
ELSE False END as highextreme
from user_custom) as subquery
where user_custom.user_id = subquery.user_id;