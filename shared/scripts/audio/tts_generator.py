#!/usr/bin/env python3
"""
TTS Generator
Generador de voz sintetizada usando Edge-TTS (gratuito, de Microsoft).

Edge-TTS ofrece:
- Voces naturales de alta calidad
- Múltiples idiomas y acentos
- Gratis sin límites
- Sin API key necesaria
"""

import asyncio
import subprocess
from pathlib import Path
from typing import Optional, List, Dict


class TTSGenerator:
    """Generador de Text-to-Speech usando Edge-TTS"""
    
    # Voces recomendadas por idioma
    RECOMMENDED_VOICES = {
        "es": {
            "male": ["es-ES-AlvaroNeural", "es-MX-JorgeNeural", "es-AR-TomasNeural"],
            "female": ["es-ES-ElviraNeural", "es-MX-DaliaNeural", "es-AR-ElenaNeural"]
        },
        "en": {
            "male": ["en-US-GuyNeural", "en-GB-RyanNeural", "en-AU-WilliamNeural"],
            "female": ["en-US-JennyNeural", "en-GB-SoniaNeural", "en-AU-NatashaNeural"]
        },
        "pt": {
            "male": ["pt-BR-AntonioNeural", "pt-PT-DuarteNeural"],
            "female": ["pt-BR-FranciscaNeural", "pt-PT-RaquelNeural"]
        },
        "fr": {
            "male": ["fr-FR-HenriNeural", "fr-CA-AntoineNeural"],
            "female": ["fr-FR-DeniseNeural", "fr-CA-SylvieNeural"]
        },
        "de": {
            "male": ["de-DE-ConradNeural", "de-AT-JonasNeural"],
            "female": ["de-DE-KatjaNeural", "de-AT-IngridNeural"]
        }
    }
    
    def __init__(
        self,
        voice: str = "es-ES-AlvaroNeural",
        rate: str = "+0%",
        pitch: str = "+0Hz",
        volume: str = "+0%"
    ):
        """
        Inicializa el generador TTS.
        
        Args:
            voice: ID de la voz de Edge-TTS
            rate: Velocidad (-50% a +100%)
            pitch: Tono (-50Hz a +50Hz)
            volume: Volumen (-50% a +50%)
        """
        self.voice = voice
        self.rate = rate
        self.pitch = pitch
        self.volume = volume
    
    def generate(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        rate: Optional[str] = None,
        pitch: Optional[str] = None
    ) -> Optional[str]:
        """
        Genera audio desde texto.
        
        Args:
            text: Texto a convertir en voz
            output_path: Ruta del archivo de salida (.mp3)
            voice: Voz a usar (override del default)
            rate: Velocidad (override)
            pitch: Tono (override)
            
        Returns:
            Ruta al archivo generado o None si falla
        """
        voice = voice or self.voice
        rate = rate or self.rate
        pitch = pitch or self.pitch
        
        # Asegurar directorio existe
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Construir comando
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate,
            "--pitch", pitch,
            "--volume", self.volume,
            "--text", text,
            "--write-media", output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0 and Path(output_path).exists():
                return output_path
            else:
                print(f"Error TTS: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Timeout generando audio")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def generate_from_file(
        self,
        input_path: str,
        output_path: str,
        voice: Optional[str] = None
    ) -> Optional[str]:
        """
        Genera audio desde archivo de texto.
        
        Args:
            input_path: Ruta al archivo de texto
            output_path: Ruta de salida
            voice: Voz a usar
            
        Returns:
            Ruta al archivo generado
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        return self.generate(text, output_path, voice)
    
    def generate_with_srt(
        self,
        text: str,
        audio_path: str,
        srt_path: str,
        voice: Optional[str] = None
    ) -> Dict[str, Optional[str]]:
        """
        Genera audio y archivo SRT con timestamps.
        
        Args:
            text: Texto a convertir
            audio_path: Ruta para el audio
            srt_path: Ruta para subtítulos SRT
            voice: Voz a usar
            
        Returns:
            Dict con rutas a audio y srt
        """
        voice = voice or self.voice
        
        Path(audio_path).parent.mkdir(parents=True, exist_ok=True)
        Path(srt_path).parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", self.rate,
            "--pitch", self.pitch,
            "--text", text,
            "--write-media", audio_path,
            "--write-subtitles", srt_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            return {
                "audio": audio_path if result.returncode == 0 and Path(audio_path).exists() else None,
                "srt": srt_path if result.returncode == 0 and Path(srt_path).exists() else None
            }
            
        except Exception as e:
            print(f"Error: {e}")
            return {"audio": None, "srt": None}
    
    @staticmethod
    def list_voices(language: Optional[str] = None) -> List[Dict]:
        """
        Lista todas las voces disponibles.
        
        Args:
            language: Filtrar por código de idioma (es, en, pt, etc.)
            
        Returns:
            Lista de voces con info
        """
        try:
            result = subprocess.run(
                ["edge-tts", "--list-voices"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            voices = []
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                    
                # Parse formato: Name: es-ES-AlvaroNeural
                parts = line.split(':')
                if len(parts) >= 2:
                    voice_id = parts[1].strip()
                    
                    if language:
                        if not voice_id.lower().startswith(language.lower()):
                            continue
                    
                    voices.append({
                        "id": voice_id,
                        "language": voice_id.split('-')[0] if '-' in voice_id else "",
                        "region": voice_id.split('-')[1] if voice_id.count('-') >= 1 else ""
                    })
            
            return voices
            
        except Exception as e:
            print(f"Error listando voces: {e}")
            return []
    
    @staticmethod
    def get_recommended_voice(language: str = "es", gender: str = "male") -> str:
        """
        Obtiene una voz recomendada para el idioma y género.
        
        Args:
            language: Código de idioma (es, en, pt, fr, de)
            gender: male | female
            
        Returns:
            ID de voz recomendada
        """
        lang_voices = TTSGenerator.RECOMMENDED_VOICES.get(language, {})
        voices = lang_voices.get(gender, [])
        
        if voices:
            return voices[0]
        
        # Fallback
        return "es-ES-AlvaroNeural"
    
    def set_voice(self, voice: str):
        """Cambia la voz activa"""
        self.voice = voice
    
    def set_rate(self, rate: str):
        """Cambia la velocidad"""
        self.rate = rate
    
    def set_pitch(self, pitch: str):
        """Cambia el tono"""
        self.pitch = pitch


def generate_narration(
    text: str,
    output_path: str,
    voice: str = "es-ES-AlvaroNeural",
    rate: str = "+0%"
) -> Optional[str]:
    """
    Función helper para generar narración rápidamente.
    
    Args:
        text: Texto a narrar
        output_path: Ruta de salida
        voice: ID de voz
        rate: Velocidad
        
    Returns:
        Ruta al archivo generado
    """
    tts = TTSGenerator(voice=voice, rate=rate)
    return tts.generate(text, output_path)


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🎙️ TTS Generator - Test")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("""
Uso: python tts_generator.py <comando> [opciones]

