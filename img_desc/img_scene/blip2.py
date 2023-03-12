import torch
from PIL import Image
from lavis.models import load_model_and_preprocess
# setup device to use
device = torch.device("cuda") if torch.cuda.is_available() else "cpu"

def get_img_desc(image):
    # load sample image
    raw_image = Image.open("../math_api/mathequation.png")
    # loads BLIP-2 pre-trained model
    model, vis_processors, _ = load_model_and_preprocess(name="blip2_t5", model_type="pretrain_flant5xxl", is_eval=True, device=device)
    # # prepare the image
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    caption = model.generate({"image": image})
    return caption