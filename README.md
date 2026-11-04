# 黑胶专辑封面 Skill

提供唱片封面、歌手和专辑名，自动核实曲目，为全专辑逐首制作视频封面，输出 **4:3（1600×1200）** 与 **16:9（1920×1080）** PNG，并打包 ZIP。

当前仓库包含完整 Skill、频道透明 LOGO、原始 B 站参考图、默认画法校准图和生成规则。当前版本对应本地 v9。

## 使用

将本仓库克隆到个人 Skill 目录，保留现有 Skill 标识：

```bash
git clone https://github.com/foreverdesmond/vinyl-album-covers-skill.git ~/.codex/skills/artifact-template-vinyl-album-covers
```

如果该路径已安装旧版，请先保存旧目录，再将仓库安装到同一路径，不要覆盖未保存的修改。

在支持 Skill 的环境中调用 `$artifact-template-vinyl-album-covers`，上传唱片封面并提供：

```text
歌手：……
专辑名：……
主题：万圣节（可选）
画风：赛博朋克风（可选）
```

也可直接读取本仓库根目录的 `SKILL.md`，按相对路径加载所需素材和参考说明。在 Gemini 等环境使用时，需要能够读取相应文件并调用图像生成/编辑工具；本仓库是 Skill 指令与素材，不是独立的出图程序。

## 主要规则

- **默认画法**：陈奕迅精选确认成品的细腻半写实编辑插画，只借鉴绘制技法，不继承其配色、家具或布局。用户明确给出其他画风时替换默认画法。
- **配色与主题独立**：默认从当前唱片取色；主题重建场景，不能把历史成品的紫色、音箱或书架自动带进来。
- **保留原作**：先保留内部构图，将用户提供的专辑封面转换画法并锁定素材；不重新创作专辑图。
- **同专辑有变化**：逐曲轮换构图、字体、唱机、唱片、配饰和 LOGO 位置，保持共同视觉语言。
- **LOGO 直接使用**：默认只使用 `assets/channel-logo.png` 透明 PNG，不重新抠图、改字或改色。
- **黑胶试听醒目**：四字单行、粗字重、高对比，实际字高目标为画高的 10–13%，下限 9%。
- **输出目录**：直接在任务项目根目录创建以专辑名命名的文件夹，图片、清单、素材和最终 ZIP 均置于其中。

## 文件结构

```text
SKILL.md                    Skill 入口与工作流程
artifact-template.json      模板信息
agents/openai.yaml          显示与调用配置
assets/channel-logo.png     默认使用的透明 LOGO
assets/bilibili-references/  三张原始 B 站封面
assets/history/             历史成品与默认画法校准资料
references/                 画法、构图、配色、主题和生成提示词
```

历史成品和 LOGO 整张原始素材用于留档；是否传入模型由 `SKILL.md` 明确规定，不应将整个素材目录无差别附给模型。

## 更新与验证

在克隆目录中修改并通过 Git 提交，以仓库历史管理版本。同步到其他环境时使用完整仓库，保持 `SKILL.md`、`references/` 与 `assets/` 一起更新。

Skill 名仍为 `artifact-template-vinyl-album-covers`，与仓库名 `vinyl-album-covers-skill` 不同；保留该名称可继续使用现有调用方式。
