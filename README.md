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

## Brief Description of Indices
| Index Name                | Index Category                 | Basic Description                                                                | Reference Corpus/Database                                                       | Details                          |
|---------------------------|--------------------------------|----------------------------------------------------------------------------------|---------------------------------------------------------------------------------|----------------------------------|
| filename                  | Basic Description              | name of processed text file                                                      | n/a                                                                             | n/a                              |
| nwords                    | Basic Description              | number of word tokens                                                            | n/a                                                                             | n/a                              |
| ncontentwords             | Basic Description              | number of content word tokens                                                    | n/a                                                                             | n/a                              |
| MATTR_lemmas              | Lexical Diversity              | moving average type-token ratio (50-word window)                                 | n/a                                                                             | n/a                              |
| lemma_frequency_log_AW    | Word Frequency                 | Average reference-corpus frequency (log-transformed) for all words               | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| lemma_frequency_log_CW    | Word Frequency                 | Average reference-corpus frequency (log-transformed) for content words           | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| lemma_frequency_log_verbs | Word Frequency                 | Average reference-corpus frequency (log-transformed) for verbs                   | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| lemma_frequency_log_nouns | Word Frequency                 | Average reference-corpus frequency (log-transformed) for nouns                   | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_freq_log           | Bigram Frequency               | Average reference-corpus frequency (log-transformed) for bigrams                 | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_soa_dp_LR          | Bigram Strength of Association | Average delta p score (left word as cue) for bigrams                             | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_soa_dp_RL          | Bigram Strength of Association | Average delta p score (right word as cue) for bigrams                            | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_soa_dp_max         | Bigram Strength of Association | Average max delta p score max(right word as cue, left word as cue) for   bigrams | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_soa_MI             | Bigram Strength of Association | Average mutual information score for bigrams                                     | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| bigram_soa_T              | Bigram Strength of Association | Average T score for bigrams                                                      | Spanish Corpus of the Web (ESCOW14; Schäfer, 2015; Schäfer &   Bildhauer, 2012) | Section ax01 (450 million words) |
| valency_CW                | Psycholinguistic Information   | Average valency score for content words                                          | Guash et al., 2016                                                              | Includes ratings for 1,400 words |
| arousal_CW                | Psycholinguistic Information   | Average arousal score for content words                                          | Guash et al., 2017                                                              | Includes ratings for 1,400 words |
| concreteness_CW           | Psycholinguistic Information   | Average concreteness score for content words                                     | Guash et al., 2018                                                              | Includes ratings for 1,400 words |
| imageability_CW           | Psycholinguistic Information   | Average imageability score for content words                                     | Guash et al., 2019                                                              | Includes ratings for 1,400 words |
| availability_CW           | Psycholinguistic Information   | Average availability score for content words                                     | Guash et al., 2020                                                              | Includes ratings for 1,400 words |
| familiarity_CW            | Psycholinguistic Information   | Average familiarity score for content words                                      | Guash et al., 2021                                                              | Includes ratings for 1,400 words |
## License
TAALES_ES is available for use under a Creative Commons Attribution-NonCommercial-Sharealike license (4.0)

For a summary of this license (and a link to the full license) <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">click here</a>.