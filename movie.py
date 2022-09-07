import pickle
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer


ps = PorterStemmer()

data_path = 'data/'
pickle_1 = open(data_path + "docs_tfidf.txt", "rb")
pickle_2 = open(data_path + 'data.txt', 'rb')
pickle_3 = open(data_path + 'vectorizer.txt', 'rb')
docs_tfidf = pickle.load(pickle_1)
data = pickle.load(pickle_2)
vectorizer = pickle.load(pickle_3)


def get_sim(vectorizer, docs_tfidf, query):
    query_tfidf = vectorizer.transform([query])
    cosinesimilarities = cosine_similarity(query_tfidf, docs_tfidf).flatten()
    return cosinesimilarities


def get_rec(query):
    out_q = ''
    for word in query.split(' '):
        out_q += ps.stem(word)
        out_q += ' '
    out = get_sim(vectorizer, docs_tfidf, out_q)
    indices = out.argsort()[-5:][::-1]
    out = []
    for idx in indices:
        out_data = {}
        out_data['title'] = data['original_title'][idx]
        out_data['overview'] = data['overview'][idx]
        out_data['rating'] = data['vote_average'][idx]
        out_data['release_date'] = data['release_date'][idx]
        out.append(out_data)
    return out



if __name__ == '__main__':
    print(get_rec('bear attacks'))

