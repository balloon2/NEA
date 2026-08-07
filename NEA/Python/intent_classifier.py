#maths label:1
#Note label:0

import os 

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

#dataset 25 maths 25 notes
#maths[1],notes[0]

TrainingData =[
    #maths
    ("integral of x squared with respect to x", 1),
    ("square root of a plus b", 1),
    ("dy dx of sine x equals cosine x", 1),
    ("5 plus 10 over 2", 1),
    ("derivative of exponential x", 1),
    ("evaluate the limit as x approaches zero", 1),
    ("matrix multiplication of a and b", 1),
    ("solve for x in quadratic equation", 1),
    ("sine theta squared plus cosine theta squared", 1),
    ("log base 10 of 100 is 2", 1),
    ("partial derivative with respect to y", 1),
    ("calculate the area under the curve", 1),
    ("vector dot product of u and v", 1),
    ("sum of n terms of arithmetic progression", 1),
    ("factorial of n is n times n minus 1", 1),
    ("tangent of angle theta", 1),
    ("integrate 3 x cubed plus 2 x", 1),
    ("find the roots of x squared minus 4", 1),
    ("dy over dx is the gradient of the function", 1),
    ("hypotenuse equals square root of a squared plus b squared", 1),
    ("pi times radius squared for area of circle", 1),
    ("logarithm of x plus logarithm of y", 1),
    ("binomial expansion of 1 plus x to the power n", 1),
    ("divide 50 by 5 and multiply by 3", 1),
    ("differentiate polynomial with respect to x", 1),
    #notes
    ("the industrial revolution began in Britain", 0),
    ("photosynthesis occurs in plants using sunlight", 0),
    ("remember to review chapter 4 for the upcoming test", 0),
    ("mitochondria is the powerhouse of the cell", 0),
    ("the prime minister gave a speech on foreign policy", 0),
    ("cold war started after the end of world war two", 0),
    ("water is composed of two hydrogen atoms and one oxygen atom", 0),
    ("the main theme of Hamlet is revenge and morality", 0),
    ("supply and demand dictate market price equilibrium", 0),
    ("dont forget to submit the coursework assignment on Monday", 0),
    ("atoms consist of protons neutrons and electrons", 0),
    ("Shakespeare wrote many famous plays in England", 0),
    ("the French revolution broke out in 1789", 0),
    ("key factors of climate change include greenhouse gas emissions", 0),
    ("make a summary of key terms for history revision", 0),
    ("the human heart has four distinct chambers", 0),
    ("inflation reduces the purchasing power of money", 0),
    ("read pages 45 to 60 before the next seminar", 0),
    ("DNA carries genetic instructions in living organisms", 0),
    ("central bank controls the interest rates of the country", 0),
    ("tectonic plates shift and cause earthquakes", 0),
    ("write down the definition of democracy for political science", 0),
    ("the digestive system breaks down food into nutrients", 0),
    ("feudal system dominated medieval European society", 0),
    ("prepare presentation slides for group project", 0),
]

#classifies the voice transcripts into MATHS or NOTES
class IntentClassifier:
    #ngram range(1.1) meaning one and wo words at a time meaning the program looks for everything
    def __init__(self, ngramrange: tuple=(1,2)):
        self.vectorizer=TfidfVectorizer(ngram_range=ngramrange,lowercase=True)
        self.model=LinearSVC(C=1,random_state=42)
        self.fitted=False
        


    #supposed to return intentClassifier
    def fit(self, X: list[str], Y:list[int]) -> "intentClassifier":
        Xvec=self.vectorizer.fit_transform(X)
        self.model.fit(Xvec,Y)
        self.is_fitted = True
        return self
    

    def predict(self, cleantxt: str)->"IntentClassifier":
        
        if not self.is_fitted:
            print("Model is not fitted. Train it or load a saved model first.")
            exit(1)
        
        Xvec=self.vectorizer.transform([cleantxt])
        prediction=self.model.predict(Xvec)[0]
        return "MATHS" if prediction == 1 else "NOTE"

    def save(self, filepath):
        if not self.is_fitted:
            print("fit the model first")
            exit(1)
        dire=os.path.dirname(filepath)
        if dire:
            os.makedirs(dire, exist_ok=True)

        model_state = {"vectorizer": self.vectorizer, "model": self.model}
        f=open(filepath,"wb")
        pickle.dump(model_state,f,protocol=pickle.HIGHEST_PROTOCOL)
    
    #Deserializes vectorizer and model from a single pickle file using pickle
    def loadModel(self, filepath):
        if not os.path.exists(filepath):
            print("model not found at filepath specified")
            exit(1)
        f=open(filepath,"rb")
        model_state=pickle.load(f)
        self.vectorizer=model_state["vectorizer"]
        self.model = model_state["model"]
        self.is_fitted = True
        return self