import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        properties={
            "response": content.Schema(
                type=content.Type.STRING,
            ),
        },
    ),
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        prompt = [
            "You are a translator AI assistant designed to convert informal language into professional and respectful tone. Your responses should focus on rephrasing the original message in a polite and constructive manner, without adding any negative or judgmental comments. Please provide a translated output that maintains the original message's intent while conveying it in a respectful and professional tone.",
            "input: I really don't like working with my colleague. They always take credit for my ideas.",
            "output: I'm experiencing some challenges in collaborating with my colleague, specifically regarding the attribution of ideas and contributions. I've noticed that there have been instances where my suggestions and concepts have been presented as their own, which can hinder our team's ability to work effectively and recognize individual strengths. I believe it's essential to establish clear communication channels and ensure that all team members receive proper recognition for their work to foster a more positive and productive work environment.",
            "input: What should I do if my boss is micromanaging me?",
            "output: I'm facing some challenges with my supervisor's management style, as I feel that my ability to work independently is being constrained. I would appreciate guidance on how to communicate my desire for more autonomy in a constructive manner while still meeting the expectations set by my supervisor.",
            "input: Can you give me advice on how to handle office gossip?",
            "output: I'm encountering a situation where there are ongoing discussions and rumors in the office that may not be entirely constructive. I recognize the importance of maintaining a positive work environment, and I would like to explore strategies for addressing this issue without contributing to the gossip myself.",
            "input: How do I ask for a raise without sounding greedy?",
            "output: I would like to initiate a discussion regarding my compensation, ensuring that I frame it in a way that highlights my contributions and the value I bring to the team. My goal is to approach this conversation professionally and with a clear understanding of my achievements and the market standards.",
            "input: go screw yourself",
            "output: I disagree with your approach, and I'd appreciate it if we could find a more constructive way to move forward.",
            "input: fuck you",
            "output: I strongly disagree with your decision/action, and I believe it's essential we revisit this topic to find a more suitable solution.",
            "input: Get out of my way",
            "output: I need some space to focus on this task, can we discuss this later?",
            "input: You're an idiot",
            "output: I disagree with your approach, can we explore alternative solutions?",
            "input: Shut up",
            "output: Let's focus on the topic at hand, can we avoid distractions?",
            "input: i dont care",
            "output: I understand your perspective, but I have concerns about the impact of this decision.",
            "input: You're so stupid",
            "output: I think there might be a misunderstanding, can we clarify the situation?",
            f"input: {user_input}",
            "output: ",
        ]
        
        response = model.generate_content(prompt)
        translated_text = response.text.strip()
        return render_template('index.html', original=user_input, translated=translated_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)