import cv2
import numpy as np
import gradio as gr
from PIL import Image
import logging
import subprocess
import os
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

# 默认保存路径
DEFAULT_SAVE_PATH = r"C:\Users\ZYB\Desktop\PIP脚本汇总\临时保存"
DEFAULT_PANORADO_PATH = r"C:\Program Files\Panorado\Panorado64.exe"

def ensure_save_path(path):
    os.makedirs(path, exist_ok=True)

def create_panorama_from_single_image(input_image):
    # 如果输入是 PIL Image，转换为 numpy 数组
    if isinstance(input_image, Image.Image):
        image = np.array(input_image)
    else:
        image = input_image
    
    # 如果图像是RGBA格式，转换为RGB
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
    # 创建全景图
    h, w = image.shape[:2]
    panorama_height = h
    panorama_width = w * 2
    panorama = np.zeros((panorama_height, panorama_width, 3), dtype=np.uint8)
    panorama[:, :w] = image
    panorama[:, w:] = np.fliplr(image)

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
        
        return Image.open(save_file_path), f"已将图片转换为全景图并保存至 {save_file_path}"
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
        
        return input_image, f"全景图已保存至 {save_file_path}，准备使用Panorado打开。"
    except Exception as e:
        logging.error(f"处理图像时发生错误: {str(e)}")
        return None, f"处理图像时发生错误: {str(e)}"

def view_with_look(image_path):
    try:
        # 启动 look.py 查看器
        look_script_path = os.path.join(os.path.dirname(__file__), 'look.py')
        
        # 使用 subprocess 启动新的 Python 进程运行 look.py
        env = os.environ.copy()
        env['PYTHONPATH'] = os.path.dirname(__file__)  # 确保能找到相关模块
        
        # 将图片路径作为参数传递给 look.py
        subprocess.Popen([
            'python', 
            look_script_path,
            '--image', 
            image_path
        ], env=env)
        
        return f"已使用全景图查看器打开图片: {image_path}"
    except Exception as e:
        logging.error(f"启动查看器时发生错误: {str(e)}")
        return f"启动查看器失败: {str(e)}"

def process_and_view(image, save_path, process_func):
    try:
        result, message = process_func(image, save_path)
        if result:
            # 获取最新保存的图片路径
            latest_image = max(
                [os.path.join(save_path, f) for f in os.listdir(save_path)], 
                key=os.path.getctime
            )
            view_result = view_with_look(latest_image)
            return result, f"{message}\n{view_result}"
        return result, message
    except Exception as e:
        logging.error(f"处理图像时发生错误: {str(e)}")
        return None, f"处理失败: {str(e)}"

def process_folder(input_folder, output_folder):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    if not input_folder.is_dir():
        return f"输入路径不是文件夹: {input_folder}"

    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in input_folder.iterdir() if f.suffix.lower() in image_extensions]

    if not image_files:
        return f"文件夹中没有找到图像文件: {input_folder}"

    ensure_save_path(str(output_folder))
    processed_count = 0
    for image_file in image_files:
        try:
            input_image = Image.open(image_file)
            panorama = create_panorama_from_single_image(input_image)
            
            # 使用原始文件名，但添加 'panorama_' 前缀
            output_filename = f"panorama_{image_file.name}"
            output_path = output_folder / output_filename
            
            panorama.save(str(output_path))
            processed_count += 1
            logging.info(f"已处理并保存: {output_path}")
        except Exception as e:
            logging.error(f"处理图像 {image_file} 时发生错误: {str(e)}")

    return f"已处理 {processed_count} 张图片，输出至 {output_folder}"

# 创建Gradio界面
with gr.Blocks() as iface:
    gr.Markdown("# 全景图转换器")
    gr.Markdown("上传非全景图进行转换,或直接上传全景图查看。也可以批量处理文件夹中的图片。")
    
    with gr.Tab("单张图片处理"):
        panorama_input = gr.Image(type="pil", label="上传全景图")
        non_panorama_input = gr.Image(type="pil", label="上传非全景图")
        panorama_output = gr.Image(type="pil", label="转换后的全景图")
        
    with gr.Tab("批量处理"):
        input_folder = gr.Textbox(label="输入文件夹路径")
        output_folder = gr.Textbox(label="输出文件夹路径")
        process_button = gr.Button("开始批量处理")
    
    save_path = gr.Textbox(label="保存路径", value=DEFAULT_SAVE_PATH)
    result_text = gr.Textbox(label="结果")
    
    # 修改事件处理函数
    non_panorama_input.change(
        fn=lambda img, save: process_and_view(img, save, process_non_panorama),
        inputs=[non_panorama_input, save_path],
        outputs=[panorama_output, result_text]
    )
    
    panorama_input.change(
        fn=lambda img, save: process_and_view(img, save, process_panorama),
        inputs=[panorama_input, save_path],
        outputs=[panorama_output, result_text]
    )
    
    process_button.click(
        fn=process_folder,
        inputs=[input_folder, output_folder],
        outputs=result_text
    )

# 启动Gradio应用
iface.launch()
