# Social Media Insights

A basic analytics module using Langflow and DataStax to analyze engagement data from mock social media accounts.

## Features

- Analyze engagement metrics for different post types (carousel, reels, static posts)
- Generate AI-powered insights using GPT integration
- Clean and modern web interface
- Mock data generation for testing

## Prerequisites

- Python 3.7+
- DataStax Astra DB account
- OpenAI API key
- Langflow installation

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd social_media_insights
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Fill in your DataStax Astra DB credentials
- Add your OpenAI API key
- Specify the path to your Astra DB secure connect bundle

4. Initialize the database:
- Create a keyspace in your Astra DB instance
- The application will automatically create the necessary tables on first run

## Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

1. Click on different post type buttons to view engagement metrics
2. Use the "Generate Insights" button to get AI-powered analysis
3. View metrics and insights in the clean web interface

## Project Structure

- `/static` - CSS and JavaScript files
- `/templates` - HTML templates
- `/database` - Database connection and operations
- `/analysis` - Engagement analysis and AI integration

## Contributing

Feel free to submit issues and enhancement requests! 