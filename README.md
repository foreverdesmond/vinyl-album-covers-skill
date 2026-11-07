# Vinyl Album Covers

黑胶试听频道的视频封面 Skill。

流程:原封面转简笔画 → 人工审核 → GPT 出样片 → 人工审核并选择立刻做、定时做或待定 → 出剩余曲目 → 总览图人工审核。全程不设 AI 审核。GPT 额度耗尽时全部暂停,等负责人授权恢复。

- `SKILL.md`:完整流程。
- `references/prompts.md`:简笔画和封面提示词。
- `references/hermes-card-template.md`:Hermes 派卡模板。
- `assets/gpt-inputs/`:固定参考图,每张小于 1,000,000 字节。
- `scripts/prepare_gpt_inputs.sh`:生图前准备并检查参考图。
- `scripts/make_review_sheet.sh`:生成待审总览图。
- `scripts/batch_covers.py`:full 阶段批量出图并检查文字。
