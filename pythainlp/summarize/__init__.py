# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
from pythainlp.corpus import stopwords
from string import punctuation
from collections import defaultdict
from pythainlp.tokenize import sent_tokenize, word_tokenize
from heapq import nlargest


class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('thai') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        m = float(max(freq.values()))
        for w in list(freq):
            freq[w] = freq[w]/m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def _rank(self, ranking, n):
        return nlargest(n, ranking, key=ranking.get)

    def summarize(self, text, n):
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking,n)
        return [sents[j] for j in sents_idx]
def summarize(text,n,engine='frequency'):
    '''
    คำสั่งสรุปเอกสารภาษาไทย
    summarize(text,n,engine='frequency')
    text เป็นข้อความ
    n คือ จำนวนประโยคสรุป
    engine ที่รองรับ
    - frequency
    '''
    if engine=='frequency':
        data=FrequencySummarizer().summarize(text,n)
    return data