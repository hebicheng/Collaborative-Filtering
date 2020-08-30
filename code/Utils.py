'''
Descripttion: 
version: 
Author: hebicheng
Date: 2020-08-26 16:55:45
LastEditors: hebicheng
LastEditTime: 2020-08-31 07:48:49
'''
import json

def LoadData(path):
    with open(path, 'r',  encoding='utf-8') as f:
        data = json.load(f) 
    return data

if __name__ == "__main__":
    print(LoadData('../data/data.json')) 
