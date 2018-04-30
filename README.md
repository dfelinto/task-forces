# Task Force Tracker

This is a main Python script and some bash crontab scripts to be used together with [Grafista](https://github.com/armadillica/grafista).

## Instalation
* Install grafista in the server.
* See configurations to customize your database.
* Install your updated scripts with `crontab -e`.
e.g., `0  2 * * * PATH_TO_THIS_REPO/crontab/update_multi_object.sh`

## Configuration
```
DATA_SOURCES = [
    {'url': '',
     'series': [
         {
            'name': 'copy_on_write',
            'description': 'Copy on Write T54810',
            'sample_unit': 'tasks',
            'force_y': 0,
        },
        {
            'name': 'multi_object',
            'description': 'Multi-Object T54641',
            'sample_unit': 'tasks',
            'force_y': 0,
        },
        ],
    }
]
```
