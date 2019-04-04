import codecs
import sys



# 2.按词汇表将单词映射到编号
# 读取词汇表，并建立词汇到单词编号的映射。
def produce_idseq(RAW_DATA,VOCAB,OUTPUT_DATA):
    with codecs.open(VOCAB, "r", "utf-8") as f_vocab:
        vocab = [w.strip() for w in f_vocab.readlines()]
    word_to_id = {k: v for (k, v) in zip(vocab, range(len(vocab)))}

    # 如果出现了不在词汇表内的低频词，则替换为"unk"。
    def get_id(word):
        return word_to_id[word] if word in word_to_id else word_to_id["<unk>"]


    # 3.将数据进行替换并保存结果
    fin = codecs.open(RAW_DATA, "r", "utf-8")
    fout = codecs.open(OUTPUT_DATA, 'w', 'utf-8')
    for line in fin:
        words = line.strip().split() + ["<eos>"]  # 读取单词并添加<eos>结束符
        # 将每个单词替换为词汇表中的编号
        out_line = ' '.join([str(get_id(w)) for w in words]) + '\n'
        fout.write(out_line)
    fin.close()
    fout.close()

def get_word(VOCAB,id):#根据单词的序号查找单词
    with codecs.open(VOCAB, "r", "utf-8") as f_vocab:
        vocab = [w.strip() for w in f_vocab.readlines()]
    if(id>len(vocab)):
        return "#"
    return vocab[id]