#!/usr/bin/env python3
"""
FFmpeg Utilities
Funciones helper para operaciones comunes con FFmpeg.
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, Optional, List, Tuple


def get_duration(file_path: str) -> float:
    """
    Obtiene la duración de un archivo multimedia.
    
    Args:
        file_path: Ruta al archivo
        
    Returns:
        Duración en segundos
    """
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ], capture_output=True, text=True)
    
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def get_video_info(file_path: str) -> Dict:
    """
    Obtiene información completa de un video.
    
    Args:
        file_path: Ruta al video
        
    Returns:
        Diccionario con info del video
    """
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,r_frame_rate,codec_name",
        "-show_entries", "format=duration,size,bit_rate",
        "-of", "json",
        file_path
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        stream = data.get("streams", [{}])[0]
        format_info = data.get("format", {})
        
        # Parse frame rate
        fps = stream.get("r_frame_rate", "0/1")
        if "/" in fps:
            num, den = fps.split("/")
            fps = float(num) / float(den) if float(den) > 0 else 0
        
        return {
            "width": stream.get("width"),
            "height": stream.get("height"),
            "duration": float(format_info.get("duration", 0)),
            "fps": round(fps, 2),
            "codec": stream.get("codec_name"),
            "size_bytes": int(format_info.get("size", 0)),
            "size_mb": round(int(format_info.get("size", 0)) / (1024 * 1024), 2),
            "bitrate": int(format_info.get("bit_rate", 0))
        }
    except:
        return {}


def get_audio_info(file_path: str) -> Dict:
    """
    Obtiene información de un archivo de audio.
    
    Args:
        file_path: Ruta al audio
        
    Returns:
        Diccionario con info del audio
    """
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,bit_rate",
        "-show_entries", "format=duration,size",
        "-of", "json",
        file_path
    ], capture_output=True, text=True)
    
    try:
        data = json.loads(result.stdout)
        stream = data.get("streams", [{}])[0]
        format_info = data.get("format", {})
        
        return {
            "duration": float(format_info.get("duration", 0)),
            "codec": stream.get("codec_name"),
            "sample_rate": int(stream.get("sample_rate", 0)),
            "channels": stream.get("channels"),
            "bitrate": int(stream.get("bit_rate", 0)),
            "size_mb": round(int(format_info.get("size", 0)) / (1024 * 1024), 2)
        }
    except:
        return {}


def normalize_audio(
    input_path: str,
    output_path: str,
    target_level: float = -16.0
) -> bool:
    """
    Normaliza el volumen del audio.
    
    Args:
        input_path: Audio de entrada
        output_path: Audio de salida
        target_level: Nivel objetivo en LUFS
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-af", f"loudnorm=I={target_level}:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame", "-b:a", "192k",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def concat_videos(
    video_paths: List[str],
    output_path: str,
    transition: Optional[str] = None
) -> bool:
    """
    Concatena múltiples videos.
    
    Args:
        video_paths: Lista de rutas a videos
        output_path: Video de salida
        transition: Tipo de transición (fade, none)
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Crear archivo de lista
    list_file = Path(output_path).parent / "concat_list.txt"
    with open(list_file, 'w') as f:
        for path in video_paths:
            f.write(f"file '{path}'\n")
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(list_file),
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "aac",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    
    # Limpiar
    list_file.unlink(missing_ok=True)
    
    return result.returncode == 0


def add_audio_to_video(
    video_path: str,
    audio_path: str,
    output_path: str,
    replace_audio: bool = True
) -> bool:
    """
    Añade pista de audio a un video.
    
    Args:
        video_path: Video de entrada
        audio_path: Audio a añadir
        output_path: Video de salida
        replace_audio: Si True, reemplaza audio existente
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if replace_audio:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            output_path
        ]
    else:
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-filter_complex", "[0:a][1:a]amix=inputs=2[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            output_path
        ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def scale_video(
    input_path: str,
    output_path: str,
    width: int,
    height: int,
    mode: str = "crop"
) -> bool:
    """
    Redimensiona un video.
    
    Args:
        input_path: Video de entrada
        output_path: Video de salida
        width: Ancho objetivo
        height: Alto objetivo
        mode: crop | pad | stretch
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    if mode == "crop":
        vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
    elif mode == "pad":
        vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
    else:  # stretch
        vf = f"scale={width}:{height}"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"{vf},setsar=1",
        "-c:v", "libx264", "-preset", "fast",
        "-c:a", "copy",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def loop_video(
    input_path: str,
    output_path: str,
    duration: float
) -> bool:
    """
    Hace loop de un video hasta alcanzar la duración deseada.
    
    Args:
        input_path: Video de entrada
        output_path: Video de salida
        duration: Duración objetivo en segundos
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", input_path,
        "-t", str(duration),
        "-c:v", "libx264", "-preset", "fast",
        "-an",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def extract_audio(
    video_path: str,
    output_path: str,
    format: str = "mp3"
) -> bool:
    """
    Extrae audio de un video.
    
    Args:
        video_path: Video de entrada
        output_path: Audio de salida
        format: Formato (mp3, aac, wav)
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    codec = {
        "mp3": "libmp3lame",
        "aac": "aac",
        "wav": "pcm_s16le"
    }.get(format, "libmp3lame")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-c:a", codec,
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def burn_subtitles(
    video_path: str,
    subtitle_path: str,
    output_path: str
) -> bool:
    """
    Quema subtítulos en el video.
    
    Args:
        video_path: Video de entrada
        subtitle_path: Archivo de subtítulos (ASS, SRT)
        output_path: Video de salida
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Determinar filtro según extensión
    ext = Path(subtitle_path).suffix.lower()
    if ext == ".ass":
        vf = f"ass={subtitle_path}"
    else:
        vf = f"subtitles={subtitle_path}"
    
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "23",
        "-c:a", "copy",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def create_silence(output_path: str, duration: float) -> bool:
    """
    Crea un archivo de audio en silencio.
    
    Args:
        output_path: Ruta de salida
        duration: Duración en segundos
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-c:a", "libmp3lame",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def create_color_video(
    output_path: str,
    width: int,
    height: int,
    duration: float,
    color: str = "black"
) -> bool:
    """
    Crea un video de color sólido.
    
    Args:
        output_path: Ruta de salida
        width: Ancho
        height: Alto
        duration: Duración
        color: Color (black, white, red, #RRGGBB)
        
    Returns:
        True si exitoso
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c={color}:s={width}x{height}:d={duration}:r=30",
        "-c:v", "libx264", "-preset", "fast",
        output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True)
    return result.returncode == 0


def check_ffmpeg_installed() -> bool:
    """Verifica si FFmpeg está instalado"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    print("🔧 FFmpeg Utilities")
    print("=" * 40)
    
    if check_ffmpeg_installed():
        print("✅ FFmpeg está instalado")
        
        # Mostrar versión
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        version = result.stdout.split('\n')[0]
        print(f"   {version}")
    else:
        print("❌ FFmpeg no está instalado")
        print("   Instalar con: sudo apt install ffmpeg")
