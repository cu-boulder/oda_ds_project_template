# Cookiecutter for ODA Data Science Projects

A custom cookiecutter template based on [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/)


### Requirements to use the cookiecutter template:
-----------
 - Python 3.8.x
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0
 - [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

``` bash
$ pip install cookiecutter
```
### To start a new project, run:
-----------

`cookiecutter https://github.com/cu-boulder/oda_ds_project_template.git`

### Project Organization


    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creators initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    |   └── automatic_eda  <- Generated pandas-profiling reports
    │
    ├── Pipfile            <- The requirements file for reproducing the analysis environment.
    |
    |── src                <- Source code for use in this project.
        │── automatic_eda  <- Scripts to create an automated eda report using pandas-profiling
        │   
        ├── data           <- Scripts to download or generate data
        │
        ├── features       <- Scripts to turn raw data into features for modeling
        │
        ├── models         <- Scripts to train models and then use trained models to make
        │                  predictions
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
 
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. cookiecutterdatascience</small></p>

### Installing development requirements
-----------
`cd` to the newly created project and run `pipenv install`
