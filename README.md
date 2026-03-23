# 剪辑自动化

本目录用于承接当前线程“剪辑自动化”的任务、脚本、素材和输出文件。

## 当前状态

- 线程名称：剪辑自动化
- 工作目录：`G:\AI_Workspaces\剪辑自动化`
- 已完成：基础线程继承、项目骨架、配置模板、素材清单脚本
- 待继续：补充真实剪辑规则、接入渲染工具链

## 目录结构

```text
config/              项目配置
docs/                流程说明与规则文档
jobs/                任务清单与素材 manifest
logs/                运行日志和汇总
materials/
  raw/               原始视频素材
  audio/             配音、BGM、音效
  subtitles/         字幕和文案
output/
  renders/           最终导出
  tmp/               中间文件
scripts/             自动化脚本
README.md            工作区说明
TASKS.md             当前任务清单
THREAD_CONTEXT.md    线程上下文
```

## 快速开始

1. 将素材放入 `materials/raw`、`materials/audio`、`materials/subtitles`
2. 按需修改 `config/project.json`
3. 运行 `powershell -ExecutionPolicy Bypass -File .\scripts\run_manifest.ps1`
4. 查看 `jobs/material_manifest.json` 和 `jobs/material_manifest.csv`

## 已提供能力

- 初始化剪辑自动化工作目录
- 扫描素材目录并生成统一清单
- 提供批处理任务模板
- 为后续接入 ffmpeg、PR 脚本或其他剪辑流程保留配置位

后续如果你继续在这个线程里提需求，我会默认把实现直接写进本目录。
