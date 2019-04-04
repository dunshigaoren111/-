import ParseXml
import Text_vocab
import Senten_id_seq
import TFRecord_operate
import neural_network

skip_window = 1  # 窗口的大小
num_skips = 2  # 每个词产生的最多样本

def set_param(MODE):   # 将MODE设置为 "TRANSLATE_GW", "TRANSLATE_XH"之一。
    if MODE == "TRANSLATE_GW":  # 翻译语料的古文部分
        RAW_DATA = "./textdata/train.txt.gw"
        VOCAB = "./vocab/gw.vocab"
        OUTPUT_DATA = "./ID_seq/train.gw"
        TFRecordfile="./TFRecord_file/gw.tfrecords"
        VOCAB_SIZE = 4000
        embedding_size = 128  # 词向量的维度
        MODEL_SAVE_PATH="./gwmodel"
        MODEL_NAME = "gw_model"
    elif MODE == "TRANSLATE_XH":  # 翻译语料的现代汉语部分
        RAW_DATA = "./textdata/train.txt.xh"
        VOCAB = "./vocab/xh.vocab"
        OUTPUT_DATA = "./ID_seq/train.xh"
        TFRecordfile = "./TFRecord_file/xh.tfrecords"
        VOCAB_SIZE = 4000
        embedding_size = 128  # 词向量的维度
        MODEL_SAVE_PATH = "./xhmodel"
        MODEL_NAME = "xh_model"
    return RAW_DATA,VOCAB,VOCAB_SIZE,OUTPUT_DATA,TFRecordfile,embedding_size,MODEL_SAVE_PATH,MODEL_NAME


def pre_treat():
    # 解析并切分出原始的语料
    # ParseXml.tmxTotext()
# 古文
#     MODE="TRANSLATE_GW"
    # 古文部分的参数的设定
    # RAW_DATA,VOCAB,VOCAB_SIZE,OUTPUT_DATA,TFRecordfile,embedding_size,MODEL_SAVE_PATH,MODEL_NAME =set_param(MODE)
    # 生成古文的字典
    # Text_vocab.produce_vocab(RAW_DATA,VOCAB,VOCAB_SIZE)
    # 将预料转换成词编号序列
    # Senten_id_seq.produce_idseq(RAW_DATA,VOCAB,OUTPUT_DATA)
    # 生成词向量训练所需的训练数据
    # TFRecord_operate.write_tfRecord(TFRecordfile, OUTPUT_DATA, skip_window, num_skips)
    # 神经网络训练词向量
    # neural_network.train_word2vec(TFRecordfile,VOCAB,embedding_size,VOCAB_SIZE,MODEL_SAVE_PATH,MODEL_NAME )


# 现代汉语
    MODE="TRANSLATE_XH"
    RAW_DATA, VOCAB, VOCAB_SIZE, OUTPUT_DATA, TFRecordfile, embedding_size, MODEL_SAVE_PATH, MODEL_NAME = set_param(MODE)
#     Text_vocab.produce_vocab(RAW_DATA,VOCAB,VOCAB_SIZE)
#     Senten_id_seq.produce_idseq(RAW_DATA,VOCAB,OUTPUT_DATA)
#     TFRecord_operate.write_tfRecord(TFRecordfile, OUTPUT_DATA, skip_window, num_skips)
    neural_network.train_word2vec(TFRecordfile, VOCAB, embedding_size, VOCAB_SIZE, MODEL_SAVE_PATH, MODEL_NAME)

# pre_treat()


