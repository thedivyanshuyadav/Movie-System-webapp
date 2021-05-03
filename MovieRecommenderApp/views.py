from django.shortcuts import render
from django.http import HttpResponse


from MovieRecommenderApp.RecommenderModel.RModel import Recommender
from django.shortcuts import redirect
import json
import numpy as np
import pandas as pd
from django import db


rec=Recommender()  

def index(request):
    global rec 
    allMovies =rec._Recommender__titles.title.tolist()
    return render(request,'MovieRecommenderApp/index.html',context={"allMovies":json.dumps(allMovies)})
 
               
# Create your views here.
def movieInput(request):
    global rec
    if(request.method=="POST"):
        input_movie=request.POST['movie_name']
        relDf=pd.DataFrame(rec.getRelatedMovies(input_movie)).T
        # RelatedMovies,PosterLink=rec.getRelatedMovies(input_movie)
        relDf=relDf.replace(np.nan,"")
        RelatedMovies,PosterLink=relDf.iloc[:,0].to_list(),relDf.iloc[:,1].to_list()
         
        response_data=dict(zip(RelatedMovies,PosterLink))
        response_data[input_movie]=PosterLink[0]
        db.reset_queries()
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
 
  
