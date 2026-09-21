import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
print(f"Dataset shape:\n{data.shape}")
print(f"Column names:\n{data.columns.tolist()}")
print(f"Data types:\n{data.dtypes}")
print(f"First few rows:\n{data.head()}")
data['species'] = iris.target
species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
data['species'] = data['species'].map(species_map)
plt.figure(figsize=(10, 6))
plt.scatter(data['sepal length (cm)'], data['sepal width (cm)'], c=pd.Categorical(data['species']).codes)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.title('Sepal Length vs Sepal Width')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
plt.show()
plt.figure(figsize=(10, 6))
plt.scatter(data['petal length (cm)'], data['petal width (cm)'], c=pd.Categorical(data['species']).codes)
plt.xlabel('Petal Length (cm)')
plt.ylabel('Petal Width (cm)')
plt.title('Petal Length vs Petal Width')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
plt.show()
plt.figure(figsize=(10, 6))
plt.scatter(data['sepal length (cm)'], data['petal length (cm)'], c=pd.Categorical(data['species']).codes)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Petal Length (cm)')
plt.title('Sepal Length vs Petal Length')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
plt.show()
plt.figure(figsize=(10, 6))
plt.scatter(data['sepal width (cm)'], data['petal width (cm)'], c=pd.Categorical(data['species']).codes)
plt.xlabel('Sepal Width (cm)')
plt.ylabel('Petal Width (cm)')
plt.title('Sepal Width vs Petal Width')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
plt.savefig('1789953289_Sepal_Width_vs_Petal_Width.png')
plt.show()
import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

for i, species in enumerate(data['species'].unique()):
    species_data = data[data['species'] == species]
    axs[0, 0].hist(species_data['sepal length (cm)'], alpha=0.5, label=species)
    axs[0, 1].hist(species_data['sepal width (cm)'], alpha=0.5, label=species)
    axs[1, 0].hist(species_data['petal length (cm)'], alpha=0.5, label=species)
    axs[1, 1].hist(species_data['petal width (cm)'], alpha=0.5, label=species)

axs[0, 0].set_title('Sepal Length')
axs[0, 0].set_xlabel('Length (cm)')
axs[0, 0].set_ylabel('Frequency')
axs[0, 0].legend()

axs[0, 1].set_title('Sepal Width')
axs[0, 1].set_xlabel('Width (cm)')
axs[0, 1].set_ylabel('Frequency')
axs[0, 1].legend()

axs[1, 0].set_title('Petal Length')
axs[1, 0].set_xlabel('Length (cm)')
axs[1, 0].set_ylabel('Frequency')
axs[1, 0].legend()

axs[1, 1].set_title('Petal Width')
axs[1, 1].set_xlabel('Width (cm)')
axs[1, 1].set_ylabel('Frequency')
axs[1, 1].legend()

plt.tight_layout()
plt.show()
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

for i, species in enumerate(data['species'].unique()):
    species_data = data[data['species'] == species]
    axs[0, 0].boxplot(species_data['sepal length (cm)'], positions=[i], widths=0.5)
    axs[0, 1].boxplot(species_data['sepal width (cm)'], positions=[i], widths=0.5)
    axs[1, 0].boxplot(species_data['petal length (cm)'], positions=[i], widths=0.5)
    axs[1, 1].boxplot(species_data['petal width (cm)'], positions=[i], widths=0.5)

axs[0, 0].set_title('Sepal Length')
axs[0, 0].set_xlabel('Species')
axs[0, 0].set_ylabel('Length (cm)')
axs[0, 0].set_xticks(range(len(data['species'].unique())))
axs[0, 0].set_xticklabels(data['species'].unique())

axs[0, 1].set_title('Sepal Width')
axs[0, 1].set_xlabel('Species')
axs[0, 1].set_ylabel('Width (cm)')
axs[0, 1].set_xticks(range(len(data['species'].unique())))
axs[0, 1].set_xticklabels(data['species'].unique())

axs[1, 0].set_title('Petal Length')
axs[1, 0].set_xlabel('Species')
axs[1, 0].set_ylabel('Length (cm)')
axs[1, 0].set_xticks(range(len(data['species'].unique())))
axs[1, 0].set_xticklabels(data['species'].unique())

