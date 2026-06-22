# Maple 端游贴图包量清理分析方案

> 数据源：`/Users/a1_builder/Downloads/all_texture_0525.csv`
> 总盘子：**42,463 张贴图，压缩后 31.50 GB / 解压后 68.57 GB**，全部 `Texture2D`
> 用户偏好：① 第三方资产先列清单，自己核对；② 清理力度 **激进** —— 低置信度可疑都纳入列表

---

## 一、分析逻辑（怎么判"垃圾"）

CSV 字段非常有限：`Name, Path, Compressed Size, SHA1, Dependent Count`。在没有引擎引用图的情况下，我用**多维度证据 + 置信度分层**来判定"垃圾"，而不是只靠单一信号下结论：

### 判定信号（按置信度从高到低）

| 信号 | 含义 | 置信度 |
|---|---|---|
| **S1. SHA1 完全重复** | 不同路径下二进制一致（同一张贴图被多份保留） | ⭐⭐⭐⭐⭐ |
| **S2. 命名带 demo / sample / test / temp / dummy / placeholder / example** | 厂商示例素材或临时调试资源 | ⭐⭐⭐⭐⭐ |
| **S3. 路径含 `Demo/`, `Examples/`, `StarterContent/`** | 第三方包自带演示子目录 | ⭐⭐⭐⭐⭐ |
| **S4. 命名带 `_old / _bak / _backup / _legacy / _orig / _v1 / _v2 / _final / _new`** | 旧版本残留 | ⭐⭐⭐⭐ |
| **S5. 整包 Marketplace 未集成** | 在 `Game/Scene/UnrealMarketplace/<Pkg>/` 下但未被 `Game/Maps/` 实际拼场景调用（需 PM 核对） | ⭐⭐⭐ |
| **S6. 同名不同 SHA 多版本** | 命名相同但内容不同（疑似多套美术方案残留） | ⭐⭐⭐ |
| **S7. 超大单贴图（≥10 MB 压缩）且为 `_N` 法线/`_D` 颜色** | 4K/8K 滥用，应降到 2K（可瘦身但不删） | ⭐⭐⭐ |
| **S8. `Dependent Count = 0`** | pak 内无文件引用（受限：跨 pak、Material Hard Reference 不准，仅作弱信号） | ⭐⭐ |
| **S9. 命名带 `_01/_02/...` 数字尾缀的高度集中目录** | 疑似一组备选纹理只用了其中 1-2 张 | ⭐ |

### 置信度分层 → 操作建议

- **A 级（直接可删）**：S1 + S2 + S3 命中
- **B 级（强烈建议删）**：S4 + S5 整包 + S6 同名旧版
- **C 级（待 PM/主美核对）**：S7 大贴图降级 + S8 + S9
- **D 级（需要研发实际跑引用）**：仅 S8 单独命中，没有 Editor 引用图无法确诊

---

## 二、当前已扫描出的关键发现（先给个底）

### 1. 总览
- 42,463 张贴图，**压缩 31.50 GB**
- Top 5 大目录：
  - `Game/Scene/UnrealMarketplace` —— **11.79 GB / 13,541 文件 / 占 37.4%** ⚠️ 第三方场景包
  - `Game/Characters/Props` —— 5.05 GB / 5,076 文件
  - `Game/Eqpt/weapon` —— 1.78 GB
  - `Game/Characters/Monsters` —— 1.65 GB
  - `Game/Characters/Heroes` —— 1.44 GB
- `Megascans` 1.02 GB；`Thirdparty` 0.46 GB

### 2. 高置信度浪费（A 级，已可量化）
| 类别 | 命中数 | 压缩体积 | 占总 |
|---|---:|---:|---:|
| **SHA1 完全重复** | 447 个冗余副本（356 组） | **634.5 MB** | 1.97% |
| **命名/路径含 test/demo/sample/example/placeholder** | 328 | **134.4 MB** | 0.42% |
| **命名含 backup/old/v1/v2/legacy/orig** | 763 | **830.6 MB** | 2.58% |
| **命名 `_v\d+` 版本尾缀** | 169 | 79.3 MB | 0.25% |
| **A 级合计（去重后约）** | ~1,500 | **≈ 1.6 GB** | **≈ 5.1%** |

