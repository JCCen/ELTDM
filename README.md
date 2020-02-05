# Fast keyword extraction from text using graph degeneracy-based approaches

*Authors : Romain Avouac, Jaime Costa Centena*

This is our final project for the ELTDM (software guidelines to process massive data) course at ENSAE. Our purpose was to find computationally efficient ways of performing keyword extraction using graph representation of text data, as described in Tixier, Malliaros & Vazirgiannis (2016). 

We focused on two major steps of the data processing pipeline : k-core decomposition to identify dense subgraphs (see 1_k_core_decomp.ipynb), and computation of the elbow criteria to select relevant keywords (see 2_elbow_criteria.ipynb). For each part, we provide extensive performance comparison for all the approaches we implemented (including cythonization, multithreading, multiprocessing). We provide an in-depth description and discussion of our results in a report (in French).
