import warnings
warnings.filterwarnings('ignore')

from mxnet import gluon
from mxnet import nd
import gluonnlp as nlp
import re


class wordEmbedding:
    def __init__(self):
        self.glove_6b50d = nlp.embedding.create('glove', source='glove.6B.50d')
        self.vocab = nlp.Vocab(nlp.data.Counter(self.glove_6b50d.idx_to_token))
        self.vocab.set_embedding(self.glove_6b50d)

    def cos_sim(self,x, y):
        return nd.dot(x, y) / (nd.norm(x) * nd.norm(y))

    def cos_sim_by_word(self,word1, word2):
        x=self.vocab.embedding[word1]
        y=self.vocab.embedding[word2]
        return nd.dot(x, y) / (nd.norm(x) * nd.norm(y))

    def norm_vecs_by_row(self,x):
        return x / nd.sqrt(nd.sum(x * x, axis=1) + 1E-10).reshape((-1,1))

    def get_knn(self, k, word):
        word_vec = self.vocab.embedding[word].reshape((-1, 1))
        vocab_vecs = self.norm_vecs_by_row(self.vocab.embedding.idx_to_vec)
        dot_prod = nd.dot(vocab_vecs, word_vec)
        indices = nd.topk(dot_prod.reshape((len(self.vocab), )), k=k+1, ret_typ='indices')
        indices = [int(i.asscalar()) for i in indices]
        # Remove unknown and input tokens.
        return self.vocab.to_tokens(indices[1:])

    def get_top_k_by_analogy(self,k, words):
        #word_vecs = self.vocab.embedding[word1, word2, word3]
        word_vecs = self.vocab.embedding[words]
        word_diff = (word_vecs[1] - word_vecs[0] + word_vecs[2]).reshape((-1, 1))
        vocab_vecs = self.norm_vecs_by_row(self.vocab.embedding.idx_to_vec)
        dot_prod = nd.dot(vocab_vecs, word_diff)
        indices = nd.topk(dot_prod.reshape((len(self.vocab), )), k=k, ret_typ='indices')
        indices = [int(i.asscalar()) for i in indices]
        return self.vocab.to_tokens(indices)

    def cos_sim_word_analogy(self, words):
        vecs = self.vocab.embedding[words]
        return self.cos_sim(vecs[1] - vecs[0] + vecs[2], vecs[3])

    def getEmbedding(self,word):
        return self.vocab.embedding[word].reshape((-1,1))

    def getWordByIndex(self,index):
        return self.vocab.idx_to_token[index]

    def getIndexOfWord(self,word):
        return self.vocab[word]



#wordEmb=wordEmbedding()

#print('finn embedding til ord')
#print(wordEmb.getEmbedding('beautiful'))
##print()
#print('finn embedding fra index')
#print(wordEmb.getWordByIndex(71424))
#print()
#print('finn index til ord')
#print(wordEmb.getIndexOfWord('office'))
#print()
#print('finn cosinus liket mellom 2 ord')
#print(wordEmb.cos_sim_by_word('cat','dog'))
#print()
#print("finn k nærmest til eit ord")
#print(wordEmb.get_knn( 5, 'computers'))
#print()
#print('finn k nærmest til 3 ord')
#print(wordEmb.get_top_k_by_analogy( 1,['man','woman','son']))
#print()
#print('finn cos likhet mellom k ord:')
#print(wordEmb.cos_sim_word_analogy(['man', 'woman', 'son', 'daughter','car']))


"""https://gluon-nlp.mxnet.io/examples/word_embedding/word_embedding.html
https://gluon-nlp.mxnet.io/examples/word_embedding/word_embedding_training.html

https://nlp.stanford.edu/projects/glove/

http://colah.github.io/posts/2015-08-Understanding-LSTMs/
https://www.bouvet.no/bouvet-deler/explaining-recurrent-neural-networks
"""
