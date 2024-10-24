# 全景图处理工具集

这是一个用于处理和查看全景图的工具集，包含两个主要组件：全景图转换器和全景图查看器。

## 功能特点

### 全景图转换器 (全景图转换V2.py)
- 将普通图片转换为360度全景图
- 支持单张图片处理
- 支持批量处理文件夹中的图片
- 自动打开全景图查看器预览结果

### 全景图查看器 (look.py)
- 支持360度全景图查看
- 支持柱面投影和球面投影切换
- 支持鼠标拖拽和滚轮缩放
- 支持录制360度旋转视频
- 支持WebM和MP4格式导出

## 安装说明

1. 确保已安装 Python 3.8 或更高版本
2. 安装依赖包：


pip install -r requirements.txt


https://github.com/user-attachments/assets/83199a04-0b43-4473-bfbf-003a60780f18

![微信截图_20241024185843](https://github.com/user-attachments/assets/21792a78-8535-481c-845c-ce0841a7d463)

![GUI](https://github.com/user-attachments/assets/87ac9109-1064-4cbc-8af1-5431d7ae0e9b)
![TEST1](https://github.com/user-attachments/assets/b1826c50-7e9d-4871-817a-cff3d0edc601)
![TEST2](https://github.com/user-attachments/assets/8b510822-08aa-44bd-b241-26fe542a1b8d)

## 使用技巧

默认对于横版1:2的图像支持最好

## 安装说明

1. 确保您的系统已安装Python 3.7或更高版本。 确保您的系统已安装Python 3.7或更高版本。

2. 克隆或下载此项目到本地。 克隆或下载此项目到本地。

3. 在项目目录中，使用pip安装所需的依赖： 在项目目录中，使用pip安装所需的依赖：

   ```
   pip install opencv-python numpy gradio pillow
   ```

4. 下载并安装Panorado软件： 下载并安装Panorado软件：
   - 访问 https://www.panorado.com/Download/Panorado50Setup64.exe 访问 https://www.panorado.com/Download/Panorado50Setup64.exe
   - 下载并运行安装程序 下载并运行安装程序
   - 记住Panorado的安装路径（默认为  记住Panorado的安装路径（默认为 `C:\Program Files\Panorado\Panorado64.exe`））

## 使用方法（已更新）

1.全景图转换 是用来做转换的，之前的版本是用一个三方软件看图

2.look是直接看全景图的。可以录视频。
 
在浏览器中打开显示的本地URL（通常是 http://127.0.0.1:7860）。 在浏览器中打开显示的本地URL（通常是 http://127.0.0.1:7860）。


