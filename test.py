#!/usr/bin/python3

# input variables
conduit_api_key = '/home/dfelinto/.conduit-dev.b.o'

multi_object_tasks = 54641
copy_on_write_tasks = 54810

import requests
manifest_url = "https://developer.blender.org/api/maniphest.info"
phid_url = "https://developer.blender.org/api/phid.lookup"

api_token = open(conduit_api_key).read().rstrip()


def get_tasks(task_id):
    """
    Return all the children tasks for a given task id.
    """
    api_token = open(conduit_api_key).read().rstrip()

    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'api.token': api_token,
        'task_id': task_id,
    }

    response = requests.post(manifest_url, headers=headers, params=params)
    tasks_phids = response.json()['result']['dependsOnTaskPHIDs']

    params = {
        'api.token': api_token,
        'names[0]': tasks_phids[0],
        'names[1]': tasks_phids[1],
    }

    for i, task_phid in enumerate(tasks_phids):
        params['names[{0}]'.format(i)] = task_phid

    response = requests.post(phid_url, headers=headers, params=params)
    result = response.json()['result']

    tasks = []
    for phid_dict in result.values():
        task_raw = phid_dict['name']
        task = int(task_raw[1:])
        tasks.append(task)
    return tasks


def main():
    headers = {
        'Content-Type': 'application/json',
    }

    params = {
        'api.token': api_token,
    }

    # TODO get this from cli
    tasks = get_tasks(multi_object_tasks)
    #tasks = get_tasks(copy_on_write_tasks)

    for task_id in tasks:
        params['task_id'] = task_id

        response = requests.post(manifest_url, headers=headers, params=params)
        result = response.json()

        if result['error_code'] is not None:
            print("Error: {0}".format(result['error_info']))
        else:
            print(result['result']['description'])


if __name__ == '__main__':
    main()
