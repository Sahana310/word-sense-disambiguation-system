# Lab Exercise 5 — Word Sense Disambiguation Using Lexical Relations

## Aim
To identify different senses of ambiguous words, explore lexical relations, and apply a Simplified Lesk WSD algorithm to sample sentences.

## Tools
Python 3.15 standard library (`http.server`, `json`, `csv`, `re`), HTML5, CSS3, JavaScript. Optional NLTK WordNet corpus.

## Theory
Word sense disambiguation selects the meaning of a polysemous word based on context. A sense inventory associates each word with multiple definitions and lexical relations. Synonyms are related expressions, antonyms convey opposites, hypernyms represent broader categories, and hyponyms represent more specific categories.

## Method
1. Read a target word and context sentence.
2. Obtain candidate senses from a curated offline lexical dataset, or optional NLTK WordNet.
3. Tokenize and lowercase the context; remove stop words and the target word.
4. Construct each sense signature from its definition, usage examples, synonyms, hypernyms, and hyponyms.
5. Count unique words shared between context and signature.
6. Rank senses by overlap. Resolve ties by inventory order. Mark zero-overlap predictions as fallback.
7. Present predictions, candidate scores, lexical relations, and exportable sample results.

## Sample inputs
- bank: She deposited money at the bank before going home.
- bank: The fisherman sat on the bank of the river.
- bat: The bat flew out of the cave at night.
- plant: The workers operate the industrial plant.
- spring: Flowers bloom in spring.

## Expected observations
Financial context words such as *deposited* and *money* favor the financial-bank sense; *river* favors riverbank. The *cave* and *night* context favors the mammal sense of *bat*. *Industrial* and *workers* support the factory sense of *plant*. *Flowers* and *bloom* support the season sense of *spring*. Inspect actual scores in the running app; results depend on the exact lexical signatures.

## Deliverables
- Sense inventory: Sense Inventory tab with definitions and lexical relations.
- WSD results: Disambiguation tab and Batch Analysis tab.
- Output export: `/api/export` produces `wsd_results.csv`.
- Short analysis: This report.

## Limitations and conclusion
The bundled offline data is a curated, small, WordNet-style demonstration rather than the complete WordNet corpus. The optional NLTK WordNet mode provides actual WordNet senses if its package and data are available. Lesk scores are not probabilities and no gold-standard accuracy is claimed. The system illustrates transparent, reproducible lexical-overlap WSD with a modern frontend.
