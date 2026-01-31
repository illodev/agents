#!/usr/bin/env python3
"""
Video Generator
Generador completo de videos para plataformas verticales (Shorts/Reels/TikTok).

Soporta múltiples fuentes de visuales:
- Videos de stock (Pexels API)
- Imágenes con efecto Ken Burns
- Fondos animados generados con FFmpeg
- Fondos espaciales con estrellas
"""

import os
import subprocess
import random
from pathlib import Path
from typing import List, Dict, Optional, Literal
from enum import Enum

# Imports locales
try:
    from .pexels_client import PexelsClient
    from .subtitle_generator import SubtitleGenerator
except ImportError:
    from pexels_client import PexelsClient
    from subtitle_generator import SubtitleGenerator


class VideoStyle(Enum):
    """Estilos de video disponibles"""
    STOCK_VIDEO = "stock_video"
    STOCK_IMAGES = "stock_images"
    ANIMATED = "animated"
    SPACE = "space"
    AUTO = "auto"


class VideoGenerator:
    """Generador principal de videos"""
    
    # Resoluciones soportadas
    RESOLUTIONS = {
        "shorts": (1080, 1920),   # YouTube Shorts, TikTok, Reels
        "landscape": (1920, 1080), # YouTube estándar
        "square": (1080, 1080)     # Instagram feed
    }
    
    def __init__(
        self,
        pexels_api_key: Optional[str] = None,
        output_dir: Optional[str] = None
    ):
        """
        Inicializa el generador.
        
        Args:
            pexels_api_key: API key de Pexels (opcional si está en config)
            output_dir: Directorio de salida
        """
        self.pexels_client = None
        if pexels_api_key:
            try:
                self.pexels_client = PexelsClient(pexels_api_key)
            except ValueError:
                pass
        else:
            try:
                self.pexels_client = PexelsClient()
            except ValueError:
                pass
        
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.temp_dir = self.output_dir / ".temp"
        self.temp_dir.mkdir(exist_ok=True)
    
    def generate(
        self,
        audio_path: str,
        output_path: str,
        style: VideoStyle = VideoStyle.AUTO,
        keywords: Optional[List[str]] = None,
        subtitle_text: Optional[str] = None,
        subtitle_path: Optional[str] = None,
        resolution: str = "shorts",
        duration: Optional[float] = None
    ) -> Dict:
        """
        Genera un video completo.
        
        Args:
            audio_path: Ruta al archivo de audio
            output_path: Ruta de salida del video
            style: Estilo de video a usar
            keywords: Palabras clave para buscar contenido
            subtitle_text: Texto para generar subtítulos
            subtitle_path: Ruta a archivo de subtítulos existente
            resolution: shorts | landscape | square
            duration: Duración forzada (default: duración del audio)
            
        Returns:
            Diccionario con información del video generado
        """
        # Obtener resolución
        width, height = self.RESOLUTIONS.get(resolution, self.RESOLUTIONS["shorts"])
        
        # Obtener duración
        if duration is None:
            duration = self._get_duration(audio_path)
        
        # Seleccionar estilo
        if style == VideoStyle.AUTO:
            style = self._select_best_style(keywords)
        
        # Generar fondo según estilo
        bg_video = self._generate_background(
            style=style,
            keywords=keywords or [],
            duration=duration,
            width=width,
            height=height
        )
        
        if not bg_video:
            return {"success": False, "error": "No se pudo generar fondo"}
        
        # Generar subtítulos si hay texto
        if subtitle_text and not subtitle_path:
            subtitle_path = str(self.temp_dir / "subs.ass")
            gen = SubtitleGenerator()
            gen.from_text(subtitle_text, duration, subtitle_path)
        
        # Componer video final
        result = self._compose_final_video(
            background=bg_video,
            audio=audio_path,
            subtitles=subtitle_path,
            output=output_path,
            duration=duration
        )
        
        # Limpiar temporales
        self._cleanup_temp()
        
        if result:
            size_mb = Path(output_path).stat().st_size / (1024 * 1024)
            return {
                "success": True,
                "output": output_path,
                "duration": duration,
                "size_mb": round(size_mb, 2),
                "style": style.value,
                "resolution": f"{width}x{height}"
            }
        
        return {"success": False, "error": "Error al componer video"}
    
    def _generate_background(
        self,
        style: VideoStyle,
        keywords: List[str],
        duration: float,
        width: int,
        height: int
    ) -> Optional[str]:
        """Genera el fondo según el estilo seleccionado"""
        
        if style == VideoStyle.STOCK_VIDEO:
            return self._generate_stock_video_bg(keywords, duration, width, height)
        
        elif style == VideoStyle.STOCK_IMAGES:
            return self._generate_ken_burns_bg(keywords, duration, width, height)
        
        elif style == VideoStyle.ANIMATED:
            return self._generate_animated_bg(duration, width, height)
        
        elif style == VideoStyle.SPACE:
            return self._generate_space_bg(duration, width, height)
        
        return None
    
    def _generate_stock_video_bg(
        self,
        keywords: List[str],
        duration: float,
        width: int,
        height: int
    ) -> Optional[str]:
        """Genera fondo con video de stock de Pexels"""
        if not self.pexels_client:
            print("⚠️ No hay API key de Pexels, usando fondo animado")
            return self._generate_animated_bg(duration, width, height)
        
        # Buscar videos
        query = " ".join(keywords) if keywords else "abstract background"
        orientation = "portrait" if height > width else "landscape"
        
        videos = self.pexels_client.search_videos(query, orientation=orientation, count=5)
        
        if not videos:
            print(f"⚠️ No se encontraron videos para '{query}', probando alternativas")
            for alt_query in ["abstract", "nature", "sky"]:
                videos = self.pexels_client.search_videos(alt_query, orientation=orientation, count=3)
                if videos:
                    break
        
        if not videos:
            return self._generate_animated_bg(duration, width, height)
        
        # Descargar video
        video = random.choice(videos)
        local_path = str(self.temp_dir / f"pexels_{video['id']}.mp4")
        
        if not self.pexels_client.download_video(video, local_path):
            return self._generate_animated_bg(duration, width, height)
        
        # Procesar para ajustar resolución y hacer loop
        output = str(self.temp_dir / "bg_stock.mp4")
        
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", local_path,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1",
            "-t", str(duration),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-an",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return output if result.returncode == 0 else None
    
    def _generate_ken_burns_bg(
        self,
        keywords: List[str],
        duration: float,
        width: int,
        height: int
    ) -> Optional[str]:
        """Genera fondo con imágenes y efecto Ken Burns"""
        if not self.pexels_client:
            return self._generate_animated_bg(duration, width, height)
        
        query = " ".join(keywords) if keywords else "nature landscape"
        orientation = "portrait" if height > width else "landscape"
        
        # Calcular imágenes necesarias (5 seg por imagen)
        num_images = max(3, int(duration / 5))
        
        images = self.pexels_client.search_images(query, orientation=orientation, count=num_images)
        
        if len(images) < 2:
            return self._generate_animated_bg(duration, width, height)
        
        # Descargar imágenes
        image_paths = []
        for i, img in enumerate(images[:num_images]):
            local_path = str(self.temp_dir / f"img_{i}.jpg")
            if self.pexels_client.download_image(img, local_path):
                image_paths.append(local_path)
        
        if len(image_paths) < 2:
            return self._generate_animated_bg(duration, width, height)
        
        # Crear video con Ken Burns
        output = str(self.temp_dir / "bg_kenburns.mp4")
        time_per_image = duration / len(image_paths)
        
        # Crear videos individuales con efecto
        segments = []
        for i, img_path in enumerate(image_paths):
            segment = str(self.temp_dir / f"segment_{i}.mp4")
            
            # Alternar zoom in/out
            if i % 2 == 0:
                zoom = f"zoompan=z='min(zoom+0.0015,1.5)':d={int(time_per_image*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}"
            else:
                zoom = f"zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d={int(time_per_image*30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={width}x{height}"
            
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", img_path,
                "-vf", f"scale=8000:-1,{zoom}",
                "-t", str(time_per_image),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                segment
            ]
            
            result = subprocess.run(cmd, capture_output=True)
            if result.returncode == 0:
                segments.append(segment)
        
        if not segments:
            return self._generate_animated_bg(duration, width, height)
        
        # Concatenar segmentos
        list_file = str(self.temp_dir / "segments.txt")
        with open(list_file, 'w') as f:
            for seg in segments:
                f.write(f"file '{seg}'\n")
        
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", list_file,
            "-c:v", "libx264", "-preset", "fast",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return output if result.returncode == 0 else None
    
    def _generate_animated_bg(
        self,
        duration: float,
        width: int,
        height: int
    ) -> Optional[str]:
        """Genera fondo con gradiente animado"""
        output = str(self.temp_dir / "bg_animated.mp4")
        
        # Colores para gradiente
        colors = [
            ("0x1a0a2e", "0x16213e"),  # Azul oscuro
            ("0x1e3a5f", "0x0f4c75"),  # Azul medio
            ("0x2d132c", "0x801336"),  # Púrpura
            ("0x1b1b2f", "0x162447"),  # Azul noche
        ]
        c1, c2 = random.choice(colors)
        
        # Generar con gradiente animado + ruido
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={c1}:s={width}x{height}:d={duration}:r=30,format=rgb24,"
                  f"geq=r='clip(r(X,Y)+random(1)*20,0,255)':"
                  f"g='clip(g(X,Y)+random(1)*15,0,255)':"
                  f"b='clip(b(X,Y)+random(1)*25,0,255)',format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return output if result.returncode == 0 else None
    
    def _generate_space_bg(
        self,
        duration: float,
        width: int,
        height: int
    ) -> Optional[str]:
        """Genera fondo espacial con estrellas"""
        output = str(self.temp_dir / "bg_space.mp4")
        
        # Fondo oscuro con estrellas
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x050510:s={width}x{height}:d={duration}:r=30,format=rgb24,"
                  f"geq=r='if(lt(random(1),0.0008),255,r(X,Y)+random(1)*3)':"
                  f"g='if(lt(random(1),0.0008),255,g(X,Y)+random(1)*2)':"
                  f"b='if(lt(random(1),0.0008),255,b(X,Y)+random(1)*8)',format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return output if result.returncode == 0 else None
    
    def _compose_final_video(
        self,
        background: str,
        audio: str,
        subtitles: Optional[str],
        output: str,
        duration: float
    ) -> bool:
        """Compone el video final con audio y subtítulos"""
        
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        
        # Construir filtro
        vf = []
        if subtitles:
            vf.append(f"ass={subtitles}")
        
        vf_str = ",".join(vf) if vf else "null"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", background,
            "-i", audio,
            "-filter_complex", f"[0:v]{vf_str}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "23",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(duration),
            "-movflags", "+faststart",
            output
        ]
        
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0
    
    def _select_best_style(self, keywords: Optional[List[str]]) -> VideoStyle:
        """Selecciona el mejor estilo según contexto"""
        if self.pexels_client:
            return VideoStyle.STOCK_VIDEO
        return VideoStyle.SPACE
    
    def _get_duration(self, file_path: str) -> float:
        """Obtiene duración de un archivo multimedia"""
        result = subprocess.run([
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            file_path
        ], capture_output=True, text=True)
        return float(result.stdout.strip())
    
    def _cleanup_temp(self):
        """Limpia archivos temporales"""
        for f in self.temp_dir.glob("*"):
            try:
                f.unlink()
            except:
                pass


