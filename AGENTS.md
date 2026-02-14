# AGENTS.md — Zotero TagVocab (AI-assisted controlled vocabulary)

## 0. What this repo is

This project maintains a **stable, faceted, controlled tag vocabulary** for **Zotero**, built through **interactive LLM sessions**.

- Collections = 项目管理
- Tags = 知识与工作流管理（学科/方向、方法/模型、状态）

Core principles: **概念清晰、可扩展、受控词表、低噪音、易维护**。
Special rule: **鼓励缩写**；核心缩写 **必须大写**；其余 **小写**。

Detailed rules: see `文献Tag维护说明.md`.

---

## 1. Faceted tag system

### 1.1 Canonical tag format

- `facet:value` or `facet:path/leaf`
- facet is **always lowercase**
- hierarchy uses `/`
- multiword uses `-`
- no spaces anywhere

### 1.2 Core facets (8 facets)

| Facet | 含义 | 约束 | 每篇数量 |
|-------|------|------|----------|
| `field:` | 学科体系（一级/二级/方向） | **严格受控** | 1–2 |
| `topic:` | 研究对象/问题域 | 半受控 | 0–4 |
| `method:` | 研究方法/流程 | 半受控 | 1–2 |
| `model:` | 模型/算法/本构 | 受控 | 0–3 |
| `ai_task:` | AI 任务类型 | 受控（仅AI文献） | 0–2 |
| `data:` | 数据类型/模态 | 受控（仅AI/监测类） | 0–2 |
| `tool:` | 工具/平台/框架 | 受控（只收实际用的） | 0–2 |
| `status:` | 阅读与加工状态 | **严格受控** | 1 |

### 1.3 `field:` 三段式结构

```
field:<一级>/<二级>/<方向>
```

- 方向可省略，尽量给到二级
- 示例: `field:CE/UG/Tunnel`, `field:CS/AI/CV`, `field:MGMT/Risk/Assessment`
- "包含关系合并"：`UG` 作为二级，`Tunnel` 作为方向

### 1.4 Abbreviation rules

- **规则 A**: 缩写注册表中的缩写 **必须大写** (`AI`, `DL`, `FEM`, `TBM`...)
- **规则 B**: 非缩写部分 **一律小写** (`topic:rockburst`, `method:risk/bayesian`)
- **规则 C**: **鼓励缩写优先** (`field:CE/UG/Tunnel` > `field:civil/underground/tunneling`)

Abbreviation registry: `tags/abbrev.yaml`

### 1.5 LTS stability

- Within an LTS window: no breaking renames.
- Allowed: additive new tags, new aliases, deprecation.

---

## 2. Non-goals / constraints

- No autonomous tag creation without explicit user confirmation.
- No "散装状态标签" — must use `status:*`
- No synonym coexistence (e.g., `DL` and `deep-learning` cannot both exist)

---

## 3. Vocabulary building (LLM interactive sessions)

### 3.1 Session workflow

1. User describes a facet area or research topic.
2. LLM proposes candidate tags in canonical format.
3. User reviews: **accept** / **reject** / **modify**.
4. LLM writes accepted tags to `tags.yaml`.
5. LLM runs `scripts/validate.py` to confirm consistency.

### 3.2 LLM rules

- **MUST** present candidates before writing.
- **MUST** use canonical format and abbreviation rules.
- **MUST** check for duplicates and synonyms before proposing.
- **MUST NOT** create tags outside defined facets without approval.
- **SHOULD** propose in batches of 10–30.

---

## 4. Repo layout

```
tags/
  tags.yaml          # canonical controlled tags (LTS)
  aliases.yaml       # synonym/legacy → canonical mapping
  abbrev.yaml        # abbreviation registry (UPPERCASE)
  sources.yaml       # provenance log
  changelog.md       # version history
  policy.md          # governance rules

scripts/
  compile_vocab.py   # compile decisions into tags.yaml
  validate.py        # check tags.yaml format consistency

文献Tag维护说明.md    # detailed maintenance rules (Chinese)
```

---

## 5. `status:` workflow (fixed)

```
status:0-inbox → status:1-triaged → status:2-to-read → status:3-reading
→ status:4-annotated → status:5-extracted → status:6-cited
→ status:x-parked (any time)
```

---

## 6. Tag governance

### 6.1 Adding tags (easiest → strictest)

1. `topic:` — if you'll actually filter by it
2. `tool:` — tools you actually use
3. `model:` — important models/algorithms
4. `method:` — important method families
5. `status:` — **fixed, do not add**
6. `field:` — **strictest: must evaluate if discipline truly expands**

### 6.2 Monthly maintenance

- Fix casing violations
- Merge synonymous `topic:` tags
- Check `field:` is not bloated
- Ensure all items have `status:*`

---

## 7. Data model

### 7.1 tags.yaml

```yaml
- tag: "field:CE/UG/Tunnel"
  facet: "field"
  source: "llm-interactive"
  note: "土木/地下工程/隧道"
  deprecated: false
```
