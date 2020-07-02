# Project Dash
In this project I will gather data from different sources to create a dashboard to monitor performance of different projects.

## Integrations
- Jira :white_check_mark:
- Github :white_check_mark:
- CircleCI :calendar:

## Configuration
I use `confuse` to handle the configuration. This requires three steps:

1. Define an application name in `__main__.py` to initialize the configuration:
    ```python
    """ __main__.py """
    ...
    APPNAME = "PROJECTDASH"
    ...
    config = confuse.Configuration(APPNAME)
    ...
    ```
2. Export `APPNAMEDIR` to the directory of this repo to make sure `confuse` can find the configuration:
    ```bash
    export PROJECTDASHDIR=/Users/jitse-jan/code/project-dash
    ```
3. Add the following to `config.yaml` in the root folder:
    ```yaml
    # config.yaml
    jira:
        project: ABC
        board_id: 1234
    github:
    repos:
        myuser/myrepo-1
        myuser/myrepo-2
    ```

