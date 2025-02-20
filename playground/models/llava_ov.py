'''
https://github.com/huggingface/transformers/blob/main/docs/source/en/model_doc/llava_onevision.md
'''
import requests
from PIL import Image
import torch
from transformers import AutoProcessor, LlavaOnevisionForConditionalGeneration

# Load the model in half-precision
model = LlavaOnevisionForConditionalGeneration.from_pretrained("llava-hf/llava-onevision-qwen2-7b-ov-hf", torch_dtype=torch.float16, device_map="auto")
processor = AutoProcessor.from_pretrained("llava-hf/llava-onevision-qwen2-7b-ov-hf")

# Generate
def eval(prompt, target_image_path, render_image_path):
    if target_image_path:
        target_image = Image.open(target_image_path)
    render_image = Image.open(render_image_path)
    
    if target_image_path and render_image_path:
        messages = [{
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "image"},
                {"type": "text", "text": prompt},
                ],
        },]

        processed_prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(
            images=[target_image, render_image], 
            text=[processed_prompt], 
            padding=True, 
            return_tensors="pt").to(model.device, torch.float16)
   
        # conversation_1 = [
        #     {
        #         "role": "user",
        #         "content": [
        #             {"type": "image"},
        #             {"type": "text", "text": "What is shown in this target image?"},
        #             ],
        #     },
        #     {
        #         "role": "assistant",
        #         "content": [
        #             {"type": "text", "text": "There is a red stop sign in the image."},
        #             ],
        #     },
        #     {
        #         "role": "user",
        #         "content": [
        #             {"type": "image"},
        #             {"type": "text", "text": "What about this image? How many cats do you see?"},
        #             ],
        #     },
        # ]
    elif render_image_path:
        messages = [{
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt},
                ],
        },]
        processed_prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = processor(
            images=[render_image], 
            text=[processed_prompt], 
            padding=True, 
            return_tensors="pt").to(model.device, torch.float16)

    
    processor.tokenizer.padding_side = "left"
    generate_ids = model.generate(**inputs, max_new_tokens=300)
    
    [result] = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return result

def parse_edit_description(response):
    return response.split('assistant',1)[1].split("Change Suggestion: ",1)[1].split("```",1)[0].strip()

def parse_code(response):
    return response.split('assistant',1)[1]