import pickle
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
class SpamClassifierModel():
    def __init__(self,):
        data = pd.read_csv(r"./src/data/spam.csv",sep="\t",names=["label", "message"])
        self.porterStemmer = PorterStemmer()
        corpus = []
        for i in range(0, len(data)):
            review = re.sub('[^a-zA-Z]', ' ', data['message'][i]).lower().split()
            review = [self.porterStemmer.stem(word) for word in review if not word in stopwords.words('english')]
            review = ' '.join(review)
            corpus.append(review)

        self.countVectorization = CountVectorizer(max_features=2500)
        X = self.countVectorization.fit_transform(corpus).toarray()

        y=pd.get_dummies(data['label']).iloc[:,1].values

        self.spam_detect_model = MultinomialNB().fit(X, y)

    def predict(self,new_text):
        new_review = re.sub('[^a-zA-Z]', ' ', new_text).lower().split()
        new_review = [self.porterStemmer.stem(word) for word in new_review if not word in stopwords.words('english')]
        new_review = ' '.join(new_review)

        new_X = self.countVectorization.transform([new_review]).toarray()

        prediction = self.spam_detect_model.predict(new_X)

        return prediction
