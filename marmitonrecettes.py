# -*- coding: utf-8 -*-
"""marmitonrecettes.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yhrCisHyR80OIiTJIv1OneRGao6U8M9l
"""

import pandas
import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, Activation 
import numpy as np
import tensorflow as tf
from sklearn.linear_model import SGDRegressor
from sklearn import preprocessing
from keras.utils import np_utils
from sklearn.feature_extraction.text import CountVectorizer

"""# 新段落"""

filename = 'marmitonrecettes.csv'
token = '48eb51ebd68f3d2a99b72ec339b32756402007c5'
url='https://gitarero.ecam.fr/api/v1/repos/etienne.vienot/machine_learning/raw/' + filename+'?token=' + token
df = pandas.read_csv(url,sep=";")

df

df.replace(100,0,inplace=True)
df.replace(101,1,inplace=True)
df.replace(112,2,inplace=True)

df

df.shape

#frequence de chaque valeur d'une colonne
# ici il y a 5 classe0 et 5 classe1
frequence = pandas.crosstab(index=df["classe"],columns="count")
frequence



#instanciation
#parseur = CountVectorizer(binary=True)
parseur = CountVectorizer()

Xmatrice = parseur.fit_transform(df['ingredients'])

#inaffichable
Xmatrice

#nombre de colonnes de la matrice
print(len(parseur.get_feature_names_out()))

# parseur.get_feature_names() contient tous les mots
parseur.get_feature_names_out()

"""On transforme Xmatrice en un vecteur utilisable

"""

X = Xmatrice.toarray()

y = df['classe'];
yN = np_utils.to_categorical(y, 3)

X.shape

yN

X

X_train, X_test, y_train, y_test = train_test_split(X, yN, test_size=0.2, random_state=1)

print( 'nombre et formes des données d\'apprentissage: ', X_train.shape)
print( 'nombre et formes des données de test : ', X_test.shape)
print( 'labels (étiquettes) pour l\'apprentissage: ', y_train.shape)

print( 'nombre et formes des données de test : ', y_test.shape)
print('nombre et forme de yTrain :', y_train.shape)

y_train

model = Sequential()
model.add(Dense(20, input_dim=3074, activation='sigmoid'))
#un softmax pour la sortie qui contient autant de neurones que de classes à discriminer
model.add(Dense(3, activation='softmax'))
#affichage du résumé du modèle
model.summary()

# on définit les fonctions liées au modèle

#version de base avec MSE comme fonction de cout
model.compile(optimizer='rmsprop',loss='mean_squared_error', metrics=['accuracy'])

# on entraine le modèle
model.fit(X_train, y_train, epochs=20, initial_epoch=0, batch_size=128)
model.summary()

score = model.evaluate(X_test, y_test)
print("%s: %.2f%%" % (model.metrics_names[1], score[1]*100))

from keras.callbacks import EarlyStopping


ourCallback = keras.callbacks.EarlyStopping(monitor='val_accuracy', min_delta=0.0001, patience=20, verbose=0, mode='auto', baseline=None, restore_best_weights=False)

# et c'est reparti !
# On ne sait pas quand l'apprentissage s'arrêtera, mais au pire, après 2000 époques.
history=model.fit(X_train, y_train, epochs=2000, batch_size=128, validation_split=0.2, callbacks=[ourCallback])

print("stopped at epoch: ", ourCallback.stopped_epoch)

model.evaluate(X_train, y_train)

model.evaluate(X_test, y_test)

test_pred_plat = np.argmax(model.predict(X_test), axis=-1) 
y_test_plat=np.argmax(y_test, axis=-1)
print(confusion_matrix(y_test_plat, test_pred_plat))



print(history.history)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

test_pred = np.argmax(model.predict(X_test), axis=-1) #model.predict_classes(xTest)


# cm = confusion_matrix( yN,  test_pred)
# print(cm)

"""Affichage

"""

#frequence de chaque mot : on somme chaque colonne
freq_mots = np.sum(X,axis=0)

X.shape[1]

index = np.arange(0,X.shape[1],1);
#ou si on le veut trié (attention temps de calcul du tri)
#index = np.argsort(freq_mots)

index

imp = {'terme':np.asarray(parseur.get_feature_names_out())[index],'freq':freq_mots[index]}
affichage = pandas.DataFrame(imp)

affichage

affichage = affichage[affichage['freq']<1000]

""" affichage un image pour trouve le relation entre le mots et combien de fois il affiche

"""

x=affichage['terme'].to_numpy();
y=affichage['freq'].to_numpy();
plt.plot(x, y, 'ro');
plt.show()

affichage=affichage[ ~ affichage['terme'].str.contains('0')]
affichage=affichage[ ~ affichage['terme'].str.contains('1')]
affichage=affichage[ ~ affichage['terme'].str.contains('2')]
affichage=affichage[ ~ affichage['terme'].str.contains('3')]
affichage=affichage[ ~ affichage['terme'].str.contains('4')]
affichage=affichage[ ~ affichage['terme'].str.contains('5')]
affichage=affichage[ ~ affichage['terme'].str.contains('6')]
affichage=affichage[ ~ affichage['terme'].str.contains('8')]
affichage=affichage[ ~ affichage['terme'].str.contains('7')]
affichage=affichage[ ~ affichage['terme'].str.contains('9')]
affichage

x=affichage['terme'].to_numpy();
y=affichage['freq'].to_numpy();
plt.plot(x, y, 'ro');
plt.show()