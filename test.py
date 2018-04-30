#!/usr/bin/python3

# input variables
conduit_api_key = '/home/dfelinto/.conduit-dev.b.o'
multi_object_tasks = 54641
copy_on_write_tasks = 54810


import requests
manifest_url = "https://developer.blender.org/api/maniphest.info"
phid_url = "https://developer.blender.org/api/phid.lookup"


# Settings required for all the requests calls.
api_token = open(conduit_api_key).read().rstrip()
headers = {'Content-Type': 'application/json'}


def get_tasks(task_id):
    """
    Return all the children tasks for a given task id.
    """
    params = {
        'api.token': api_token,
        'task_id': task_id,
    }

    response = requests.post(manifest_url, headers=headers, params=params)
    tasks_phids = response.json()['result']['dependsOnTaskPHIDs']

    params = {
        'api.token': api_token,
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


def get_tasks_content(tasks):
    params = {
        'api.token': api_token,
    }

    results = []
    for task_id in tasks:
        params['task_id'] = task_id

        response = requests.post(manifest_url, headers=headers, params=params)
        result = response.json()

        if result['error_code'] is not None:
            print("Error: {0}".format(result['error_info']))
        else:
            results.append(result['result']['description'])
    return "".join(results)


def extract_info(raw_text):
    import re
    all_operators = re.compile('_OT_')
    done_operators = re.compile('~~.*_OT_.*~~')

    count_done = len(done_operators.findall(raw_text))
    count_all = len(all_operators.findall(raw_text))

    return count_done, count_all


def get_main_task_id():
    # TODO get this from cli
    multi_object_tasks = 54641
    copy_on_write_tasks = 54810
    tasks = multi_object_tasks
    tasks = copy_on_write_tasks

    return tasks


def main():
    main_task_id = get_main_task_id()
    tasks = get_tasks(main_task_id)
    content = get_tasks_content(tasks)
    count_done, count_all = extract_info(content)

    print(count_done, count_all)


if __name__ == '__main__':
    main()

