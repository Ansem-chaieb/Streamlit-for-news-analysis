import urllib
import pandas as pd
import json
import itertools
# from OpenNRE import opennre


ENTITY_TYPES = ["human", "person", "company", "enterprise", "business", "geographic region",
                "human settlement", "geographic entity", "territorial entity type", "organization"]


# this part of code was inspired from
#  https://towardsdatascience.com/from-text-to-knowledge-the-information-extraction-pipeline-b65e7e30273e


def wikifier(text, lang="en", threshold=0.8):
    data = urllib.parse.urlencode([
        ("text", text), ("lang", lang),
        ("userKey", "tgbdmkpmkluegqfbawcwjywieevmza"),
        ("pageRankSqThreshold", "%g" %
         threshold), ("applyPageRankSqThreshold", "true"),
        ("nTopDfValuesToIgnore", "100"), ("nWordsToIgnoreFromList", "100"),
        ("wikiDataClasses", "true"), ("wikiDataClassIds", "false"),
        ("support", "true"), ("ranges", "false"), ("minLinkFrequency", "2"),
        ("includeCosines", "false"), ("maxMentionEntropy", "3")
    ])
    url = "http://www.wikifier.org/annotate-article"
    # Call the Wikifier and read the response.
    req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
    with urllib.request.urlopen(req, timeout=60) as f:
        response = f.read()
        response = json.loads(response.decode("utf8"))
    # Output the annotations.
    results = list()
    for annotation in response["annotations"]:
        # Filter out desired entity classes
        if ('wikiDataClasses' in annotation) and (
        any([el['enLabel'] in ENTITY_TYPES for el in annotation['wikiDataClasses']])):

            # Specify entity label
            if any([el['enLabel'] in ["human", "person"] for el in annotation['wikiDataClasses']]):
                label = 'Person'
            elif any([el['enLabel'] in ["company", "enterprise", "business", "organization"] for el in
                      annotation['wikiDataClasses']]):
                label = 'Organization'
            elif any([el['enLabel'] in ["geographic region", "human settlement", "geographic entity",
                                        "territorial entity type"] for el in annotation['wikiDataClasses']]):
                label = 'Location'
            else:
                label = None

            results.append({'title': annotation['title'], 'wikiId': annotation['wikiDataItemId'], 'label': label,
                            'characters': [(el['chFrom'], el['chTo']) for el in annotation['support']]})
    return results


def generate_relations(model, docx):
    entities = wikifier(docx)

    # Iterate over every permutation pair of entities
    relations_list = []
    for permutation in itertools.permutations(entities, 2):
        for source in permutation[0]['characters']:
            for target in permutation[1]['characters']:
                # Relationship extraction with OpenNRE
                data = model.infer(
                    {'text': docx, 'h': {'pos': [source[0], source[1] + 1]},
                     't': {'pos': [target[0], target[1] + 1]}})
                if data[1] > 0.8:
                    relations_list.append(
                        {'source': permutation[0]['title'], 'target': permutation[1]['title'], 'type': data[0]})

    relations_list = [dict(t) for t in {tuple(d.items()) for d in relations_list}]
    k, v, r = [], [], []
    for i in range(len(relations_list)):
        k.append(relations_list[i]['source'])
        v.append(relations_list[i]['target'])
        r.append(relations_list[i]['type'])
    data = {'source': k, 'target': v, 'type': r}
    rf = pd.DataFrame(data)
    return rf
