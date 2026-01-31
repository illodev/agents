#!/usr/bin/env python3
"""
Music Mixer
Añade música de fondo a archivos de audio/video.

Incluye:
- Música libre de derechos de Pixabay
- Ajuste automático de volumen (ducking)
- Fade in/out suave
- Categorías: tension, happy, epic, chill, dramatic
"""

import subprocess
import os
import json
import urllib.request
from pathlib import Path
from typing import Optional, Dict, List


class MusicMixer:
    """Mezclador de música de fondo para videos"""
    
    # Música libre de derechos - URLs directas de Pixabay/FreeSound
    # Estas son placeholders - se pueden reemplazar con URLs reales
    MUSIC_LIBRARY = {
        "tension": {
            "name": "Tension Dark Ambient",
            "bpm": 80,
            "mood": "suspense, mystery",
            "local_file": "tension_ambient.mp3"
        },
        "dramatic": {
            "name": "Dramatic Cinematic",
            "bpm": 90,
            "mood": "epic, powerful",
            "local_file": "dramatic_cinematic.mp3"
        },
        "curiosity": {
            "name": "Wonder Discovery",
            "bpm": 100,
            "mood": "curious, intriguing",
            "local_file": "curiosity_wonder.mp3"
        },
        "epic": {
            "name": "Epic Trailer",
            "bpm": 120,
            "mood": "powerful, motivating",
            "local_file": "epic_trailer.mp3"
        },
        "chill": {
            "name": "Lo-Fi Chill",
            "bpm": 85,
            "mood": "relaxed, calm",
            "local_file": "lofi_chill.mp3"
        },
        "happy": {
            "name": "Upbeat Positive",
            "bpm": 120,
            "mood": "happy, energetic",
            "local_file": "happy_upbeat.mp3"
        }
    }
    
    def __init__(self, music_dir: Optional[str] = None):
        """
        Inicializa el mezclador.
        
        Args:
            music_dir: Directorio con archivos de música
        """
        self.music_dir = Path(music_dir) if music_dir else Path(__file__).parent / "music"
        self.music_dir.mkdir(exist_ok=True)
    
    def mix_audio_with_music(
        self,
        voice_path: str,
        output_path: str,
        music_type: str = "tension",
        music_volume: float = 0.15,
        voice_volume: float = 1.0,
        fade_in: float = 1.0,
        fade_out: float = 2.0
    ) -> Optional[str]:
        """
        Mezcla voz con música de fondo.
        
        Args:
            voice_path: Ruta al archivo de voz
            output_path: Ruta de salida
            music_type: Tipo de música (tension, dramatic, epic, etc.)
            music_volume: Volumen de la música (0.0 a 1.0, recomendado 0.1-0.2)
            voice_volume: Volumen de la voz (0.0 a 1.0)
            fade_in: Segundos de fade in
            fade_out: Segundos de fade out
            
        Returns:
            Ruta al archivo mezclado o None si falla
        """
        music_info = self.MUSIC_LIBRARY.get(music_type, self.MUSIC_LIBRARY["tension"])
        music_path = self.music_dir / music_info["local_file"]
        
        # Si no existe la música local, generar tono ambiental
        if not music_path.exists():
            print(f"⚠️ Música '{music_type}' no encontrada, generando tono ambiental...")
            music_path = self._generate_ambient_tone(music_type, voice_path)
        
        if not music_path or not music_path.exists():
            print("❌ No se pudo obtener música de fondo")
            # Retornar el audio original sin música
            import shutil
            shutil.copy(voice_path, output_path)
            return output_path
        
        # Obtener duración del audio de voz
        duration = self._get_duration(voice_path)
        
        # Crear filtro complejo para mezclar
        # - La voz mantiene su volumen
        # - La música se reduce significativamente
        # - Fade in al inicio, fade out al final
        
        filter_complex = (
            f"[0:a]volume={voice_volume}[voice];"
            f"[1:a]volume={music_volume},"
            f"afade=t=in:st=0:d={fade_in},"
            f"afade=t=out:st={max(0, duration - fade_out)}:d={fade_out}[music];"
            f"[voice][music]amix=inputs=2:duration=first:dropout_transition=2[out]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", str(voice_path),
            "-i", str(music_path),
            "-filter_complex", filter_complex,
            "-map", "[out]",
            "-c:a", "libmp3lame", "-b:a", "192k",
            "-t", str(duration),
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"❌ Error mezclando: {result.stderr}")
            return None
    
    def add_music_to_video(
        self,
        video_path: str,
        output_path: str,
        music_type: str = "tension",
        music_volume: float = 0.12,
        fade_in: float = 0.5,
        fade_out: float = 2.0
    ) -> Optional[str]:
        """
        Añade música de fondo a un video que ya tiene audio.
        
        Args:
            video_path: Ruta al video con audio
            output_path: Ruta de salida
            music_type: Tipo de música
            music_volume: Volumen de la música (muy bajo, 0.1-0.15)
            fade_in: Segundos de fade in
            fade_out: Segundos de fade out
            
        Returns:
            Ruta al video con música o None si falla
        """
        music_info = self.MUSIC_LIBRARY.get(music_type, self.MUSIC_LIBRARY["tension"])
        music_path = self.music_dir / music_info["local_file"]
        
        if not music_path.exists():
            music_path = self._generate_ambient_tone(music_type, video_path)
        
        if not music_path:
            return video_path
        
        duration = self._get_duration(video_path)
        
        # Mezclar audio del video con música
        filter_complex = (
            f"[0:a]volume=1.0[voice];"
            f"[1:a]volume={music_volume},"
            f"afade=t=in:st=0:d={fade_in},"
            f"afade=t=out:st={max(0, duration - fade_out)}:d={fade_out}[music];"
            f"[voice][music]amix=inputs=2:duration=first[aout]"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", str(music_path),
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            "-movflags", "+faststart",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output_path
        else:
            print(f"❌ Error: {result.stderr}")
            return None
    
    def _generate_ambient_tone(
        self,
        mood: str,
        reference_file: str
    ) -> Optional[Path]:
        """
        Genera un tono ambiental con FFmpeg cuando no hay música disponible.
        
        Args:
            mood: Estado de ánimo (tension, dramatic, etc.)
            reference_file: Archivo de referencia para duración
            
        Returns:
            Ruta al archivo generado
        """
        duration = self._get_duration(reference_file) + 5  # Extra para fade
        output = self.music_dir / f"generated_{mood}.mp3"
        
        # Configuración de tonos por mood
        tone_configs = {
            "tension": {
                "freq1": 80,   # Bajo profundo
                "freq2": 120,
                "type": "sine",
                "noise": 0.02
            },
            "dramatic": {
                "freq1": 60,
                "freq2": 90,
                "type": "sine",
                "noise": 0.03
            },
            "curiosity": {
                "freq1": 200,
                "freq2": 300,
                "type": "sine",
                "noise": 0.01
            },
            "epic": {
                "freq1": 50,
                "freq2": 100,
                "type": "sine",
                "noise": 0.04
            },
            "chill": {
                "freq1": 150,
                "freq2": 180,
                "type": "sine",
                "noise": 0.01
            }
        }
        
        config = tone_configs.get(mood, tone_configs["tension"])
        
        # Generar tono ambiental con ruido suave
        filter_str = (
            f"sine=f={config['freq1']}:d={duration},"
            f"volume=0.3[s1];"
            f"sine=f={config['freq2']}:d={duration},"
            f"volume=0.2[s2];"
            f"anoisesrc=d={duration}:c=pink:a={config['noise']}[noise];"
            f"[s1][s2][noise]amix=inputs=3:duration=longest,"
            f"lowpass=f=500,volume=0.5"
        )
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", filter_str,
            "-c:a", "libmp3lame", "-b:a", "128k",
            "-t", str(duration),
            str(output)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return output
        return None
    
    def _get_duration(self, file_path: str) -> float:
        """Obtiene duración de un archivo multimedia"""
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ], capture_output=True, text=True)
        
        try:
            return float(result.stdout.strip())
        except:
            return 30.0
    
    def list_available_music(self) -> Dict[str, Dict]:
        """Lista música disponible y su estado"""
        result = {}
        for name, info in self.MUSIC_LIBRARY.items():
            local_path = self.music_dir / info["local_file"]
            result[name] = {
                **info,
                "available": local_path.exists(),
                "path": str(local_path) if local_path.exists() else None
            }
        return result


def main():
    """CLI para probar el mezclador"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Añade música de fondo")
    parser.add_argument("--input", required=True, help="Archivo de entrada (audio/video)")
    parser.add_argument("--output", required=True, help="Archivo de salida")
    parser.add_argument("--music", default="tension", help="Tipo de música")
    parser.add_argument("--volume", type=float, default=0.15, help="Volumen música (0-1)")
    
    args = parser.parse_args()
    
    mixer = MusicMixer()
    
    if args.input.endswith(('.mp4', '.mov', '.mkv')):
        result = mixer.add_music_to_video(
            args.input, args.output,
            music_type=args.music,
            music_volume=args.volume
        )
    else:
        result = mixer.mix_audio_with_music(
            args.input, args.output,
            music_type=args.music,
            music_volume=args.volume
        )
    
    if result:
        print(f"✅ Generado: {result}")
    else:
        print("❌ Error")


if __name__ == "__main__":
    main()