axs[1, 1].set_title('Petal Width')
axs[1, 1].set_xlabel('Species')
axs[1, 1].set_ylabel('Width (cm)')
axs[1, 1].set_xticks(range(len(data['species'].unique())))
axs[1, 1].set_xticklabels(data['species'].unique())

plt.tight_layout()
plt.savefig('1789953313_Petal_Width.png')
plt.show()
import numpy as np

for species in data['species'].unique():
    species_data = data[data['species'] == species]
    print(f"Species: {species}")
    print(f"Sepal Length Mean: {np.mean(species_data['sepal length (cm)'])}, Std: {np.std(species_data['sepal length (cm)'])}")
    print(f"Sepal Width Mean: {np.mean(species_data['sepal width (cm)'])}, Std: {np.std(species_data['sepal width (cm)'])}")
    print(f"Petal Length Mean: {np.mean(species_data['petal length (cm)'])}, Std: {np.std(species_data['petal length (cm)'])}")
    print(f"Petal Width Mean: {np.mean(species_data['petal width (cm)'])}, Std: {np.std(species_data['petal width (cm)'])}")
    print()

for column in data.columns[:-1]:
    print(f"{column} Correlation: {data[column].corr(data['sepal length (cm)'])}")

from scipy.stats import f_oneway
for column in data.columns[:-1]:
    species_data = [data[data['species'] == species][column] for species in data['species'].unique()]
    f_stat, p_val = f_oneway(*species_data)
    print(f"{column} ANOVA F-statistic: {f_stat}, p-value: {p_val}")
from sklearn.datasets import load_iris
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
print(f"Dataset shape:\n{data.shape}")
print(f"Column names:\n{data.columns.tolist()}")
print(f"Data types:\n{data.dtypes}")
print(f"First few rows:\n{data.head()}")
data['species'] = iris.target
species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
data['species'] = data['species'].map(species_map)
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(data.drop('species', axis=1))
pca_df = pd.DataFrame(data=pca_data, columns=['Principal Component 1', 'Principal Component 2'])
pca_df['species'] = data['species']
print(f"Explained Variance:\n{pca.explained_variance_ratio_}")
print(f"Dataset shape after PCA:\n{pca_df.shape}")
print(f"Column names after PCA:\n{pca_df.columns.tolist()}")
print(f"Data types after PCA:\n{pca_df.dtypes}")
print(f"First few rows after PCA:\n{pca_df.head()}")
plt.figure(figsize=(10, 6))
plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'], c=pd.Categorical(pca_df['species']).codes)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
plt.show()
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

pca = PCA(n_components=3)
pca_data = pca.fit_transform(data.drop('species', axis=1))
pca_df = pd.DataFrame(data=pca_data, columns=['Principal Component 1', 'Principal Component 2', 'Principal Component 3'])
pca_df['species'] = data['species']

print(f"Explained Variance:\n{pca.explained_variance_ratio_}")
print(f"Dataset shape after PCA:\n{pca_df.shape}")
print(f"Column names after PCA:\n{pca_df.columns.tolist()}")
print(f"Data types after PCA:\n{pca_df.dtypes}")
print(f"First few rows after PCA:\n{pca_df.head()}")

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(projection='3d')
for species in pca_df['species'].unique():
    species_data = pca_df[pca_df['species'] == species]
    ax.scatter(species_data['Principal Component 1'], species_data['Principal Component 2'], species_data['Principal Component 3'], label=species)
ax.set_xlabel('Principal Component 1')
ax.set_ylabel('Principal Component 2')
ax.set_zlabel('Principal Component 3')
ax.set_title('PCA')
ax.legend()
plt.show()

import uuid
plt.savefig(f'{uuid.uuid4().int}_PCA.png')
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

tsne = TSNE(n_components=2, random_state=42)
tsne_data = tsne.fit_transform(data.drop('species', axis=1))
tsne_df = pd.DataFrame(data=tsne_data, columns=['t-SNE Component 1', 't-SNE Component 2'])
tsne_df['species'] = data['species']

print(f"Dataset shape after t-SNE:\n{tsne_df.shape}")
print(f"Column names after t-SNE:\n{tsne_df.columns.tolist()}")
print(f"Data types after t-SNE:\n{tsne_df.dtypes}")
print(f"First few rows after t-SNE:\n{tsne_df.head()}")