### 3. 第三方资产分包详情（**13.5 GB / 占 43%**，需 PM 逐包确认是否真用）
最大的 25 个第三方子包，体积均在 100 MB+：
- 头部：`MedievalVillage 620 MB`、`LightHouse_Meshingun 528 MB`、`Megascans/3D_Assets 509 MB`、`Megascans/Surfaces 507 MB`、`SD_Art 486 MB`、`FC_MilitaryCamp 404 MB`
- 中段：`Sci_Fi_Laboratory 382 MB`、`Dirt_Track_Decals 348 MB`、`Shipping_Dock 329 MB`、`Northwood 314 MB`、`US_Military 292 MB`、`ChemicalPlantEnv 286 MB`、`MilitaryFiringRange 263 MB`、`IndustrialMegaCollection 255 MB+246 MB`（两份⚠️）、`Realistic_Rock_Set_02 242 MB`
- 长尾还有 30+ 个包

### 4. 超大单贴图 Top（**降级而非删**，C 级）
- `T_Monster_Siren_Head_N.ubulk` —— **80.8 MB**（典型 8K 法线，砍到 2K 可省 95%）
- `Monster_walker_Blind`、`PelicanCase`、`Siren_Body/Leg`、`GunShield_FullProtection` 系列每张都 19-22 MB
- 仅 Top 30 大贴图就占用 **614 MB**

### 5. 弱信号
- `Dependent Count = 0` 的文件：**22,542 / 31.28 GB**（占 99% 体积），明显失真 → 不能单独作为依据

---

## 三、最终交付的 MD 报告将包含

输出位置：`/Users/a1_builder/WorkBuddy/tapd_agent/maple_texture_cleanup_report.md`

### 章节大纲
1. **执行摘要** —— 一句话给老板看："可省 X GB / 占 Y%"
2. **数据总览** —— 总量、Top 目录、文件类型分布（_N/_D/_ORM 通道占比）
3. **A 级清理清单（直接可删）**
   - SHA1 重复表：每组列出保留路径 + 删除路径 + 体积
   - test/demo/sample/example/placeholder 全量列表
   - `Demo/Examples/StarterContent` 路径全列表
4. **B 级清理清单（强烈建议）**
   - `_old/_bak/_v1/_v2/_legacy` 全量列表
   - 同名不同 SHA 多版本组
5. **C 级清单（需要确认）**
   - 超大贴图 Top 100（建议从 4K/8K 降到 2K，估算节省体积）
   - 第三方包逐包清单（**专门一节**：每个包的文件数、体积、命名样例、是否带 Demo 子目录），让你拿去问主美/关卡哪些没集成
6. **D 级（弱信号）**
   - Dependent Count = 0 但路径不在主流业务目录的可疑组
7. **可省体积估算总表**（保守 / 中等 / 激进 三个版本）
8. **行动建议**
   - 第一步动作（A 级，0 风险，直接打 MR）
   - 第二步动作（B 级，需要走代码搜索复核）
   - 第三步动作（第三方包整包退役 + 超大图降级，需要主美/关卡介入）

### 配套产物
- 主报告：`maple_texture_cleanup_report.md`
- 详单 CSV（清单较长，单独导出便于排序筛选）：
  - `cleanup_A_sha1_duplicates.csv`
  - `cleanup_A_test_demo.csv`
  - `cleanup_B_backup_old_version.csv`
  - `cleanup_C_thirdparty_packages.csv`
  - `cleanup_C_oversize_textures.csv`

---

## 四、限制与免责

> 这份分析**只基于 pak 元信息**，没有跑引擎里的实际引用图。所以：
> - SHA1 重复、命名/路径关键字、第三方目录归属 → **结论可靠**
> - "是否被引用" → **不能 100% 确诊**，需要在编辑器里跑 Reference Viewer 或编译 cook 报告交叉验证
> - 最终任何删除动作都建议先放进 deprecated 目录跑一轮 cook + 关键场景冒烟，再彻底删除
