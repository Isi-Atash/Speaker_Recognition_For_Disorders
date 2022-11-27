import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import BaggingRegressor


ds_org_hun = pd.read_csv('Xvector_embedding_hun.csv')
ds_org_dutch = pd.read_csv('Xvector_embedding_dutch.csv')

ds_hun = ds_org_hun[(ds_org_hun.label == 'OD') | (ds_org_hun.label == 'HC')]
ds_dutch = ds_org_dutch[(ds_org_dutch.label == 'OD') | (ds_org_dutch.label == 'HC')]

ds_hun = ds_hun.drop(['filename', 'label'], axis=1)
ds_dutch = ds_dutch.drop(['filename', 'label'], axis=1)

# Scaling features to 0-1 range
scaler = MinMaxScaler()
ds_hun = scaler.fit_transform(ds_hun)
ds_dutch = scaler.fit_transform(ds_dutch)

ds_hun = pd.DataFrame(ds_hun)
ds_dutch = pd.DataFrame(ds_dutch)

# split the data to X and y
X_hun = ds_hun.iloc[:, :512]
y_hun = ds_hun.iloc[:, 513]
X_dutch = ds_dutch.iloc[:, :512]
y_dutch = ds_dutch.iloc[:, 513]

# merge the datasets
X = pd.concat([X_hun, X_dutch])
y = pd.concat([y_hun, y_dutch])


scores_H = cross_val_score(LinearRegression(), X_hun, y_hun, cv=10)
print('Linear Regression H Accuracy: %0.2f (+/- %0.2f)' % (scores_H.mean(), scores_H.std() * 2))

scores_D = cross_val_score(LinearRegression(), X_dutch, y_dutch, cv=10)
print('Linear Regression D Accuracy: %0.2f (+/- %0.2f)' % (scores_D.mean(), scores_D.std() * 2))

scores_H_D = cross_val_score(LinearRegression(), X, y, cv=10)
print('Linear Regression H+D Accuracy: %0.2f (+/- %0.2f)' % (scores_H_D.mean(), scores_H_D.std() * 2))


bag_model = BaggingRegressor(LinearRegression(),
                              n_estimators=100,
                              max_samples=0.8,
                              bootstrap=True,
                              oob_score=True)
bag_model.fit(X_hun, y_hun)
print('H Bagging score: ', bag_model.score(X_hun, y_hun))
print('D Bagging score: ', bag_model.score(X_dutch, y_dutch))
print('H+D Bagging score: ', bag_model.score(X, y))
print('OOB score: ', bag_model.oob_score_)
print('OOB accuracy: ', bag_model.oob_score_ * 100)
#
# cross validation
scores = cross_val_score(bag_model, X_hun, y_hun, cv=10)
print('Cross_val H Bagging Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

scores = cross_val_score(bag_model, X_dutch, y_dutch, cv=10)
print('Cross_val D Bagging Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))

scores = cross_val_score(bag_model, X, y, cv=10)
print('Cross_val H+D Bagging Accuracy: %0.2f (+/- %0.2f)' % (scores.mean(), scores.std() * 2))
