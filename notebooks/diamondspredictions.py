# -*- coding: utf-8 -*-
"""DiamondsPredictions.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ypew4RxiW9G7CWm7bjf1uj2oibWK7RbX

### Import Library yang dibutuhkan
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

"""### Load Dataset dari : https://github.com/tidyverse/ggplot2/tree/main/data-raw"""

# Load Dataset
link = 'https://raw.githubusercontent.com/tidyverse/ggplot2/master/data-raw/diamonds.csv'
diamonds = pd.read_csv(link)
diamonds

"""## Exploratory Data Analysis"""

diamonds.info()

diamonds.describe()

#Cek missing value
x = (diamonds.x == 0).sum()
y = (diamonds.y == 0).sum()
z = (diamonds.z == 0).sum()

print("Nilai 0 di kolom x : ", x)
print("Nilai 0 di kolom y : ", y)
print("Nilai 0 di kolom z : ", z)

#cek nilai 0 paDA kolom z
diamonds.loc[(diamonds['z']==0)]

#hapus nilai x,y,z yang bernilai 0
diamonds = diamonds.loc[(diamonds[['x','y','z']]!=0).all(axis=1)]

diamonds.shape

diamonds.describe()

"""### Mengecek Nilai Outlier"""

#Cek nilai Outliers tiap fitur
#Fitur carat
sns.boxplot(x=diamonds['carat'])

#Fitur Table
sns.boxplot(x=diamonds['table'])

#Fitur X
sns.boxplot(x=diamonds['x'])

#Mengatasi nilai outliers
Q1 = diamonds.select_dtypes(include=['number']).quantile(0.25)
Q3 = diamonds.select_dtypes(include=['number']).quantile(0.75)

IQR=Q3-Q1

