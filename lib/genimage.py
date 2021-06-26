from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter, TokenCountFilter
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer


def get_image_by_frequencies(text):
    token_filters = [
        POSKeepFilter(['名詞']),  # 名詞を抽出するようにする
        TokenCountFilter(),  # トークンの出現回数をカウントする
    ]
    word_dict = dict(Analyzer(token_filters=token_filters).analyze(text))

    image = WordCloud(font_path='/Library/Fonts/Arial Unicode.ttf').generate_from_frequencies(word_dict)
    return image


def get_image_by_tfidf(text, docs):
    token_filters = [
        POSKeepFilter(['名詞']),  # 名詞を抽出するようにする
    ]
    analyzer = Analyzer(token_filters=token_filters)
    target = " ".join([v.surface for v in analyzer.analyze(text)])
    corpus = []
    for i, doc in enumerate(docs):
        corpus.append(" ".join([v.surface for v in analyzer.analyze(doc)]))

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    words = vectorizer.get_feature_names()
    vec = X.toarray()[corpus.index(target)]
    word_dict = {word: weight for word, weight in zip(words, vec)}

    image = WordCloud(font_path='/Library/Fonts/Arial Unicode.ttf').generate_from_frequencies(word_dict)
    return image
