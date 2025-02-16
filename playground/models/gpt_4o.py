import os
import openai
import base64

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

def encode_image(image_path):
    if not image_path:
        return None
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def eval(prompt, target_image_path, render_image_path):
    target_image_url = f"data:image/jpeg;base64,{encode_image(target_image_path)}"
    render_image_url = f"data:image/jpeg;base64,{encode_image(render_image_path)}"
    if target_image_path and render_image_path:
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": target_image_url}},
                {"type": "image_url", "image_url": {"url": render_image_url}},
            ],
        }]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=4096,
            n=1,
        )
        response_list = [c.message.content for c in response.choices]
    elif render_image_path:
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": render_image_url}},
            ],
        }]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=4096,
            n=1,
        )
        response_list = [c.message.content for c in response.choices]
    return response_list[0]

def parse_edit_description(response):
    return response.split("Change Suggestion: ",1)[1].split("```",1)[0].strip()

def parse_code(response):
    return response.split("```python",1)[1].split("```",1)[0].strip()