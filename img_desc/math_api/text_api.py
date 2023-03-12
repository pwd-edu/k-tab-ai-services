import requests
import json
from .config import mathpix_config

file_path = r'mathequation.png'
img_url = "https://content-pwd-aat.s3.us-east-1.amazonaws.com/img-desc/mathequation.png?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEPH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCWV1LXdlc3QtMyJGMEQCIGwieLM3ONSnCTUrjUoFnBeAY25iQg5nB4CTeRyIccfgAiAGP668TaNp0s2XwQ1erlaWyvbV6XO34DiY3Hulm0mWDyrtAgiq%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAMaDDkyMDE1MzM2MjI5NSIMpxeG4n5ZcOni57sOKsECcf38YsRc9fTs5C8D1kY%2FtozJlSuU9X56kxi%2BSY4ucvt4P2qFH54NslwqTzrw2J7yHF0dpGZXhMUHzhHTEEu%2BlU1I4ToL41fzuv%2BLuDwUtthfInrsShx7mMJW6PryFw7DaINBZWxtsqepzV1r%2F0TNhL4L0tXxH7NoG9jdp2VWsAVyKjKFXPe0kPnVRaMiQqk9jwVCJefcbbE2FC30aj9GElOlimIyMmhdsgvbFUuu3b0mf6Dp90YAJ8hD7SayipK3hizBHW5Myc7M6ftSTpV1dgAoLDu2mbMGvFDl6TxXZ7BSXGViJ%2BNkrZMuFl8kRWD%2BjNcuf7nxSUNoKS6%2Ffx3Ipftj6VSyPdI3feYErN7YBfHL9TzCsrmk9L%2F5XtDRegN%2FqUWnHD2zURwVvhOYBqX4OL3B6DlZxmbLL3b%2B%2BiLypffZML%2BMuKAGOrQCoUH52bsGypuqY6Bx9u1zAKjm5Kt8DImG8ephkBlbH7kvqAQoOikaYPfhev3VhMXUHFcAiVDlFflC69UZY01vyBwsB7jlDAc0p26GZzDDWacFFhFUYt7PG1BX0Wz3jKs%2F3KWaThAfswwo6IXWBX%2Bfq0bRMhRQOHMjaS7Qs7%2B2H6FbwgoSmnd893zexQYPxBig%2Fi5US%2BM9BkTpdc42OoZ72CeOF0dMPQrFq7ZTAR409loa2zkbi%2BOkznoBDDjP82wj1Y6Ag70gJOAiwG9TuTZlH2ZFZyxCQGih1bU9cRChY2xtJC9UHazuPOkzAxLf9vk9vibZjDkOfyRhfWLAHyxZbyGvAB%2B4UGHLhXEfSO1KeXrmytBohO%2B24wfkFGp9Gg93N4Lfm2XHkSMjzg97kWy%2BVwpaO8c%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20230312T170532Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7199&X-Amz-Credential=ASIA5MPLKB534AQODUHJ%2F20230312%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ebd6d0562c718a623d01955f04d5f41e1921457f3467cd4196cda741a720077e"
def process_image(image_url):
    r = requests.post("https://api.mathpix.com/v3/text",
        # files={"file": image},
        json = {
            "src": image_url,
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
        },
        headers={
            "app_id": mathpix_config.APP_ID,
            "app_key": mathpix_config.APP_KEY,
            "Content-type": "application/json"
        }
    )
    print(json.dumps(r.json(), indent=4, sort_keys=True))
    return r.json()

# processed_math = process_image(img_url)
