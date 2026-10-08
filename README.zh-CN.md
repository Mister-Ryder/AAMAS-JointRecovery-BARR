# AAMAS · Joint Recovery · BARR pair-fusion

本仓库管理产生 **BARR v0.4 B 确认批次**的候选 B 冻结源码、输入和结果。
该算法的原生命令为 `--mode pair --pair-policy fusion-refine`。

同一 `main` 分支集中存储 B 的局部搜索、融合、解析 pair 筛选、选择性扩展、结构恢复和归档反馈组件，以及紧相关的 E 源码与 E/F 数值记录。

![算法结构](docs/figures/barr-pair-fusion-zh.png)

- [详细算法与实现映射](docs/ALGORITHM.md)
- [问题模型、数学定义与伪代码](docs/MODEL_AND_PSEUDOCODE.md)
- [模型与算法 PDF](docs/barr_model_algorithm.pdf)
- [结果、逐种子记录与运行协议](docs/RESULTS.md)
- [可编辑 draw.io](docs/figures/barr-pair-fusion-zh.drawio) / [矢量 PDF](docs/figures/barr-pair-fusion-zh.drawio.pdf)
- [源码哈希](provenance/frozen_sources.json) / [原始参数](profiles/pair-fusion.json)

B 确认使用 8 个视图 × 种子 31/37/41，24 条记录的八视图等权均值为
**1,135,933.2073965834 contact-seconds**。相关 E 的 F 对照使用种子
83/89/97，其均值为 **1,135,843.5161470417**。批次、种子和二进制身份分列保存。

构建和运行命令见 [README](README.md)。入口固定种群 4、单线程和不少于
360 秒的原生搜索预算；`--dry-run` 仅显示命令。仓库中的原始记录来自既有实验，
本次整理未重新进行性能搜索。
