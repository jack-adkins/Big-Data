import numpy as np

# Data I'm using based on my Question 3 answers for signatures and jaccard similarities
signatures = {
    "S1": [1, 0, 1, 3],
    "S2": [3, 2, 4, 0],
    "S3": [0, 0, 0, 1],
    "S4": [1, 0, 1, 0],
}
jaccard_similarities = {
    ("S1", "S2"): 0.4,
    ("S1", "S3"): 0.67,
    ("S1", "S4"): 0.67,
    ("S2", "S3"): 0.2,
    ("S2", "S4"): 0.2,
    ("S3", "S4"): 1.0,
}

# Hash function + buckets for bands
def band_hash(x, y):
    return (x + y) % 5

b1Buckets = {key: band_hash(values[0], values[1]) for key, values in signatures.items()}
b2Buckets = {key: band_hash(values[2], values[3]) for key, values in signatures.items()}

# Find alike pairs in each band
def getAlikePairs(bucket):
    pairs = []
    for key1 in bucket:
        for key2 in bucket:
            if key1 != key2 and bucket[key1] == bucket[key2]:
                p = tuple(sorted((key1, key2)))
                if p not in pairs:
                    pairs.append(p)
    return pairs

b1Pairs = getAlikePairs(b1Buckets)
b2Pairs = getAlikePairs(b2Buckets)

# LSH identified pairs
lshPairs = set(b1Pairs + b2Pairs)

# Compute average Jaccard similarities
lshSim = [jaccard_similarities[pair] for pair in lshPairs]
notlshPairs = set(jaccard_similarities.keys()) - lshPairs
notlshSim = [jaccard_similarities[pair] for pair in notlshPairs]

avg_lshSim = round(np.mean(lshSim),4)
avg_notlshSim = round(np.mean(notlshSim),4)

# 4a
print("Band 1 Buckets:", b1Buckets)
print("Band 2 Buckets:", b2Buckets)
# 4b
print("LSH Pairs Identified:", lshPairs)
# 4c
print("Avg JS (LSH):", avg_lshSim)
print("Avg JS (Non-LSH):", avg_notlshSim)
