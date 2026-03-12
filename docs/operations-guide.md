# 操作指引

## 📦 仓库内操作（Python 端）

### 日常操作

| 操作 | 命令 | 说明 |
|:---|:---|:---|
| **新增标签** | `python scripts/add_tag.py` | 交互式，直接写入 `tags.json` |
| **搜索标签** | `python scripts/search_tags.py <关键词>` | 支持 `--facet` 过滤 |
| **查看统计** | `python scripts/stats.py --recent 10` | 按 facet 统计 + 最近添加 |
| **导出标签** | `python scripts/export_tags.py -f json -o out.json` | 支持 yaml/json/md/txt |
| **校验词表** | `python scripts/validate.py --json --strict` | 校验 JSON 真源 |

### 派生操作（从真源生成视图）

| 操作 | 命令 | 说明 |
|:---|:---|:---|
| **生成 per-facet YAML** | `python scripts/derive_facets.py` | `tags.json` → `tags/<facet>.yaml`（浏览用） |
| **生成 compiled YAML** | `python scripts/compile_vocab.py` | `tags.json` → `tags/tags.yaml`（兼容用） |

### Git 工作流

```bash
# 本地修改后推送
python scripts/add_tag.py          # 写入 tags.json
python scripts/derive_facets.py    # 可选：更新浏览视图
python scripts/compile_vocab.py    # 可选：更新兼容 YAML
git add tags/tags.json
git commit -m "Add tag: topic:xxx"
git push

# 拉取远程更新（插件回写后）
git pull
python scripts/derive_facets.py    # 从 JSON 更新本地 YAML 视图
python scripts/compile_vocab.py    # 从 JSON 更新兼容 YAML
```

---

## 🌐 外部应用操作（Zotero 插件等）

### 订阅（读取词表）

```
GET https://raw.githubusercontent.com/{owner}/{repo}/main/tags/tags.json
```

- 公开仓库无需认证
- 返回完整 JSON，直接 `JSON.parse()` 使用
- 建议缓存 + 定期刷新（如每次 Zotero 启动时）

### 回写（贡献新标签）

使用 [GitHub Contents API](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents)：

```
PUT /repos/{owner}/{repo}/contents/tags/tags.json
```

**流程：**

1. **GET** 当前文件（获取 `sha` 和 `content`）
2. 解码 `content`（base64 → JSON），修改 tags 数组
3. 更新 `updated_at`、`tag_count`
4. **PUT** 回 GitHub（带上 `sha` + base64 编码的新内容 + commit message）

```javascript
// 伪代码
const res = await fetch(
  `https://api.github.com/repos/${owner}/${repo}/contents/tags/tags.json`,
  { headers: { "Authorization": `Bearer ${PAT}` } }
);
const { sha, content } = await res.json();
const vocab = JSON.parse(atob(content));

// 添加新标签
vocab.tags.push({
  tag: "topic:karst", facet: "topic",
  source: "zotero-plugin", note: "岩溶", deprecated: false
});
vocab.tags.sort((a, b) => (a.facet + a.tag).localeCompare(b.facet + b.tag));
vocab.updated_at = new Date().toISOString();
vocab.tag_count = vocab.tags.length;

// 写回
await fetch(
  `https://api.github.com/repos/${owner}/${repo}/contents/tags/tags.json`,
  {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${PAT}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: "Add tag: topic:karst (via Zotero plugin)",
      content: btoa(JSON.stringify(vocab, null, 2) + "\n"),
      sha: sha
    })
  }
);
```

**冲突处理：** 如果 `sha` 不匹配（有人先更新了），PUT 返回 **409 Conflict** → 重新 GET → merge → 重试。

### 插件配置项

| 配置 | 值 |
|:---|:---|
| `github_owner` | GitHub 用户名 |
| `github_repo` | `Zotero_TagVocab` |
| `github_token` | PAT（需 `repo` 权限） |
| `file_path` | `tags/tags.json` |

---

## 🔄 数据流全景

```
                  tags/tags.json  ← 唯一真源
                  ┌─────┴─────┐
         Python 端│           │外部应用
         ┌────────▼───┐  ┌───▼────────┐
         │ add_tag.py  │  │ Zotero 插件 │
         │ search/stats│  │ (JS, HTTP) │
         │ export/valid│  └───┬────────┘
         └────────┬───┘      │
                  │          │ PUT (GitHub API)
                  │ derive   │
         ┌────────▼──────┐   │
         │ <facet>.yaml  │   │
         │ tags.yaml     │   │
         │ (派生视图)     │   │
         └───────────────┘   │
                  ▲          │
                  └──────────┘
                   git pull + derive
```
