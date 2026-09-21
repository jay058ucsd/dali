import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, LocallyLinearEmbedding
import uuid

# Load iris dataset
iris = load_iris()
data = pd.DataFrame(data=iris.data, columns=iris.feature_names)
data['species'] = iris.target
species_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
data['species'] = data['species'].map(species_map)

# Print dataset information
print(f"Dataset shape:\n{data.shape}")
print(f"Column names:\n{data.columns.tolist()}")
print(f"Data types:\n{data.dtypes}")
print(f"First few rows:\n{data.head()}")

# Plot scatter plots for each pair of features
feature_pairs = [
    ('sepal length (cm)', 'sepal width (cm)'),
    ('petal length (cm)', 'petal width (cm)'),
    ('sepal length (cm)', 'petal length (cm)'),
    ('sepal width (cm)', 'petal width (cm)'),
]
for feature1, feature2 in feature_pairs:
    plt.figure(figsize=(10, 6))
    plt.scatter(data[feature1], data[feature2], c=pd.Categorical(data['species']).codes)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.title(f'{feature1} vs {feature2}')
    plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
    plt.show()

# Plot histograms for each feature
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

# Plot box plots for each feature
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
plt.show()

# Calculate and print mean and standard deviation for each feature
for species in data['species'].unique():
    species_data = data[data['species'] == species]
    print(f"Species: {species}")
    print(f"Sepal Length Mean: {np.mean(species_data['sepal length (cm)'])}, Std: {np.std(species_data['sepal length (cm)'])}")
    print(f"Sepal Width Mean: {np.mean(species_data['sepal width (cm)'])}, Std: {np.std(species_data['sepal width (cm)'])}")
    print(f"Petal Length Mean: {np.mean(species_data['petal length (cm)'])}, Std: {np.std(species_data['petal length (cm)'])}")
    print(f"Petal Width Mean: {np.mean(species_data['petal width (cm)'])}, Std: {np.std(species_data['petal width (cm)'])}")
    print()

# Calculate and print correlation between each feature and sepal length
for column in data.columns[:-1]:
    print(f"{column} Correlation: {data[column].corr(data['sepal length (cm)'])}")

# Calculate and print ANOVA F-statistic and p-value for each feature
from scipy.stats import f_oneway
for column in data.columns[:-1]:
    species_data = [data[data['species'] == species][column] for species in data['species'].unique()]
    f_stat, p_val = f_oneway(*species_data)
    print(f"{column} ANOVA F-statistic: {f_stat}, p-value: {p_val}")

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
plt.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', label=v, markerfacecolor='C'+str(i), markersize=10) for i, v in enumerate(species_map.values())], loc='upper right')
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