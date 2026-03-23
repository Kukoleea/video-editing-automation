# 任务格式说明

`jobs/edit_job.template.json` 用来定义单条视频或单批次视频的处理参数。

## 字段说明

- `job_name`：任务名，建议唯一
- `enabled`：是否启用
- `source_materials.video`：输入视频列表
- `source_materials.audio`：输入音频列表
- `source_materials.subtitles`：字幕或文案文件列表
- `timeline.target_duration_seconds`：目标时长
- `timeline.aspect_ratio`：画幅比例，例如 `16:9` 或 `9:16`
- `timeline.resolution`：输出分辨率
- `timeline.fps`：帧率
- `rules.intro_seconds`：片头预留秒数
- `rules.outro_seconds`：片尾预留秒数
- `rules.subtitle_burn_in`：是否压制字幕
- `rules.bgm_mix_level_db`：BGM 混音音量
- `output.directory`：输出目录
- `output.filename`：输出文件名

## 使用建议

1. 从模板复制出实际任务文件
2. 将素材路径改成当前项目的真实路径
3. 按视频类型调整时长和比例
4. 后续接入执行脚本时，以这个结构作为输入
