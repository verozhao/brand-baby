# Brand Baby

**AI-Powered Content Creation Platform**

![Brand Baby](image.png)

## Overview

Brand Baby is a Flask-based web application that helps content creators generate video ideas and analyze viral content using AI models.

## Features

### YouTube Viral Analysis Dashboard
- Track viral metrics across different genres (Gaming, Music, Education, Tech, Lifestyle)
- Analyze engagement metrics (views, likes, comments)
- Filter and sort content by various metrics
- Detailed video analysis with engagement scores and recommendations

### Content Calculator
- Combine multiple content references using mathematical operations
- Input types:
  - YouTube links
  - Genre categories
  - Creator usernames
- Generate hybrid content ideas with OpenAI GPT-4
- Auto-generate video scripts and thumbnails using DALL-E 3

## Tech Stack

- Backend: Flask
- Frontend: HTML/CSS/JavaScript
- AI Models:
  - OpenAI GPT-4 for content generation
  - DALL-E 3 for thumbnail generation
  - YouTube Data API v3 for analytics
  
## Dependencies

```bash
pip install flask openai youtube-transcript-api moviepy
```

## Configuration

Create a `.env` file with required API keys:
```env
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
```

## Running Locally

```bash
# Clone repository
git clone https://github.com/yourusername/brand-baby.git
cd brand-baby

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

Server runs on http://localhost:5001

## Features in Detail

### Dashboard
- Video transcription and analysis
- Comment extraction and sentiment analysis
- Engagement metrics calculation
- Trend pattern detection
- Content recommendations

### Calculator
- Reference content combination
- Script generation
- Thumbnail creation
- Brand partnership suggestions

## License
MIT