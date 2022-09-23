import os
import streamlit as st
from pathlib import Path

def exec_cmd(prompt):
    res = os.popen(prompt)
    output = res.readlines()
    print(output)

    return output

def print_progress(msg, strmlit_ui):
    st.write(msg) if strmlit_ui else print(msg)

def dwnld_model(exceptions_log, address, target_location, source_model_name=None, target_model_name=None, strmlit_ui=False):
    target_name = Path(target_model_name)

    if not target_name.exists():
        msg = f"Downloading {address} to {target_location}"
        print_progress(msg, strmlit_ui)
        try:
            os.system(f'wget {address} -P {target_location}')
            if target_model_name is not None:
                os.system(f'mv {source_model_name} {target_model_name}')
            print_progress("Done", strmlit_ui)
        except Exception as e:
            st.write(e) if strmlit_ui else exceptions_log.append([msg,e])
    else:
        msg = f"Skipping {target_name}"
        print_progress(msg, strmlit_ui)
    
    return exceptions_log



def download_models(dest="stable_diffusion_models", strmlit_ui = False):
    exceptions_log = []
    dest = dest.strip("/").replace(" ", "_")

    dest = os.path.expanduser("~/" + dest)

    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://www.googleapis.com/storage/v1/b/aai-blog-files/o/sd-v1-4.ckpt?alt=media', 
                                target_location = f'{dest}/models/ldm/stable-diffusion-v1/', 
                                source_model_name= f'{dest}/models/ldm/stable-diffusion-v1/sd-v1-4.ckpt?alt=media', 
                                target_model_name= f'{dest}/models/ldm/stable-diffusion-v1/model.ckpt', 
                                strmlit_ui=False)

    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth', 
                                target_location = f'{dest}/models/src/realesrgan/experiments/pretrained_models', 
                                source_model_name= f'{dest}/models/src/realesrgan/experiments/pretrained_models/RealESRGAN_x4plus.pth', 
                                target_model_name= f'{dest}/models/src/realesrgan/experiments/pretrained_models/RealESRGAN_x4plus.pth', 
                                strmlit_ui=False)

    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth', 
                                target_location = f'{dest}/models/src/gfpgan/experiments/pretrained_models', 
                                source_model_name= f'{dest}/models/src/gfpgan/experiments/pretrained_models/GFPGANv1.3.pth', 
                                target_model_name= f'{dest}/models/src/gfpgan/experiments/pretrained_models/GFPGANv1.3.pth', 
                                strmlit_ui=False)
    
    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth', 
                                target_location = f'{dest}/models/src/realesrgan/experiments/pretrained_models', 
                                source_model_name= f'{dest}/models/src/realesrgan/experiments/pretrained_models/RealESRGAN_x4plus_anime_6B.pth', 
                                target_model_name= f'{dest}/models/src/realesrgan/experiments/pretrained_models/RealESRGAN_x4plus_anime_6B.pth', 
                                strmlit_ui=False)
    
    if not Path(f'{dest}/models/src/latent-diffusion').exists():
        os.system(f'cd {dest}/models/ ; git clone https://github.com/devilismyfriend/latent-diffusion.git')
        os.system(f'mv {dest}/models/latent-diffusion  {dest}/models/src/latent-diffusion')

    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1', 
                                target_location = f'{dest}/models/src/latent-diffusion/experiments/pretrained_models', 
                                source_model_name= f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1', 
                                target_model_name= f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/project.yaml', 
                                strmlit_ui=False)

    exceptions_log = dwnld_model(exceptions_log, 
                                address = 'https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1', 
                                target_location = f'{dest}/models/src/latent-diffusion/experiments/pretrained_models', 
                                source_model_name= f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1', 
                                target_model_name= f'{dest}/models/src/latent-diffusion/experiments/pretrained_models/model.ckpt', 
                                strmlit_ui=False)

    return exceptions_log

def st_ui():
    st.title("Stable Diffusion Models download")

    if st.button("Download models"):
        exceptions_log = download_models(dest="stable_diffusion_models", strmlit_ui = True)


if __name__ == "__main__":
    download_models(dest="stable_diffusion_models", strmlit_ui = False)


    
