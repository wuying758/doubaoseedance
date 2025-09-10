# 豆包视频生成工具 (Doubao Video Generation Tool)

一个基于豆包（Doubao）API 的图像到视频生成工具，支持批量处理和单张图片处理两种模式。

## 功能特性

- 🎬 **图像到视频生成**：将静态图片转换为动态视频
- 📁 **批量处理**：支持批量处理多张图片
- 🎯 **单张处理**：支持单张图片的精确处理
- 🎨 **自定义参数**：支持自定义视频分辨率、帧率、时长等参数
- 📸 **帧提取**：自动从生成的视频中提取关键帧
- 💾 **结果保存**：自动保存生成结果和参数配置

## 项目结构

```
doubaoance/
├── doubaoance.py      # 主程序入口
├── utils.py           # 工具函数集合
├── frame.py           # 视频帧处理模块
└── readme.md          # 项目说明文档
```


## 使用方法

### 基本用法

```bash
python doubaoance.py
```

### 命令行参数

| 参数 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--api_key` | `-a` | str || 豆包API密钥 |
| `--save_path` | `-p` | str | ./outputs/ | 结果保存路径 |
| `--base_url` | `-u` | str | https://ark.cn-beijing.volces.com/api/v3 | API基础URL |
| `--prompt` | `-r` | str | None | 视频生成提示词 |
| `--model` | `-m` | str | doubao-seedance-1-0-lite-i2v-250428 | 使用的模型 |
| `--seed` | `-s` | int | -1 | 随机种子 |
| `--size` | `-z` | str | 1280x720 | 视频尺寸 |
| `--num` | `-n` | int | 1 | 生成数量 |
| `--image_dir` | `-i` | str | ./inputs/ | 输入图片目录 |
| `--guidance_scale` | `-g` | float | 5.5 | 引导强度 |
| `--bingxing` | `-b` | bool | True | 是否批量处理 |
| `--resolution` | `-o` | str | 480p | 视频分辨率 |
| `--ratio` | `-t` | str | 16:9 | 宽高比 |
| `--duration` | `-j` | int | 3 | 视频时长（秒） |
| `--fps` | `-f` | int | 24 | 帧率 |
| `--watermark` | `-y` | bool | False | 是否添加水印 |
| `--num_of_frames` | - | int | 5 | 提取帧数 |

### 使用示例

#### 1. 批量处理模式（默认）

```bash
# 使用默认设置批量处理 inputs/ 目录下的所有图片
python doubaoance.py

# 自定义提示词和保存路径
python doubaoance.py -r "摄像机视角旋转一百八十度,快速，无人" -p ./my_outputs/

# 自定义视频参数
python doubaoance.py -o 720p -t 16:9 -j 5 -f 30
```

#### 2. 单张图片处理模式

```bash
# 关闭批量处理，选择单张图片
python doubaoance.py -b False

# 指定特定图片
python doubaoance.py -b False -i ./inputs/specific_image.jpg
```

#### 3. 使用自定义提示词文件

将提示词写入 `prompt.txt` 文件，程序会自动读取：

```
摄像机视角旋转一百八十度,快速，无人
```

## 输出结果

程序会在指定的保存路径下创建以下结构：

```
outputs/
└── YYYYMMDD_HHMMSS/          # 时间戳目录
    ├── args.txt              # 参数配置文件
    ├── 0_of_1/               # 批量处理结果目录
    │   ├── 14_1000.jpg      # 原始输入图片
    │   ├── video.mp4        # 生成的视频
    │   └── frames/          # 提取的关键帧
    │       ├── frame_0.jpg
    │       ├── frame_1.jpg
    │       └── ...
    └── ...
```

## 提示词格式

提示词支持以下特殊参数：

- `--rs <resolution>`: 设置视频分辨率
- `--rt <ratio>`: 设置宽高比
- `--dur <duration>`: 设置视频时长
- `--fps <fps>`: 设置帧率

示例：
```
摄像机视角旋转一百八十度,快速，无人 --rs 720p --rt 16:9 --dur 5 --fps 30
```

## 注意事项

1. **API密钥**：请确保使用有效的豆包API密钥
2. **输入图片**：支持 JPG、JPEG、PNG、BMP、TIFF 格式
3. **网络连接**：需要稳定的网络连接访问豆包API
4. **存储空间**：确保有足够的磁盘空间保存生成的视频文件

## 错误处理

- 程序会自动重试失败的请求
- 错误信息会显示在控制台
- 参数配置会保存到 `args.txt` 文件中便于调试

## 许可证

本项目仅供学习和研究使用，请遵守豆包API的使用条款。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具！
