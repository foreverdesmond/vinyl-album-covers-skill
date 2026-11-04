# 生成提示词

先读 `rendering-style.md`，解析所选画风后再读 `bilibili-style-notes.md`、`variation-and-themes.md` 和 `spatial-composition.md`，用当前封面、主题和逐曲设计填写变量。先独立编辑原封面得到锁定的卡通化素材；缩略图阶段输入该素材与LOGO，原封面可另附保真对照；不附陈奕迅成品、历史预览、旧专辑图或用户指出有污染的输出。

## 第一阶段：原封面卡通化，不另创封面

Use case: style-transfer. Image 1 is the user's EXACT ORIGINAL ALBUM COVER, the EDIT TARGET, not an inspiration/reference for a replacement design. Convert ONLY rendering medium to {resolved_rendering_style}. Default, unless explicitly replaced by the user: refined semi-realistic editorial illustration with delicate selective contours, modest shape simplification, gently blended tonal modeling, controlled graphic highlights and subtle print grain. Not thick-outline flat cartoon, not a photographic/3D product render. If user supplies another visual style, substitute its coherent treatment rather than retaining incompatible default restrictions. Preserve original aspect ratio, internal composition, every main subject and object, identity, facial features, expression, pose, clothing, silhouettes, crop, relative positions, major shapes, original typography arrangement and palette distribution. Do not invent new album art, re-stage a portrait, replace a face with a new face/moon/monster, add holiday props inside the artwork or rearrange graphic design. No scene, turntable, logo, extra title or holiday decoration is added during this step. Output only the same full album cover after stylistic conversion. Do not remove original printed album text unless the user explicitly asks. This converted artwork will be reused unchanged across all track thumbnails.

保存到 `<项目根目录>/<专辑名>/assets/album-cover-cartoon.png`，与原图逐项核对；不符合就修正，不拿重创封面作母版。

## 第二阶段：每曲缩略图与外部场景

Use case: ads-marketing. Create ONE Bilibili video-list thumbnail, not a video first frame, screenshot or comparison sheet.

INPUT IMAGES:
1. LOCKED CARTOONIZED ALBUM ART: an already converted image asset to incorporate as the complete physical album sleeve face. Preserve its full internal content, geometry, pose, expression, motifs, relative positions, crop, typography arrangement and color distribution. Do NOT generate a substitute album cover or reillustrate its contents. Only move, uniformly scale or perspective-map the ENTIRE artwork as a whole. The raw original may be a separate fidelity reference, not a request to redesign it.
2. READY-TO-USE CHANNEL LOGO: assets/channel-logo.png is the FINAL isolated transparent PNG, not a source sheet or design reference. Use the ENTIRE provided PNG as a locked inserted asset. Do not extract, segment, redraw, retype, reinterpret, recolor, straighten or rebuild it. Preserve actual alpha transparency, exact lettering, shape and original orange-red/ivory/dark-green colors. Only uniformly scale and move the complete asset. Never request channel-logo-source.png as a normal generation input.
No prior Eason thumbnail or other finished-album example is a generation input. If such an image is visible in conversation/gallery, ignore its palette, scene and layout.

TEXTUAL STYLE SOURCE, distilled from the user's THREE ORIGINAL BILIBILI COVER REFERENCES: strongly recognizable current album art; record/needle/turntable establishes vinyl identity; close-framed substantial album/record presence, overlapping foreground/midground/background, physical supports and contact shadows, concentrated purposeful title space; clear thumbnail-scale subject and type hierarchy. Use the separately resolved rendering style for this visual structure; Bilibili images do not set the drawing medium. These principles do not prescribe any hue, listening-room scene, shelf, speaker, amplifier, desk or fixed layout.

