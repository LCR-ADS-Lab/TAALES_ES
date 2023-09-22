# TAALES_ES
Code for the Spanish version of TAALES (TAALES Español)

This page includes the code for the Spanish Version of TAALES (TAALES Español) used in Diez-Ortega & Kyle (2023).

## Getting Started
In order to use this code, you will first need to have a working Python 3 environment. If this is your first time using Python, we suggest using the [Anaconda distribution of Python](https://www.anaconda.com/).

You will also need to install (Spacy)[https://spacy.io/usage] and download/install the "es_core_news_sm" Spanish language model for Spacy. Spacy has excellent tutorials for installing both the Spacy package itself and its language models.

Finally, you will need to install the [lexical-diversity package](https://pypi.org/project/lexical-diversity/).

You can install this using pip:

```bash
pip install lexical-diversity
```

## Running TAALES_ES
Once Spacy, the "es_core_news_sm" model, and lexical-diversity are installed, TAALES_ES can be run.

Make sure that your working directory includes the TAALES_ES_0501 script and the data files. Then, open a Python interpreter and run the following code:

```python
import TAALES_ES_0501 as tes
tes.TAALES_ES("path_to_texts_files/","results.csv") #where path_to_texts_files/ is the name of the folder that your text files are in
```

TAALES_ES will then process each text file in the target folder and produce a .csv file with the results for each text AND three files that include the index scores for each word/bigram in each file.
