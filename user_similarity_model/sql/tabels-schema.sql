DROP TABLE IF EXISTS user_assessment_scores;
CREATE TABLE user_assessment_scores (
    user_handle INTEGER NOT NULL,
    assessment_tag VARCHAR(255) NOT NULL,
    user_assessment_date TIMESTAMP NOT NULL,
    user_assessment_score INTEGER NOT NULL
);

DROP TABLE IF EXISTS user_interests;
CREATE TABLE user_interests (
    user_handle INTEGER NOT NULL,
    interest_tag VARCHAR(255) NOT NULL,
    date_followed TIMESTAMP NOT NULL
);

DROP TABLE IF EXISTS course_tags;
CREATE TABLE course_tags (
    course_id VARCHAR(255) NOT NULL,
    course_tags VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS user_course_views;
CREATE TABLE user_course_views (
    user_handle INTEGER NOT NULL,
    view_date DATE NOT NULL,
    course_id VARCHAR(255) NOT NULL,
    author_handle INTEGER NOT NULL,
    level VARCHAR(255) NOT NULL,
    view_time_seconds INTEGER NOT NULL
);