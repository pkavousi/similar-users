select  
    count(index)  
from 
    public.course_tags
where 
    course_id = '2d-racing-games-unity-volume-2-1286';

select
    user_assessment_score as score
from 
    public.user_assessment_scores
where 
    user_handle = 7487 
    and assessment_tag = 'angular-js';

select  
    user_handle
from 
    public.user_course_views
where
    view_date = '2017-06-27'
    and author_handle = 875;

select
    user_handle
from 
    public.user_interests
where 
    interest_tag = 'devops' 
    and date_followed = '2017-11-06 16:55:35'
