import numpy as np
from src.util.config_helper import CONFIG
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

class AffinityGrouper:
    def __init__(self):
        self.model_name = CONFIG["ai_grouping"]["AI_MODEL_NAME"]
        self.n_clusters = CONFIG["ai_grouping"]["AI_CLUSTERS"]
        self.n_distance_threshold = CONFIG["ai_grouping"]["AI_DISTANCE_THRESHOLD"]
        self.agglomerative_type = CONFIG["ai_grouping"]["AI_AGGLOMERATIVE_TYPE"]

#    def fit(self, texts):
#        embeddings = self.model.encode(texts, convert_to_tensor=True)
#        embeddings = embeddings.cpu().numpy()
        
#        clustering_model = AgglomerativeClustering(n_clusters=self.n_clusters, affinity='cosine', linkage='average')
#        self.labels_ = clustering_model.fit_predict(embeddings)

#    def predict(self, texts):
#        return self.labels_
        
    def getAffinityGroups(self,
                      notes,
                      model_name=None,
                      n_clusters=None,
                      n_distance_threshold=None):
        model_name = model_name if model_name else self.model_name
        # Determine the type of agglomerative clustering to use, either by distance threshold or number of clusters. Set the other to None.
        if self.agglomerative_type == "distance":
            n_clusters = None
            n_distance_threshold = n_distance_threshold if n_distance_threshold else self.n_distance_threshold
        elif self.agglomerative_type == "clusters":
            n_distance_threshold = None
            n_clusters = n_clusters if n_clusters else self.n_clusters
        else:
            raise ValueError(f"Unknown agglomerative type: {self.agglomerative_type}")
        
        model = SentenceTransformer(model_name)
        
        embeddings = model.encode(notes, convert_to_tensor=True)
        embeddings = embeddings.cpu().numpy()
        clustering_model = AgglomerativeClustering(n_clusters=n_clusters, distance_threshold=n_distance_threshold, metric='cosine', linkage='average')
        labels = clustering_model.fit_predict(embeddings)

        # Group notes by their cluster labels
        clusters = {}
        for label, note in zip(labels, notes):
            clusters.setdefault(label, []).append(note)
        return clusters
