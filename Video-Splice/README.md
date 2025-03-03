# 视频拼接

## 论文

* **综述论文**：如《A survey on image and video stitching》提供全面概述，适合了解领域现状 ([A survey on image and video stitching](https://www.sciencedirect.com/science/article/pii/S2096579619300063))。
* **实时视频拼接**：如《Real-Time Video Stitching Using Camera Path Estimation and Homography Refinement》，聚焦实时性 ([Real-Time Video Stitching Using Camera Path Estimation and Homography Refinement](https://www.mdpi.com/2073-8994/10/1/4))。
* **深层学习方法**：如《Parallax-Tolerant Unsupervised Deep Image Stitching》，展示最新深层学习技术 ([Parallax-Tolerant Unsupervised Deep Image Stitching](https://arXiv.org/abs/2302.08207))。

这些论文可帮助理解视频拼接的挑战，如动态对象、视差和实时性需求。

## GitHub项目分析

以下GitHub项目提供可复现的代码，适合用户实践和验证。项目通常包括安装说明和示例，但可能需要技术背景调整。以下为推荐列表及其特点：


| 项目名称                  | GitHub URL                                                                                                   | 描述                                                                       | 适用场景                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| Real-time-video-stitching | [https://github.com/wjy5446/Real-time-video-stitching](https://github.com/wjy5446/Real-time-video-stitching) | 基于2017年论文实现，采用光学流和块匹配优化，适合移动相机实时拼接。         | 实时视频拼接，研究效率优化。                                       |
| stitchEm/stitchEm         | [https://github.com/stitchEm/stitchEm](https://github.com/stitchEm/stitchEm)                                 | 360° VR视频拼接工具，支持实时和后期制作，包含用户指南。                   | 沉浸式VR视频，复杂场景应用。                                       |
| UDIS2                     | [https://github.com/nie-lang/UDIS2](https://github.com/nie-lang/UDIS2)                                       | 实现ICCV 2023论文，深层学习无监督图像拼接，可扩展至视频。                  | 深层学习研究，视差处理。                                           |
| video-stitcher            | [https://github.com/ultravideo/video-stitcher](https://github.com/ultravideo/video-stitcher)                 | 基于OpenCV的实时360视频拼接，适合多流输入。                                | 360视频，工业应用。                                                |
| multi\_video\_stitching   | [https://github.com/YMilton/multi\_video\_stitching](https://github.com/YMilton/multi_video_stitching)       | 多视频实时拼接，包含全局和局部对齐，适合多相机场景。                       | 多相机拼接，研究对齐技术。                                         |
| ImageStitching            | [https://github.com/WillBrennan/Imagestitching](https://github.com/WillBrennan/Imagestitching)               | 从视频生成3D全景，适合高分辨率文档扫描，简单易用。                         | 视频到全景，初学者实践。                                           |
| StabStitch                | [https://github.com/nie-lang/StabStitch.git](https://github.com/nie-lang/StabStitch.git)                     | StabStitch是一个前沿的视频拼接工具，特别适合研究无监督学习和在线处理的学者 | 专注于无监督在线视频拼接，旨在消除拼接视频中非重叠区域的抖动问题。 |

这些项目覆盖不同场景，如实时性（Real-time-video-stitching）、沉浸式VR（stitchEm/stitchEm）和深层学习（UDIS2）。用户可根据需求选择，如研究实时算法可优先考虑前者，探索深层学习可选择UDIS2。注意，部分项目（如ImageStitching）专注于图像拼接，但通过逐帧处理可扩展至视频。

# 我的学习日志
