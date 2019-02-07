import argparse
import os
import sys
import pyndri
import math
import numpy as np

from reader.reader import *
from algorithm.bipartite_graph import *
from tools.descriptive_stats import *
from tools.sorting import *

def get_U0(docids, docids_rankscore):
        m = len(docids)
        U = np.zeros((m), 1, dtype=np.float64)
        for i range(0, len(docids)):
            docid = docids[i]
            rankscore = docids_rankscore.get(docid)
            rank = rankscore[0]
            score = rankscore[1]

            weight = 1.0/math.sqrt(rank + 2.0)
            U[i,1]= weight

        return U


def get_V0(docids, features_id, topics_docids_features):
        n = len(features_id)
        V = np.zeros((n), 1, dtype=np.float64)
        weights = [1.0/n for i in range(0, n)]
        for f in range(0, len(features_id)):
            V[f, 1] = weights[f]

        return V


def get_UV_matrix(U0, V0, docids, features_id, docids_features):
        m = U0.shape[0]
        n = V0.shape[0]
        M = np.zeros((m, n), dtype=np.float64)

        for f in range(0, len(features_id)):

            docids_feature = {}
            for d in range(0, len(docids)):
                docid = docids[d]
                features = docids_features.get(docid)
                feature = features[f]
                docids_feature[docid] = feature

            ranked_docids, ranked_docids_score = get_descending(docids_feature)
            for r in range(0, len(ranked_docids)):
                rdocid = ranked_docids[r]
                index = docids.index(rdocid)
                weight = 1.0/math.sqrt(2.0 + r)
                M[index, f] = weight

        return M


def get_predictors(docids_imp):
        '''
        Computing QPP predictors for the re-estimated documents' score
        '''
        qpp_mean = np.mean(docids_imp)
        qpp_std = np.std(docids_imp)
        qpp_var = np.var(docids_imp)

        return [qpp_mean, qpp_std, qpp_var]


def get_BGP(topics_id_title, topics_id, topics_docids_rankscore, topics_docids, features_id, topics_docids_features):
        '''
        Computing bipartite graph based QPP features using LETOR
        '''
        l1 = 0.5
        l2 = 0.5

        topics_bgp = {}
        for topic_id in topics_id:
            docids = topics_docids.get(topic_id)
            docids_rankscore = topics_doicds_rankscore.get(topic_id)
            docids_features = topics_docids_features.get(topic_id)

            #prepare the format for bipartite graph based learning
            U0 = get_U0(docids, docids_rankscore) #from rank or retrieval score
            V0 = get_V0(docids, features_id, topics_docids_features) #Uniformly or learned
            M0 = get_UV_matrix(U0, V0, docids, features_id, docids_features)
            docids_imp, features_imp = getUV_ranking(l1, l2, U0, V0, M0)
            predictors = get_predictors(docids_imp)
            topics_bgp[topic_id] = predictors

        return topics_bgp


def write_features(topics_id, topics_bqp, features_file_path):
        '''
        Write the query performan predictor or features
        '''
        with open(features_file_path, 'w') as writer:

            writer.write('query_id\tqpp_mean\tqpp_std\tqpp_var\n')
            line =''
            for topic_id in topics_id:
                writer.write(topic_id)

                predictors = topics_bqp.get(topic_id)
                for predictor in predictors:
                    writer.write('\t')
                    writer.write(str(predictor))
                writer.write('\n')


parser = argparse.ArgumentParser(description='A tool used to compute QPP using biparite graph based ranking')
parser.add_argument('-topic-path', '--topic_file_path', nargs='?', type=str, required=True, help='The topics file path')
parser.add_argument('-k', '--topk', nargs='?', type=int, required=True, help='Number of documents retrieved for each query')
parser.add_argument('-index','--index_dir', nargs='?', type=str, required=True, help='Indri Index directory')
parser.add_argument('-ltr-path', '--ltr_features_path', nargs='?', type=str, required=True, help='The LTR features path')
parser.add_argument('-result-path', '--result_path', nargs='?', type=str, required=True, help='The result path')
parser.add_argument('-predictor-path', '--predictor_path', nargs='?', type=str, required=True, help='Predictor path')


topics_path=None
topk=0
index_dir=None
ltr_features_path=None
result_path=None
predictor_path=None

def parse_args():
        '''
        Function used to parse the arguments provided to the script
        '''
        global topics_path
        global topk
        global index_dir
        global ltr_features_path
        global result_path
        global predictor_path

        # Parsing the args
        args = parser.parse_args()

        # Retrieving the args
        topics_path = args.topic_file_path
        print(topics_file_path)
        topk = args.topk
        print(topk)

        index_dir = args.index_dir
        print(index_dir)

        ltr_features_path = args.ltr_features_path
        print(ltr_features_path)

        result_path = args.result_path
        print(result_path)

        predictor_path = args.predictor_path
        print(predictor_path)


print("Starting ... ")
parse_args()

print("Loading topics file")
topics_id_title, topics_id = get_topics(topics_path)
print("Done.")

print("Loading results file")
topics_docid_rankscore = get_run_result(result_path)
print("Done")

print ("Loading LTR features file")
topics_docids, features_id, topics_docids_features = get_topics_docs_ltr_features(ltr_features_path)
print("Done")

print ("Computing BGP ...")
topics_bgp = get_BGP(topics_id_title, topics_id, topics_docid_rankscore, topics_docids, features_id, topics_docids_features)
print ("Done")

print("Writing features to file ....")
write_features(topics_id, topics_bgp, predictor_path)
print("Done")
