# De-Hardcoding: Configuration Summary

This document summarizes the shift from inline hardcoded values to environment‑driven, template‑based, JSON‑backed settings.

## What Changed

### 1. Settings Module (`config/settings.py`)
- **STT/TTS**: `VOICE_LANG`, `VOICE_RATE`, `VOICE_PITCH`, `VOICE_VOLUME`, `PREFERRED_VOICES`, `STT_RESTART_DELAY_MS`
- **Directories**: `PRIMARY_SAVE_DIR` (default `~/Desktop/AimyCode`), `SECONDARY_SAVE_DIR` (`~/Documents/AimyGenerated`)
- **Preview Policy**: `CONTENT_PREVIEW_LIMIT` (default 1000 chars), `ALLOWED_PREVIEW_TYPES` (default csv list)
- **API Routing**: `API_PREFIX` for proxy mounts (e.g., `/api`)
- **Prompts**: `TOOL_NAME` (default `aimy_tool`), `CAPABILITIES` (CSV override for prompt variable)
- **UI Strings Path**: `ui_strings_path` (loads `ui/ui_strings.json`)

### 2. UI Strings (`ui/ui_strings.json`)
All user-visible text (welcome messages, error messages, button labels, status text) moved from inline JS to JSON.

**Example keys**:
- `voice_button_default`, `voice_button_listening`, `voice_button_processing`
- `status_ready`, `status_listening`, `status_processing`
- `welcome_initial`, `welcome_tts`
- `mic_denied`, `no_speech`, `audio_missing`, `network_error`, `processing_error`, `connection_error`

### 3. Prompt Template (`prompts/assistant_system.j2`)
- **Tool name**: `{{ tool_name }}` (from `settings.tool_name`)
- **Capabilities**: `{{ capabilities | join(', ') }}` (from `settings.capabilities()`)

### 4. Web Interface (`app.py`)
- **Server-side injection**: `home()` renders `WEB_TEMPLATE` with `ui_strings` and `client_config` JSON objects.
- **Client-side usage**: JS reads `AIMY_CONFIG` and `STR` objects for runtime behavior (voice params, API routes, UI text).
- **View route**: Now queries `settings.primary_save_dir` and `settings.secondary_save_dir` for preview files.

### 5. Orchestrator (`src/pipeline/orchestrator.py`)
- Renders system prompt with `tool_name` and `capabilities` from settings.

### 6. Environment File (`.env.example`)
Updated with new variables and organized by category (LLM, STT/TTS, Save/Preview, API, Prompt).

## How to Customize

### UI Strings
Edit `ui/ui_strings.json` and reload the page. No code changes needed.

### Voice Settings
Set in `.env`:
```bash
VOICE_LANG=en-GB
VOICE_RATE=1.2
VOICE_PITCH=0.9
VOICE_VOLUME=1.0
PREFERRED_VOICES=Daniel,Moira
```
Reload the page to apply.

### Save Directories
```bash
PRIMARY_SAVE_DIR=~/Projects/Aimy
SECONDARY_SAVE_DIR=~/Backups/AimyGenerated
```

### Preview Policy
```bash
CONTENT_PREVIEW_LIMIT=500
ALLOWED_PREVIEW_TYPES=html,py,md
```

### API Prefix (for reverse proxies)
```bash
API_PREFIX=/api
```
Client fetches become `/api/chat`, `/api/api/transcribe` (with internal deduplication).

### Prompt Variables
```bash
TOOL_NAME=my_custom_tool
CAPABILITIES="Web search,App creation,Data analysis"
```

## No More Hardcoding
- **Before**: Fixed strings, magic numbers, and inline HTML/JS blobs.
- **After**: Env-driven settings, external JSON strings, Jinja prompt templates, and runtime config injection.

## Next Steps (Optional)
- Add multilingual support via alternate `ui_strings_<lang>.json` files.
- Create a simple admin UI at `/config` to edit settings via web form.
- Add user profiles (per-user preferences saved in DB or session).
