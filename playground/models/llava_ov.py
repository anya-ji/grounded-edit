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
    target_image = Image.open(target_image_path)
    if render_image_path:
        render_image = Image.open(render_image_path)
    
    if target_image_path and render_image_path:
        # messages = [{
        #     "role": "user",
        #     "content": [
        #         {"type": "image"},
        #         {"type": "image"},
        #         {"type": "text", "text": "What is shown in this image?"},
        #         ],
        # },]
   
        conversation_1 = [
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "What is shown in this target image?"},
                    ],
            },
            {
                "role": "assistant",
                "content": [
                    {"type": "text", "text": "There is a red stop sign in the image."},
                    ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "image"},
                    {"type": "text", "text": "What about this image? How many cats do you see?"},
                    ],
            },
        ]

    prompt_1 = processor.apply_chat_template(conversation_1, add_generation_prompt=True)
    prompt_2 = processor.apply_chat_template(conversation_2, add_generation_prompt=True)
    prompts = [prompt_1, prompt_2]
    inputs = processor(
        images=[image_stop, image_cats, image_snowman], 
        text=prompts, 
        padding=True, 
        return_tensors="pt").to(model.device, torch.float16)
    processor.tokenizer.padding_side = "left"
    generate_ids = model.generate(**inputs, max_new_tokens=30)
    
    processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)