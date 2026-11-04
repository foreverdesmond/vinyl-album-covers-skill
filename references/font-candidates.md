# 歌曲标题候选字体

## 英文：已确认候选池

Agent按专辑的风格、画法、音乐氛围与清理后的歌名长度选择下表**一种**，在专辑开始时锁定。整个专辑的英文曲名和英文歌手名共用该字族及样式，两种比例、所有子任务一致。不同专辑可以选不同候选，不需要每次让用户审批。用户明确指定字体时优先。

| 字族与准确样式 | 字重/样式 | 选字方向 |
| --- | --- | --- |
| Playfair Display Black Italic | 900 / Italic | 厚实、动势明显的展示衬线标题 |
| Fraunces Black Italic | 900 / Italic；固定opsz=96、SOFT=50、WONK=1 | 厚实圆润、略带复古俏皮感的海报标题 |
| DM Serif Display Italic | 400 / Italic，本身为展示设计，不伪造Bold | 流畅、较柔和的展示斜体 |
| Racing Sans One Regular | 400 / 正式样式名Regular，字体自带倾斜动势，不额外伪斜 | 动感、有力量的无衬线展示标题 |

字体来源为Google Fonts官方仓库，对应目录 `ofl/playfairdisplay/`、`ofl/fraunces/`、`ofl/dmserifdisplay/`、`ofl/racingsansone/`。实际使用准确字体文件/字样样张，不依靠模型从名称猜字。字体文件不随本Skill打包，避免突破Agent单文件大小限制；运行时按环境获取字体，或由主任务提供已排好的透明标题素材。不得在无法加载时让子Agent各自替换。

“Black Italic”是本Skill锁定的字重/样式组合，变量字体需设置相应轴；不能只用同名家族默认400正体。全专辑字号、换行可按模板适配，字族、样式和字重不变。纯中文曲目不必强塞英文；混排曲名按已锁定的中英映射分别排字。

## 中文：已确认候选池

主任务按专辑风格选定下表一种，所有中文曲名/中文歌手名和两种比例统一；新专辑可重新选择，子Agent不各自选。原专辑图内文字保持原作。“黑胶试听”继续使用频道固定思源黑体Heavy，不受中文曲名字体选择影响。

| 字族与准确样式 | 字重/样式 | 选字方向 |
| --- | --- | --- |
| Noto Serif SC Black | 900 / 正体 | 厚重、具有笔画对比的标题宋体 |
| 站酷快乐体 ZCOOL KuaiLe Regular | 400 / 正体，不伪粗 | 活泼、有棱角的海报标题 |
| 站酷庆科黄油体 ZCOOL QingKe HuangYou Regular | 400 / 正体，不伪粗 | 圆润、几何感、适合轻快现代方向 |
| 马善政毛笔楷书 Ma Shan Zheng Regular | 400 / 正体，不伪粗 | 有书写感的国风、怀旧方向 |

官方字体源为Google Fonts仓库 `ofl/notoserifsc/`、`ofl/zcoolkuaile/`、`ofl/zcoolqingkehuangyou/`、`ofl/mashanzheng/`。站酷小薇体已否决，不列入候选。每次须核对歌名全部字形有覆盖，不能缺字后让模型编造，不能把中文字体的日文假名缺失交给随机回退。

## 日文：已确认候选池

主任务按专辑风格从下表选择一种；所有日文歌手名、日文曲名、两种比例和子任务统一该字族及字重。不同专辑可换候选，不逐曲重选。

| 字族与准确样式 | 字重/样式 | 选字方向 |
| --- | --- | --- |
| Noto Serif JP Black | 900 / 正体 | 重明朝，典雅、有张力 |
| Mochiy Pop One Regular | 400 / 正体，不伪粗 | 圆润、可爱、轻快 |
| Reggae One Regular | 400 / 正体，不伪粗 | 棱角鲜明的个性展示标题 |
| Yuji Boku Regular | 400 / 正体，不伪粗 | 和风、毛笔笔触 |

官方字体源为Google Fonts仓库 `ofl/notoserifjp/`、`ofl/mochiypopone/`、`ofl/reggaeone/`、`ofl/yujiboku/`。Dela Gothic One已被替换，不再使用。

日文按整段标题/词组使用日文字体，汉字与平假名、片假名共用日文字体，不能按单字回退到中文映射。中英日混排按语言段落/词组使用已锁定映射，数字和标点跟随所属段落。所谓“每专辑一种”指每种实际语言各选一种，歌手与歌曲按语言共用，不能给歌手另选字体；频道“黑胶试听”是唯一独立固定字样，不参与候选选择。
