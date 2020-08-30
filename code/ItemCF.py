'''
Descripttion: 
version: 
Author: hebicheng
Date: 2020-08-27 16:52:20
LastEditors: hebicheng
LastEditTime: 2020-08-31 07:48:18
'''

from Utils import LoadData
from math import sqrt

class ItemCF():
    def __init__(self):
        self.prefs = LoadData('../data/data.json') 

    # 将Item作为中心
    def transformPrefs(self):
        result={}
        for person in self.prefs:
            for item in self.prefs[person]:
                result.setdefault(item,{})
                result[item][person] = self.prefs[person][item]
        return result

    # 欧式距离
    def sim_distance(self,prefs,Item1,Item2):
        si = {}
        for item in prefs[Item1]:
            if item in prefs[Item2]:
                si[item] = 1 
        if len(si) == 0:
            return 0
        #计算所有距离的和（差值的平方和）
        sum_of_squares = sum([pow(prefs[Item1][item]-prefs[Item2][item],2)
                            for item in prefs[Item1] if item in prefs[Item2]])
        return 1 / (1 + sqrt(sum_of_squares))#分子上加1,是为了防止分母为0

        
    # 选出最相近的电影
    def topMatches(self,prefs,item,n=5,similarity=sim_distance):
        #求参数用户和其他所有用户的相似系数
        scores=[(similarity(self,prefs,item,other),other) for other in prefs if other!=item]
        #排序
        scores.sort()
        scores.reverse()
        return scores[0:n]

    
    #基于物品的协同过滤
    def calculateSimilarItems(self,n=10):
        #与这些电影最为相近的其他所有电影
        result = {}
        #以物品为中心对偏好矩阵实施倒置处理
        itemPrefs = self.transformPrefs()
        c = 0
        for item in itemPrefs:
            scores = self.topMatches(itemPrefs,item)
            result[item] = scores
        return result
    
    def getRecommendedItems(self,itemMatch,user):
        userRatings = self.prefs[user]
        scores ={}
        totalSim={}
        #循环遍历与当前物品相近的物品
        for (item, rating) in userRatings.items():
            for (similarity, item2) in itemMatch[item]:
                # 如果该用户已经对当前物品做出过评价，就忽略
                if item2 in userRatings: continue
                # 评价值与相似度的加权之和
                scores.setdefault(item2, 0)
                scores[item2] += similarity * rating
                # 全部相似度之和
                totalSim.setdefault(item2, 0)
                totalSim[item2] += similarity
            # 将每个和值除以加权和，求平均值
        rankings = [(score / totalSim[item], item) for item, score in scores.items()]
        # 排序
        rankings.sort()
        rankings.reverse()
        return rankings

if __name__ == "__main__":
    ItemCF = ItemCF()
    itemMatch = ItemCF.calculateSimilarItems()
    print(ItemCF.getRecommendedItems(itemMatch, 'Toby'))
    # print(ItemCF.transformPrefs())