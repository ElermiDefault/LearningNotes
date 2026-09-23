---
title: A2：构建 PathMNIST 数据管线
date: 2026-09-23
stage: Project A · MedMNIST 学习
tags: 病理影像, PyTorch, DataLoader, 图像预处理
summary: 用 PyTorch 完成 PathMNIST 的数据变换、三种数据划分与批量加载，检查了首个 batch 的形状、类型、取值范围和设备，并将图像反归一化后可视化。
---

## 今天做了什么

- 在 `02_data_pipeline.ipynb` 中定位项目目录，并确认本地 `pathmnist.npz` 存在；
- 用 `ToTensor()` 将图像从 `HWC` 排列转换为 `CHW` 张量，并把像素缩放到 `[0, 1]`；
- 用 `Normalize(mean=0.5, std=0.5)` 对三个通道分别归一化；
- 创建 PathMNIST 的训练集、验证集和测试集，样本数分别为 `89996`、`10004` 和 `7180`；
- 用 `DataLoader` 以 `batch_size=32` 组织数据：训练集打乱顺序，验证集和测试集保持固定顺序；
- 取出一个 batch，检查图像和标签的形状、数据类型、数值范围与所在设备；
- 将前 8 张图像反归一化并从 `CHW` 转为 `HWC`，结合类别名称完成可视化。

Notebook：`/Volumes/GYF's HDD/预备工作/Project_A/work/02_data_pipeline.ipynb`

可视化结果：`/Volumes/GYF's HDD/预备工作/Project_A/project_notes/figures/pathmnist_transformed_bacth.png`

## 我弄明白了什么

- `Dataset` 负责定义单个样本如何读取，`DataLoader` 负责把样本组成 batch，并控制是否打乱、batch 大小和加载进程数；
- PathMNIST 返回的单个标签形状为 `(1,)`，因此一个 batch 的标签形状是 `(32, 1)`。使用 `targets.squeeze(1).long()` 后，标签变为交叉熵损失常用的 `(32,)` 和 `torch.int64`；
- 图像 batch 的形状是 `(N, C, H, W)`。本次实际得到 `(32, 3, 28, 28)`，数据类型为 `torch.float32`；
- `Normalize(mean=0.5, std=0.5)` 实际执行 `(x - 0.5) / 0.5`，所以输入在 `[0, 1]` 时理论范围为 `[-1, 1]`。当前 batch 的实际范围是约 `[-0.851, 0.984]`；
- `iter(train_loader)` 创建迭代器，`next(...)` 取出第一个 batch；常规训练循环中的 `for` 会自动完成这一步；
- `.to(device)` 将图像和标签移动到 MPS 或 CPU。本次运行使用 `mps:0`；
- 可视化前需要用 `x * 0.5 + 0.5` 撤销归一化，再用 `permute(1, 2, 0)` 将 `CHW` 转回 Matplotlib 使用的 `HWC`。

## 还没有解决的问题

本次 notebook 已完整运行，没有出现报错，但有两处概念需要继续保持准确：

1. `squeeze()` 不传参数时会删除所有大小为 1 的维度，并不是默认等同于 `squeeze(1)`。这里明确写 `squeeze(1)` 更安全；
2. `.numpy()` 只能直接用于 CPU 张量。当前用于显示的 `images` 仍在 CPU 上，所以可以直接转换；如果从 MPS 张量开始，应先调用 `.cpu()`。

## 下一步

在这条数据管线上加入一个简单分类模型，用一个 batch 跑通前向传播、交叉熵损失和反向传播，并记录输入、输出与损失张量的形状。
