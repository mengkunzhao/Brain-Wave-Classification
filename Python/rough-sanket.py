import pandas as pd
import numpy as np

d1 = pd.read_csv('../data/train_subject1_psd01.csv',header=None)
d2 = pd.read_csv('../data/train_subject1_psd02.csv',header=None)
d3 = pd.read_csv('../data/train_subject1_psd03.csv',header=None)
d4 = pd.read_csv('../data/train_subject2_psd01.csv',header=None)
d5 = pd.read_csv('../data/train_subject2_psd02.csv',header=None)
d6 = pd.read_csv('../data/train_subject2_psd03.csv',header=None)
d7 = pd.read_csv('../data/train_subject3_psd01.csv',header=None)
d8 = pd.read_csv('../data/train_subject3_psd02.csv',header=None)
d9 = pd.read_csv('../data/train_subject3_psd03.csv',header=None)
training_data = pd.concat([d1,d2,d3,d4,d5,d6,d7,d8,d9],axis=0)

#continuous_data.corr().to_csv('data/correlation_continuous_data.csv')
training_data = pd.read_csv('../data/training_data_complete.csv')
training_data.corr().to_csv('../data/correlation_matrix.csv',index=False)
#np.corrcoef(continuous_data)
# plot the correlation matrix
from matplotlib import pyplot as plt
from matplotlib import cm as cm
def plotCorrMatrix(data,title='Continuous Feature Correlation Figure 1'):
	fig = plt.figure(figsize = (50,50) )
	ax1 = fig.add_subplot(111)
	cmap = cm.get_cmap('jet', 30)
	cax = ax1.imshow(data.corr(), interpolation="nearest", cmap=cmap)
	ax1.grid(True)
	plt.title(title)
	labels=list(data.columns)
	ax1.set_xticklabels(labels,fontsize=6)
	ax1.set_yticklabels(labels,fontsize=6)
	# Add colorbar, make sure to specify tick locations to match desired ticklabels
	fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
	plt.show()

plotCorrMatrix(training_data, 'Correlation matrix')
# Removing correlated variables
# Stage 1 Rules for removing them: 1. It should be highly correlated to at least 3 variables
corr_matrix = pd.read_csv('../data/correlation_matrix.csv')
vec = list(corr_matrix.iloc[:,0])
correlated_features = set()
cutoff_limit = 0.7
cutoff_count = 3
for i in range(1,len(corr_matrix.columns)):
	for j in range(i+2,len(corr_matrix.columns)):
		if corr_matrix.iloc[i,j] >= cutoff_limit or corr_matrix.iloc[i,j] <= -cutoff_limit:
			correlated_features.add(corr_matrix.iloc[i,0])
			break

correlated_features
# set(['RightApp', 'cumul_UseCount', 'CurrPro_avgProbTimeWE', 'cumul_RightApp', 'MorphCount', 'cumul_WrongApp', 'DirectProofActionCount', 'cumul_Interaction', 'cumul_TotalPSTime', 'cumul_DirectProofActionCount', 'cumul_FDActionCount', 'cumul_AppRatio', 'cumul_WrongSemanticsApp', 'WrongApp', 'WrongSemanticsApp', 'AppRatio', 'BlankRatio', 'cumul_MorphCount', 'cumul_OptionalCount', 'RrightAppRatio', 'cumul_TotalTime', 'FDActionCount', 'CurrPro_avgProbTime', 'TotalTime', 'cumul_actionCount', 'cumul_WrongSyntaxApp', 'cumul_PrepCount', 'CurrPro_avgProbTimePS', 'UseCount', 'actionCount'])
# >>> len(correlated_features)
# 30
vec = list(training_data.columns)
for v in correlated_features:
	vec.remove(v)
uncorrelated_continuous_data = training_data[vec]
uncorrelated_continuous_data.to_csv('../data/uncorrelated_training_data.csv',index=False)
plotCorrMatrix(uncorrelated_continuous_data, 'Matrix after removing highly correlated features')

training_data = pd.read_csv('../data/uncorrelated_training_data.csv')
training_data.head()


# PCA
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing

temp = pd.read_csv('../data/uncorrelated_training_data.csv')
vec = list(temp.columns)
temp = temp[vec[:-1]]
#preprocessing.scale(temp,axis=1,copy=False)
pca = PCA()
temp_pca = pca.fit_transform(temp)
temp_pca = pd.DataFrame(temp_pca)

original_pca = pd.read_csv('data/pca_data.csv')

exp_variance = list(pca.explained_variance_ratio_)

# Try random forest and other classification techniques like SVM
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd
import numpy as np

training_data = pd.read_csv('../data/pca_data.csv')
rf = RandomForestClassifier(n_estimators = 10, n_jobs=-1)
scores = cross_val_score(rf, training_data.iloc[:,:-1], training_data.iloc[:,-1], cv = 10)
print scores