from typing import Generator, Optional
from ..parse_subtitles import parse_file, Subtitle

# input search term
# flexible search method
# output search line and timeline


class Searchable:
    def __init__(self, corpus: str, method=None) -> None:
        """
        Params:
            corpus: string, filepath to substitle files
            method: string, the implementation method of search
        """
        self.corpus = self.parse_corpus(corpus)
        if self.corpus:
            self.corpus_indexed = self.index_corpus(self.corpus, method=method)

    def parse_corpus(self, corpus: str) -> Optional[Generator[Subtitle, None, None]]:
        return parse_file(corpus)

    def index_corpus(self, method=None):
        return corpus

    def search(self, search_term, method="kmp"):
        if method == "kmp":
            return search_kmp(search_term, self.corpus)
        return []


def search_kmp(search_term, corpus):
    CHAR_SIZE = 256
    # todo: 1. further clean up search term and sentence; 2. reduce character space
    search_hash = 0
    search_term_clean = clean_up_search_string(search_term)
    k = len(search_term_clean)
    for char in search_term_clean:
        search_hash *= CHAR_SIZE
        search_hash += ord(char)

    corpus_hash, char_cnt = 0, 0
    item_buffer, buffer_len = [], 0
    res = []
    for item in corpus:
        sentence = clean_up_corpus_string(item.sentence)

        # refresh item buffer
        if buffer_len > k:
            item_buffer.pop()
        item_buffer.append(item)
        buffer_len += len(sentence)

        for char in sentence:
            if char_cnt < k:
                char_cnt += 1
            else:
                corpus_hash = corpus_hash % CHAR_SIZE ** (k - 1)
            corpus_hash *= CHAR_SIZE
            corpus_hash += ord(char)

            if corpus_hash == search_hash:
                res.append(item_buffer)
                item_buffer, buffer_len = [], 0
    return res


def clean_up_search_string(s):
    return s.lower()


def clean_up_corpus_string(s):
    # remove special characters
    return s.replace("<i>", "").replace("</i>", "").lower() + " "


if __name__ == "__main__":
    res = search_kmp(
        "Spider-Man. I mean",
        parse_file(
            "/Users/lezhili/work/quipper/data/Spider-Man.Into.the.Spider-Verse.2018.720p.BluRay.x264-SPARKS.srt"
        ),
    )
    print('length:', len(res))
    for r in res:
        for item in r:
            print(item.sentence)
        print()

