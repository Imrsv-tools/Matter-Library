# GitHub (releases as the library's publishing channel)

*Observed on the library machine, 2026-10-14, publishing the dev snapshot `matterlib-0.2.0-dev.1` (Phase13 13.1). Evidence: the phase's execution ledger and the commit that made `--publish` resume (`tools/releases/build_snapshot.py`).*

**G1 — An interrupted `gh release create` leaves a DRAFT, and the releases LIST does not show its half-uploaded assets.** `gh release create <tag> <files…>` keeps the release a draft until every asset is up, then publishes it. Stopped part-way (a slow network, then a dead battery), it left a draft holding what had finished. Measured on that draft:
- `GET /repos/{owner}/{repo}/releases` (the list) embedded **46** assets, all `uploaded`;
- `GET /repos/{owner}/{repo}/releases/{id}/assets` (paginated) returned **49**: the same 46 plus **3 in state `starter`**, the uploads cut off mid-file.

*(Inferred, not tried:* re-running `gh release create` for the same tag is the wrong recovery, since a draft creates no tag, so `create` would see no existing release by that tag and start a second draft.*)*

**So:** resume the draft. Read its assets from the **assets endpoint**, never the list. Delete each one not `uploaded`, upload only the missing files (`gh release upload <tag> …`), then `gh release edit <tag> --draft=false`. `build_snapshot.py --publish` does exactly this. The release stays invisible until the last step, so an interruption publishes nothing half-made.
