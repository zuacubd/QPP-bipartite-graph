import os
import sys

from reader.reader import get_topics, get_qrels, get_topics_docs_ltr_features
from tools.normalization import *


def prepare_dataset(topics_path, query_doc_features_path, qrels_file_path, ltr_train_file_path, ltr_test_file_path):

        topics, topic_ids = get_topics(topics_path)
        topics_docid_rel = get_qrels(qrels_file_path)
        topics_docs, topics_docid_features = get_topics_docs_ltr_features(query_doc_features_path)

        print ("total topics: ", topic_ids)

        #training features
        with open(ltr_train_file_path, 'w') as fw:

            for topic_id in topic_ids:
                docid_rel = topics_docid_rel.get(topic_id)
                docid_features = topics_docid_features.get(topic_id)

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
            for topic_id in topic_ids:
                docid_rel = topics_docid_rel.get(topic_id)
                docid_features = topics_docid_features.get(topic_id)

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
