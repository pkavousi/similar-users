import os

import pandas as pd
import psycopg2

from user_similarity_model.config.core import SQL_DIR, config


def test_course_tag_pull(sample_local_data):

    conn = psycopg2.connect(**config.app_config.database_specs)
    cur = conn.cursor()
    # create table one by one
    # for command in commands:
    #     cur.execute(command)
    with open(os.path.join(SQL_DIR, "test-sql-fetch.sql")) as file:
        query = file.read().split(";")
    cur.execute(query[0])
    rows = cur.fetchall()
    courses_remote = pd.DataFrame(rows, columns=["count"]).loc[0, "count"]
    local_df_course_tag = sample_local_data["course_tags"]
    courses_local = local_df_course_tag[
        local_df_course_tag.course_id == "2d-racing-games-unity-volume-2-1286"
    ].shape[0]
    assert courses_remote == courses_local

    # test a score between two databases
    cur.execute(query[1])
    rows = cur.fetchall()
    assessments_remote = pd.DataFrame(rows, columns=["score"]).loc[0, "score"]
    local_df_assessments = sample_local_data["user_assessment_scores"]
    local = local_df_assessments[
        (local_df_assessments.user_handle == 7487)
        & (local_df_assessments.assessment_tag == "angular-js")
    ].loc[0, "user_assessment_score"]
    assert assessments_remote == local

    # test the third tables
    cur.execute(query[2])
    rows = cur.fetchall()
    views_remote = pd.DataFrame(rows, columns=["user_handle"]).loc[0, "user_handle"]
    local_df_views = sample_local_data["user_course_views"]
    local = local_df_views[
        (local_df_views.view_date == "2017-06-27")
        & (local_df_views.author_handle == 875)
    ].loc[0, "user_handle"]
    assert views_remote == local

    # test the fourth table
    cur.execute(query[3])
    rows = cur.fetchall()
    interests_remote = pd.DataFrame(rows, columns=["user_handle"]).loc[0, "user_handle"]
    local_df_interests = sample_local_data["user_interests"]
    local = (
        local_df_interests[
            (local_df_interests.interest_tag == "devops")
            & (local_df_interests.date_followed == "2017-11-06 16:55:35")
        ]
        .reset_index()
        .loc[0, "user_handle"]
    )
    assert interests_remote == local
