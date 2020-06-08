
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from preprocess_corpus import get_corpus,getChinese
from sklearn.metrics import classification_report
import pickle
import sys
import os
#使用高斯贝叶斯分类器

model_path="model.pkl"
target_names=["simplified","traditional"]

def train():
    clt = GaussianNB()
    vectorizer = CountVectorizer(analyzer='char')
    print("loading corpus...")
    data = tuple(get_corpus())
    label,corpus = zip(*data)
    X_train, X_test, y_train, y_test = train_test_split(corpus, label, test_size=0.2, random_state=33)


    #学习词汇的词典并返回文档矩阵
    X_count_train = vectorizer.fit_transform(X_train)
    #不进行学习直接转换文档document-term矩阵
    X_count_test = vectorizer.transform(X_test)

    print("training corpus...")
    # 使用朴素贝叶斯分类器，对CountVectorizer（不去除停用词）后的训练样本进行参数学习
    clt.fit(X_count_train.toarray(), y_train)


    # 测试训练结果
    print ('The accuracy of classifying corpus using Naive Bayes (CountVectorizer without filtering stopwords):', clt.score(X_count_test.toarray(), y_test))
    y_count_predict = clt.predict(X_count_test.toarray())
    print (classification_report(y_test, y_count_predict, target_names = target_names))
    with open(model_path,'wb')as f:
        pickle.dump((clt,vectorizer),f)
    

def get_model():
    f = open(model_path,"rb")
    obj = pickle.load(f)
    f.close()
    return obj

if __name__=="__main__":
    print('''
    ===========================================
    usage:
    0. t :train model
    1. f [filename]:detect one file
    2. s [sentence]:detect one sentence
    3. d [diratory]:detect one diratory
    ===========================================
    ''')

    while True:
        gets = input('input:').split()
        if gets[0]=='f':
            clt,vectorizer = get_model()
            with open(gets[1],"r",encoding='utf-8')as f:
                data = [getChinese(f.read())]
            print("result :",target_names[clt.predict(vectorizer.transform(data).toarray())[0]])
        elif gets[0]=='s':
            clt,vectorizer = get_model()
            data=[gets[1]]
            print("result :",target_names[clt.predict(vectorizer.transform(data).toarray())[0]])
        elif gets[0]=='d':
            clt,vectorizer = get_model()
            file_list = os.listdir(gets[1])
            output=open("output_of_files.txt","w")
            output.write(f"test dir:{gets[1]}\n")
            for i,file in enumerate(file_list):
                f = open(f"{gets[1]}/{file}","r",encoding='utf-8')
                print(f"{gets[1]}/{file}",":",target_names[clt.predict(vectorizer.transform([getChinese(f.read())]).toarray())[0]])
                output.write(f"{gets[1]}/{file}:{target_names[clt.predict(vectorizer.transform([getChinese(f.read())]).toarray())[0]]}\n")
                f.close()
            output.close()
        elif gets[0]=='t':
            train()
            