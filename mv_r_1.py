import pickle
import pandas as pd
from ast import literal_eval
import numpy as np
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


path = "archive/"
credits_df = pd.read_csv(path + "tmdb_5000_credits.csv")
movies_df = pd.read_csv(path + "tmdb_5000_movies.csv")

ps = PorterStemmer()

credits_df.columns = ['id','title', 'cast','crew']
movies_df = movies_df.merge(credits_df, on="id")

movies_df['title_x'] = [title.lower() for title in movies_df['title_x']]


features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(literal_eval)


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan


def get_overview(overview):
    out = ''
    try:
        for word in overview.split(' '):
            out += ps.stem(word)
            out += ' '
    except:
        return out
    return out

def get_cast(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names
    return []

def get_list(x):
    if isinstance(x, list):
        names = [ps.stem(i["name"]) for i in x]
        return names
    return []

movies_df["director"] = movies_df["crew"].apply(get_director)
movies_df["mod_overview"] = movies_df["overview"].apply(get_overview)
movies_df['cast'] = movies_df['cast'].apply(get_cast)
features = ["keywords", "genres"]
for feature in features:
    movies_df[feature] = movies_df[feature].apply(get_list)


def clean_data(row):
    if isinstance(row, list):
        return [str.lower(i) for i in row]
    else:
        if isinstance(row, str):
            return str.lower(row)
        else:
            return ""
features = ['cast', 'keywords', 'director', 'genres', 'mod_overview']

for feature in features:
    movies_df[feature] = movies_df[feature].apply(clean_data)


def create_soup(features):
    return (' '.join(features['keywords']) + ' ' + ' '.join(features['cast']) +
            ' ' + features['director'] + ' ' + ' '.join(features['genres'])
            +features['mod_overview'] + features['title_x'])

movies_df["soup"] = movies_df.apply(create_soup, axis=1)

# end of creating soup !!

"""

count_vectorizer = CountVectorizer()
count_matrix = count_vectorizer.fit_transform(movies_df["soup"])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
movies_df = movies_df.reset_index()

indices = pd.Series(movies_df.index, index=movies_df["title_x"]).drop_duplicates()


def get_sim_scores(title):
    count_vectorizer = CountVectorizer()
    data = list(movies_df["title_x"])
    data.append(title)
    count_matrix = count_vectorizer.fit_transform(data)
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    similarity_scores = list(enumerate(cosine_sim2[len(data) - 1]))
    return similarity_scores


def get_recommendations2(title):
    out = []
    similarity_scores = get_sim_scores(title)
    similarity_scores= sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    for c in range(1, 6):
        similarity_score= similarity_scores[c]
        movie_index = similarity_score[0]
        movie = movies_df["title_x"].iloc[movie_index]
        out.append(movie)
    return out



print(get_recommendations2("mystry island"))
"""
vectorizer = TfidfVectorizer(stop_words=('english'))
docs_tfidf = vectorizer.fit_transform(movies_df['soup'])
with open('docs_tfidf.txt', 'wb') as fh:
    pickle.dump(docs_tfidf, fh)

data = movies_df[['original_title', 'overview',
                  'release_date', 'vote_average']]

with open('data.txt', 'wb') as fh:
    pickle.dump(data, fh)

with open('vectorizer.txt', 'wb') as fh:
    pickle.dump(vectorizer, fh)



def get_sim(vectorizer, docs_tfidf, query):
    query_tfidf = vectorizer.transform([query])
    cosineSimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cosineSimilarities



def get_rec(query):
    out_q = ''
    for word in query.split(' '):
        out_q += ps.stem(word)
        out_q += ' '
    out = get_sim(vectorizer, docs_tfidf, out_q)
    indices = out.argsort()[-5:][::-1]
    for idx in indices:
        print(movies_df['title_x'][idx])


get_rec('bear attack')



