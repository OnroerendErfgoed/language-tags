import json

index = json.load(open("../data/json/index.json"))
registry = json.load(open("../data/json/registry.json"))


def Tag(tag):

    # Lowercase for consistency (case is only a formatting convention, not a standard requirement).
    tag = tag.strip().lower()

    data = {'tag': tag}

    # Check if the input tag is grandfathered or redundant.
    if tag in index:
        types = index[tag]
        if 'grandfathered' in types or 'redundant' in types:
            data['record'] = registry[types['grandfathered']] if 'grandfathered' in types \
                else registry[types['redundant']]
    types = index[tag]
    return types