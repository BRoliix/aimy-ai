#!/usr/bin/env python3
"""
NekoAI - Agentic AI Assistant Web Interface
Railway Deployment Entry Point
"""

import os
from flask import Flask, request, jsonify, render_template, Blueprint
from config.settings import settings

# Import AgenticAICore with graceful handling for missing voice libraries
try:
    from agents.agentic_core import AgenticAICore
except ImportError as e:
    print(f"Warning: Some voice libraries not available in web environment: {e}")
    from agents.agentic_core import AgenticAICore

app = Flask(__name__)
aimy = AgenticAICore()


def _ensure_dirs():
    """Create save/extra directories if missing."""
    dirs = {
        settings.primary_save_dir,
        settings.secondary_save_dir,
        *[os.path.expanduser(p) for p in settings.extra_save_paths],
    }
    for d in dirs:
        if not d:
            continue
        try:
            os.makedirs(d, exist_ok=True)
        except Exception:
            # best effort; don't crash startup
            pass


_ensure_dirs()

# Optional: pipeline orchestrator (LLM + prompt templates)
try:
    from src.pipeline.orchestrator import AgentPipeline
    from src.tools.aimy_bridge import make_aimy_bridge
    pipeline = AgentPipeline(tool_executor=make_aimy_bridge(aimy)) if True else None
except Exception as _e:
    pipeline = None

pipeline_active = bool(pipeline) and bool(getattr(settings, 'pipeline_enabled', False))

# API blueprint with optional prefix
api_bp = Blueprint("api", __name__, url_prefix=settings.api_prefix or "")

