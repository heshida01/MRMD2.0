
"""
部分代码引用作者：刀刀流
PageRank算法--从原理到实现
源地址：https://www.cnblogs.com/rubinorth/p/5799848.html
"""
from collections import OrderedDict

import itertools
from pygraph.classes.digraph import digraph
from feature_selection import ANOVA, mRMD
import feature_selection.mRMD
import feature_selection.mrmr
import feature_selection.mic
import feature_selection.ANOVA
import  feature_selection.lasso
import  pandas as pd
import  feature_selection.chisquare
import feature_selection.recursive_feature_elimination
import networkx as nx
from  feature_rank.trustrank import trustrank
from feature_rank.leaderank import  leaderrank


class MapReduce:
    __doc__ = '''提供map_reduce功能'''
    @staticmethod
    def map_reduce(i, mapper, reducer):

        intermediate = []  # 存放所有的(intermediate_key, intermediate_value)
        for (key, value) in i.items():
            intermediate.extend(mapper(key, value))

        groups = {}
        for key, group in itertools.groupby(sorted(intermediate, key=lambda im: im[0]), key=lambda x: x[0]):

            groups[key] = [y for x, y in group]


        return [reducer(intermediate_key, groups[intermediate_key]) for intermediate_key in groups]

class PRMapReduce:
    __doc__ = '''计算PR值'''

    def __init__(self, dg,logger):
        self.damping_factor = 0.85  # 阻尼系数,即α
        self.max_iterations = 100  # 最大迭代次数
        self.min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
        self.num_of_pages = len(dg.nodes())  # 总网页数
        self.logger = logger

        self.graph = {}
        for node in dg.nodes():
            self.graph[node] = [1.0 / self.num_of_pages, len(dg.neighbors(node)), dg.neighbors(node)]

    def ip_mapper(self, input_key, input_value):

        if input_value[1] == 0:
            return [(1, input_value[0])]
        else:
            return []

    def ip_reducer(self, input_key, input_value_list):

        return sum(input_value_list)

    def pr_mapper(self, input_key, input_value):

        p=[(input_key, 0.0)] + [(out_link, input_value[0] / input_value[1]) for out_link in input_value[2]]
        return p

    def pr_reducer_inter(self, intermediate_key, intermediate_value_list, dp):

        return (intermediate_key,
                self.damping_factor * sum(intermediate_value_list) +
                self.damping_factor * dp / self.num_of_pages +
                (1.0 - self.damping_factor) / self.num_of_pages)

    def page_rank(self):
        list = []
        iteration = 100  # 迭代次数
        change = 1  # 记录每轮迭代后的PR值变化情况，初始值为1保证至少有一次迭代
        self.logger.info('rank start ...')
        while change > self.min_delta:
            #print("Iteration: " + str(iteration))
            #print('.',end='')

            dangling_list = MapReduce.map_reduce(self.graph, self.ip_mapper, self.ip_reducer)
            if dangling_list:
                dp = dangling_list[0]
            else:
                dp = 0

            new_pr = MapReduce.map_reduce(self.graph, self.pr_mapper, lambda x, y: self.pr_reducer_inter(x, y, dp))
            change = sum([abs(new_pr[i][1] - self.graph[new_pr[i][0]][0]) for i in range(self.num_of_pages)])
            list.append(change)
            for i in range(self.num_of_pages):
                self.graph[new_pr[i][0]][0] = new_pr[i][1]
            iteration += 1

        return self.graph
def init(mrmd,ANOVA,mrmr,mic,lasso,chi2_,ref_):

    t=[(x+1,x) for x in range (len(mrmd)-1)]
    t1 = [(x + 1, x) for x in range(len(ANOVA) - 1)]
    t2 = [(x + 1, x) for x in range(len(mrmr) - 1)]


    mrmd_link=[(mrmd[x[0]],mrmd[x[1]])for x in t]
    ANOVA_link = [(ANOVA[x[0]], ANOVA[x[1]]) for x in t1]
    mrmr_link = [(mrmr[x[0]], mrmr[x[1]]) for x in t2]
    mic_link = [(mic[x[0]], mic[x[1]]) for x in t]
    t = [(x + 1, x) for x in range(len(lasso) - 1)]
    lasso_link = [(lasso[x[0]], lasso[x[1]]) for x in t]

    t = [(x + 1, x) for x in range(len(mrmd) - 1)]
    #lasso2_link = [(lasso2[x[0]], lasso2[x[1]]) for x in t]
    chi2_link = [(chi2_[x[0]], chi2_[x[1]]) for x in t]
    ref_link = [(ref_[x[0]], ref_[x[1]]) for x in t]

    link_node=mrmd_link
    link_node.extend(ANOVA_link)
    link_node.extend(mrmr_link)
    link_node.extend(mic_link)
    link_node.extend(lasso_link)
    link_node.extend(chi2_link)
    link_node.extend(ref_link)
    #link_node.extend(lasso2_link)

    link_node = list(OrderedDict.fromkeys(link_node))  #有序去重
    return link_node