Comandos:
  list [idioma]              - Lista voces disponibles
  generate <texto> <output>  - Genera audio
  test                       - Prueba rápida
        """)
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        lang = sys.argv[2] if len(sys.argv) > 2 else None
        voices = TTSGenerator.list_voices(lang)
        print(f"\n🎤 Voces disponibles" + (f" ({lang})" if lang else "") + ":")
        for v in voices[:20]:
            print(f"  - {v['id']}")
        if len(voices) > 20:
            print(f"  ... y {len(voices) - 20} más")
    
    elif cmd == "test":
        print("\n🔊 Generando audio de prueba...")
        tts = TTSGenerator(voice="es-ES-AlvaroNeural")
        result = tts.generate(
            "Hola, esto es una prueba del generador de voz.",
            "/tmp/test_tts.mp3"
        )
        if result:
            print(f"✅ Audio generado: {result}")
        else:
            print("❌ Error generando audio")
    
    elif cmd == "generate" and len(sys.argv) >= 4:
        text = sys.argv[2]
        output = sys.argv[3]
        voice = sys.argv[4] if len(sys.argv) > 4 else "es-ES-AlvaroNeural"
        
        result = generate_narration(text, output, voice)
        if result:
            print(f"✅ Audio generado: {result}")
        else:
            print("❌ Error generando audio")
    
    else:
        print("Comando no reconocido")
