import pandas as pd

df = pd.read_excel('data/occupations/3-digit-hisco.xlsx')

df.columns
# concatencate name to "description_(tasks_and_duties)"
df['description'] = df['name'] + " //" + df['description_(tasks_and_duties)']


occupation_names = df['description'].tolist()

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(occupation_names)

import umap

reducer = umap.UMAP(n_components=2, random_state=42)
umap_embeddings = reducer.fit_transform(embeddings)

umap_df = pd.DataFrame(umap_embeddings, columns=['UMAP Component 1', 'UMAP Component 2'])
umap_df['name'] = occupation_names
umap_df.to_excel('umap_occupations.xlsx', index=False)
