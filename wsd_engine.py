"""Offline lexical sense inventory and transparent Simplified Lesk WSD.
Optional NLTK WordNet integration is used only if installed and corpus is present.
"""
import json
import re
from pathlib import Path

DATA = json.loads((Path(__file__).parent / 'senses.json').read_text(encoding='utf-8'))
STOP = set('a an the is are was were be to of for on in at by with and or from as it its this that she he they i we my his her their before after into out over under going'.split())

def tokens(text):
    return set(re.findall(r"[a-z]+", text.lower())) - STOP

def wordnet_senses(word):
    try:
        from nltk.corpus import wordnet as wn
        synsets = wn.synsets(word)
        if not synsets:
            return []
        results = []
        for syn in synsets:
            results.append({'id':syn.name(), 'pos':syn.pos(), 'definition':syn.definition(),
                'examples':syn.examples(),
                'synonyms':sorted({lemma.name().replace('_',' ') for lemma in syn.lemmas()}),
                'antonyms':sorted({a.name().replace('_',' ') for lemma in syn.lemmas() for a in lemma.antonyms()}),
                'hypernyms':[x.name().replace('_',' ') for x in syn.hypernyms()[:8]],
                'hyponyms':[x.name().replace('_',' ') for x in syn.hyponyms()[:8]]})
        return results
    except (ImportError, LookupError, OSError):
        return []

def inventory(word, source='offline'):
    word = word.strip().lower()
    if source == 'wordnet':
        found = wordnet_senses(word)
        if found:
            return {'source':'NLTK WordNet', 'senses':found}
        return {'source':'NLTK WordNet unavailable', 'senses':[], 'error':'Install nltk and download wordnet corpus, or select Offline.'}
    return {'source':'Curated offline lexical inventory (limited WordNet-style subset)', 'senses':DATA.get(word, [])}

def disambiguate(sentence, word, source='offline'):
    result = inventory(word, source)
    context = tokens(sentence) - tokens(word)
    scores = []
    for idx, sense in enumerate(result['senses']):
        signature = ' '.join([sense['definition'], *sense['examples'], *sense['synonyms'], *sense['hypernyms'], *sense['hyponyms']])
        overlap = sorted(context & tokens(signature))
        scores.append({'id':sense['id'], 'definition':sense['definition'], 'score':len(overlap), 'matches':overlap, 'index':idx})
    scores.sort(key=lambda item:(-item['score'], item['index']))
    best = scores[0] if scores else None
    return {'word':word, 'sentence':sentence, 'source':result['source'], 'best':best,
            'fallback':bool(best and best['score']==0), 'ranking':scores, 'sense_count':len(scores),
            'error':result.get('error')}
