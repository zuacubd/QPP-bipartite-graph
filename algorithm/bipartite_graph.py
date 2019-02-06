import os
import sys
import numpy as np


def get_Du(M):
        '''
        computing Drow^(-1) of M
        '''
        num_row = M.shape[0]
        Du = np.zeros((num_row, num_row), dtype=np.float64)
        U_sum = M.sum(axis=1)
        U_inv = 1.0/U_sum

        for i in range(0, num_row):
            Du[i,i]= U_inv[i,]
        return Du

def get_Dv(M):
        '''
        computing Dcol^(-1) of M
        '''
        num_col = M.shape[1]
        Dv = np.zeros((num_col, num_col), dtype=np.float64)
        V_sum = M.sum(axis=0)
        V_inv = 1.0/V_sum

        for i in range(0, num_col):
            Dv[i,i]= V_inv[i,]
        return Dv

def getUV_ranking(l1, l2, U0, V0, M):
        '''
        estimate the ranking of nodes (U, V) in a bipartite graph
        '''
        Du = get_Du(M)
        Dv = get_Dv(M)

        Mt = np.transpose(M)
        W1 = np.dot(Du, M)
        W2 = np.dot(Dv, Mt)

        U = U0
        V = V0

        lU0 = (1.0-l1)*U0
        lV0 = (1.0-l2)*V0

        lW1 = l1*W1
        lW2 = l2*W2

        stepk = 1
        sum_Vk = V.sum()
        th = 0.001

        while 1:
            U = np.dot(lW1, V) + lU0
            V = np.dot(lW2, U) + lV0

            sum_Vk1 = V.sum()
            diff = abs(sum_Vk1-sum_vk)
            if diff < th:
                break
            print ("Step: %d %f".format(stepk, diff))
            sum_Vk = sum_Vk1
            stepk = stepk + 1

        print ("Iteration: ", stepk)
        return U, V


def getVU_ranking(l1, l2, U0, V0, M):
        '''
        estimate the ranking of nodes (U, V) in a bipartite graph
        '''
        Du = get_Du(M)
        Dv = get_Dv(M)

        Mt = np.transpose(M)
        W1 = np.dot(Du, M)
        W2 = np.dot(Dv, Mt)

        U = U0
        V = V0

        lU0 = (1.0-l1)*U0
        lV0 = (1.0-l2)*V0

        lW1 = l1*W1
        lW2 = l2*W2

        stepk = 1
        sum_Uk = U.sum()
        th = 0.001

        while 1:
            V = np.dot(lW1, U) + lV0
            U = np.dot(lW2, V) + lU0

            sum_Uk1 = U.sum()
            diff = abs(sum_Uk1-sum_Uk)
            if diff < th:
                break
            print ("Step: %d %f".format(stepk, diff))
            sum_Uk = sum_Uk1
            stepk = stepk + 1

        print ("Iteration: ", stepk)
        return U, V
