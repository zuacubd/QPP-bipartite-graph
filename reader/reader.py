import os
import sys
import pickle


def get_topics(topics_path):
        '''
        this function read a topics file where each line represents a topic but
        seperated by colon (:) for topic_id and topic_title
        '''
        topics_id_title = {}
        topics_id = []

        with open(topics_path, 'r') as reader:

            lines = reader.readlines()
            reader.close()

        for line in lines:
            line_parts = line.strip().split(':')
            topic_id = line_parts[0]
            topic_title = line_parts[1]

            topics_id_title[topic_id] = topic_title
            topics_id.append(topic_id)

        return topics_id_title, topics_id


def get_qrels(qrels_path):
        '''
        Load qrels files where topicid -> {(docid, rel), (docid, rel), ...., (docid, rel)}
        '''
        with open(qrels_path, 'r') as fread:
            lines = fread.readlines()
            fread.close()

        topics_docid_rel = {}
        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split(" ")

            #1 0 clueweb09-en0003-55-31884 0
            topic_id = parts[0]
            doc_id = parts[2]
            rel = parts[3]

            docid_rel = topics_docid_rel.get(query_id)
            if docid_rel is None:
                docid_rel = {}
            docid_rel[doc_id] = rel
            topics_docid_rel[query_id] = docid_rel

        return topics_docid_rel


def get_run_result(results_path):
        '''
        load a result run having topic_id --> {(docid=>(rank, score)), .... }
        '''
        result_lines = []
        with open(results_path, 'r') as fread:
            lines = fread.readlines()
            fread.close()

        topics_docid_rankscore = {}
        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split(" ")

            result_lines.append(line.strip())
            #1 0 clueweb09-en0003-55-31884 0
            topic_id = parts[0]
            doc_id = parts[2]
            rank = parts[3]
            score = parts[4]

            docid_rankscore = topics_docid_rankscore.get(query_id)
            if docid_rankscore is None:
                docid_rankscore = {}
            docid_rankscore[doc_id] = [rank, score]
            topics_docid_rankscore[topic_id] = docid_rankscore

        return topics_docid_rankscore


def get_topics_docs_ltr_features(features_path):
        '''
        loading a topics => document-ids with features
        '''
        with open(path, 'r') as fread:
            lines = fread.readlines()
            fread.close()

        topics_docid_features = {}
        topics_docids = {}

        line = lines[0]
        parts = line.rstrip().split("\t")
        features_id = [parts[i] for i in range(2, len(parts))]

        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split("\t")

            topic_id = parts[0]
            doc_id = parts[1]
            docid_features = topics_docids_features.get(topic_id)

            if docid_features is None:
                docid_features = {}

            features = []
            for jdx in range(2, len(parts)):
                feature = float(parts[jdx])
                features.append(feature)
            docid_features[doc_id] = features
            topics_docids_features[query_id] = docid_features

            docids = topics_docids.get(topic_id)
            if docids is None:
                docids = []
            docids.append(doc_id)
            topics_docids[topic_id] = docids

        return topics_docids, features_id, topics_docids_features


def loading_pkl_model(model_path):

        model = pickle.load(open(model_path, 'rb'))
        return model
