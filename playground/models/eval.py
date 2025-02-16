from . import gpt_4o, llava

def generate_edit_description(model_type, prompt, target_image, render_image):
    if model_type == "gpt-4o":
        return gpt_4o.eval(prompt, target_image, render_image)
    else:
        raise ValueError("Unsupported model type")
    
def generate_code_edit(model_type, prompt, render_image):
    if model_type == "gpt-4o":
        return gpt_4o.eval(prompt, None, render_image)
    else:
        raise ValueError("Unsupported model type")
    
def parse_edit_description(model_type, response):
    if model_type == "gpt-4o":
        return gpt_4o.parse_edit_description(response)
    else:
        raise ValueError("Unsupported model type")

def parse_code(model_type, response):
    if model_type == "gpt-4o":
        return gpt_4o.parse_code(response)
    else:
        raise ValueError("Unsupported model type")