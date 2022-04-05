from cProfile import label
import json
import numpy as np

test ='{"id": "fd2a1d78-eebd-4a27-b707-9da67b4a8ad8", "downloadCandidates": [{"id": "0", "label": "json", "selectedByDefault": false}], "outputs": [{"type": "json", "data": {"result": {"sequence": "I love the Tango", "labels": ["music", "travel"], "scores": [0.9751193523406982, 0.024880604818463326]}}}]}'

def extract_labels(json_in):
    u = json.loads(json_in)

    print(u['outputs'][0]['data']['result'])
    labels = u['outputs'][0]['data']['result']['labels']
    scores = np.array(u['outputs'][0]['data']['result']['scores'])

    sorting = np.argsort(scores)[::-1]
    print(sorting)

    label_out = [labels[i] for i in sorting]
    s = ''
    for l in label_out:
        s += l + ';'

    s = s.strip(';')
    print(s)

    return s