def feature_rank(file,logger,mrmr_length,rank_method):
    if rank_method.lower()=='pagerank':
        ANOVA_data = feature_selection.ANOVA.run(file,logger)
        mic_data = feature_selection.mic.run(file,logger)
        mrmd_data = feature_selection.mRMD.run(file,logger)
        mrmr_data = feature_selection.mrmr.run(file,logger)
        lasso_data = feature_selection.lasso.run(file,logger)
        #lasso2_data = feature_selection.lasso2.run(file,logger)
        chi2_data = feature_selection.chisquare.run(file,logger)
        ref_data = feature_selection.recursive_feature_elimination.run(file,logger)
        edge=init(mrmd_data,ANOVA_data,mrmr_data,mic_data,lasso_data,chi2_data,ref_data)

        #edge = init(mrmd_data, ANOVA_data, mic_data)
        features_name = pd.read_csv(file).columns[1:]
        dg = digraph()
        dg.add_nodes(features_name)

        for e in edge:

            dg.add_edge(e)

        pr = PRMapReduce(dg,logger)
        page_ranks = pr.page_rank()

        logger.info("The final  rank is")
        result=[]
        for key, value in page_ranks.items():
            #print(key + " : ", value[0])
            result.append((key,value[0]))

        result = sorted(result, key=lambda x: x[1], reverse=True)

        features={}
        i=1
        for x in features_name:
            features[x]=i
            i+=1
        features_sorted=[]
        for key,value in result:
            value='{:0.4f}'.format(value)
            logger.info(str(key)+' : '+str(value))
            features_sorted.append((key,value))
        #print(features_sorted)
        #print(features)
        logger.info('feature_rank end')
        return features,features_sorted
    ANOVA_data = feature_selection.ANOVA.run(file,logger)
    MIC = feature_selection.mic.run(file,logger)
    mrmd = feature_selection.mRMD.run(file,logger)
    mrmr= feature_selection.mrmr.run(file,logger)
    lasso = feature_selection.lasso.run(file, logger)
    chi2 = feature_selection.chisquare.run(file,logger)

    ref1= feature_selection.recursive_feature_elimination.run(file,logger)


    def node2edge(*nodeOrder_des):  #特征 大-》小
        edges=[]
        for onetype_featureSelection in nodeOrder_des:
            edges +=[(onetype_featureSelection[i+1],onetype_featureSelection[i]) for  i,x in enumerate(onetype_featureSelection) if i<len(onetype_featureSelection)-1]
        ###去重
        #edges = [elem for elem in edges if elem not in edges]
        print(edges)
        # edges = sorted(set(edges), key=lambda x: edges.index(x))
        return  edges

    edges=node2edge(mrmd,ANOVA_data,MIC,mrmr,lasso,chi2,ref1)
    G = nx.DiGraph()
    G.add_edges_from(edges)

    features = {}
    i = 1
    dataset = pd.read_csv(file, engine='python').dropna(axis=1)
    features_name = dataset.columns.values.tolist()[1:]
    for x in features_name:
        features[x] = i
        i += 1
    features_rc = features.copy()

    rankresultWithsocre = webpage_rank(features, graph=G,method=rank_method,edges=edges)
    print(rankresultWithsocre)
    #print("rankresultWithsocre",rankresultWithsocre)
    logger.info("The final  rank is")
    for value in rankresultWithsocre:
        logger.info(str(value[0])+ " : "+str(value[1]))

    #print('features',features_rc)
    logger.info('feature_rank end')
    return features_rc,rankresultWithsocre
def webpage_rank(features,graph,method,edges):

    if method.lower() == "hits_a":
        h, a = nx.hits(graph)
        return sorted(a.items(), key=lambda x: x[1], reverse=True)
    elif method.lower() == "hits_h":
        h, a = nx.hits(graph)
        return sorted(h.items(), key=lambda x: x[1], reverse=True)
    elif method.lower() == "leaderrank":
        lr = leaderrank(graph)
        #print("leaderrank+++++++++++",lr.items())
        return sorted(lr.items(), key=lambda item: item[1], reverse=True)
    else:   ###trustrank
        tr = trustrank(features,edges)
        return sorted(tr.items(), key=lambda item: item[1], reverse=True)
if __name__ == '__main__':
    feature_rank('')





