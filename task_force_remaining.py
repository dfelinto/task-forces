#!/usr/bin/python3

import requests
manifest_url = "https://developer.blender.org/api/maniphest.info"
phid_url = "https://developer.blender.org/api/phid.lookup"

# Settings required for all the requests calls.
headers = {'Content-Type': 'application/json'}

def get_tasks(api_token, task_id):
    """
    Return all the children tasks ids for a task id
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


def get_tasks_content(api_token, tasks):
    """
    Return the raw content of given tasks
    """
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
    """
    Process the blob of all tasks
    Returns a tuple with done and total ammount of tasks.
    """
    import re
    all_operators = re.compile('_OT_')
    done_operators = re.compile('~~.*_OT_.*~~')

    count_done = len(done_operators.findall(raw_text))
    count_all = len(all_operators.findall(raw_text))

    return count_done, count_all


def parse_arguments():
    """
    Parse input
    We get the main task id from command-line and the conduit API.
    """
    import argparse

    parser = argparse.ArgumentParser("task_force_remaining")
    parser.add_argument("task_id", help=
    "The task number for the task force (e.g., 54641 for multi-object or 54810 for copy-on-write)"
    , type=int)
    parser.add_argument("conduit_api_key", help=
    "Certificate token obtain from https://developer.blender.org/conduit/token"
    , type=str)
    args = parser.parse_args()

    return args.task_id, args.conduit_api_key


def main():
    """
    Return (print) the remaining tasks for a given task-force.
    """
    main_task_id, api_key = parse_arguments()

    # Require connection.
    tasks = get_tasks(api_key, main_task_id)
    content = get_tasks_content(api_key, tasks)

    # Process the obtained info.
    count_done, count_all = extract_info(content)

    # Return the final result.
    remaining_tasks = count_all - count_done
    print(remaining_tasks)


if __name__ == '__main__':
    main()

