from pydaisi import Daisi, SharedDataClient
import io
from PIL import Image
import time

color = Daisi("ImageColorization")

sd = SharedDataClient(access_token="iYDE89fkV6iQhRQdhJYn6q6QMiJy1tW3")


def give_color(repeat = 10):
    results = []
    for i in range(int(repeat)):
        obj = sd.download_fileobj("/JM/Images/B2DBy.jpeg")
        # print(obj)
        img = Image.open(io.BytesIO(obj))
        results.append(color.run(img))
    
    return results

if __name__ == "__main__":
    results = give_color(10)
    while results[-1].get_status() != "FINISHED":
        print(results[-1].get_status())
        time.sleep(0.1)

    print(results[0].value)