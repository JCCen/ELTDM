# Fast keyword extraction from text using k-core decomposition

*Authors : Romain Avouac, Jaime Costa Centena*

This is our final project for the ELTDM (software guidelines to process massive data) course at ENSAE. Our purpose was to find computationally efficient ways of performing keyword extraction using graph representation of text data, as described in Tixier, Malliaros & Vazirgiannis (2016). More specifically, we focused on two major steps of the data processing pipeline : k-core decomposition to identify dense subgraphs, and computation of the elbow criteria to select relevant keywords. For each part, we provide extensive performance comparison for all the approaches we implemented (including cythonization, multithreading, multiprocessing).
