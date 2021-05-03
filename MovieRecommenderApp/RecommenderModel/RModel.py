import numpy as np
import pandas as pd
import urllib
import os

def extractName(companies):
    company_names=[]
    for c in companies:
        company_names.append(c['name'])

    return ' , '.join(company_names)


         
class Recommender:
    def __init__(self):
         
        compressed=np.load('./MovieRecommenderApp/RecommenderModel/input/cos_compressed.npz')
    
        self.__cosine_sim=compressed.f.arr_0
        
        self.__titles=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/titles.csv')
        self.__titles.columns=['id','title']
        self.__titles=self.__titles.set_index('id')
           
        self.__indices=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/indices.csv')
        self.__md=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/md.csv')
        self.__poster_df=pd.read_csv('./MovieRecommenderApp/RecommenderModel/input/MovieGenre.csv',encoding="ISO-8859-1")

        print('\n\n Recommender is ready...\n\n')

    def getRelatedMoviesDataframe(self,title):
        idx=self.__indices[self.__indices.title==title]['0'].values[0]
        sim_scores = list(enumerate(self.__cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[:61]

        movie_indices = [i[0] for i in sim_scores]
        
        return self.__titles.iloc[movie_indices]

    def getRelatedMovies(self,title):
        # title='Inception'
        relatedMoviesDf=self.getRelatedMoviesDataframe(title)
        MoviesLink=[]
        Movies=[]
        for movieName in relatedMoviesDf.title:
            movieDetails=self.__md[self.__md.title==movieName].sort_values(by='vote_count',ascending=False).iloc[0]
            movieImdbId=int(movieDetails.imdb_id[2:],10)
            try:
                posterLink=self.__poster_df[self.__poster_df.imdbId==movieImdbId].Poster.values[0]
            except:posterLink='' 
            MoviesLink.append(posterLink)
            Movies.append(movieName)

        temp=self.__md[self.__md.title==title].sort_values(by='vote_count',ascending=False).iloc[0]
        temp['mainMoviePoster']=MoviesLink[0]
        temp['genres']=' , '.join(eval(temp['genres']))
        temp['production_companies']=extractName(eval(temp['production_companies']))
        temp['spoken_languages']=extractName(eval(temp['spoken_languages']))
        temp['budget']=str(temp['budget'])+' USD '
        
        MoviesLink[0]=temp.to_json()
        
        return Movies,MoviesLink

# rec=Recommender()