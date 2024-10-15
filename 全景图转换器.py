import cv2
import numpy as np
import gradio as gr
from PIL import Image
import logging
import subprocess
import os
import shutil
import winreg
import urllib.request
import zipfile

logging.basicConfig(level=logging.DEBUG)

# 默认保存路径
DEFAULT_SAVE_PATH = r"C:\Users\ZYB\Desktop\PIP脚本汇总\临时保存"

def ensure_save_path(path):
    os.makedirs(path, exist_ok=True)

def create_panorama_from_single_image(input_image):
    # 将PIL Image转换为numpy数组
    image = np.array(input_image)
    
    # 如果图像是RGBA格式，转换为RGB
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # 创建全景图
    h, w = image.shape[:2]
    panorama_height = h
    panorama_width = w * 2
    panorama = np.zeros((panorama_height, panorama_width, 3), dtype=np.uint8)
    panorama[:, :w] = image
    panorama[:, w:] = image[:, ::-1]

    return Image.fromarray(panorama)

def process_non_panorama(input_image, save_path):
    if input_image is None:
        return None, "请先上传非全景图片。"
    try:
        ensure_save_path(save_path)
        # 清除之前的处理结果
        for file in os.listdir(save_path):
            file_path = os.path.join(save_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        # 生成唯一的文件名
        filename = f"panorama_{os.urandom(8).hex()}.png"
        save_file_path = os.path.join(save_path, filename)
        
        # 创建全景图并保存
        panorama = create_panorama_from_single_image(input_image)
        panorama.save(save_file_path)
        
        return Image.open(save_file_path), "已将图片转换为全景图。"
    except Exception as e:
        logging.error(f"处理图像时发生错误: {str(e)}")
        return None, f"处理图像时发生错误: {str(e)}"

def process_panorama(input_image, save_path):
    if input_image is None:
        return None, "请先上传全景图片。"
    try:
        ensure_save_path(save_path)
        # 清除之前的处理结果
        for file in os.listdir(save_path):
            file_path = os.path.join(save_path, file)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        # 生成唯一的文件名
        filename = f"original_{os.urandom(8).hex()}.png"
        save_file_path = os.path.join(save_path, filename)
        
        # 保存原始全景图
        input_image.save(save_file_path)
        
        return input_image, "全景图已保存，准备使用Panorado打开。"
    except Exception as e:
        logging.error(f"处理图像时发生错误: {str(e)}")
        return None, f"处理图像时发生错误: {str(e)}"

def find_panorado(custom_path=None):
    if custom_path and os.path.exists(custom_path):
        return custom_path
    if os.path.exists(DEFAULT_PANORADO_PATH):
        return DEFAULT_PANORADO_PATH
    return None

def download_and_install_panorado():
    url = "https://www.panorado.com/Download/Panorado50Setup64.exe"
    install_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    exe_path = os.path.join(install_path, 'Panorado50Setup64.exe')
    
    try:
        # 确保下载目录存在
        os.makedirs(install_path, exist_ok=True)
        
        # 下载Panorado安装程序
        logging.info(f"正在从 {url} 下载Panorado安装程序...")
        urllib.request.urlretrieve(url, exe_path)
        logging.info("下载完成。")
        
        # 运行安装程序
        logging.info("正在运行Panorado安装程序...")
        subprocess.run([exe_path], check=True)
        logging.info("Panorado安装完成。")
        
        # 安装完成后,返回可能的Panorado执行文件路径
        possible_panorado_path = os.path.join(os.environ['PROGRAMFILES'], 'Panorado', 'Panorado64.exe')
        if os.path.exists(possible_panorado_path):
            return possible_panorado_path
        else:
            logging.warning("无法找到Panorado安装路径,请手动指定。")
            return None
    except Exception as e:
        logging.error(f"下载或安装Panorado时发生错误: {str(e)}")
        # 清理下载的文件
        if os.path.exists(exe_path):
            os.remove(exe_path)
        raise

def view_with_panorado(message, panorado_path, save_path):
    panorado_exe = find_panorado(panorado_path)
    if not panorado_exe:
        download_link = "https://www.panorado.com/Download/Panorado50Setup64.exe"
        return f"未找到Panorado程序。请从以下链接下载并安装Panorado: {download_link}\n安装后,请在上方输入框中输入Panorado的安装路径。"
    
    try:
        # 获取最新保存的图片路径
        latest_image = max([os.path.join(save_path, f) for f in os.listdir(save_path)], key=os.path.getctime)
        
        subprocess.Popen([panorado_exe, latest_image])
        
        return f"已使用Panorado打开全景图。请检查Panorado窗口。\n{message}"
    except Exception as e:
        logging.error(f"打开Panorado时发生错误: {str(e)}")
        return f"处理图像时发生错误: {str(e)}"

# 默认Panorado路径
DEFAULT_PANORADO_PATH = r"C:\Program Files\Panorado\Panorado64.exe"

# 创建Gradio界面
with gr.Blocks() as iface:
    gr.Markdown("# 全景图转换器")
    gr.Markdown("上传非全景图进行转换,或直接上传全景图查看。")
    
    panorama_input = gr.Image(type="pil", label="上传全景图")
    
    non_panorama_input = gr.Image(type="pil", label="上传非全景图")
    
    panorama_output = gr.Image(type="pil", label="转换后的全景图")
    
    panorado_path = gr.Textbox(label="Panorado路径", value=DEFAULT_PANORADO_PATH)
    
    save_path = gr.Textbox(label="保存路径", value=DEFAULT_SAVE_PATH)
    
    result_text = gr.Textbox(label="结果")
    
    def process_and_view(image, panorado_path, save_path, process_func):
        result, message = process_func(image, save_path)
        view_result = view_with_panorado(message, panorado_path, save_path)
        return result, view_result
    
    non_panorama_input.change(
        fn=lambda img, path, save: process_and_view(img, path, save, process_non_panorama),
        inputs=[non_panorama_input, panorado_path, save_path],
        outputs=[panorama_output, result_text]
    )
    
    panorama_input.change(
        fn=lambda img, path, save: process_and_view(img, path, save, process_panorama),
        inputs=[panorama_input, panorado_path, save_path],
        outputs=[panorama_output, result_text]
    )

# 启动Gradio应用
iface.launch()
