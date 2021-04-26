import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

def get_characters_det(a):
    a=eval(a)
    det=[]
    for d in a:
        det.append(d['name'])
    return ' '.join(det)

def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]

md=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/the-movies-dataset/movies_metadata.csv')
md.genres=md.genres.fillna('[]').apply(eval).apply(lambda a:[i['name'] for i in a])
md = md.drop([19730, 29503, 35587])
md.id=md.id.apply(int)

links=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/the-movies-dataset/links_small.csv')
links=links[links['tmdbId'].notnull()]['tmdbId'].apply(int)


df=md[md['id'].isin(links)]
df['tagline']=df['tagline'].fillna('')
df['description']=df['overview']+df['tagline']
df['description']=df['description'].fillna('')
df['basis']=df['adult']+' '+df['genres'].apply(lambda a:' '.join(a))+' '+df['original_language']


credits = pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/the-movies-dataset/credits.csv')
keywords = pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/the-movies-dataset/keywords.csv')

keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')

credits=credits[credits['id'].isin(links)]
keywords=keywords[keywords['id'].isin(links)]


df=df.merge(credits,on='id')
df=df.merge(keywords,on='id')

df.cast=df.cast.apply(get_characters_det)
df['director']=df.crew.apply(lambda a:' '.join([i['name'] for i in eval(a) if(i['job']=='Director')]))
df['keyw']=df.keywords.apply(lambda a :' '.join([i['name'] for i in eval(a)])).apply(stemmer.stem)

df.basis.fillna('',inplace=True)
df.cast.fillna('',inplace=True)


df['soup']=df.director+' '+df['basis']+' '+df.keyw+' '+df['cast']


#STEMMING
df['soup']=df['soup'].apply(stemmer.stem)
df['soup']=df['description']+' '+df['basis']+' '+df['director']
df['soup'].fillna('',inplace=True)
df['soup']=df['soup'].apply(stemmer.stem)


#VECTORIZOR
count=CountVectorizer(analyzer='word',ngram_range=(1,2),min_df=0,stop_words='english')
count_matrix=count.fit_transform(df['soup'])


cosine_sim=cosine_similarity(count_matrix,count_matrix)

df=df.reset_index()
titles=df['title']
indices=pd.Series(df.index,index=df.title)




# np.save('cosine_sim',cosine_sim)

poster_df=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/movie-genre-from-its-poster/MovieGenre.csv',encoding="ISO-8859-1")

import urllib
from skimage import io

movieName='Lucy'
movieDetails=md[md.title==movieName].sort_values(by='vote_count',ascending=False).iloc[0]
movieImdbId=eval(movieDetails.imdb_id[2:])
posterLink=poster_df[poster_df.imdbId==movieImdbId].Poster.values[0]
f=io.imread(posterLink)
plt.imshow(f)
plt.show()



