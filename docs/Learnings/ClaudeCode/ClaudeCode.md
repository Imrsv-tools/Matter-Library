# Claude Code (the agent harness)

*Observed on the maintainer's box, 2026-09-26, while setting up the Blender MCP server. Evidence: the BigPicture research session's retro (in git history under `docs/Planning/Support/WorkflowFeedback/`).*

**CC1 — An MCP server added mid-session reaches only a FRESH session, never a resumed one.** After `claude mcp add` (any scope), the server's tools do not appear in the conversation that added them, and they still do not appear after a restart that **resumes** that conversation (`--continue` / `--resume`). Claude Code's own MCP log showed the server connecting and listing its tools at the restart, yet a tool search in the resumed conversation found nothing, twice. `claude mcp list` reporting *Connected* proves only that the server starts, not that this conversation can call it.

**So:** in the same message that adds a server, tell the lead that the tools arrive only in a **new** session, and verify from that new session with one live call. Do not diagnose "the setup is broken" from a resumed conversation.

**CC2 — A `run_in_background` task is killed at its time limit (two hours at most), whatever it is doing.** *(Phase09, 2026-09-30.)* A viewer opened for a sitting as a background task died mid-sitting across a break, with *"stopped after reaching its background time limit"*, and the harness says not to restart a task that already had the maximum. **Launch a window the lead will sit in front of detached from the session** (`setsid <tool> <file>`, or the desktop's opener), never as a harness task.