import os, platform, subprocess, re

def get_gpuinfo():
    if platform.system() == "Linux":
        command = "nvidia-smi"
        all_info = subprocess.check_output(command, shell=True).decode().strip().replace('\n', '<br/>')
        return all_info
    return ""