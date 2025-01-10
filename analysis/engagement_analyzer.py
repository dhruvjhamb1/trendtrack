import requests
import json
import os
from requests.adapters import HTTPAdapter

class EngagementAnalyzer:
    def __init__(self, db):
        self.db = db
        self.base_api_url = "https://api.langflow.astra.datastax.com"
        self.langflow_id = "d6b3208e-b8d1-469a-970d-e069c4573743"
        self.flow_id = "788b6b11-f179-4b8f-a47d-5a0e6e5de57f"
        self.application_token = os.getenv('LANGFLOW_APPLICATION_TOKEN')
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter())

    def _run_flow(self, message: str, tweaks: dict = None) -> dict:
        api_url = f"{self.base_api_url}/lf/{self.langflow_id}/api/v1/run/{self.flow_id}"
        
        message_data = json.loads(message)
        payload = {
            "input_value": message_data['data']['metrics']['text'],
            "output_type": "chat",
            "input_type": "chat"
        }
        
        if tweaks:
            payload["tweaks"] = tweaks
        
        headers = {
            "Authorization": f"Bearer {self.application_token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = self.session.post(api_url, json=payload, headers=headers)
            response_data = response.json()
            response.raise_for_status()
            
            if 'outputs' in response_data:
                for output in response_data.get('outputs', []):
                    for inner_output in output.get('outputs', []):
                        if 'results' in inner_output:
                            message_data = inner_output['results'].get('message', {})
                            if isinstance(message_data, dict) and 'text' in message_data:
                                return {"result": message_data['text'].strip()}
            
            return {"error": "Could not extract insights from response"}
                
        except Exception as e:
            return {"error": f"Failed to communicate with Langflow: {str(e)}"}

    def analyze_post_type(self, post_type):
        all_metrics = self.db.get_engagement_metrics()
        if not all_metrics:
            return {"error": "No data found"}
        
        metrics_by_type = {m['post_type']: m for m in all_metrics}
        if post_type not in metrics_by_type:
            return {"error": f"No data found for {post_type}"}
        
        current_metrics = metrics_by_type[post_type]
        other_types = [t for t in metrics_by_type.keys() if t != post_type]
        
        if not other_types:
            return {"error": "No other post types available for comparison"}
        
        comparison_type = min(
            other_types,
            key=lambda x: metrics_by_type[x]['avg_engagement_rate']
        )

        message = {
            "data": {
                "post_type": post_type,
                "metrics": {
                    "text": (
                        f"Based on these metrics for {post_type}:\n"
                        f"Likes: {current_metrics['avg_likes']:.2f}\n"
                        f"Shares: {current_metrics['avg_shares']:.2f}\n"
                        f"Comments: {current_metrics['avg_comments']:.2f}\n"
                        f"Reach: {current_metrics['avg_reach']:.2f}\n"
                        f"Engagement: {current_metrics['avg_engagement_rate']:.2f}%\n\n"
                        f"RESPOND WITH EXACTLY 2 TIPS IN THIS FORMAT:\n"
                        f"1. [Single action] → [X]% increase in [metric]\n"
                        f"2. [Single action] → [X]% increase in [metric]"
                    )
                }
            }
        }
        
        tips_result = self._run_flow(json.dumps(message))
        ai_tips = tips_result.get('result', 'Unable to generate tips')

        complete_insights = (
            f"Metrics for {post_type}:\n"
            f"• Average Likes: {current_metrics['avg_likes']:.2f}\n"
            f"• Average Shares: {current_metrics['avg_shares']:.2f}\n"
            f"• Average Comments: {current_metrics['avg_comments']:.2f}\n"
            f"• Average Reach: {current_metrics['avg_reach']:.2f}\n"
            f"• Average Engagement Rate: {current_metrics['avg_engagement_rate']:.2f}%\n"
            f"\n"
            f"Key Insights:\n"
            f"• {post_type.capitalize()} vs {comparison_type}: {self._calculate_comparison(current_metrics['avg_shares'], metrics_by_type[comparison_type]['avg_shares'])}x more shares\n"
            f"• Engagement: {self._calculate_percentage_diff(current_metrics['avg_engagement_rate'], self._get_avg_metric_other_types(metrics_by_type, post_type, 'avg_engagement_rate'))}% vs other formats\n"
            f"• Reach: {self._calculate_comparison(current_metrics['avg_reach'], self._get_avg_metric_other_types(metrics_by_type, post_type, 'avg_reach'))}x more views\n"
            f"• Comments: {self._calculate_percentage_diff(current_metrics['avg_comments'], self._get_avg_metric_other_types(metrics_by_type, post_type, 'avg_comments'))}% vs others\n"
            f"\n"
            f"AI Tips:\n"
            f"{ai_tips}"
        )

        return {
            "metrics": current_metrics,
            "insights": complete_insights
        }

    def _calculate_comparison(self, value1, value2):
        return round(value1 / value2, 1)

    def _calculate_percentage_diff(self, value1, value2):
        return round(((value1 - value2) / value2) * 100)

    def _get_avg_metric_other_types(self, metrics_by_type, exclude_type, metric_name):
        other_types = [m[metric_name] for t, m in metrics_by_type.items() if t != exclude_type]
        return sum(other_types) / len(other_types)

    def generate_insights(self):
        all_metrics = self.db.get_engagement_metrics()
        if not all_metrics:
            return {"error": "No data available for analysis"}
            
        try:
            message = {
                "data": {
                    "metrics": {
                        "text": (
                            "Compare these metrics between post types:\n\n"
                            "• Reels vs Others: Compare engagement rate and reach\n"
                            "• Carousel vs Others: Compare shares and comments\n"
                            "• Static vs Others: Compare overall performance\n\n"
                            "Provide EXACTLY 5 bullet points comparing metrics between types.\n"
                            "Format EXACTLY like this:\n"
                            "• [Type A] has [X]% higher [metric] than [Type B]\n"
                            "• [Type A] generates [X]x more [metric] than [Type B]\n"
                            "DO NOT provide any additional analysis or text."
                        )
                    }
                }
            }
            
            flow_result = self._run_flow(json.dumps(message))
            
            if 'error' in flow_result:
                return flow_result
                
            return {
                "metrics": all_metrics,
                "insights": flow_result.get('result', 'No insights generated')
            }
            
        except Exception as e:
            return {"error": f"Failed to generate insights: {str(e)}"}