plt.figure(figsize=(10, 6))
plt.scatter(tsne_df['t-SNE Component 1'], tsne_df['t-SNE Component 2'], c=pd.Categorical(tsne_df['species']).codes)
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.title('t-SNE')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(data['species'].unique())], loc='upper right')
plt.show()
from sklearn.manifold import LocallyLinearEmbedding
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import uuid

lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10, eigen_solver='arpack')
lle_data = lle.fit_transform(data.drop('species', axis=1))
lle_df = pd.DataFrame(data=lle_data, columns=['LLE Component 1', 'LLE Component 2'])
lle_df['species'] = data['species']

print(f"Dataset shape after LLE:\n{lle_df.shape}")
print(f"Column names after LLE:\n{lle_df.columns.tolist()}")
print(f"Data types after LLE:\n{lle_df.dtypes}")
print(f"First few rows after LLE:\n{lle_df.head()}")

plt.figure(figsize=(10, 6))
plt.scatter(lle_df['LLE Component 1'], lle_df['LLE Component 2'], c=pd.Categorical(lle_df['species']).codes)
plt.xlabel('LLE Component 1')
plt.ylabel('LLE Component 2')
plt.title('LLE')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(data['species'].unique())], loc='upper right')
plt.show()
plt.savefig(f'{uuid.uuid4().int}_LLE.png')
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, LocallyLinearEmbedding
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import uuid

# Apply PCA
pca = PCA(n_components=2)
pca_data = pca.fit_transform(data.drop('species', axis=1))
pca_df = pd.DataFrame(data=pca_data, columns=['Principal Component 1', 'Principal Component 2'])
pca_df['species'] = data['species']

print(f"Explained Variance:\n{pca.explained_variance_ratio_}")
print(f"Dataset shape after PCA:\n{pca_df.shape}")
print(f"Column names after PCA:\n{pca_df.columns.tolist()}")
print(f"Data types after PCA:\n{pca_df.dtypes}")
print(f"First few rows after PCA:\n{pca_df.head()}")

plt.figure(figsize=(10, 6))
plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'], c=pd.Categorical(pca_df['species']).codes)
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(data['species'].unique())], loc='upper right')
plt.show()
plt.savefig(f'{uuid.uuid4().int}_PCA.png')

# Apply t-SNE
tsne = TSNE(n_components=2, random_state=42)
tsne_data = tsne.fit_transform(data.drop('species', axis=1))
tsne_df = pd.DataFrame(data=tsne_data, columns=['t-SNE Component 1', 't-SNE Component 2'])
tsne_df['species'] = data['species']

print(f"Dataset shape after t-SNE:\n{tsne_df.shape}")
print(f"Column names after t-SNE:\n{tsne_df.columns.tolist()}")
print(f"Data types after t-SNE:\n{tsne_df.dtypes}")
print(f"First few rows after t-SNE:\n{tsne_df.head()}")

plt.figure(figsize=(10, 6))
plt.scatter(tsne_df['t-SNE Component 1'], tsne_df['t-SNE Component 2'], c=pd.Categorical(tsne_df['species']).codes)
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.title('t-SNE')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(data['species'].unique())], loc='upper right')
plt.show()
plt.savefig(f'{uuid.uuid4().int}_tSNE.png')

# Apply LLE
lle = LocallyLinearEmbedding(n_components=2, n_neighbors=10, eigen_solver='arpack')
lle_data = lle.fit_transform(data.drop('species', axis=1))
lle_df = pd.DataFrame(data=lle_data, columns=['LLE Component 1', 'LLE Component 2'])
lle_df['species'] = data['species']

print(f"Dataset shape after LLE:\n{lle_df.shape}")
print(f"Column names after LLE:\n{lle_df.columns.tolist()}")
print(f"Data types after LLE:\n{lle_df.dtypes}")
print(f"First few rows after LLE:\n{lle_df.head()}")

plt.figure(figsize=(10, 6))
plt.scatter(lle_df['LLE Component 1'], lle_df['LLE Component 2'], c=pd.Categorical(lle_df['species']).codes)
plt.xlabel('LLE Component 1')
plt.ylabel('LLE Component 2')
plt.title('LLE')
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(data['species'].unique())], loc='upper right')
plt.show()
plt.savefig(f'{uuid.uuid4().int}_LLE.png')