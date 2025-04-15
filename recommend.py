import map_classification as mc


def _rating_scale(rating):
    if rating == 1:
        return 1.0
    elif rating == 2:
        return 0.7
    elif rating == 3:
        return 0.2
    return 0


def recommend_player(player_id, class_id, max_rank):
    mc.load_model(class_id)
    maps = mc.get_maps()
    tts = mc.get_player_tts(player_id, class_id, max_rank)

    if len(tts) == 0:
        return None

    # get recommendations and apply weight
    recommendations = {}
    for time in tts:
        similar = mc.get_similar(time["map_name"])
        for s in similar:
            if s["name"] in recommendations:
                recommendations[s["name"]] += s["value"]
            else:
                recommendations[s["name"]] = s["value"]

    class_rating = "srating" if class_id == 3 else "drating"

    recommendations_list = []
    for k, v in recommendations.items():
        map = [x for x in maps if x["name"] == k][0]
        recommendations_list.append({"name": k, "value": v * _rating_scale(map[class_rating])})
    recommendations_list.sort(key=lambda r: -r["value"])
    return recommendations_list


def recommend_maps(map_name, class_id):
    mc.load_model(class_id)
    similar = mc.get_similar(map_name)
    return similar
