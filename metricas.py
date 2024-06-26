import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import f1_score
import ast

def generate(stemmer):
    expected_df, results_df = getBaseDfs(stemmer)
    results_processed_df = getResultsProcessed(results_df)
    SavePrecisionRecall(expected_df, results_processed_df, stemmer)
    generateF1Score(expected_df, results_processed_df, stemmer)

def getBaseDfs(stemmer):
    expected_df = pd.read_csv('./result/esperados.csv', sep=';')
    results_df = pd.read_csv('./result/RESULTADOS-' + stemmer + '.csv', header=None, sep=';')
    results_df.columns = ['query_id', 'results']
    return (expected_df, results_df)

def process_results(row):
    query_id, results = row['query_id'], row['results']
    results = results.strip('][').split(',')
    processed_results = []
    for i in range(0, len(results), 3):
        rank = int(results[i])
        doc_id = int(results[i+1])
        score = float(results[i+2])
        processed_results.append((query_id, doc_id, rank, score))
    return processed_results

def getResultsProcessed(results_df):
    processed_results = results_df.apply(process_results, axis=1)
    processed_results = [item for sublist in processed_results for item in sublist]
    results_processed_df = pd.DataFrame(processed_results, columns=['query_id', 'doc_id', 'rank', 'score'])
    return results_processed_df

def precision_recall_at_k(expected_df, results_processed_df, k=11):
    precisions, recalls = [], []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values
        retrieved_docs = results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values[:k]
        true_positives = len(set(true_docs) & set(retrieved_docs))
        precision = true_positives / len(retrieved_docs) if retrieved_docs.size else 0
        recall = true_positives / len(true_docs) if true_docs.size else 0
        precisions.append(precision)
        recalls.append(recall)
    return np.mean(precisions), np.mean(recalls)

def SavePrecisionRecall(expected_df, results_processed_df, stemmer):
    precisions, recalls = [], []
    for k in range(1, 12):
        precision, recall = precision_recall_at_k(expected_df, results_processed_df, k=k)
        precisions.append(precision)
        recalls.append(recall)

    plt.plot(recalls, precisions, marker='o')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('11-point Precision-Recall Curve - ' + stemmer)
    plt.grid()
    plt.savefig('metricas/11pontos-' + stemmer.lower() +'.png')


def generateF1Score(expected_df, results_processed_df, stemmer):
    f1 = calculate_f1_score(expected_df, results_processed_df)
    with open('metricas/f1-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("f1,"+str(f1))


def calculate_f1_score(expected_df, results_processed_df):
    y_true, y_pred = [], []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = set(expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values)
        retrieved_docs = set(results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values)
        
        # Criação das listas de y_true e y_pred
        for doc_id in true_docs.union(retrieved_docs):
            y_true.append(1 if doc_id in true_docs else 0)
            y_pred.append(1 if doc_id in retrieved_docs else 0)
            
    return f1_score(y_true, y_pred)