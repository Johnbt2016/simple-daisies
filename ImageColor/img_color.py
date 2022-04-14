from pydaisi import Daisi, SharedDataClient
import io

color = Daisi("ImageColorization")

sd = SharedDataClient(access_token="iYDE89fkV6iQhRQdhJYn6q6QMiJy1tW3")


def give_color(repeat = 1):
    results = []
    for i in range(repeat):
        obj = sd.download_fileobj("/JM/Images/B2DBy.jpeg")
        img = io.BytesIO(obj)
        results.append(color.run_(img))
    
    return results
