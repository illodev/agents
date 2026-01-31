#!/usr/bin/env python3
"""
TikTok Video Producer
Pipeline automatizado para producción de videos TikTok.

Este script integra:
- Generación de audio TTS (Edge-TTS) con voz rápida y dinámica
- Música de fondo ambiental (tensión, dramática, etc.)
- Descarga de videos stock (Pexels)
- Composición de video (FFmpeg)
- Generación de subtítulos ASS

Uso:
    python tiktok_producer.py --script "texto del guion" --output "video_final.mp4"
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# Añadir el directorio padre al path
sys.path.insert(0, str(Path(__file__).parent))

from audio.tts_generator import TTSGenerator
from audio.music_mixer import MusicMixer
from video.pexels_client import PexelsClient


class TikTokProducer:
    """Pipeline de producción de videos TikTok"""
    
    # Configuración por defecto - OPTIMIZADA PARA TIKTOK
    DEFAULT_CONFIG = {
        "resolution": (1080, 1920),  # 9:16 vertical
        "fps": 30,
        "voice": "es-ES-AlvaroNeural",
        "voice_rate": "+20%",         # Más rápido para TikTok
        "voice_pitch": "+5Hz",        # Ligeramente más agudo = más energía
        "max_duration": 60,
        "subtitle_style": "viral",
        # Música de fondo
        "background_music": True,
        "music_type": "tension",      # tension, dramatic, curiosity, epic
        "music_volume": 0.12,         # Volumen bajo para no tapar voz
        "music_fade_in": 0.5,
        "music_fade_out": 1.5
    }
    
    def __init__(
        self,
        output_dir: str,
        pexels_api_key: Optional[str] = None,
        config: Optional[Dict] = None
    ):
        """
        Inicializa el productor.
        
        Args:
            output_dir: Directorio base de salida
            pexels_api_key: API key de Pexels (opcional)
            config: Configuración personalizada
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}
        
        # Inicializar generadores
        self.tts = TTSGenerator(
            voice=self.config["voice"],
            rate=self.config["voice_rate"],
            pitch=self.config.get("voice_pitch", "+0Hz")
        )
        
        # Mezclador de música
        self.music_mixer = MusicMixer(
            music_dir=str(self.output_dir / "music")
        )
        
        try:
            self.pexels = PexelsClient(pexels_api_key) if pexels_api_key else PexelsClient()
        except ValueError:
            self.pexels = None
            print("⚠️ Pexels no configurado - se usarán fondos animados")
        
        # Directorios de trabajo
        self.audio_dir = self.output_dir / "audio"
        self.video_dir = self.output_dir / "video"
        self.temp_dir = self.output_dir / ".temp"
        
        for d in [self.audio_dir, self.video_dir, self.temp_dir]:
            d.mkdir(exist_ok=True)
    
    def produce(
        self,
        script_text: str,
        video_id: str,
        keywords: Optional[List[str]] = None,
        caption: Optional[str] = None
    ) -> Dict:
        """
        Produce un video TikTok completo.
        
        Args:
            script_text: Texto del guion para TTS
            video_id: Identificador único del video
            keywords: Palabras clave para buscar stock
            caption: Descripción/caption del video
            
        Returns:
            Diccionario con resultados de producción
        """
        result = {
            "video_id": video_id,
            "success": False,
            "files": {},
            "errors": []
        }
        
        try:
            # 1. Generar audio TTS
            print(f"🎙️ Generando audio TTS...")
            audio_path = str(self.audio_dir / f"narration-{video_id}.mp3")
            vtt_path = str(self.audio_dir / f"narration-{video_id}.vtt")
            
            tts_result = self.tts.generate_with_srt(
                script_text,
                audio_path,
                vtt_path.replace('.vtt', '.srt')
            )
            
            if not tts_result.get("audio"):
                result["errors"].append("Error generando audio TTS")
                return result
            
            result["files"]["audio"] = audio_path
            result["files"]["subtitles_srt"] = tts_result.get("srt")
            
            # Obtener duración del audio
            duration = self._get_duration(audio_path)
            result["duration"] = duration
            print(f"   ✓ Audio generado: {duration:.1f}s")
            
            # 2. Obtener videos de stock
            print(f"📹 Obteniendo videos de stock...")
            clips = self._get_stock_clips(keywords or [], duration)
            
            if not clips:
                result["errors"].append("No se pudieron obtener clips de stock")
                return result
            
            result["files"]["clips"] = clips
            print(f"   ✓ {len(clips)} clips descargados")
            
            # 3. Componer video
            print(f"🎬 Componiendo video...")
            video_no_subs = str(self.temp_dir / f"{video_id}_no_subs.mp4")
            
            if not self._compose_video(clips, audio_path, video_no_subs, duration):
                result["errors"].append("Error componiendo video")
                return result
            
            print(f"   ✓ Video base creado")
            
            # 4. Generar subtítulos ASS
            print(f"📝 Generando subtítulos...")
            ass_path = str(self.video_dir / f"subtitles-{video_id}.ass")
            
            if tts_result.get("srt"):
                self._create_viral_ass(tts_result["srt"], ass_path)
                result["files"]["subtitles_ass"] = ass_path
            
            # 5. Añadir subtítulos al video
            video_with_subs = str(self.temp_dir / f"{video_id}_with_subs.mp4")
            
            if ass_path and Path(ass_path).exists():
                if not self._add_subtitles(video_no_subs, ass_path, video_with_subs):
                    # Si falla, usar video sin subs
                    import shutil
                    shutil.copy(video_no_subs, video_with_subs)
            else:
                import shutil
                shutil.copy(video_no_subs, video_with_subs)
            
            # 6. Añadir música de fondo
            final_path = str(self.video_dir / f"final" / f"{video_id}-final.mp4")
            Path(final_path).parent.mkdir(exist_ok=True)
            
            if self.config.get("background_music", True):
                print(f"🎵 Añadiendo música de fondo ({self.config.get('music_type', 'tension')})...")
                music_result = self.music_mixer.add_music_to_video(
                    video_with_subs,
                    final_path,
                    music_type=self.config.get("music_type", "tension"),
                    music_volume=self.config.get("music_volume", 0.12),
                    fade_in=self.config.get("music_fade_in", 0.5),
                    fade_out=self.config.get("music_fade_out", 1.5)
                )
                if music_result:
                    print(f"   ✓ Música añadida")
                    result["music_added"] = True
                else:
                    import shutil
                    shutil.copy(video_with_subs, final_path)
            else:
                import shutil
                shutil.copy(video_with_subs, final_path)
            
            result["files"]["video"] = final_path
            result["success"] = True
            
            # Info final
            size_mb = Path(final_path).stat().st_size / (1024 * 1024)
            result["size_mb"] = round(size_mb, 2)
            
            print(f"✅ Video producido: {final_path}")
            print(f"   📊 Duración: {duration:.1f}s | Tamaño: {size_mb:.1f}MB")
            
            # Limpiar temporales
            self._cleanup()
            
        except Exception as e:
            result["errors"].append(str(e))
            print(f"❌ Error: {e}")
        
        return result
    
    def _get_stock_clips(self, keywords: List[str], duration: float) -> List[str]:
        """Descarga clips de stock de Pexels"""
        if not self.pexels:
            return []
        
        clips = []
        clips_needed = max(3, int(duration / 8))  # ~8 segundos por clip
        
        # Si no hay keywords, usar genéricos
        if not keywords:
            keywords = ["abstract", "technology", "nature"]
        
        for i, kw in enumerate(keywords[:clips_needed]):
            videos = self.pexels.search_videos(kw, orientation="portrait", count=2)
            
            if videos:
                video = videos[0]
                clip_path = str(self.temp_dir / f"clip_{i:02d}.mp4")
                
                if self.pexels.download_video(video, clip_path):
                    clips.append(clip_path)
        
        return clips
    
    def _compose_video(
        self,
        clips: List[str],
        audio_path: str,
        output_path: str,
        duration: float
    ) -> bool:
        """Compone el video concatenando clips con audio"""
        width, height = self.config["resolution"]
        fps = self.config["fps"]
        
        # Calcular tiempo por clip
        time_per_clip = duration / len(clips)
        
        # Construir filtro complejo
        inputs = []
        filters = []
        concat_inputs = []
        
        for i, clip in enumerate(clips):
            inputs.extend(["-i", clip])
            filter_name = f"v{i}"
            filters.append(
                f"[{i}:v]trim=0:{time_per_clip},setpts=PTS-STARTPTS,"
                f"scale={width}:{height}:force_original_aspect_ratio=increase,"
                f"crop={width}:{height},setsar=1[{filter_name}]"
            )
            concat_inputs.append(f"[{filter_name}]")
        
        # Añadir audio
        inputs.extend(["-i", audio_path])
        
        # Concatenar
        concat_filter = f"{''.join(concat_inputs)}concat=n={len(clips)}:v=1:a=0[outv]"
        filters.append(concat_filter)
        
        cmd = [
            "ffmpeg", "-y",
            *inputs,
            "-filter_complex", ";".join(filters),
            "-map", "[outv]",
            "-map", f"{len(clips)}:a",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-r", str(fps),
            "-t", str(duration),
            "-movflags", "+faststart",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    def _create_viral_ass(self, srt_path: str, ass_path: str):
        """Convierte SRT a ASS con estilo viral"""
        # Leer SRT
        with open(srt_path, 'r', encoding='utf-8') as f:
            srt_content = f.read()
        
        # Crear ASS básico
        ass_header = """[Script Info]
Title: TikTok Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Montserrat ExtraBold,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,0,2,50,50,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        
        # Parsear SRT y convertir a ASS
        events = []
        blocks = srt_content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                time_line = lines[1]
                text = ' '.join(lines[2:])
                
                # Parsear tiempos
                start, end = time_line.split(' --> ')
                start = self._srt_to_ass_time(start)
                end = self._srt_to_ass_time(end)
                
                # Añadir colores a palabras clave
                text = self._highlight_keywords(text)
                
                events.append(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}")
        
        with open(ass_path, 'w', encoding='utf-8') as f:
            f.write(ass_header + '\n'.join(events))
    
    def _srt_to_ass_time(self, srt_time: str) -> str:
        """Convierte tiempo SRT a formato ASS"""
        srt_time = srt_time.strip().replace(',', '.')
        parts = srt_time.split(':')
        if len(parts) == 3:
            h, m, s = parts
            return f"{int(h)}:{m}:{s[:5]}"
        return "0:00:00.00"
    
    def _highlight_keywords(self, text: str) -> str:
        """Resalta palabras clave en mayúsculas"""
        # Palabras en mayúsculas se colorean
        import re
        
        def colorize(match):
            word = match.group(0)
            return f"{{\\c&H00FFFF&}}{word}{{\\c&HFFFFFF&}}"
        
        return re.sub(r'\b[A-ZÁÉÍÓÚÑ]{2,}\b', colorize, text)
    
    def _add_subtitles(self, video_path: str, ass_path: str, output_path: str) -> bool:
        """Añade subtítulos ASS al video"""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", f"ass={ass_path}",
            "-c:v", "libx264", "-preset", "medium", "-crf", "22",
            "-c:a", "copy",
            "-movflags", "+faststart",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
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
    
    def _cleanup(self):
        """Limpia archivos temporales"""
        import shutil
        if self.temp_dir.exists():
            for f in self.temp_dir.iterdir():
                if f.is_file():
                    f.unlink()


def main():
    parser = argparse.ArgumentParser(description="Produce videos TikTok")
    parser.add_argument("--script", required=True, help="Texto del guion")
    parser.add_argument("--id", required=True, help="ID del video")
    parser.add_argument("--output", required=True, help="Directorio de salida")
    parser.add_argument("--keywords", nargs="+", help="Keywords para stock")
    
    args = parser.parse_args()
    
    producer = TikTokProducer(args.output)
    result = producer.produce(
        script_text=args.script,
        video_id=args.id,
        keywords=args.keywords
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
