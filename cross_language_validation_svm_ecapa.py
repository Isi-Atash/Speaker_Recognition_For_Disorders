import pandas as pd
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

# get th data from csv
# 2 datasets, 1 for Hungary, 1 for Dutch
ds_org_hun = pd.read_csv('Ecapa_embedding_hun.csv')
ds_org_dutch = pd.read_csv('Ecapa_embedding_dutch.csv')

# # Normalize the data
# # 1st, we need to save only OD and HC labels from the dataset
# # 2nd, we need to label_encoder the labels
#
# # find OD and HC from ds and create a new dataset
ds_hun = ds_org_hun[(ds_org_hun.label == 'OD') | (ds_org_hun.label == 'HC')]
ds_dutch = ds_org_dutch[(ds_org_dutch.label == 'OD') | (ds_org_dutch.label == 'HC')]
#
# # drop filename and grade columns
ds_hun = ds_hun.drop(['filename', 'grade'], axis=1)
ds_dutch = ds_dutch.drop(['filename', 'grade'], axis=1)
#
# print(ds_hun)
# # label_encoder OD and HC to 0 and 1
labelencoder = LabelEncoder()
ds_hun['label'] = labelencoder.fit_transform(ds_hun['label'])
ds_dutch['label'] = labelencoder.fit_transform(ds_dutch['label'])

# Scaling features to 0-1 range
scaler = MinMaxScaler()
ds_hun = scaler.fit_transform(ds_hun)
ds_dutch = scaler.fit_transform(ds_dutch)

ds_hun = pd.DataFrame(ds_hun)
ds_dutch = pd.DataFrame(ds_dutch)

# split the data to X and y
X_hun = ds_hun.iloc[:, 1:192]
y_hun = ds_hun.iloc[:, 193]
X_dutch = ds_dutch.iloc[:, 1:192]
y_dutch = ds_dutch.iloc[:, 193]
X = pd.concat([X_hun, X_dutch])
y = pd.concat([y_hun, y_dutch])
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.8, random_state=0)

# from sklearn.model_selection import GridSearchCV
# param_grid = {'C': [0.1, 1, 10, 100, 1000], 'gamma': [1, 0.1,0.4, 0.01, 0.001, 0.0001], 'kernel': ['rbf']}
# grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=3)
# grid.fit(X_dutch, y_dutch)
# grid_predictions = grid.predict(X_hun)
# print("Accuracy:", metrics.accuracy_score(y_hun, grid_predictions))
# # print the best parameters
# print(grid.best_params_)
# # print the best estimator
# print(grid.best_estimator_)
# # print the best score
# print(grid.best_score_)
# # classification report
# # print(classification_report(y_hun, grid_predictions))


# 1, 0.1 (0.4)




svc = SVC(kernel='rbf', C=1000, gamma=0.001)
svc.fit(X_train, y_train)
prediction = svc.predict(X_test)

#confusion matrix
cm = confusion_matrix(y_test, prediction)
#acurracy score round to 2 decimals
acc = round(metrics.accuracy_score(y_test, prediction), 2)
print('Accuracy:', acc)
#senstivity round to 2 decimals
sens = round(cm[0, 0] / (cm[0, 0] + cm[0, 1]), 2)
print('Sensitivity:', sens)
#specificity round to 2 decimals
spec = round(cm[1, 1] / (cm[1, 0] + cm[1, 1]), 2)
print('Specificity:', spec)
#f1 score round to 2 decimals
f1 = round(metrics.f1_score(y_test, prediction), 2)
print('F1 score:', f1)