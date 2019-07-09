# musing_recommender
Recommendation System for Musing

## Installation

Packages used

```bash
pip install pandas
pip install scipy
pip install sklearn
pip install lightfm
```

## Usage

```python
MatrixFactorization #factorizes matrix with training algorithm
RelevanceCalculator #find relevance of keywords for items based on users
MatDictSave #randomly generates matrices and dictionaries for RelevanceCalculator and Matrix Factorization
LightFMAttempt #uses generated data to create LightFM dataset to use with LightFM system
```