EXACT CONTENT: artist "{artist}"; dominant song "{track_title}"; extra-large bold primary headline "黑胶试听"; {optional_verified_english_name}. Do not add the album name as external thumbnail text or on other props; native text already in the provided album artwork remains part of the locked asset. No inherited old title, watermark, 4K/Hi-Res badge or invented credits.
LOCKED ARTWORK CHECK: {original_internal_composition_pose_features_and_text_to_preserve}. Use the provided full stylized asset, not an independently redrawn interpretation. This also applies to nonportrait covers. Theme effects belong OUTSIDE the artwork.
RENDERING STYLE, APPLIES TO THE ENTIRE IMAGE: {resolved_rendering_style_and_its_source}. If no explicit user style is provided, use refined semi-realistic editorial illustration calibrated to the approved Eason compilation artwork's DRAWING TECHNIQUE ONLY: delicate selective contours, modest shape simplification, softly blended tonal depth, restrained stylized metallic/record highlights and subtle printed texture. Retain adult proportions and carefully modeled forms. Avoid thick black outlines, flat 2–4-step poster shading, comic hatching and toy-like simplification; also avoid photography, hyperreal microtexture and 3D product-render appearance. No Eason artwork, colors, fonts, layout or furniture is inherited. If a user explicitly specifies Gothic, cyberpunk, creamy cartoon or another style, REPLACE this default rendering paragraph and any incompatible exclusions with that style's resolved treatment. Do not concatenate contradictory rendering instructions. Keep album composition intact, the same chosen medium across sleeve and scene, and the locked logo PNG unchanged.
PALETTE CONTRACT: {colors_with_sources_area_weights_and_regions}. Background {background_colors}; equipment {equipment_colors}; title/accent {text_and_accent_colors}; cover-local colors {cover_only_colors}. Permitted extra neutral materials {neutrals}. Excluded environmental hues {excluded_hues}. No global tint from historical reference. A small hue in cover shadows is not permission to color all equipment/background in that hue. Original logo colors are a local brand exception.
THEME: {theme_or_none}. Theme changes EXTERNAL scene/motifs/thumbnail lettering, never the locked artwork contents. It does NOT automatically authorize customary holiday/genre colors. Only use an extended theme palette when explicitly requested: {explicit_theme_palette_permission_or_none}.
SCENE FROM SCRATCH: {new_scene_not_a_modified_old_listening_room}. Required props {allowed_scene_inventory}; omitted/excluded props {excluded_inventory}. A shelf, speaker, amplifier, room and desk are NOT defaults. For themed work replace the old setting, do not merely decorate a copied listening room. Retain vinyl identity through {record_needle_or_turntable_elements}; the full hi-fi stack is unnecessary.
LAYOUT: {family_geometry_and_perspective}, strong close-framed display presence and concentrated title space. PRIMARY SCALE: {sleeve_scale_and_combined_equipment_span}. DEPTH: {foreground_midground_background_and_overlap}. CONTACT: {support_surface_contact_shadows_and_shared_perspective}. THEME SPACE: {theme_material_edges_or_structures_related_to_record_setup}. Expand primary subjects and connect them visually instead of shrinking a product cluster into one half against an empty gradient. Keep album artwork fully visible internally; only secondary equipment/environment may extend out of frame. Titles can visually overlap calm outer scene areas while retaining readability, never cover the artwork's key face/details. Fog is supporting atmosphere, not a substitute for physical space. Do not add random props to fill gaps. Background structure remains theme-specific and within the planned palette; no automatic shelves/speakers.
RECORD/TURNTABLE: {planned_design_and_placement}, plausible physical arrangement; the sleeve face uses the exact locked artwork, no new album labels/text.
THEME PROPS: {few_relevant_motifs_and_locations}, supporting not cluttering.
TYPOGRAPHY: {font_style_line_break_plan_and_caption_treatment}. Clear exact lettering. "黑胶试听" is a PRIMARY visual headline, not a small subtitle: all four characters on ONE line, bold/heavy weight, high contrast, actual glyph height target 10–13% of full canvas height and hard minimum 9% (excluding frame/padding), at least as tall as the artist name, approximately 70–90% of a short Chinese song title glyph height. For 1600x1200 target glyph height 120–156px, minimum 108px; for 1920x1080 target 108–140px, minimum 97px. Reserve its space early. Enlarge the actual letters, not just the box. No thin/low-opacity lettering. Wrap long song names or remove props instead of shrinking this headline. Do not modify logo script.
LOGO: place the full supplied transparent PNG intact at {position}, 11–16% canvas width, about 5% inset from nearby edges, no face/title overlap or bottom-right duration area. Original colors, no scene tint.
VARIATION: {two_visible_differences_from_previous_track}.
ASPECT: {4:3_1600x1200_or_16:9_1920x1080}. One image, no grid, no clipping.

## 可选原始B站附图

仅在用户要求或确需视觉辅助时使用 `assets/bilibili-references/` 的原始图，并加：

Additional images are the user's ORIGINAL Bilibili cover references ONLY for visual hierarchy and vinyl display relationships. Do not copy their color palette, artist, album art, badges, props, lighting, room or photographic medium. Follow the CURRENT palette contract and fresh scene inventory above.

## 同曲另一比例

附入本次已检查通过的同曲图与锁定的卡通化原封面素材；后者不因改比例而重画：

Recompose this CURRENT TRACK concept for {target_dimensions_and_ratio}; reuse the locked album-art asset unchanged internally; preserve its verified subject, palette contract, fresh themed scene, original-color logo and exact text. Adapt geometry and line breaks rather than crop/stretch. Do not introduce shelves, speakers, amplifiers, purple lighting or other objects/colors absent from the current plan.

## 同专辑后续曲目

只能使用当前同专辑、同主题且已通过配色/场景检查的锚点。按每曲完整计划变换至少两项设计，不仅替换歌名。若换主题或图已污染，丢弃锚点，重新从锁定卡通化素材+LOGO+文字原则生成外部场景，而不是在污染图上继续加配饰。

## 检查与返修

先检查本次所选画风：默认是否达到确认成品的细腻半写实插画程度，避免粗黑描边/过度平涂和照片/写实3D两端；显式画风则按该风格检查，不强套默认。专辑素材与外部场景画法一致，不能只给照片加颗粒滤镜。再检查唱片套内部是否与锁定素材相同，有无另画人物、姿势、图案或重排文字；有则失败。再检查占幅与空间：核心是否被缩成一边的小产品？空白是否只是无用途渐变？物件是否共用承托/接触影/透视，主题是否进入空间而不只是漂浮贴纸？优先拉近画面、放大主体、收紧文字/主体关系，再调整少量相关道具；不要通过加回固定音响或改专辑内部填空。再与本次调色分区和场景清单对照：有无无来源的全局紫/蓝/粉？是否小块封面颜色扩散全景？是否主题只体现为旧房间加几件贴纸？有无清单外架子、音箱、功放？如有，判为失败，不作为后续锚点；重新生成错误的场景/色彩，而非用更多否定词重复编辑同一污染图。

## 保存位置

原封面副本、锁定卡通化素材、设计清单、各曲4:3与16:9成品，以及最终ZIP，都放在 `<项目根目录>/<专辑名>/` 内。禁止默认使用 `output/vinyl-covers/` 或Skill目录。打包明确枚举本次素材、最终图和清单，排除所有ZIP与草稿，ZIP自身也写入该专辑目录。
