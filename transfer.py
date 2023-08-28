# %%
import json
import urllib.request

url = 'http://127.0.0.1:8765'
origin_deck = "考研词汇5500::1 Recite"
target_deck = "2024红宝书考研词汇（必考词+基础词+超纲词）"
origin_word_field_name = "单词"
target_word_field_name = "正面"


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request(url, requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

# %%
# get cards ID
origin_cards = invoke("findCards", query=f"\"deck:{origin_deck}\"")

# %%
# filter learned cards
card_infos = invoke("cardsInfo", cards=origin_cards)
del origin_cards
card_infos = [info for info in card_infos if info["type"] > 0 ]

# %%
# for key in card_infos[0]:
#     print(key, end=" ")

# %%
# find the same cards in target deck
for i, info in enumerate(card_infos):
    origin_id = info['cardId']
    word = info["fields"][origin_word_field_name]["value"]
    ids = invoke("findCards", query=f"\"deck:{target_deck}\" \"{target_word_field_name}:{word}\"")
    if(len(ids) > 0):
        if (len(ids) > 1): 
            print(f"Warning: find duplicated cards in target deck: [{word}]. Skip Now.")
            continue
        
        target_id = ids[0]
        new_infos = invoke("cardsInfo", cards=[target_id])

        assert(len(new_infos) == 1 and new_infos[0]["fields"][target_word_field_name]["value"] == word)

        print(f"[{i + 1}/{len(card_infos)}] Start Merge word [{word}] Origin ID {origin_id} ---> Target ID {target_id}")

        # update card
        print(f"- Updating word: {word}")
        __type_ = info["type"]
        __queue = info["queue"]
        __due = info["due"] # no way to calculate due time delta now
        __ivl = info["interval"]
        __factor = info["factor"]
        __reps = info["reps"]
        __lapses = info["lapses"]
        __left = info["left"]
        sc_result = invoke("setSpecificValueOfCard", 
                        card=target_id, 
                        keys=["type", "queue", "due", "ivl", "factor", "reps", "lapses", "left", "usn"],
                        newValues=[__type_, __queue, __due, __ivl, __factor, __reps, __lapses, __left, -1], warning_check=True)
        assert(sc_result[0])
        
        # update related review records
        print(f"- Updating reviews records: {word}")
        reviews = invoke("getReviewsOfCards", cards=[origin_id])
        reviews = reviews[f"{origin_id}"]

        print(f"- Find {len(reviews)} reviews records of CardID {origin_id}")
        new_reviews = []
        # build new reviews
        for review in reviews:
            __reviewTime = review['id'] + 1
            __cardID = target_id
            __usn = -1
            __buttonPressed = review['ease']
            __newInterval = review['ivl']
            __previousInterval = review['lastIvl']
            __newFactor = review['factor']
            __reviewDuration = review['time']
            __reviewType = review['type']
            new_reviews.append([__reviewTime, __cardID, __usn, __buttonPressed, __newInterval, __previousInterval, __newFactor, __reviewDuration, __reviewType])

        try:
            insert_result = invoke("insertReviews", reviews=new_reviews)
        except Exception as e:
            print("Note: Record already exists. Skip it.")

        print(f"- Success to merge word [{word}]!")
        # break
    else:
        print(f"Note: Cannot find word {word} in target deck.")

print("*** Done")
