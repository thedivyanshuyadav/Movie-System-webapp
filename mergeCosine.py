import numpy as np
path="MovieRecommenderApp/RecommenderModel/input/cosine/"

cos1=np.load(path+'cos1.npy')
cos2=np.load(path+'cos2.npy')
cos3=np.load(path+'cos3.npy')
cos4=np.load(path+'cos4.npy')
cos5=np.load(path+'cos5.npy')
cos6=np.load(path+'cos6.npy')
cos7=np.load(path+'cos7.npy')
cos8=np.load(path+'cos8.npy')
cos9=np.load(path+'cos9.npy')

cosine_sim=np.concatenate((cos1, cos2,cos3,cos4,cos5,cos6,cos7,cos8,cos9))
print(cosine_sim.shape)


np.save("/app/MovieRecommenderApp/RecommenderModel/input/cosine_sim.npy",cosine_sim)
