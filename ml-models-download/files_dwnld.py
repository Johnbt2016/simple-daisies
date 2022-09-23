import os
import streamlit as st

def exec_cmd(prompt):
    res = os.popen(prompt)
    output = res.readlines()
    print(output)

    return output

def download_models(dest="stable_diffusion_models", strmlit_ui = True):
    exceptions_log = []
    dest = dest.strip("/").replace(" ", "_")

    dest = "~/" + dest

    target_name = f'{dest}/models/ldm/stable-diffusion-v1/model.ckpt'

    check_file = exec_cmd(f'(ls {target_name} >> /dev/null 2>&1 && echo yes) || echo no')
    if check_file == 'no':
        msg = f"Downloading stable diffusion v1 to {dest}/models/ldm/stable-diffusion-v1/"
        st.write(msg) if strmlit_ui else print(msg)
        try:
            os.system(f'wget https://www.googleapis.com/storage/v1/b/aai-blog-files/o/sd-v1-4.ckpt?alt=media -P {dest}/models/ldm/stable-diffusion-v1/')
            os.system(f'mv {dest}/models/ldm/stable-diffusion-v1/sd-v1-4.ckpt?alt=media {dest}/models/ldm/stable-diffusion-v1/model.ckpt')
            st.write("Done") if strmlit_ui else print("Done")
        except Exception as e:
            st.write(e) if strmlit_ui else exceptions_log.append([msg,e])
    else:
        msg = f"Skipping {target_name}"
        st.write(msg) if strmlit_ui else print(msg)

    msg = f"Downloading stable diffusion v1 to {dest}/models/ldm/stable-diffusion-v1/"
    st.write(msg) if strmlit_ui else print(msg)
    try:
        os.system(f'wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth -P {dest}/models/src/realesrgan/experiments/pretrained_models')
        st.write("Done") if strmlit_ui else print("Done")
    except Exception as e:
        st.write(e) if strmlit_ui else exceptions_log.append([msg,e])

    msg = f"Downloading GFPGANv1.3 to {dest}/models/src/gfpgan/experiments/pretrained_models"
    st.write(msg) if strmlit_ui else print(msg)
    try:
        os.system(f'wget https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth -P {dest}/models/src/gfpgan/experiments/pretrained_models')
        st.write("Done") if strmlit_ui else print("Done")
    except Exception as e:
        st.write(e) if strmlit_ui else exceptions_log.append([msg,e])

    msg = f"Downloading RealESRGAN_x4plus_anime_6B to {dest}/models/src/realesrgan/experiments/pretrained_models"
    st.write(msg) if strmlit_ui else print(msg)
    try:
        os.system(f'wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth -P {dest}/models/src/realesrgan/experiments/pretrained_models')
        os.system(f'cd {dest}/models/ ; git clone https://github.com/devilismyfriend/latent-diffusion.git')
        os.system(f'mv {dest}/models/latent-diffusion  {dest}/models/src/latent-diffusion')
        st.write("Done") if strmlit_ui else print("Done")
        # os.mkdir(f'{dest}/models/src/latent-diffusion/experiments')
        # os.mkdir(f'{dest}/models/src/latent-diffusion/experiments/pretrained_models')
    except Exception as e:
        st.write(e) if strmlit_ui else exceptions_log.append([msg,e])

    msg = f"Downloading latent-diffusion/experiments/pretrained_models to {dest}/models/src/latent-diffusion/experiments/pretrained_models"
    st.write(msg) if strmlit_ui else print(msg)
    try:
        os.system(f'wget https://heibox.uni-heidelberg.de/f/31a76b13ea27482981b4/?dl=1 -P {dest}/models/src/latent-diffusion/experiments/pretrained_models')
        os.system(f'mv {dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1 {dest}/models/src/latent-diffusion/experiments/pretrained_models/project.yaml')
        st.write("Done") if strmlit_ui else print("Done")
    except Exception as e:
        st.write(e) if strmlit_ui else exceptions_log.append([msg,e])

    msg = f"Downloading latent-diffusion/experiments/pretrained_models to {dest}/models/src/latent-diffusion/experiments/pretrained_models"
    st.write(msg) if strmlit_ui else print(msg)
    try:
        os.system(f'wget https://heibox.uni-heidelberg.de/f/578df07c8fc04ffbadf3/?dl=1 -P {dest}/models/src/latent-diffusion/experiments/pretrained_models')
        os.system(f'mv {dest}/models/src/latent-diffusion/experiments/pretrained_models/index.html?dl=1 {dest}/models/src/latent-diffusion/experiments/pretrained_models/model.ckpt')
        st.write("Done") if strmlit_ui else print("Done")
    except Exception as e:
        st.write(e) if strmlit_ui else exceptions_log.append([msg,e])
    

    return exceptions_log

def st_ui():
    st.title("Stable Diffusion Models download")

    if st.button("Download models"):
        exceptions_log = download_models(dest="stable_diffusion_models", strmlit_ui = True)


if __name__ == "__main__":
    st_ui()


    
