import io
import re
from openai import OpenAI
from utils import *
from moviepy import *
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, render_template, request, redirect, url_for
import json


openai_key = '' # Replace this with your own OpenAI API key

client = OpenAI(api_key=openai_key)

app = Flask(__name__)

GENRES = ['Beauty', 'Comedy', 'Fashion', 'Fitness', 'Food', 'Travel']
OPERATORS = ['+', '-', '*', '/']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text_input = request.form.get('text_input', '')
        print(text_input)
        equation = request.form.get('equation', '')
        categorized_inputs = json.loads(request.form.get('categorized_inputs', '[]'))
        return redirect(url_for('calculate', equation=equation, text_input=text_input, categorized_inputs=json.dumps(categorized_inputs)))
    
    return render_template('index.html', genres=GENRES, operators=OPERATORS)

@app.route('/calculate')
def calculate():
    text_input = request.args.get('text_input', '')
    print(text_input)
    equation = request.args.get('equation', 'No equation provided')
    categorized_inputs = json.loads(request.args.get('categorized_inputs', '[]'))

    print(equation)
    if '-' in equation:
        print('subtraction')
        sub_flag = True
    else:
        sub_flag = False

    input_dict = {item['value']: item['category'] for item in categorized_inputs}
    
    genres = []
    images = []
    commentss = []
    transcripts = []
    
    for value, category in input_dict.items():
        if category == 'genre':
            print(f'Genre: {value}')
            genres.append(value)

        else:
            print(f'Link: {value}')
            match = re.search(r"v=([A-Za-z0-9_-]+)", value)
            video_id = match.group(1)
            print(f"Video ID: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
            
            try:
                comments = extract_comments(value)  
                commentss.append(comments[:10])
            except:
                pass       
            transcripts.append(transcript)
            images.append(thumbnail)
            import requests; open(f"{video_id}_thumbnail.jpg", "wb").write(requests.get(f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg").content)

    if not sub_flag:
        text_prompt = str(text_input) + "Make a new video idea based on combining the following ideas, comments, and other videos:" + str(genres) + str(transcripts) + str(commentss)
    else: 
        text_prompt = str(text_input) + "Make a new video idea that does not incorporate " + str(genres) + ", and instead is about combining: " + str(transcripts) + str(commentss)
    
    text_prompt = text_prompt[:2040]
    print(text_prompt)

    user_message = [{
        "role": "user",
        "content": [
            {"type": "text", "text": text_prompt},
            {
                "type": "image_url",
                "image_url": {"url": images[0]}
            }
        ]
    }]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=user_message,
        max_tokens=100
    )

    print(response.choices[0].message.content)
    
    user_message2 = [{
        "role": "user",
        "content": [
            {"type": "text", "text": f"Make a video script for YouTube for this: {response.choices[0].message.content}"},
        ]
    }]
    
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages= user_message2,
        max_tokens=200
    )
    
    script = response2.choices[0].message.content

    brands_list = "Museum of Flight, Boeing, Airbus, Lockheed Martin, Northrop Grumman, Raytheon Technologies, SpaceX, Blue Origin, Sierra Nevada Corporation, Honeywell Aerospace, GE Aerospace, Rolls-Royce Aerospace, Pratt & Whitney, Safran, BAE Systems, Thales Group, Virgin Galactic, Rocket Lab, L3Harris Technologies, Bell Helicopter, Embraer"

    text = f"Make a YouTube thumbnail for this: {response.choices[0].message.content}. No text!"
    response3 = client.images.generate(
        model="dall-e-3",
        prompt=text,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response3.data[0].url
    print(image_url)
    
    print(input_dict)    
    return render_template('result.html', equation=equation, inputs=categorized_inputs, 
                           image_url=image_url, idea=response.choices[0].message.content,
                           script=script, brands_list=brands_list)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
