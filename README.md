# Emotional-AI 
##部署过程
### 1. 拉取仓库

首先，需要拉取 `Emotional-AI` 项目的代码。

```bash
git clone https://github.com/your-repo/Emotional-AI.git
cd Emotional-AI
```

### 2. 安装 Conda

如果尚未安装 Conda，请根据操作系统下载并安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/individual)。

### 3. 安装GPT-SoVITS

B站的大佬做的项目，我是直接下载了最新的安装包，记住自己解压的位置就ok，未来配置需要使用

### 4. 启动项目
安装完毕后，运行以下命令启动项目：
```bash
python start_up.py
```
如果一切正常，会自动为每个项目安装conda并按照requirements.txt安装依赖，也有可能有一些requirements.txt有问题，这时候需要手动安装一些依赖
```bash
conda activate <目标文件夹名>
pip install <缺少的依赖>
```

### 5. 安装VTube Stduio
1. 本体：这个去steam上一搜就可以了，然后导入模型啥的都可以看教程
2. 虚拟麦克风：下载VBCABLE_Driver_Pack45，然后按照提示安装就可以，最后到本体中配置麦克风为这个

### 6. 修改配置
  1. 在launch_panel.bat里把cd行的路径改为你GPT-SoVITS解压的位置
  2. 把weight.json文件放到GPT-SoVITS根目录下，在未来你训练完模型后可以通过修改配置文件中的模型实现直接启动9872端口，不用再点击浏览器
  3. 如果有训练音频需要的话就去参考B站教程
