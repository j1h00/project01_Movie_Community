from pprint import pprint
import numpy as np
import pandas as pd
import json

def jaccard_similarity(s1, s2):
    if len(s1|s2) == 0:
        return 0

    return len(s1&s2)/len(s1|s2)


def main():
    with open('./z_data_api_crawl/movie_rec.json','r', encoding='UTF8') as f:
        data = json.loads(f.read())

    movie_df = pd.json_normalize(data)
    movie_df.genres = movie_df.genres.apply(set)
    movie_df.keywords = movie_df.keywords.apply(set)

    result = []
    idx = 1
    for input_id in movie_df.id:
        input_meta = movie_df.loc[movie_df['id'] == input_id].iloc[0]

        input_set = input_meta.genres | input_meta.keywords

        result2 = []
        for now_id in movie_df.id:
            if now_id == input_id:
                continue

            this_meta = movie_df.loc[movie_df['id'] == now_id].iloc[ 0]
            this_set = this_meta.genres | this_meta.keywords


            jaccard = jaccard_similarity(this_set, input_set)

            result2.append({
                "model": "movies.similarity",
                "pk": idx,
                "fields": {
                    'source': input_id,
                    'target': now_id,
                    'similarity': jaccard
                }
            })
            idx += 1

        result2.sort(key= lambda x: x['fields']['similarity'], reverse=True)
        result.extend(result2[:10])
        
    with open('similarity.json', 'w', encoding='UTF-8') as outfile:
        json.dump(result, outfile, indent=4, ensure_ascii = False)

main()