# Alias para compatibilidad
ShortVideoGenerator = VideoGenerator


def create_short(
    audio_path: str,
    output_path: str,
    keywords: Optional[List[str]] = None,
    subtitle_text: Optional[str] = None,
    style: str = "auto"
) -> Dict:
    """
    Función helper para crear shorts rápidamente.
    
    Args:
        audio_path: Ruta al audio
        output_path: Ruta de salida
        keywords: Palabras clave para buscar fondo
        subtitle_text: Texto para subtítulos
        style: stock_video | stock_images | animated | space | auto
        
    Returns:
        Diccionario con resultado
    """
    generator = VideoGenerator()
    
    style_enum = VideoStyle(style) if style != "auto" else VideoStyle.AUTO
    
    return generator.generate(
        audio_path=audio_path,
        output_path=output_path,
        style=style_enum,
        keywords=keywords,
        subtitle_text=subtitle_text
    )


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("🎬 Video Generator - Test")
    print("=" * 60)
    
    if len(sys.argv) < 3:
        print("""
Uso: python video_generator.py <audio> <output> [style]

Estilos:
  stock_video  - Videos de Pexels (requiere API key)
  stock_images - Imágenes con Ken Burns (requiere API key)
  animated     - Gradientes animados
  space        - Fondo espacial con estrellas
  auto         - Selección automática
        """)
        sys.exit(0)
    
    audio = sys.argv[1]
    output = sys.argv[2]
    style = sys.argv[3] if len(sys.argv) > 3 else "auto"
    
    result = create_short(
        audio_path=audio,
        output_path=output,
        keywords=["nature", "abstract"],
        style=style
    )
    
    print(f"\n📊 Resultado: {result}")
