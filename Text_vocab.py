import codecs
import collections
from operator import itemgetter


# 2.对单词按照词频排序
def produce_vocab(RAW_DATA,VOCAB,VOCAB_SIZE):
    counter = collections.Counter()
    with codecs.open(RAW_DATA, "r", "utf-8") as f:
        for line in f:
            for word in line.strip().split():
                counter[word] += 1

    # 按词频顺序对单词进行排序。
    sorted_word_to_cnt = sorted(
        counter.items(), key=itemgetter(1), reverse=True)
    sorted_words = [x[0] for x in sorted_word_to_cnt]


    # 3.插入特殊符号
        # 在9.3.2小节处理机器翻译数据时，除了"<eos>"以外，还需要将"<unk>"和句子起始符
        # "<sos>"加入词汇表，并从词汇表中删除低频词汇。
    sorted_words = ["<unk>", "<sos>", "<eos>"] + sorted_words
    if len(sorted_words) > VOCAB_SIZE:
        sorted_words = sorted_words[:VOCAB_SIZE]

    # 4.保存词汇列表文件

    with codecs.open(VOCAB, 'w', 'utf-8') as file_output:
        for word in sorted_words:
            file_output.write(word + "\n")

