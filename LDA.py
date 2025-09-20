from gensim import models
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
matplotlib.use('Agg')
def compute_coherence_values(dictionary, corpus, documents, limit, start=2, step=1):
    coherence_values = []
    perplexity_values = []
    model_list = []
    
    for num_topics in range(start, limit, step):
        model = models.LdaModel(corpus=corpus,
                              id2word=dictionary,
                              num_topics=num_topics,
                              random_state=100,
                              update_every=1,
                              chunksize=100,
                              passes=10,
                              alpha='auto')
        model_list.append(model)
        
        # 计算一致性
        coherencemodel = CoherenceModel(model=model, texts=documents, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
        
        # 计算困惑度
        perplexity_values.append(np.exp(-model.log_perplexity(corpus)))
    
    return model_list, coherence_values, perplexity_values

def LDAMetrics(documents):
    #输入分好词的list(将process.parse返回的数据用process.comment2tkdocs处理即可)
    dictionary = Dictionary(documents)
    corpus = [dictionary.doc2bow(text) for text in documents]
    # 测试主题数量从2到10
    model_list, coherence_values, perplexity_values = compute_coherence_values(
        dictionary=dictionary, corpus=corpus, documents=documents, start=2, limit=10, step=1
    )
    x = range(2, 10)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.title("Coherence Score by Number of Topics")
    img1=io.BytesIO()
    plt.savefig(img1, format='png', dpi=100)
    plt.close()  # 关闭当前图形
    plt.plot(x, perplexity_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Perplexity")
    plt.title("Perplexity by Number of Topics")
    img2=io.BytesIO()
    plt.savefig(img2, format='png', dpi=100)
    plt.close()
    #直接返回base64编码的图片
    return base64.b64encode(img1.getvalue()).decode('utf-8'), base64.b64encode(img2.getvalue()).decode('utf-8')

def modelLDA(documents, ntopics):
    dictionary = Dictionary(documents)
    corpus = [dictionary.doc2bow(text) for text in documents]
    lda_model = models.LdaModel(corpus=corpus,
                            id2word=dictionary,
                            num_topics=ntopics,
                            random_state=100,
                            update_every=1,
                            chunksize=100,
                            passes=10,
                            alpha='auto',
                            per_word_topics=True)
    vis_data=gensimvis.prepare(lda_model,corpus,dictionary)
    return pyLDAvis.prepared_data_to_html(vis_data)
    