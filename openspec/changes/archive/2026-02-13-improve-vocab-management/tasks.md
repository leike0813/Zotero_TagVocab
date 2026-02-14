# Tasks — Improve Vocab Management

## Per-facet storage
- [ ] Create `scripts/split_tags.py` migration script (one-time: splits current `tags.yaml` into 8 per-facet files)
- [ ] Run migration: generate `tags/field.yaml`, `tags/topic.yaml`, `tags/method.yaml`, `tags/model.yaml`, `tags/ai_task.yaml`, `tags/data.yaml`, `tags/tool.yaml`, `tags/status.yaml`
- [ ] Update `scripts/compile_vocab.py` to merge per-facet files → `tags/tags.yaml` with auto-generated header
- [ ] Verify round-trip: compiled `tags.yaml` matches original (278 tags, same content)
- [ ] Add `tags/tags.yaml` auto-generated header comment

## Interactive CLI tools
- [ ] Create `scripts/add_tag.py` (facet menu → value → note → validate → append → auto-compile)
- [ ] Create `scripts/search_tags.py` (case-insensitive substring search across all facet files)
- [ ] Create `scripts/stats.py` (per-facet counts, total, optional `--recent N`)
- [ ] Create `scripts/export_tags.py` (`--format {yaml,json,md,txt}`, `--facet`, `-o` output file)

## Validation extension
- [ ] Add `--per-facet` flag to `validate.py` (validate individual facet files)
- [ ] Add facet-filename consistency check (entry facet must match filename)
- [ ] Add cross-file duplicate detection in `--per-facet` mode

## Verification
- [ ] Run `validate.py --strict` on compiled `tags.yaml` — must pass
- [ ] Run `validate.py --per-facet --strict` on all facet files — must pass
- [ ] Test `add_tag.py`: add a test tag, verify it appears in correct facet file
- [ ] Test `search_tags.py`: search for known term, verify results
- [ ] Test `stats.py`: verify counts match 278 total
- [ ] Test `export_tags.py`: export in all 4 formats, verify output
