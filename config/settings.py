import os
import json
from dataclasses import dataclass, field
from typing import List, Optional, Union


def _bool(val: Optional[str], default: bool = False) -> bool:
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def _list(val: Optional[str], default: Optional[List[str]] = None) -> List[str]:
    if val is None:
        return list(default or [])
    return [x.strip() for x in val.split(',') if x.strip()]


@dataclass(frozen=True)
class Settings:
    # OpenAI / LLM
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    pipeline_enabled: bool = _bool(os.getenv("PIPELINE_ENABLED"), default=True)

    # Whisper (server STT)
    whisper_model_primary: str = os.getenv("WHISPER_MODEL", "whisper-1")
    whisper_model_fallback: str = os.getenv("WHISPER_FALLBACK_MODEL", "gpt-4o-mini-transcribe")

    # STT/TTS client config (surfaced to page)
    voice_lang: str = os.getenv("VOICE_LANG", "en-US")
    voice_rate: float = float(os.getenv("VOICE_RATE", "1.0"))
    voice_pitch: float = float(os.getenv("VOICE_PITCH", "1.0"))
    voice_volume: float = float(os.getenv("VOICE_VOLUME", "0.8"))
    preferred_voices: List[str] = field(default_factory=lambda: _list(os.getenv("PREFERRED_VOICES", "Karen,Samantha,Alex")))
    stt_restart_delay_ms: int = int(os.getenv("STT_RESTART_DELAY_MS", "100"))

    # Save/preview policy
    primary_save_dir: str = os.path.expanduser(os.getenv("PRIMARY_SAVE_DIR", "~/Desktop/NekoAI"))
    secondary_save_dir: str = os.path.expanduser(os.getenv("SECONDARY_SAVE_DIR", "~/Documents/NekoAIGenerated"))
    content_preview_limit: int = int(os.getenv("CONTENT_PREVIEW_LIMIT", "1000"))
    allowed_preview_types: List[str] = field(default_factory=lambda: _list(os.getenv("ALLOWED_PREVIEW_TYPES", "html,txt,md,py,js,css")))

    # API / routing
    api_prefix: str = os.getenv("API_PREFIX", "")  # e.g. "/api"

    # Assistant identity and capabilities metadata
    assistant_name: str = os.getenv("ASSISTANT_NAME", "NekoAI")
    assistant_type: str = os.getenv("ASSISTANT_TYPE", "Agentic AI Assistant")
    assistant_version: str = os.getenv("ASSISTANT_VERSION", "1.0.0")
    startup_tagline: str = os.getenv("STARTUP_TAGLINE", "")
    capabilities_csv: Optional[str] = os.getenv("CAPABILITIES")  # optional CSV override
    features_csv: Optional[str] = os.getenv("FEATURES")
    capabilities_path: str = os.path.join(os.getcwd(), "config", "capabilities.json")

    # Prompt config
    tool_name: str = os.getenv("TOOL_NAME", "neko_tool")

    # UI strings path (JSON) and template name
    ui_strings_path: str = os.path.join(os.getcwd(), "ui", "ui_strings.json")
    template_name: str = os.getenv("TEMPLATE_NAME", "index.html")

    # Extra save search locations (directories)
    extra_save_paths: List[str] = field(
        default_factory=lambda: _list(
            os.getenv("EXTRA_SAVE_PATHS"),
            ["~/Desktop", os.path.join(os.getcwd(), "generated_content")],
        )
    )

    def capabilities(self) -> List[str]:
        default_caps = [
            "Dynamic application creation",
            "System control and automation",
            "Natural language processing",
            "Code generation",
            "Web browsing and search",
            "Mathematical computations",
            "File operations",
            "Intelligent conversations",
        ]
        return _list(self.capabilities_csv, default_caps)

    def features(self) -> List[str]:
        default_features = [
            "No hardcoded responses",
            "AI-powered reasoning",
            "OpenAI integration",
            "Voice interaction support",
            "Real-time adaptation",
        ]
        return _list(self.features_csv, default_features)

    def load_capabilities_payload(self) -> dict:
        """Load assistant metadata from JSON with env/setting fallbacks."""
        fallback = {
            "name": self.assistant_name,
            "type": self.assistant_type,
            "capabilities": self.capabilities(),
            "features": self.features(),
        }
        try:
            with open(self.capabilities_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "name": data.get("name", fallback["name"]),
                "type": data.get("type", fallback["type"]),
                "capabilities": data.get("capabilities", fallback["capabilities"]),
                "features": data.get("features", fallback["features"]),
            }
        except Exception:
            return fallback

    def save_paths_for(self, safe_filename: str) -> List[str]:
        """All candidate file paths for serving generated content."""
        dirs = [
            self.primary_save_dir,
            self.secondary_save_dir,
            *[os.path.expanduser(p) for p in self.extra_save_paths],
        ]
        return [os.path.join(d, safe_filename) for d in dirs if d]

    def load_ui_strings(self) -> dict:
        try:
            with open(self.ui_strings_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # minimal defaults
            return {
                "welcome_initial": "Welcome! Click the voice button to start talking with me, or wait for me to speak.",
                "welcome_tts": "Hello! I am NekoAI, your agentic AI assistant. Click the voice button to start our conversation.",
                "voice_started": "🎤 Voice conversation started! You can now speak to NekoAI.",
                "voice_not_supported": "Voice recognition is not supported in your browser. Please use Chrome, Edge, or Firefox.",
                "mic_denied": "🔐 Microphone access denied. Please enable microphone permissions in your browser settings and reload the page.",
                "no_speech": "🤐 No speech detected. Please speak louder or closer to the microphone.",
                "audio_missing": "🎤 No microphone found. Please check your audio input device.",
                "network_error": "🌐 Network error. Please check your internet connection.",
                "processing_error": "❌ An error occurred. Please try again.",
                "connection_error": "Connection error. Please check your internet connection and try again.",
            }


settings = Settings()
