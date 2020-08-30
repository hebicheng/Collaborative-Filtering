'''
Descripttion: 
version: 
Author: hebicheng
Date: 2020-08-26 16:55:45
LastEditors: hebicheng
LastEditTime: 2020-08-31 07:49:09
'''

from Utils import LoadData 
from math import sqrt
class UserCF():
    def __init__(self):
        self.prefs = LoadData('../data/data.json')

    # 欧式距离
    def sim_distance(self,person1,person2):
        # 创建一个空集合用来存储用户1和用户2都有的电影的评分
        si = {}
        for item in self.prefs[person1]:
            if item in self.prefs[person2]:
                si[item] = 1 
        #如果两个人没有共同的评分，则返回0
        if len(si) == 0:
            return 0
        #计算所有距离的和（差值的平方和）
        sum_of_squares = sum([pow(self.prefs[person1][item]-self.prefs[person2][item],2)
                            for item in self.prefs[person1] if item in self.prefs[person2]])
        return 1 / (1 + sqrt(sum_of_squares))#分子上加1,是为了防止分母为0

    # 皮尔逊相关度
    def sim_pearson(self,p1,p2):
        si={}
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item]=1

        n=len(si) 
        if n==0:
            return 1

        #所有偏好求和
        sum1=sum([self.prefs[p1][it] for it in si])
        sum2=sum([self.prefs[p2][it] for it in si])

        #所有偏好求平方和
        sum1Sq=sum([pow(self.prefs[p1][it],2) for it in si])
        sum2Sq=sum([pow(self.prefs[p2][it],2) for it in si])

        #乘积之和
        pSum=sum([self.prefs[p1][it]*self.prefs[p2][it] for it in si])

        #计算皮尔逊相关系数
        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))

        if den==0:
            return 0
            
        r=num/den
    
        return r

    # Tanimoto相似度
    def sim_tanimoto(self, p1, p2):
        si = {}
        for item in self.prefs[p1]:
            if item in self.prefs[p2]:
                si[item] = 1
        length = len(si)
        if length == 0: return 0
        t = length/(len(self.prefs[p1]) + len(self.prefs[p2]) - length) 
        
        return t

    # 选出品位最近的TopN用户
    def topMatches(self,person,n=5,similarity=sim_pearson):
        #求参数用户和其他所有用户的相似系数
        scores=[(similarity(self.prefs,person,other),other) for other in self.prefs if other!=person]
        #排序
        scores.sort()
        scores.reverse()
        return scores[0:n]

    # 利用所有他人评价值的加权平均，为某人提供建议
    def getRecommendations(self,person,similarity=sim_pearson):
        totals={}
        simSums={}
        for other in self.prefs:
            if other==person:continue
            sim=similarity(self, person,other)

            #忽略评价值为零或者小于零的情况
            if sim<=0:continue

            for item in self.prefs[other]:
                #只对自己没有看过的电影评价
                if item not in self.prefs[person] or self.prefs[person][item]==0:
                    #相似度*评价值
                    totals.setdefault(item,0)
                    totals[item]+=self.prefs[other][item]*sim

                    #相似度之和
                    simSums.setdefault(item,0)
                    simSums[item]+=sim

        #创建一个列表，列表里面是person没有看过的电影和评分
        rankings=[(total/simSums[item],item) for item,total in totals.items()]

        #排序
        rankings.sort()
        rankings.reverse()
        return rankings

if __name__ == "__main__":
    
    UserCF = UserCF()
    print(UserCF.getRecommendations('Michael Phillips'))