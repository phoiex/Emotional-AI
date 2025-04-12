# Emotional-AI 部署过程

下面是 **Emotional-AI** 项目的详细部署步骤，包括从拉取仓库到启动项目以及后续的配置。

## 1. 拉取仓库

首先，拉取 `Emotional-AI` 项目的代码。

```bash
git clone https://github.com/your-repo/Emotional-AI.git
cd Emotional-AI
```

## 2. 安装 Conda

如果你尚未安装 Conda，可以根据操作系统下载并安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [Anaconda](https://www.anaconda.com/products/individual)。

### 安装完 Conda 后，检查是否成功安装：

```bash
conda --version
```

## 3. 安装 GPT-SoVITS

B站的大佬做的项目，推荐直接下载 GPT-SoVITS 的最新安装包。记得保存解压的位置，因为未来配置时需要使用该路径。

1. **下载 GPT-SoVITS**：访问GitHub 仓库，下载最新的安装包。
2. **解压**：解压到自己指定的目录，记住路径。

## 4. 启动项目

安装完依赖后，可以启动项目。运行以下命令：

```bash
python start_up.py
```

### 如果一切正常：

- 系统会自动为每个项目创建 Conda 环境并安装 `requirements.txt` 中的依赖。
  
### 可能会遇到的问题：

有时 `requirements.txt` 可能有一些问题，导致依赖没有完全安装。这时可以手动安装缺失的库：

```bash
conda activate <目标文件夹名>
pip install <缺少的依赖>
```

## 5. 安装 VTube Studio

1. **VTube Studio 本体**：去 [Steam](https://store.steampowered.com/) 搜索并下载 VTube Studio。
2. **虚拟麦克风**：下载 [VBCABLE_Driver_Pack45](https://www.vb-cable.com/) 并按照安装提示进行安装。安装完成后，配置麦克风为 VBCable 驱动。

## 6. 修改配置

完成上述步骤后，进行以下配置修改：

### 1. 修改 `launch_panel.bat` 中的路径

打开 `launch_panel.bat` 文件，将 `cd` 行的路径修改为你解压的 GPT-SoVITS 目录路径。

### 2. 配置 `weight.json`

将训练好的 `weight.json` 文件放置在 GPT-SoVITS 的根目录下。这样在未来你训练完模型后，可以直接通过配置文件中的模型启动，不需要再点击浏览器。

### 3. 训练音频

如果需要训练音频或进行其他调整，可以参考 B站的教程。
