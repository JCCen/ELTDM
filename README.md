# Fast keyword extraction from text using graph degeneracy-based approaches

*Authors : Romain Avouac, Jaime Costa Centena*

This is our final project for the ELTDM (software guidelines to process massive data) course at ENSAE. Our purpose was to find computationally efficient ways of performing keyword extraction from text using graph degeneracy criteria, as described in Tixier, Malliaros & Vazirgiannis (2016). 

We focused on two major steps of the data processing pipeline : k-core decomposition to identify dense subgraphs ([notebook](https://github.com/JCCen/ELTDM/blob/master/1_k_core_decomp.ipynb)), and computation of the elbow criteria to select relevant keywords ([notebook](https://github.com/JCCen/ELTDM/blob/master/2_elbow_criteria.ipynb)). For each part, we provide extensive performance comparison for all the approaches we implemented (including cythonization, multithreading, multiprocessing). We provide an in-depth discussion of our results in a [report](https://github.com/JCCen/ELTDM/blob/master/project_report.pdf) (in French).
