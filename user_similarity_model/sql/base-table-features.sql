--################################################################################
/*
The Postgresql tables that are used in this sql file are:
    1- public.user_interests
    2- public.user_assessment_scores
    3- public.user_course_views
    4- public.course_tags
The following features are extracted from the table for the
user similarity modeling:
    - latest_interest_tag: the most recent interest tag by a user
    - delta_day_interest: days between the first interest date and the 
        last interest date. It could be a proxy for user tenure.
    - number_of_distinct_interests
    - latest_assessment_tag: The most recent assessment by a user
    - number_of_assessments
    - mean_score: The average assements score by a user
    - count_views: Total number of views a user had
    - number_of_beginner_course: Total number of beginner courses
    - number_of_intermediate_course: Total number of intermediate courses
    - number_of_advanced_course: Total number of advanced courses
    - time_spent_beginner_course:  Total spent time on begineer courses
    - time_spent_intermediate_course:  Total spent time on intermediate courses
    - time_spent_advanced_course:  Total spent time on advanced courses
    - total_courses_time_spent: Total spent time on courses 
    */
--################################################################################

--Interest table
with latest_interests as(
    select  
        user_handle
        , interest_tag as latest_interest_tag
        , row_number() over(
            partition BY
                user_handle
            order by    
                date_followed desc
        ) as order_within_interests
    from    
        public.user_interests
),

interest_stats as(
    select
        user_handle
        , count(distinct interest_tag) as number_of_distinct_interests
        -- we can calculate the number of days between the first and last interest by a user
        , max(cast(date_followed as date)) - min(cast(date_followed as date)) as delta_day_interest       

    from
        public.user_interests
    group by
        user_handle
),

final_interests as(
    select  
        latest_interests.user_handle
        , latest_interests.latest_interest_tag
        , interest_stats.number_of_distinct_interests
        , interest_stats.delta_day_interest
    from
        interest_stats
        left join latest_interests
            on latest_interests.user_handle = interest_stats.user_handle
    where
        -- Here we extract the latest but we can change this
        latest_interests.order_within_interests = 1
),

-- Assessments Table
latest_assessments as(
    select  
        user_handle
        , assessment_tag as latest_assessment_tag
        , user_assessment_score as latest_assessment_score
        , row_number() over(
            partition BY
                user_handle
            order by    
                extract(month from cast(user_assessment_date as date)) desc
                , extract(day from cast(user_assessment_date as date)) desc
        ) as order_within_assessments
    from    
        public.user_assessment_scores
),

assessments_stats as(
    select
        user_handle
        , count(user_assessment_score) as number_of_assessments
        , avg(user_assessment_score) as mean_score
    from
        public.user_assessment_scores
    group by
        user_handle
),

final_assessments as(
    select  
        latest_assessments.user_handle
        , latest_assessments.latest_assessment_tag
        , latest_assessments.latest_assessment_score
        , assessments_stats.number_of_assessments
        , assessments_stats.mean_score
    from
        assessments_stats 
        left join latest_assessments
            on latest_assessments.user_handle = assessments_stats.user_handle
    where
        latest_assessments.order_within_assessments = 1
),

-- Views
latest_views as(
    select  
        a.user_handle
        , b.course_tags as latest_course_tags
        , a.level as latest_level
        , a.view_time_seconds as latest_view_time
        , row_number() over(
            partition BY
                a.user_handle
            order by    
                a.view_date desc
        ) as order_within_views
    from    
        public.user_course_views as a
        join public.course_tags as b
            on a.course_id = b.course_id
),

view_stats as(
    select
        user_handle
        , count(view_date) as count_views
        , sum(case when level = 'Beginner' then 1 else 0 end) as number_of_beginner_course
        , sum(case when level = 'Intermediate' then 1 else 0 end) as number_of_intermediate_course
        , sum(case when level = 'Advanced' then 1 else 0 end) as number_of_advanced_course
        , sum(case when level = 'Beginner' then view_time_seconds else 0 end) as time_spent_beginner_course
        , sum(case when level = 'Intermediate' then view_time_seconds else 0 end) as time_spent_intermediate_course
        , sum(case when level = 'Advanced' then view_time_seconds else 0 end) as time_spent_advanced_course
        , sum(view_time_seconds) as total_courses_time_spent
    from
        public.user_course_views
    group by
        user_handle
),

final_views as(
    select  
        latest_views.latest_level
        , view_stats.*
    from
        view_stats
        left join latest_views
            on latest_views.user_handle = view_stats.user_handle
    where
        latest_views.order_within_views = 1
)

-- Join all final tables toghether to get the final base table for modeling
select 
    final_interests.user_handle
    , final_interests.latest_interest_tag
    , final_interests.delta_day_interest
    , final_interests.number_of_distinct_interests
    -- Using coalese helps with imputing missings with 0 directly in the database side
    , coalesce(final_assessments.latest_assessment_tag, 'Missing') as latest_assessment_tag
    , coalesce(final_assessments.number_of_assessments, 0) as number_of_assessments
    , coalesce(final_assessments.mean_score, 0) as mean_score
    , coalesce(final_views.count_views, 0) as count_views
    , coalesce(final_views.number_of_beginner_course, 0) as number_of_beginner_course
    , coalesce(final_views.number_of_intermediate_course, 0) as number_of_intermediate_course
    , coalesce(final_views.number_of_advanced_course, 0) as number_of_advanced_course
    , coalesce(final_views.time_spent_beginner_course, 0) as time_spent_beginner_course
    , coalesce(final_views.time_spent_intermediate_course, 0) as time_spent_intermediate_course
    , coalesce(final_views.time_spent_advanced_course, 0) as time_spent_advanced_course
    , coalesce(final_views.total_courses_time_spent, 0) as total_courses_time_spent
--final_interests have all 10000 users
from final_interests
    left join final_views
        on final_views.user_handle = final_interests.user_handle
    -- we left join on final assessments since not every user has an assessment
    left join final_assessments
        on final_views.user_handle = final_assessments.user_handle
