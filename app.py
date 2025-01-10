from flask import Flask, render_template, jsonify, request
from database.astra_connector import AstraDB
from analysis.engagement_analyzer import EngagementAnalyzer
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, 
           static_url_path='/social_media_insights/templates/static',
           static_folder='templates/static',
           template_folder='templates')

db = AstraDB()
analyzer = EngagementAnalyzer(db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_posts():
    post_type = request.json.get('post_type')
    analysis_results = analyzer.analyze_post_type(post_type)
    
    if 'insights' in analysis_results:
        analysis_results['insights'] = analysis_results['insights'].replace('\n', '<br>')
    
    return jsonify(analysis_results)

@app.route('/api/insights', methods=['GET'])
def get_insights():
    insights = analyzer.generate_insights()
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True) 