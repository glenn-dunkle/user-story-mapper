import numpy as np
import pandas as pd
import openai as ai
from src.util.config_helper import CONFIG
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

class AffinityGrouper:
    def __init__(self):
        self.model_name = CONFIG["ai_grouping"]["AI_MODEL_NAME"]
        self.n_clusters = CONFIG["ai_grouping"]["AI_CLUSTERS"]
        self.n_distance_threshold = CONFIG["ai_grouping"]["AI_DISTANCE_THRESHOLD"]
        self.agglomerative_type = CONFIG["ai_grouping"]["AI_AGGLOMERATIVE_TYPE"]
        self.agglomerative_linkage = CONFIG["ai_grouping"]["AI_LINKAGE_TYPE"]
        self.agglomerative_metric = CONFIG["ai_grouping"]["AI_METRIC_TYPE"]
        self.openai_api_key = CONFIG["ai_grouping"]["OPEN_AI_API_KEY"]

    def __find_centroid_sentence(self, sentences, embeddings):
        cluster_center = np.mean(embeddings, axis=0)
        similarities = np.inner(embeddings, cluster_center)
        return sentences[np.argmax(similarities)]

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
#        embeddings = embeddings.cpu().numpy()
        clustering_model = AgglomerativeClustering(n_clusters=n_clusters, distance_threshold=n_distance_threshold, linkage=self.agglomerative_linkage, metric=self.agglomerative_metric, compute_full_tree=True)
        clustering_model.fit(embeddings)
        labels = clustering_model.labels_
        print(clustering_model.labels_)

        df = pd.DataFrame({
            "text": notes,
            "embedding": list(embeddings),
            "label": labels
        })

        # Group notes by their cluster labels
        clusters = {}
        ai.api_key = self.openai_api_key

        for label in sorted(df["label"].unique()):
            cluster_df = df[df["label"] == label]
            cluster_texts = cluster_df["text"].tolist()
            
            # Use most central sentence as label
#            cluster_embeddings = np.array(cluster_df["embedding"].tolist())
#            label_sentence = self.__find_centroid_sentence(cluster_texts, cluster_embeddings)

            # Use average centroid of all sentences as label; combine all sentences in the cluster
            combined_text = " ".join(cluster_texts)
            
            # Create a prompt for summarization
            prompt = f"Briefly summarize the main theme of these related items as an activity in 5-7 words: {combined_text}"

            # Requesting a summary from ChatGPT (using the chat-completion API)
            response = ai.chat.completions.create(
                model="gpt-3.5-turbo",  # Or "gpt-4" if you want to use a different version
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}
                ],
                max_tokens=100,  # Limit the length of the summary
                temperature=0.3  # Controls randomness, lower is more deterministic
            )

            # Extract and assign label as the summary from the response
            response_dict = response.to_dict()
            summary = response_dict['choices'][0]['message']['content'].strip()

            label_sentence = f"{summary}"   # ({len(cluster_texts)} items)"
            
            clusters[label_sentence] = cluster_texts

#        for group_label, entries in clusters.items():
#            print(f"\n🔹 {group_label}")
#            print("-" * (len(group_label) + 3))
#            for entry in entries:
#                print(f"• {entry}")

        return clusters
  

    def printAffinityGroups(self, affinity_groups):
        for cluster_id, stories in affinity_groups.items():
#            cluster_title = f"{cluster_id}"

            # Create an Epic (blue card)
            epic_payload = {
                "title": cluster_id,
                "cardType": "epic",  # or "step" for yellow, "story" for white
            }

            print(f"Epic: {cluster_id}")

            for story in stories:
                story_payload = {
                    "title": story,
                    "cardType": "story",
                    "parentId": cluster_id
                }
                print(f"└── Story: {story}")
 