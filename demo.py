from tokenization.crf_tokenizer import CrfTokenizer
from word_embedding.word2vec_gensim import Word2Vec
from text_classification.short_text_classifiers import BiDirectionalLSTMClassifier, load_synonym_dict

# Please give the correct paths
word2vec_model = Word2Vec.load('models/pretrained_word2vec.bin')

tokenizer = CrfTokenizer(config_root_path='tokenization/',
                         model_path='models/pretrained_tokenizer.crfsuite')
sym_dict = load_synonym_dict('data/sentiment/synonym.txt')
keras_text_classifier = BiDirectionalLSTMClassifier(tokenizer=tokenizer, word2vec=word2vec_model.wv,
                                                    model_path='models/sentiment_model.h5',
                                                    max_length=10, n_epochs=10,
                                                    sym_dict=sym_dict)
X, y = keras_text_classifier.load_data(['data/sentiment/samples/positive.txt',
                                       'data/sentiment/samples/negative.txt'],
                                       load_method=keras_text_classifier.load_data_from_file)

keras_text_classifier.train(X, y)
label_dict = {0: 'tích cực', 1: 'tiêu cực'}
test_sentences = ['Dở thế', 'Hay thế', 'phim chán thật', 'nhảm quá']
labels = keras_text_classifier.classify(test_sentences, label_dict=label_dict)
print(labels)  # Output: ['tiêu cực', 'tích cực', 'tiêu cực', 'tiêu cực']