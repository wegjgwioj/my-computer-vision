# Video-stitching


## 一、问题背景


1. 多摄像头画面存在15-30%重叠区域，导致存储资源浪费和检索效率低下
2. 单镜头视角局限（通常<90°），无法满足场景的广域监控需求

通过开发实时视频拼接系统，实现：

- 360°全景监控画面实时合成
- 多路视频流智能去重处理
- 低延时高画质的监控回放

## 二、研究记录


| Task     | Description                                                                     | Outcome |
| -------- | ------------------------------------------------------------------------------- | ------- |
| 图像增强 | 饱和度增强、对数增强、指数增强算法<br />  对比度等等<br /><br />    <br /> |         |
|          |                                                                                 |         |



## 简介


> ### 特点
>
> 现如今，由于硬件和软件中视频稳定技术的进步和广泛采用，手持相机拍摄的视频通常是稳定的。在这种情况下，我们将视频拼接重新定位到一个新兴问题，即扭曲抖动，它描述了在非重叠区域中的不希望的内容不稳定性，特别是当图像拼接技术直接应用于视频时。为了解决这个问题，我们提出了第一个无监督在线视频拼接框架，名为 StabStitch，通过生成拼接轨迹并对其进行平滑处理。
>

## 视频

在这里，我们提供了一个 [视频](https://www.youtube.com/watch?v=03kGEZJHxzI&t)（在 YouTube 上发布），展示了 StabStitch 和其他解决方案的拼接结果。

## 📝 更新日志

- [X]  2024.03.11: arXiv 版本的论文上线。
- [X]  2024.07.11: 我们已将原始 arXiv 版本替换为最终的相机就绪版本。
- [X]  2024.07.11: StabStitch-D 数据集可用。
- [X]  2024.07.11: 推理代码和预训练模型可用。
- [X]  2024.07.12: 我们添加了对局限性和前景的简单分析。

## 数据集 (StabStitch-D)

数据集的详细信息可以在我们的论文中找到。([arXiv](https://arxiv.org/abs/2403.06378))

数据集可以在 [Google Drive](https://drive.google.com/drive/folders/16EDGrKOLLwcMseOjpI7bCrv_aP1MYVcz?usp=sharing) 或 [百度云](https://pan.baidu.com/s/1TKQAQ9zryUuU4uzTiswfHg)(提取码: 1234) 获取。

## 代码

#### 要求

我们使用一块 RTX4090Ti GPU 实现 StabStitch。有关更多详细信息，请参阅 [environment.yml](https://github.com/nie-lang/StabStitch/blob/main/environment.yml)。

#### 预训练模型

预训练模型（spatial_warp.pth、temporal_warp.pth 和 smooth_warp.pth）可以在 [Google Drive](https://drive.google.com/drive/folders/1TuhQgD945MMnhmvnOwBS1LoLkYR1eetj?usp=sharing) 或 [百度云](https://pan.baidu.com/s/1TTSbR4UYFL8f-nP3aGME7g)（提取码: 1234）获取。请下载它们并放在 'model' 文件夹中。

#### 在 StabStitch-D 数据集上测试

修改 Codes/test_online.py 中的 test_path 并运行：

```
python test_online.py
```

然后，将自动创建一个名为 'result' 的文件夹来存储拼接视频。

关于 TPS 扭曲函数，我们设置了两种模式来扭曲帧，如下所示：

* 'FAST' 模式：它使用 F.grid_sample 实现插值。速度快，但可能会产生细小的黑色边界。
* 'NORMAL' 模式：它使用我们实现的插值函数。速度稍慢，但可以避免黑色边界。

您可以在 [这里](https://github.com/nie-lang/StabStitch/blob/0c3665377e8bb76e062d5276cda72a7c7f0fab5b/Codes/test_online.py#L127) 更改模式。

#### 计算 StabStitch-D 数据集上的指标

修改 Codes/test_metric.py 中的 test_path 并运行：

```
python test_metric.py
```

## 局限性和未来展望

### 泛化

为了测试模型的泛化能力，我们采用预训练模型（在 StabStitch-D 数据集上）对传统视频拼接数据集进行了一些测试。令人惊讶的是，它严重退化并产生明显的失真和伪影，如下图 (a) 所示。为了进一步验证泛化能力，我们从传统视频拼接数据集中收集了其他视频对（超过 30 对视频）并在新数据集中重新训练我们的模型。如图 (b) 所示，它在新数据集中表现良好，但在 StabStitch-D 数据集上无法生成自然的拼接视频。
![image](https://github.com/nie-lang/StabStitch/blob/main/limitation.png)

### 展望

我们发现性能退化主要发生在空间扭曲模型中。如果没有校正的空间扭曲，后续的平滑处理将放大失真。

这就提出了一个问题，即如何确保基于学习的拼接模型的泛化能力。一个简单直观的想法是建立一个大规模的真实世界拼接基准数据集，包含各种复杂场景。这应该有助于各种拼接网络的泛化。另一个想法是将持续学习应用于拼接领域，使网络能够在具有不同分布的各种数据集中稳健地工作。

这些只是一些简单的建议。我们希望您，这个领域的聪明才智，能够帮助解决这个问题并为该领域的进步做出贡献。如果您有一些想法并希望与我讨论，请随时给我发电子邮件。我对任何形式的合作都持开放态度。

## 元信息

如果您对这个项目有任何问题，请随时给我发电子邮件。

聂朗 -- nielang@bjtu.edu.cn

```
@inproceedings{nie2024eliminating,
  title={消除无监督在线视频拼接中的扭曲抖动},
  author={Nie, Lang and Lin, Chunyu and Liao, Kang and Zhang, Yun and Liu, Shuaicheng and Ai, Rui and Zhao, Yao},
  booktitle={欧洲计算机视觉会议},
  pages={390--407},
  year={2024},
  organization={Springer}
}
```

## 参考文献

[1] S. Liu, P. Tan, L. Yuan, J. Sun, and B. Zeng. Meshflow: Minimum latency online video stabilization. ECCV, 2016.
[2] L. Nie, C. Lin, K. Liao, S. Liu, and Y. Zhao. Unsupervised Deep Image Stitching: Reconstructing Stitched Features to Images. TIP, 2021.
[3] L. Nie, C. Lin, K. Liao, S. Liu, and Y. Zhao. Parallax-Tolerant Unsupervised Deep Image Stitching. ICCV, 2023.
