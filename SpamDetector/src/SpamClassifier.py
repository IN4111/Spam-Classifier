import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


class SpamClassifierModel():
    def __init__(self,):
        self.data = pd.read_csv(r"./src/data/spam.csv",sep="\t",names=["label", "message"])
        self.refreshModel()
    def refreshModel(self,):
        self.porterStemmer = PorterStemmer()
        corpus = []
        for i in range(0, len(self.data)):
            review = re.sub('[^a-zA-Z]', ' ', self.data['message'][i]).lower().split()
            review = [self.porterStemmer.stem(word) for word in review if not word in stopwords.words('english')]
            review = ' '.join(review)
            corpus.append(review)

        self.TfidfVectorization = TfidfVectorizer(max_features=2500)
        X = self.TfidfVectorization.fit_transform(corpus).toarray()

        y=pd.get_dummies(self.data['label']).iloc[:,1].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.spam_detect_model = MultinomialNB().fit(X_train, y_train)

        y_predict=self.spam_detect_model.predict(X_test)

        self.currectAccuracyScore = accuracy_score(y_predict, y_test)
        self.currentPrecisionScore = precision_score(y_predict, y_test)
        self.currentRelayScore = recall_score(y_predict, y_test)
        self.currentf1Score = f1_score(y_predict, y_test)
    def predict(self,new_text):
        new_review = re.sub('[^a-zA-Z]', ' ', new_text).lower().split()
        new_review = [self.porterStemmer.stem(word) for word in new_review if not word in stopwords.words('english')]
        new_review = ' '.join(new_review)

        new_X = self.TfidfVectorization.transform([new_review]).toarray()

        prediction = self.spam_detect_model.predict(new_X)
        if prediction[0]:
            self.iteratePerformance(new_text,"spam")
        else:
            self.iteratePerformance(new_text,"ham")

        return prediction
    def iteratePerformance(self,new_message,prediction):
        self.data.loc[len(self.data)]={"label":prediction,"message":new_message}
        self.refreshModel()
        print({"label":prediction,"message":new_message})
        print(self.data)
