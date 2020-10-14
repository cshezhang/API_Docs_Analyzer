import json


def get_sensitive_keywords():
    # Get sensitive keywords from our json file.
    keywords = []
    tree_file = open(".\\res\\sensitive_keywords.json", "r")
    tree_dict = json.load(tree_file)
    tree_file.close()
    privacy_words = []
    que = [tree_dict]
    while len(que) > 0:
        head = que[0]
        que.remove(head)
        privacy_words.append(head["name"])
        if "children" in head.keys():
            for child_node in head["children"]:
                que.append(child_node)
    for item in privacy_words:
        words = item.split("_")
        keywords.append(words)
    return keywords


sensitive_keywords = get_sensitive_keywords()
