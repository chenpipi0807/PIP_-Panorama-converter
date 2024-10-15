## 全景图转换器 全景图转换器

这是一个基于Python和Gradio开发的全景图转换和查看工具。它可以将普通图片转换为全景图，并使用Panorado软件查看全景图。这是一个基于Python和Gradio开发的全景图转换和查看工具。它可以将普通图片转换为全景图，并使用Panorado软件查看全景图。

## 功能特点

1. 将普通图片转换为全景图 将普通图片转换为全景图
2. 直接查看已有的全景图 直接查看已有的全景图
3. 使用Panorado软件打开和查看全景图 使用Panorado软件打开和查看全景图
4. 简单易用的图形界面 简单易用的图形界面

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

## 使用方法

1. 运行脚本： 运行脚本：
   ```
   python 全景图转换.py
   ```

2. 在浏览器中打开显示的本地URL（通常是 http://127.0.0.1:7860）。 在浏览器中打开显示的本地URL（通常是 http://127.0.0.1:7860）。

3. 在Gradio界面中： 在Gradio界面中：
   - 如果要转换普通图片为全景图： 如果要转换普通图片为全景图：
     1. 在"上传非全景图"区域上传您想要转换的图片 在"上传非全景图"区域上传您想要转换的图片
     2. 等待处理完成，转换后的全景图将显示在"转换后的全景图"区域 等待处理完成，转换后的全景图将显示在"转换后的全景图"区域
     3. 系统会自动尝试使用Panorado打开全景图 系统会自动尝试使用Panorado打开全景图

   - 如果要查看已有的全景图： 如果要查看已有的全景图：
     1. 在"上传全景图"区域上传您的全景图 在"上传全景图"区域上传您的全景图
     2. 系统会保存该图片并尝试使用Panorado打开 系统会保存该图片并尝试使用Panorado打开

4. 如果Panorado无法自动打开： 如果Panorado无法自动打开：
   - 检查"Panorado路径"输入框中的路径是否正确 检查"Panorado路径"输入框中的路径是否正确
   - 如果路径不正确，请输入正确的Panorado安装路径 如果路径不正确，请输入正确的Panorado安装路径
   - 如果未安装Panorado，请按照提示的链接下载并安装 如果未安装Panorado，请按照提示的链接下载并安装

5. 查看"结果"文本框中的消息，了解处理状态和任何可能的错误信息。 查看"结果"文本框中的消息，了解处理状态和任何可能的错误信息。

## 注意事项

- 确保您有足够的磁盘空间来保存转换后的图片。 确保您有足够的磁盘空间来保存转换后的图片。
- 处理大型图片可能需要一些时间，请耐心等待。 处理大型图片可能需要一些时间，请耐心等待。
- 如果遇到任何问题，请查看控制台输出的日志信息以获取更多详细信息。 如果遇到任何问题，请查看控制台输出的日志信息以获取更多详细信息。

## 故障排除

1. 如果无法找到Panorado： 如果无法找到Panorado：
   - 确保已正确安装Panorado 确保已正确安装Panorado
   - 在"Panorado路径"输入框中手动输入正确的安装路径 在"Panorado路径"输入框中手动输入正确的安装路径

2. 如果图片处理失败： 如果图片处理失败：
   - 确保上传的是有效的图片文件 确保上传的是有效的图片文件
   - 检查图片文件是否损坏或格式不受支持 检查图片文件是否损坏或格式不受支持

3. 如果Gradio界面无法加载： 如果Gradio界面无法加载：
   - 确保所有依赖项都已正确安装 确保所有依赖项都已正确安装
   - 尝试重新启动脚本 尝试重新启动脚本

如果您遇到任何其他问题或需要进一步的帮助，请随时联系开发者或在项目的问题追踪器中提出问题。如果您遇到任何其他问题或需要进一步的帮助，请随时联系开发者或在项目的问题追踪器中提出问题。

祝您使用愉快！祝您使用愉快！
