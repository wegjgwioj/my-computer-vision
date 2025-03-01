# 实时视频拼接

## 项目简介

本项目是一个基于深度学习的视频拼接系统，旨在实现实时视频流的全景拼接。系统利用三个深度学习模型（`SpatialNet`、`TemporalNet` 和 `SmoothNet`）分别完成空间对齐、时间对齐和平滑处理，最终生成高质量的拼接视频流。项目支持从两个 RTSP 视频流拉取帧，实时处理后输出为指定格式（如 RTSP 或 FLV）的全景视频流，适用于局域网或外网观看。

---

### 环境要求

- **操作系统**：Ubuntu 18.04 或更高版本
- **Python**：3.8 或更高版本
- **深度学习框架**：PyTorch（推荐使用 GPU 版本）
- **视频处理库**：OpenCV、FFmpeg
- **Web 服务框架**：Flask、Gunicorn（推荐用于生产环境）

---

### 安装步骤

1. **克隆项目代码**：

   ```bash
   git clone https://github.com/your-repo/video-stitching.git
   cd video-stitching
   ```
2. **安装依赖**：

   ```bash
   pip install -r requirements.txt
   ```

   项目依赖包括：

   ```
   torch
   torchvision
   opencv-python
   flask
   numpy
   einops
   scikit-image
   gunicorn
   ```
3. **安装 FFmpeg**（用于视频流处理）：

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
4. **准备模型权重**：

   - 将预训练模型文件（`spatial_warp.pth`、`temporal_warp.pth`、`smooth_warp.pth`）放置于 `full_model_ssd` 目录下。
   - 确保路径与代码中的 `MODEL_DIR` 配置一致。

---

### 运行指南

#### 1. 运行 Flask 开发服务器（开发环境）

- 启动服务：
  ```bash
  python app.py
  ```
- 服务将监听 `http://0.0.0.0:5000`。

#### 2. 运行 Gunicorn（生产环境）

- 推荐使用 Gunicorn 作为 WSGI 服务器，提供更好的并发处理能力。
- 启动服务：
  ```bash
  gunicorn -c gunicorn.conf.py app:app
  ```
- 服务配置（如工作进程数、端口等）在 `gunicorn.conf.py` 中定义。

---

### 模型使用

项目使用以下三个深度学习模型：

- **SpatialNet**：负责空间对齐，处理帧间的空间变换。
- **TemporalNet**：负责时间对齐，确保视频帧序列的时间一致性。
- **SmoothNet**：负责平滑处理，提升视频流拼接的平滑度。

模型权重文件需放置在 `pthdoc` 目录下：

- `spatial_warp.pth`
- `temporal_warp.pth`
- `smooth_warp.pth`

---

### 实时视频流处理

项目支持从两个 RTSP 视频流拉取帧，实时处理并拼接为一个全景视频流。处理流程如下：

1. **视频流输入**：从两个 RTSP 地址拉取视频帧。
2. **帧预处理**：调整帧尺寸、归一化等操作。
3. **模型推理**：通过 `SpatialNet`、`TemporalNet` 和 `SmoothNet` 进行空间对齐、时间对齐和平滑处理。
4. **视频流输出**：使用 FFmpeg 将处理后的帧推送为 RTSP 或 FLV 流。

#### 启动实时拼接服务

- 发送 POST 请求到 `/stitch` 端点，传入两个视频流的 RTSP 地址和输出流地址。
- 示例请求：
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{
      "url1": "rtsp://192.168.1.100:554/video1",
      "url2": "rtsp://192.168.1.100:554/video2",
      "output_url": "rtsp://localhost:8554/live"
  }' http://localhost:5000/stitch
  ```
- 服务将开始处理并在指定地址输出拼接后的视频流。

#### 查看输出流

- 使用 VLC 播放器打开 `rtsp://localhost:8554/live` 查看实时拼接视频。

---

### Gunicorn 配置

为提升并发处理能力，项目使用 Gunicorn 作为 WSGI 服务器。配置文件 `gunicorn.conf.py` 包含以下关键参数：

- `workers`：工作进程数，建议根据 CPU 核心数设置。
- `bind`：绑定地址和端口，如 `0.0.0.0:5000`。
- `timeout`：请求超时时间，设置为 120 秒以适应视频处理需求。

---

### 服务测试

1. **启动服务**：
   - 开发环境：`python app.py`
   - 生产环境：`gunicorn -c gunicorn.conf.py app:app`
2. **发送请求**：
   - 使用 curl 或 Postman 发送 POST 请求到 `/stitch` 端点。
3. **验证输出**：
   - 使用 VLC 打开输出流地址，检查视频拼接质量和实时性。

---

### 注意事项

- **GPU 环境**：确保服务器配备 NVIDIA GPU 并安装 CUDA、cuDNN。
- **网络带宽**：外网部署时，确保带宽支持高分辨率视频流传输。
- **延迟控制**：系统延迟受模型推理和处理时间影响，优化模型可进一步降低延迟。
- **日志监控**：建议启用 Gunicorn 日志，监控服务运行状态。

---

### 优化建议

- **模型加速**：使用 TensorRT 优化模型推理速度。
- **并行处理**：在多 GPU 上分配任务，提升处理能力。
- **分辨率调整**：在视觉质量可接受范围内减小输入分辨率，减少计算量。

---

通过以上 ，用户可以清晰地了解项目的功能、安装和运行步骤，以及实时视频流处理的具体操作。希望这份文档能为你的项目提供良好的使用指引！
