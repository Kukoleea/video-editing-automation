# 工作流程

## 目标

先将“剪辑自动化”工作区规范化，确保素材、规则、脚本和输出都有固定落点。

## 基本流程

1. 将待处理视频放到 `materials/raw`
2. 将配音、BGM、音效放到 `materials/audio`
3. 将字幕、文案、台词草稿放到 `materials/subtitles`
4. 根据项目实际情况调整 `config/project.json`
5. 运行素材扫描脚本，生成统一清单
6. 再基于清单接入实际剪辑、渲染、封装流程

## 当前可用命令

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\run_manifest.ps1
```

或：

```powershell
python .\scripts\generate_manifest.py
```

## 当前输出

- `jobs/material_manifest.json`
- `jobs/material_manifest.csv`
- `logs/manifest_summary.txt`

## 后续建议

- 明确每类视频的目标时长、比例、片头片尾规则
- 确认使用 `ffmpeg`、Premiere 脚本，还是其他剪辑工具
- 将“任务定义”从文档升级成结构化配置
