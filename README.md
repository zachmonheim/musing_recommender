# musing_recommender
Recommendation System for Musing

## Installation

Packages used

```bash
pip install pandas
pip install scipy
pip install sklearn
```

## Usage

```python
MatrixCreator #creates matrix after reading csv file
CommonDatasetMatrix #creates matrix based off matrix in MatDictSave
MatrixFactorization #factorizes matrix with training algorithm
RelevanceCalculator #find relevance of keywords for items based on users
MatDictSave #randomly generates matrices and dictionaries for RelevanceCalculator
```