@app.route('/')
def home():
    """NekoAI Web Interface"""
    try:
        ui_strings = settings.load_ui_strings()
        client_config = {
            'voiceLang': settings.voice_lang,
            'voiceRate': settings.voice_rate,
            'voicePitch': settings.voice_pitch,
            'voiceVolume': settings.voice_volume,
            'preferredVoices': settings.preferred_voices,
            'sttRestartDelayMs': settings.stt_restart_delay_ms,
            'apiPrefix': settings.api_prefix,
        }
    except Exception:
        ui_strings = {}
        client_config = {}
    return render_template(settings.template_name, ui_strings=ui_strings, client_config=client_config)

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for NekoAI"""
    global pipeline_active
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'error': 'No message provided'
            })
        
        # If pipeline enabled and available, use it; else fallback to core
        if pipeline_active:
            try:
                pipe_out = pipeline.run(user_message)
                response = pipe_out.get('response', 'Ready to help!')
                action_url = pipe_out.get('action_url')
                return jsonify({
                    'success': True,
                    'response': response,
                    'result': pipe_out.get('result'),
                    'action_url': action_url,
                    'execute_action': action_url is not None
                })
            except Exception as e:
                # Auto-disable pipeline on runtime failure, fall back to core
                pipeline_active = False
                fallback_msg = f"Pipeline temporarily disabled due to error: {e}"
                # Continue to core path with a warning
                warning = fallback_msg
        else:
            warning = None

        # Fallback: Process with Aimy core directly
        result = aimy.process_request(user_message)
        
        # Extract response message and handle actions
        if isinstance(result, dict):
            response = result.get('message', result.get('response', 'Task completed successfully!'))
            
            # Handle different result types with actual execution
            result_type = result.get('type', 'unknown')
            action_url = None
            
            if result_type == 'web_redirect' and result.get('url'):
                action_url = result.get('url')
                response = f"Opening {result.get('url')} for you!"
            elif result_type == 'web_navigation' and result.get('url'):
                action_url = result.get('url')
                response = f"Opening {result.get('website', 'website')} for you!"
            elif result_type in ['application_launch', 'app_launch', 'web_app_launch'] and result.get('success'):
                # Handle successful app launches
                app_name = result.get('app_name', 'application')
                if result_type == 'web_app_launch':
                    web_url = result.get('web_url', '')
                    response = f"✅ Opened web version of {app_name}! Since we're in a web environment, I opened {web_url} for you."
                    action_url = web_url
                else:
                    response = f"✅ Successfully launched {app_name}! The app should now be open on your device."
            elif result_type == 'time_information':
                # Keep original time response
                pass
            elif result_type in ['system_app_info', 'system_info', 'helpful_response']:
                # For system requests that can't be executed in web environment
                response = "I understand your request. While I can't directly control system functions in this web environment, I can help guide you!"
            elif result_type == 'content_creation':
                # Handle content creation with actual content display
                if result.get('success'):
                    content_type = result.get('content_type', 'content')
                    filename = result.get('filename', 'generated_file')
                    content_preview = result.get('content_preview', '')
                    full_content = result.get('full_content', '')
                    web_url = result.get('web_url', '')
                    file_path = result.get('file_path', '')
                    saved_locations = result.get('saved_locations', [])
                    execution_result = result.get('execution_result', {})
                    
                    response = f"✅ AI created {content_type.upper()} content successfully! Saved as: {filename}"
                    
                    # Show save locations
                    if saved_locations:
                        response += f"\n\n💾 Saved to {len(saved_locations)} locations:"
                        for loc in saved_locations:
                            response += f"\n  • {loc['type']}: {loc['path']}"
                    
                    # Show execution results
                    if execution_result.get('attempted'):
                        if execution_result.get('success'):
                            response += f"\n\n🚀 {execution_result.get('message', 'Executed successfully')}"
                            if execution_result.get('output'):
                                response += f"\n📤 Output: {execution_result.get('output')}"
                        else:
                            response += f"\n\n⚠️ {execution_result.get('message', 'Execution failed')}"
                    
                    # If there's a web URL, set it as action_url for opening
                    if web_url:
                        action_url = web_url
                        response += f"\n\n🌐 Click to view: {web_url}"
                    
                    if content_preview:
                        response += f"\n\n📄 Content Preview:\n```{content_type}\n{content_preview}\n```"
                    
                    # Show full content in a collapsible section if it's not too long
                    if full_content and len(full_content) <= 1000:
                        response += f"\n\n📖 Full Content:\n```{content_type}\n{full_content}\n```"
                    elif full_content:
                        response += f"\n\n📖 Full Content Available - {len(full_content)} characters"
                else:
                    response = "❌ Content creation failed."
            elif result_type == 'system_control':
                # Handle system control actions
                if result.get('success'):
                    setting = result.get('setting', 'system')
                    action = result.get('action', 'action')
                    response = f"✅ Successfully executed {setting} {action} on your device."
                else:
                    response = "❌ System control action failed. Please ensure proper permissions are set."
            
            payload = {
                'success': True,
                'response': response,
                'result': result,
                'action_url': action_url,
                'execute_action': action_url is not None
            }
            if 'warning' in locals() and warning:
                payload['warning'] = warning
            return jsonify(payload)
        else:
            payload = {
                'success': True,
                'response': str(result) if result else "Ready to help!",
                'result': result
            }
            if 'warning' in locals() and warning:
                payload['warning'] = warning
            return jsonify(payload)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing error: {str(e)}'
        })

@api_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ai': settings.assistant_name,
        'version': settings.assistant_version,
        'type': settings.assistant_type,
    })

@app.route('/favicon.ico')
def favicon():
    """Favicon endpoint - returns 204 No Content"""
    return '', 204

@api_bp.route('/capabilities')
def capabilities():
    """API endpoint to get NekoAI capabilities"""
    return jsonify(settings.load_capabilities_payload())

@api_bp.route('/transcribe', methods=['POST'])
def api_transcribe():
    """Transcribe uploaded audio with OpenAI Whisper (server-side)."""
    try:
        if 'audio' not in request.files:
            return jsonify({ 'error': 'No audio file provided' }), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({ 'error': 'Empty filename' }), 400

        import tempfile
        from openai import OpenAI

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return jsonify({
                'error': 'OPENAI_API_KEY not configured on server',
                'action': 'Set OPENAI_API_KEY env var and restart server.'
            }), 503

        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as tmp:
            audio_path = tmp.name
            audio_file.save(audio_path)

        client = OpenAI(api_key=api_key)
        try:
            result = client.audio.transcriptions.create(
                model=settings.whisper_model_primary,
                file=open(audio_path, 'rb')
            )
            text = getattr(result, 'text', None) or (result.get('text') if isinstance(result, dict) else None)
        except Exception:
            try:
                result = client.audio.transcriptions.create(
                    model=settings.whisper_model_fallback,
                    file=open(audio_path, 'rb')
                )
                text = getattr(result, 'text', None) or (result.get('text') if isinstance(result, dict) else None)
            except Exception as e2:
                return jsonify({ 'error': f'Transcription failed: {e2}' }), 500
        finally:
            try:
                os.remove(audio_path)
            except Exception:
                pass

        if not text:
            return jsonify({ 'error': 'Transcription failed' }), 500

        return jsonify({ 'text': text })
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

@api_bp.route('/view/<filename>')
def view_generated_content(filename):
    """Serve generated content files"""
    try:
        import os
        from flask import send_file
        # Security: only allow viewing files with safe names
        safe_filename = os.path.basename(filename)

        # Candidate locations are settings-driven
        possible_paths = settings.save_paths_for(safe_filename)
        
        for file_path in possible_paths:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_file(file_path)
        
        return f"File '{filename}' not found in any location", 404
    except Exception as e:
        return f"Error serving file: {str(e)}", 500


# Register API blueprint after routes are defined
app.register_blueprint(api_bp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"🚀 Starting {settings.assistant_name} web server on port {port}")
    print(f"🤖 {settings.assistant_name} - {settings.assistant_type}")
    if settings.startup_tagline:
        print(settings.startup_tagline)
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=False,
        threaded=True
    )