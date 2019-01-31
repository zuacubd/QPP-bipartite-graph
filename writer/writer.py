import os
import sys
import pickle

def write_model(model, model_path):
        pickle.dump(model, open(model_path, 'wb'))

