# TrendTrack: Social Media Insights Platform 🚀

> 🏆 Project submission for Level SuperMind Pre-Hackathon

A powerful social media analytics platform that leverages AI to provide deep insights into engagement patterns and content performance. 📊

## 🌟 Features

- Social media engagement pattern analysis
- AI-powered engagement insights using Langflow with Google Gemini API
- Interactive data visualization dashboard
- Historical data analysis with CSV support
- Secure data persistence with AstraDB

## 🛠 How It Works

1. **Data Collection** 📥
   - Upload your social media engagement data via CSV
   - Data is securely stored in AstraDB for persistence

2. **Analysis Pipeline** 🔍
   - Engagement data is processed using Pandas for initial analysis
   - GPT integration provides AI-powered insights on engagement patterns
   - Results are cached in AstraDB for quick retrieval

3. **Visualization** 📊
   - Chart.js renders interactive visualizations
   - Real-time updates as new data is processed
   - Customizable dashboard views for different metrics

4. **Insights Generation** 📊
   - AI analyzes engagement patterns
   - Highlights high engagement content formats.
   - Provides tips to improve the reach and engagement on particular content format.

## 🛠️ Technologies Used

### Backend
- **Python**  - Core programming language
- **Flask**  - Web framework
- **LangFlow** - AI workflow management with GPT integration
- **AstraDB** - Scalable Vector database
- **Pandas** - Data analysis and manipulation

### Frontend
- **HTML** 📝 - Structure
- **CSS** 🎨 - Styling
- **JavaScript** ⚡ - Interactive features
- **Chart.js** 📈 - Data visualization

## 📁 Project Structure

```
trendtrack/
├── analysis/
│   └── engagement_analyzer.py    # Engagement analysis logic
├── database/
│   └── astra_connector.py       # AstraDB connection handling
├── templates/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── index.html              # Main dashboard template
├── app.py                      # Main Flask application
├── run.py                      # Development server runner
├── requirements.txt            # Project dependencies
└── render_app.py               # Render Deployment 
```

## 📊 Sample CSV Data

The project includes a sample dataset (`engagement.csv`) containing social media engagement metrics:
- Engagement metrics (likes, shares, comments)
- Content categories
- Audience reach

## 🚀 Getting Started

1. Clone the repository
```bash
git clone https://github.com/dhruvjhamb1/trendtrack.git
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
ASTRA_DB_ID=your_db_id
ASTRA_DB_TOKEN=your_token
LANGFLOW_APPLICATION_TOKEN=your_token
FLASK_ENV=production
FLASK_APP=run.py
```

4. Run the application
```bash
python render_app.py
```

## 🌐 Live Demo

Check out the live project at: [TrendTrack](https://trendtrack.onrender.com)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
Built with ❤️ using Python, Flask, Langflow and AstraDB. 
