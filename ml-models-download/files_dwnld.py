import os

def download_models(dest):
    dest = dest.strip("/").replace(" ", "_")

    dest = "$HOME/" + dest
    os.system(f'wget https://www.googleapis.com/storage/v1/b/aai-blog-files/o/sd-v1-4.ckpt?alt=media -P {dest}/models/ldm/stable-diffusion-v1/')
    os.rename(f'{dest}/models/ldm/stable-diffusion-v1/sd-v1-4.ckpt?alt=media','{dest}/models/ldm/stable-diffusion-v1/model.ckpt')
    os.system(f'wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P {dest}/models/src/realesrgan/experiments/pretrained_models')
    os.system(f'wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -P {dest}/models/src/gfpgan/experiments/pretrained_models')
    os.system(f'wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P {dest}/models/src/realesrgan/experiments/pretrained_models')
    os.system(f'cd {dest}/models/ ; git clone https://github.com/devilismyfriend/latent-diffusion.git')
    os.system(f'mv latent-diffusion  {dest}/models/src/latent-diffusion')
    os.mkdir(f' {dest}/models/src/latent-diffusion/experiments')
    os.mkdir(f' {dest}/models/src/latent-diffusion/experiments/pretrained_models')
    os.system(f'wget https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1 -P {dest}/models/src/latent-diffusion/experiments/pretrained_models')
    os.rename(f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1', '{dest}/models/src/latent-diffusion/experiments/pretrained_models/project.yaml')
    os.system(f'wget https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1 -P {dest}/models/src/latent-diffusion/experiments/pretrained_models')
    os.rename(f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1', '{dest}/models/src/latent-diffusion/experiments/pretrained_models/model.ckpt')

    return "Done"