import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import f1_score
import ast

def generate(stemmer):
    print("[METRICAS]: Iniciando...")
    expected_df, results_df = getBaseDfs(stemmer)
    results_processed_df = getResultsProcessed(results_df)

    print("[METRICAS]: Gerando Grafico de Preicsao e Recall")
    save_precision_recall_11_pts_graph(expected_df, results_processed_df, stemmer)
    print("[METRICAS]: Gerando F1 Score")
    generate_f1_score(expected_df, results_processed_df, stemmer)
    print("[METRICAS]: Gerando Precision@5 e Precision@10")
    generate_precision_at_5_and_10(expected_df, results_processed_df, stemmer)
    print("[METRICAS]: Gerando MAP"	)
    mean_average_precision(expected_df, results_processed_df, stemmer)
    print("[METRICAS]: Gerando MRR"	)
    mean_reciprocal_rank(expected_df, results_processed_df, stemmer)
    print("[METRICAS]: Gerando Discounted Cumulative Gain")
    mean_dcg(expected_df, results_processed_df, 10, stemmer)
    print("[METRICAS]: Gerando Normalized Discounted Cumulative Gain")
    mean_ndcg(expected_df, results_processed_df, 10, stemmer)

    print("[METRICAS]: Fim")

def getBaseDfs(stemmer):
    expected_df = pd.read_csv('result/esperados.csv', sep=';')
    results_df = pd.read_csv('result/RESULTADOS-' + stemmer + '.csv', header=None, sep=';')
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

def save_precision_recall_11_pts_graph(expected_df, results_processed_df, stemmer):
    precisions, recalls = [], []
    for k in range(1, 12):
        precision, recall = precision_recall_at_k(expected_df, results_processed_df, k=k)
        precisions.append(precision)
        recalls.append(recall)

    with open('avalia/11pontos-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("Precision,Recall\n")
        for i in range(11):
            f.write(str(precisions[i]) + ',' + str(recalls[i]) + '\n')
    plt.plot(recalls, precisions, marker='o')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('11-point Precision-Recall Curve - ' + stemmer)
    plt.grid()
    plt.savefig('avalia/11pontos-' + stemmer.lower() +'.png')

def generate_f1_score(expected_df, results_processed_df, stemmer):
    f1 = calculate_f1_score(expected_df, results_processed_df)
    with open('avalia/f1-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("f1\n")
        f.write(str(f1))

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

def generate_precision_at_5_and_10(expected_df, results_processed_df, stemmer):
    precision_5 = precision_recall_at_k(expected_df, results_processed_df, k=5)[0]
    precision_10 = precision_recall_at_k(expected_df, results_processed_df, k=10)[0]
    with open('avalia/precision@5-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("precision@5\n")
        f.write(str(precision_5))
    with open('avalia/precision@10-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("precision@10\n")
        f.write(str(precision_10))

def average_precision_at_k(expected_df, results_processed_df, k):
    precisions = []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = set(expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values)
        retrieved_docs = results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values[:k]
        
        precision_values = []
        true_positives = 0
        for i, doc_id in enumerate(retrieved_docs, start=1):
            if doc_id in true_docs:
                true_positives += 1
                precision = true_positives / i
                precision_values.append(precision)
        
        if precision_values:
            avg_precision = np.mean(precision_values)
        else:
            avg_precision = 0
        precisions.append(avg_precision)
        
    return precisions

def mean_average_precision(expected_df, results_processed_df, stemmer):
    avg_precisions = average_precision_at_k(expected_df, results_processed_df, k=len(results_processed_df))
    map_score = np.mean(avg_precisions)
    with open('avalia/map-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("map_score\n")
        f.write(str(map_score))

def reciprocal_rank_at_k(expected_df, results_processed_df):
    reciprocal_ranks = []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = set(expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values)
        retrieved_docs = results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values
        
        for rank, doc_id in enumerate(retrieved_docs, start=1):
            if doc_id in true_docs:
                reciprocal_ranks.append(1 / rank)
                break
        else:
            reciprocal_ranks.append(0)
    
    return reciprocal_ranks

def mean_reciprocal_rank(expected_df, results_processed_df, stemmer):
    reciprocal_ranks = reciprocal_rank_at_k(expected_df, results_processed_df)
    mrr_score = np.mean(reciprocal_ranks)
    with open('avalia/mrr-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("mrr_score\n")
        f.write(str(mrr_score))

def dcg_at_k(relevances, k):
    relevances = np.asfarray(relevances)[:k]
    if relevances.size:
        return np.sum(relevances / np.log2(np.arange(2, relevances.size + 2)))
    return 0.0

def mean_dcg(expected_df, results_processed_df, k,stemmer):
    dcg_scores = []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = set(expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values)
        retrieved_docs = results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values[:k]
        
        relevances = [1 if doc_id in true_docs else 0 for doc_id in retrieved_docs]
        dcg_score = dcg_at_k(relevances, k)
        dcg_scores.append(dcg_score)
    
    mean_dcg_score = np.mean(dcg_scores)
    with open('avalia/discounted-cumulative-gain-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("mean_dcg_score\n")
        f.write(str(mean_dcg_score))

def ndcg_at_k(relevances, k):
    dcg = dcg_at_k(relevances, k)
    idcg = dcg_at_k(sorted(relevances, reverse=True), k)
    if idcg == 0:
        return 0
    return dcg / idcg

def mean_ndcg(expected_df, results_processed_df, k,stemmer):
    ndcg_scores = []
    for query_id in expected_df['QueryNumber'].unique():
        true_docs = set(expected_df[expected_df['QueryNumber'] == query_id]['DocNumber'].values)
        retrieved_docs = results_processed_df[results_processed_df['query_id'] == query_id]['doc_id'].values[:k]
        
        relevances = [1 if doc_id in true_docs else 0 for doc_id in retrieved_docs]
        ndcg_score = ndcg_at_k(relevances, k)
        ndcg_scores.append(ndcg_score)
    
    mean_ndcg_score = np.mean(ndcg_scores)
    with open('avalia/normalized-discounted-cumulative-gain-' + stemmer.lower() + '.csv', 'w') as f:
        f.write("mean_ndcg_score\n")
        f.write(str(mean_ndcg_score))