numerical_cols = diamonds.select_dtypes(include=['number']).columns  # Ambil hanya kolom numerik
diamonds = diamonds[~((diamonds[numerical_cols] < (Q1 - 1.5 * IQR)) |
                      (diamonds[numerical_cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

# Cek ukuran dataset setelah kita drop outliers
diamonds.shape

"""### Univariate Analysis"""

numerical_features = ['price', 'carat', 'depth', 'table', 'x', 'y', 'z']
categorical_features = ['cut', 'color', 'clarity']

"""Categorical Analysis"""

#Fitur Cut
feature = categorical_features[0]
count = diamonds[feature].value_counts()
percent = 100*diamonds[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature);

#Fitur Color
feature = categorical_features[1]
count = diamonds[feature].value_counts()
percent = 100*diamonds[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature)

#Fitur Clarity
feature = categorical_features[2]
count = diamonds[feature].value_counts()
percent = 100*diamonds[feature].value_counts(normalize=True)
df = pd.DataFrame({'jumlah sampel':count, 'persentase':percent.round(1)})
print(df)
count.plot(kind='bar', title=feature)

"""Numerical Features"""

#numerical Features
diamonds.hist(bins=50, figsize=(20,15))
plt.show()

"""### Multivariate Analysis"""

#Categorical features
cat_features = diamonds.select_dtypes(include='object').columns.to_list()

for col in cat_features:
  sns.catplot(x=col, y="price", kind="bar", dodge=False, height = 4, aspect = 3,  data=diamonds, palette="Set3")
  plt.title("Rata-rata 'price' Relatif terhadap - {}".format(col))

# Mengamati hubungan antar fitur numerik dengan fungsi pairplot()
sns.pairplot(diamonds, diag_kind = 'kde')

#Correlation Matrix
plt.figure(figsize=(10, 8))
correlation_matrix = diamonds[numerical_features].corr().round(2)

# Untuk menge-print nilai di dalam kotak, gunakan parameter anot=True
sns.heatmap(data=correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, )
plt.title("Correlation Matrix untuk Fitur Numerik ", size=20)

#Drop fitur yang korelasi nya rendah
diamonds.drop(['depth'], inplace=True, axis=1)
diamonds.head()

"""### One Hot Encoding"""

#One hot encoding
from sklearn.preprocessing import  OneHotEncoder
diamonds = pd.concat([diamonds, pd.get_dummies(diamonds['cut'], prefix='cut', dtype=int)], axis=1)
diamonds = pd.concat([diamonds, pd.get_dummies(diamonds['color'], prefix='color', dtype=int)], axis=1)
diamonds = pd.concat([diamonds, pd.get_dummies(diamonds['clarity'], prefix='clarity', dtype=int)], axis=1)
diamonds.drop(['cut','color','clarity'], axis=1, inplace=True)
diamonds.head()

"""## Data Preparation"""

sns.pairplot(diamonds[['x','y','z']], plot_kws={"s": 3});

"""### Reduksi Dimensi dengan PCA (Principal Componen Analysis)"""

from sklearn.decomposition import PCA
pca = PCA(n_components=1, random_state=123)
pca.fit(diamonds[['x','y','z']])
diamonds['dimension'] = pca.transform(diamonds.loc[:, ('x','y','z')]).flatten()
diamonds.drop(['x','y','z'], axis=1, inplace=True)
diamonds.head()

"""### Pembagian Data (Split Data)"""

from sklearn.model_selection import train_test_split

X = diamonds.drop(["price"],axis =1)
y = diamonds["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 123)

print(len(X))
print(len(X_train))
print(len(X_test))

"""### Standarisasi"""

from sklearn.preprocessing import StandardScaler

numerical_features = ['carat', 'table', 'dimension']
scaler = StandardScaler()
scaler.fit(X_train[numerical_features])
X_train[numerical_features] = scaler.transform(X_train.loc[:, numerical_features])
X_train[numerical_features].head()

X_train[numerical_features].describe().round(4)

"""## Modelling"""

# Siapkan dataframe untuk analisis model
models = pd.DataFrame(index=['train_mse', 'test_mse'],
                      columns=['KNN', 'RandomForest', 'Boosting'])

"""### K-Neares-Neighbors"""

from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error

knn = KNeighborsRegressor(n_neighbors=10)
knn.fit(X_train, y_train)

models.loc['train_mse','knn'] = mean_squared_error(y_pred = knn.predict(X_train), y_true=y_train)

"""### Random Forest"""

# Impor library yang dibutuhkan
from sklearn.ensemble import RandomForestRegressor

# buat model prediksi
RF = RandomForestRegressor(n_estimators=50, max_depth=16, random_state=55, n_jobs=-1)
RF.fit(X_train, y_train)

models.loc['train_mse','RandomForest'] = mean_squared_error(y_pred=RF.predict(X_train), y_true=y_train)

"""### AdaBoost"""

from sklearn.ensemble import AdaBoostRegressor

boosting = AdaBoostRegressor(learning_rate=0.05, random_state=55)
boosting.fit(X_train, y_train)
models.loc['train_mse','Boosting'] = mean_squared_error(y_pred=boosting.predict(X_train), y_true=y_train)

"""## Evaluasi Model"""

# melakukan scaling terhadap fitur numerik pada X_test sehingga memiliki Mean=0 dan Std=1
X_test.loc[:, numerical_features] = scaler.transform(X_test[numerical_features])

# Buat variabel mse yang isinya adalah dataframe nilai mse data train dan test pada masing-masing algoritma
mse = pd.DataFrame(columns=['train', 'test'], index=['KNN','RF','Boosting'])

# Buat dictionary untuk setiap algoritma yang digunakan
model_dict = {'KNN': knn, 'RF': RF, 'Boosting': boosting}

# Hitung Mean Squared Error masing-masing algoritma pada data train dan test
for name, model in model_dict.items():
    mse.loc[name, 'train'] = mean_squared_error(y_true=y_train, y_pred=model.predict(X_train))/1e3
    mse.loc[name, 'test'] = mean_squared_error(y_true=y_test, y_pred=model.predict(X_test))/1e3

mse

fig, ax = plt.subplots()
mse.sort_values(by='test', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)

"""## Uji Prediksi"""

prediksi = X_test.iloc[2:5].copy()
pred_dict = {'y_true':y_test[2:5]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediksi).round(1)

pd.DataFrame(pred_dict)

