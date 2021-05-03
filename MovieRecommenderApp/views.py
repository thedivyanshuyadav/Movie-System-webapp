from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import never_cache

from MovieRecommenderApp.RecommenderModel.RModel import Recommender
import json
import numpy as np
import pandas as pd

from django.http import JsonResponse


rec=Recommender()  

@never_cache
def index(request):
    global rec 
    allMovies =rec._Recommender__titles.title.tolist()
    return render(request,'MovieRecommenderApp/index.html',context={"allMovies":json.dumps(allMovies)})
 
               
# Create your views here.

@never_cache  
def movieInput(request):
    global rec
    if(request.method=="POST"):
        input_movie=request.POST['movie_name']
        if(input_movie=="NO RECORD"):
            print('\n-----\nNO RECORD\n--------\n')

            return JsonResponse({'status':'ok'})
        
        relDf=pd.DataFrame(rec.getRelatedMovies(input_movie)).T
        # RelatedMovies,PosterLink=rec.getRelatedMovies(input_movie)
        relDf=relDf.replace(np.nan,"")
        RelatedMovies,PosterLink=relDf.iloc[:,0].to_list(),relDf.iloc[:,1].to_list()
        
        response_data=dict(zip(RelatedMovies,PosterLink))
        response_data[input_movie]=PosterLink[0]
            
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
        
 

