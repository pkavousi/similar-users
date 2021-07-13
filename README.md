# Finding similar users model

## Table of contents
   * [Overview](#Overview)
   * [Architectural Diagram](#Architectural-Diagram)
   * [Running the app](#Running-the-app)
   * [Screencast](#Screencast)
   * [Comments and future improvements](#Comments-and-future-improvements)
   * [Project folder structure](#Project-folder-structure)
   * [References](#References)

***

## Architectural-Diagram
![Architectural Diagram](reference_images/architechture.png?raw=true "Architectural Diagram") 

## Project-folder-structure
```
.
├── LICENSE
├── MANIFEST.in
├── README.md
├── app
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── predict.py
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       └── test_api.py
├── dist
│   ├── user-similarity-model-0.1.0.tar.gz
│   └── user_similarity_model-0.1.0-py3-none-any.whl
├── mypy.ini
├── pyproject.toml
├── requirements
│   ├── requirements.txt
│   └── test_requirements.txt
├── setup.py
├── tests
│   ├── conftest.py
│   ├── test_postgresql.py
│   └── test_predict.py
├── tox.ini
├── user_similarity_model
│   ├── VERSION
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   └── core.py
│   ├── config.yml
│   ├── datasets
│   │   ├── __init__.py
│   │   ├── course_tags.csv
│   │   ├── sample_query_raw_data.csv
│   │   ├── user_assessment_scores.csv
│   │   ├── user_course_views.csv
│   │   └── user_interests.csv
│   ├── model.py
│   ├── pipeline.py
│   ├── predict.py
│   ├── processing
│   │   ├── __init__.py
│   │   ├── data_upload_manager.py
│   │   ├── modeling_data_manager.py
│   │   └── validation.py
│   ├── sql
│   │   ├── __init__.py
│   │   ├── base-table-features.sql
│   │   ├── tabels-schema.sql
│   │   └── test-sql-fetch.sql
│   ├── train_pipeline.py
│   └── trained_models
│       ├── __init__.py
│       └── user_similarity_model_output_v0.1.0.pkl
└── user_similarity_model.egg-info
    ├── PKG-INFO
    ├── SOURCES.txt
    ├── dependency_links.txt
    ├── requires.txt
    └── top_level.txt
```