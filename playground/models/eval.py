from . import gpt_4o, llava_ov

def generate_edit_description(model_type, prompt, target_image, render_image):
    if model_type == "gpt-4o":
        return gpt_4o.eval(prompt, target_image, render_image)
    if model_type == 'llava-ov':
        return llava_ov.eval(prompt, target_image, render_image)
    raise ValueError("Unsupported model type")
    
def generate_code_edit(model_type, prompt, render_image):
    if model_type == "gpt-4o":
        return gpt_4o.eval(prompt, None, render_image)
    if model_type == 'llava-ov':
        return llava_ov.eval(prompt, None, render_image)
    raise ValueError("Unsupported model type")
    
def parse_edit_description(model_type, response):
    if model_type == "gpt-4o":
        return gpt_4o.parse_edit_description(response)
    if model_type == 'llava-ov':
        return llava_ov.parse_edit_description(response)
    raise ValueError("Unsupported model type")

def parse_code(model_type, response):
    if model_type == "gpt-4o":
        return gpt_4o.parse_code(response)
    if model_type == 'llava-ov':
        return llava_ov.parse_code(response)
    raise ValueError("Unsupported model type")