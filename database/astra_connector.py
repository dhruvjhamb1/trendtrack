from astrapy import DataAPIClient
import os
import pandas as pd

class AstraDB:
    def __init__(self):
        try:
            token = os.getenv('ASTRA_DB_TOKEN')
            endpoint = os.getenv('ASTRA_DB_ENDPOINT')
            print(f"Initializing AstraDB with endpoint: {endpoint}")
            
            self.client = DataAPIClient(token)
            self.db = self.client.get_database(endpoint)
            self.keyspace = "default_keyspace"
            self.collection_name = "social_posts"
            print("Successfully initialized AstraDB client")
        except Exception as e:
            print(f"Error initializing AstraDB: {str(e)}")
            raise
        
    def _ensure_collection(self):
        """Create the collection if it doesn't exist."""
        try:
            self.db.use_keyspace(self.keyspace)
            print(f"Using keyspace: {self.keyspace}")

            try:
                collection = self.db.create_collection(self.collection_name)
                print(f"Created collection: {self.collection_name}")
            except Exception as e:
                print(f"Collection might already exist: {str(e)}")
                
        except Exception as e:
            print(f"Error in _ensure_collection: {str(e)}")
            raise
        
    def import_csv_data(self, csv_path=None):
        """Import data from the engagement CSV file."""
        try:
            if csv_path is None:
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                csv_path = os.path.join(current_dir, 'engagement.csv')
            
            print(f"\nStarting CSV import from: {csv_path}")
            self._ensure_collection()
            
            print("Reading CSV file...")
            df = pd.read_csv(csv_path)
            print(f"Read {len(df)} records from CSV")
            
            collection = self.db[self.collection_name]
            
            try:
                print("Clearing existing data...")
                collection.delete_many({})
                print("Cleared existing data")
            except Exception as e:
                print(f"Error clearing data (continuing anyway): {str(e)}")
            
            print("Inserting new records...")
            success_count = 0
            batch_size = 100
            records = []
            
            for _, row in df.iterrows():
                post_data = {
                    "post_id": str(row['Post ID']),
                    "post_type": row['Post Type'].lower(),
                    "likes": int(row['Likes']),
                    "shares": int(row['Shares']),
                    "comments": int(row['Comments']),
                    "total_reach": int(row['Total Reach']),
                    "total_interactions": int(row['Total Interactions']),
                    "engagement_rate": float(row['Engagement Rate'])
                }
                records.append(post_data)
                
                if len(records) >= batch_size:
                    try:
                        collection.insert_many(records)
                        success_count += len(records)
                        print(f"Inserted {success_count} records...")
                        records = []
                    except Exception as e:
                        print(f"Error inserting batch: {str(e)}")
            
            if records:
                try:
                    collection.insert_many(records)
                    success_count += len(records)
                except Exception as e:
                    print(f"Error inserting final batch: {str(e)}")
                
            print(f"\nSuccessfully imported {success_count} out of {len(df)} records to database")
            
        except Exception as e:
            print(f"Error in import_csv_data: {str(e)}")
            raise
                
    def get_engagement_metrics(self, post_type=None):
        """Get engagement metrics, optionally filtered by post type."""
        try:
            print("\nGetting engagement metrics...")
            self._ensure_collection()
            
            collection = self.db[self.collection_name]
            
            print("Fetching documents...")
            if post_type:
                print(f"Filtering by post_type: {post_type}")
                documents = collection.find({"post_type": post_type})
            else:
                documents = collection.find({})
            
            if not documents:
                print("No documents found")
                return []
                
            documents = list(documents)
            print(f"Found {len(documents)} documents")
            
            metrics_by_type = {}
            for doc in documents:
                ptype = doc["post_type"]
                if ptype not in metrics_by_type:
                    metrics_by_type[ptype] = {
                        "likes": [], "shares": [], "comments": [],
                        "total_reach": [], "total_interactions": [],
                        "engagement_rate": []
                    }
                
                metrics_by_type[ptype]["likes"].append(doc["likes"])
                metrics_by_type[ptype]["shares"].append(doc["shares"])
                metrics_by_type[ptype]["comments"].append(doc["comments"])
                metrics_by_type[ptype]["total_reach"].append(doc["total_reach"])
                metrics_by_type[ptype]["total_interactions"].append(doc["total_interactions"])
                metrics_by_type[ptype]["engagement_rate"].append(doc["engagement_rate"])
            
            results = []
            for ptype, values in metrics_by_type.items():
                results.append({
                    "post_type": ptype,
                    "avg_likes": sum(values["likes"]) / len(values["likes"]),
                    "avg_shares": sum(values["shares"]) / len(values["shares"]),
                    "avg_comments": sum(values["comments"]) / len(values["comments"]),
                    "avg_reach": sum(values["total_reach"]) / len(values["total_reach"]),
                    "avg_interactions": sum(values["total_interactions"]) / len(values["total_interactions"]),
                    "avg_engagement_rate": sum(values["engagement_rate"]) / len(values["engagement_rate"])
                })
            
            print(f"Calculated metrics for {len(results)} post types")
            return results
            
        except Exception as e:
            print(f"Error in get_engagement_metrics: {str(e)}")
            return [] 