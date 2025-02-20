# Open food market image and make it circular
food_img = Image.open(bg_image)
food_img = food_img.crop((0, 0, food_img.size[0], food_img.size[0]))
mask = Image.new('L', food_img.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0) + food_img.size, fill=255)

# Add the circular food market image with adjusted position
food_img_path = "../slidesbench/examples/marketing/slide_7/media/circular_food.png"
food_img.putalpha(mask)
food_img.save(food_img_path)
slide.shapes.add_picture(food_img_path, Inches(12), Inches(5), Inches(3), Inches(3))  # Adjusted position