import os
import sys

def get_letor_doc_features(path):
        with open(path, 'r') as fread:
            lines = fread.readlines()
        fread.close()

        docid_features = {}

        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split("\t")
            doc_id = parts[0]
            features = []
            for jdx in range(1, len(parts)):
                features.append(parts[jdx])
            docid_features[doc_id] = features

        return docid_features


def get_letor_query_doc_features(path):

        with open(path, 'r') as fread:
            lines = fread.readlines()
        fread.close()

        queryid_docid_features = {}
        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split("\t")

            query_id = parts[0]
            doc_id = parts[1]
            docid_features = queryid_docid_features.get(query_id)
            if docid_features is None:
                docid_features = {}

            features = []
            for jdx in range(2, len(parts)):
                features.append(parts[jdx])
            docid_features[doc_id] = features
            queryid_docid_features[query_id] = docid_features

        return queryid_docid_features


def get_query_doc_features(path):

        with open(path, 'r') as fread:
            lines = fread.readlines()
        fread.close()

        queryid_docid_features = {}
        for idx in range(1, len(lines)):
            line = lines[idx]
            parts = line.rstrip().split("\t")

            query_id = parts[0]
            doc_id = parts[1]
            docid_features = queryid_docid_features.get(query_id)
            if docid_features is None:
                docid_features = {}

            features = []
            for jdx in range(2, len(parts)):
                feature = float(parts[jdx])
                features.append(feature)
            docid_features[doc_id] = features
            queryid_docid_features[query_id] = docid_features

        return queryid_docid_features



