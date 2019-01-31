import os
import sys

from loader.topics import *
from loader.features import *
from loader.qrels import *
from tools.normalization import *


def prepare_dataset(topics_path, query_doc_features_path, qrels_file_path, ltr_train_file_path, ltr_test_file_path):

        topics, query_ids = get_topics(topics_path)
        queryid_docid_rel = get_qrels(qrels_file_path)
        queryid_docid_features = get_query_doc_features(query_doc_features_path)

        #query_ids = sorted(list(queryid_docid_features.keys()), key=int)
        #query_ids = sorted(topics.keys(), key=str.lower)
        print ("total topics: ", query_ids)

        #training features
        with open(ltr_train_file_path, 'w') as fw:

            for query_id in query_ids:
                #query_id = query_ids[qdx]

                docid_rel = queryid_docid_rel.get(query_id)
                docid_features = queryid_docid_features.get(query_id)

                if docid_rel is None:
                    continue

                for doc_id in docid_features:

                    rel = docid_rel.get(doc_id)
                    raw_features = docid_features.get(doc_id)
                    #print (doc_id)
                    #print (raw_features)
                    features = get_l2_normalize(raw_features)

                    if rel is None:
                        continue

                    line = str(rel) + " " + "qid:"+str(query_id)

                    feature_id = 1
                    for idx in range(0, len(features)):

                        feature = features[idx]
                        line = line + " " + str(feature_id) + ":"+str(feature)
                        feature_id = feature_id + 1

                    line = line + " # "+ str(doc_id)
                    fw.write(line+'\n')
            fw.close()

        #validation features
        with open(ltr_test_file_path, 'w') as fw:
            for query_id in query_ids:
                docid_rel = queryid_docid_rel.get(query_id)
                docid_features = queryid_docid_features.get(query_id)

                if docid_rel is None:
                    docid_rel = {}

                for doc_id in docid_features:

                    rel = docid_rel.get(doc_id)
                    raw_features = docid_features.get(doc_id)
                    #print (doc_id)
                    #print (raw_features)
                    features = get_l2_normalize(raw_features)

                    if rel is None:
                        rel = 0 #dummy relevance for unjudged test data
                    if int(rel) < 0:
                        rel = 0

                    line = str(rel) + " " + "qid:"+str(query_id)

                    feature_id = 1
                    for idx in range(0, len(features)):

                        feature = features[idx]
                        line = line + " " + str(feature_id) + ":"+str(feature)
                        feature_id = feature_id + 1

                    line = line + " # "+ str(doc_id)
                    fw.write(line+'\n')
            fw.close()

def main():
        topics_path = sys.argv[1]
        query_doc_features_path = sys.argv[2]
        rel_judgment_path = sys.argv[3]
        train_path = sys.argv[4]
        test_path = sys.argv[5]

        prepare_dataset(topics_path, query_doc_features_path, rel_judgment_path, train_path, test_path)

if __name__ == '__main__':
    main()
