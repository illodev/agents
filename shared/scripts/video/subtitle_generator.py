#!/usr/bin/env python3
"""
Subtitle Generator
Generador de subtítulos en formato ASS para videos verticales (Shorts/Reels/TikTok).

Formato ASS soporta estilos avanzados:
- Fuentes personalizadas
- Colores y efectos
- Posicionamiento preciso
- Animaciones
"""

import re
from pathlib import Path
from typing import List, Optional, Tuple


class SubtitleGenerator:
    """Generador de subtítulos ASS para videos verticales"""
    
    # Estilos predefinidos
    STYLES = {
        "default": {
            "fontname": "Montserrat",
            "fontsize": 72,
            "primary_color": "&H00FFFFFF",  # Blanco
            "outline_color": "&H00000000",  # Negro
            "back_color": "&H80000000",     # Negro semi-transparente
            "bold": 1,
            "outline": 4,
            "shadow": 2,
            "alignment": 2,  # Centro inferior
            "margin_v": 400
        },
        "bold_center": {
            "fontname": "Impact",
            "fontsize": 80,
            "primary_color": "&H00FFFFFF",
            "outline_color": "&H00000000",
            "back_color": "&H00000000",
            "bold": 1,
            "outline": 5,
            "shadow": 3,
            "alignment": 5,  # Centro
            "margin_v": 50
        },
        "minimal": {
            "fontname": "Arial",
            "fontsize": 64,
            "primary_color": "&H00FFFFFF",
            "outline_color": "&H00000000",
            "back_color": "&H00000000",
            "bold": 0,
            "outline": 2,
            "shadow": 1,
            "alignment": 2,
            "margin_v": 300
        },
        "neon": {
            "fontname": "Bebas Neue",
            "fontsize": 76,
            "primary_color": "&H0000FFFF",  # Cyan
            "outline_color": "&H00FF00FF",  # Magenta
            "back_color": "&H00000000",
            "bold": 1,
            "outline": 3,
            "shadow": 0,
            "alignment": 5,
            "margin_v": 50
        }
    }
    
    def __init__(self, style: str = "default", custom_style: Optional[dict] = None):
        """
        Inicializa el generador.
        
        Args:
            style: Nombre del estilo predefinido
            custom_style: Diccionario con estilos personalizados
        """
        self.style = self.STYLES.get(style, self.STYLES["default"]).copy()
        if custom_style:
            self.style.update(custom_style)
    
    def from_text(
        self,
        text: str,
        duration: float,
        output_path: str,
        words_per_subtitle: int = 5
    ) -> str:
        """
        Genera subtítulos desde texto plano.
        
        Args:
            text: Texto completo para subtitular
            duration: Duración total del video en segundos
            output_path: Ruta del archivo ASS de salida
            words_per_subtitle: Palabras máximas por subtítulo
            
        Returns:
            Ruta al archivo generado
        """
        # Dividir en oraciones y luego en fragmentos
        sentences = self._split_into_sentences(text)
        fragments = self._split_into_fragments(sentences, words_per_subtitle)
        
        # Calcular timing
        time_per_fragment = duration / len(fragments) if fragments else duration
        
        # Generar ASS
        ass_content = self._generate_ass_header()
        
        for i, fragment in enumerate(fragments):
            start = i * time_per_fragment
            end = (i + 1) * time_per_fragment
            ass_content += self._create_dialogue_line(fragment, start, end)
        
        # Guardar
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        
        return output_path
    
    def from_lines(
        self,
        lines: List[str],
        duration: float,
        output_path: str
    ) -> str:
        """
        Genera subtítulos desde lista de líneas.
        
        Args:
            lines: Lista de líneas de texto
            duration: Duración total
            output_path: Ruta de salida
            
        Returns:
            Ruta al archivo generado
        """
        time_per_line = duration / len(lines) if lines else duration
        
        ass_content = self._generate_ass_header()
        
        for i, line in enumerate(lines):
            start = i * time_per_line
            end = (i + 1) * time_per_line
            ass_content += self._create_dialogue_line(line.strip(), start, end)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        
        return output_path
    
    def from_script(
        self,
        script_path: str,
        audio_duration: float,
        output_path: str
    ) -> str:
        """
        Genera subtítulos desde archivo de script markdown.
        
        Args:
            script_path: Ruta al script (.md)
            audio_duration: Duración del audio
            output_path: Ruta de salida
            
        Returns:
            Ruta al archivo generado
        """
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extraer texto narrable (ignorar metadata)
        text = self._extract_narration(content)
        
        return self.from_text(text, audio_duration, output_path)
    
    def from_timed_segments(
        self,
        segments: List[Tuple[str, float, float]],
        output_path: str
    ) -> str:
        """
        Genera subtítulos desde segmentos con timing específico.
        
        Args:
            segments: Lista de (texto, inicio_seg, fin_seg)
            output_path: Ruta de salida
            
        Returns:
            Ruta al archivo generado
        """
        ass_content = self._generate_ass_header()
        
        for text, start, end in segments:
            ass_content += self._create_dialogue_line(text, start, end)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ass_content)
        
        return output_path
    
    def _generate_ass_header(self) -> str:
        """Genera el header del archivo ASS"""
        s = self.style
        
        return f"""[Script Info]
Title: Short Video Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{s['fontname']},{s['fontsize']},{s['primary_color']},&H000000FF,{s['outline_color']},{s['back_color']},{s['bold']},0,0,0,100,100,0,0,1,{s['outline']},{s['shadow']},{s['alignment']},50,50,{s['margin_v']},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    def _create_dialogue_line(self, text: str, start: float, end: float) -> str:
        """Crea una línea de diálogo ASS"""
        start_str = self._format_time(start)
        end_str = self._format_time(end)
        
        # Escapar caracteres especiales de ASS
        text = text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
        
        return f"Dialogue: 0,{start_str},{end_str},Default,,0,0,0,,{text}\n"
    
    def _format_time(self, seconds: float) -> str:
        """Convierte segundos a formato ASS (H:MM:SS.cc)"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}:{minutes:02d}:{secs:05.2f}"
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Divide texto en oraciones"""
        # Limpiar y normalizar
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        
        # Dividir por puntuación
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_into_fragments(
        self,
        sentences: List[str],
        max_words: int
    ) -> List[str]:
        """Divide oraciones en fragmentos de tamaño manejable"""
        fragments = []
        
        for sentence in sentences:
            words = sentence.split()
            
            if len(words) <= max_words:
                fragments.append(sentence)
            else:
                # Dividir oración larga
                for i in range(0, len(words), max_words):
                    fragment = ' '.join(words[i:i + max_words])
                    fragments.append(fragment)
        
        return fragments
    
    def _extract_narration(self, markdown: str) -> str:
        """Extrae texto narrable de un script markdown"""
        lines = []
        in_narration = False
        
        for line in markdown.split('\n'):
            line = line.strip()
            
            # Ignorar headers, metadata y código
            if line.startswith('#'):
                continue
            if line.startswith('```'):
                continue
            if line.startswith('---'):
                continue
            if line.startswith('[') and line.endswith(']'):
                continue
            if ':' in line and line.split(':')[0].isupper():
                continue
            
            # Limpiar markdown
            line = re.sub(r'\*\*(.+?)\*\*', r'\1', line)  # Bold
            line = re.sub(r'\*(.+?)\*', r'\1', line)      # Italic
            line = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', line)  # Links
            
            if line:
                lines.append(line)
        
        return ' '.join(lines)


def create_subtitles(
    text: str,
    duration: float,
    output_path: str,
    style: str = "default"
) -> str:
    """
    Función helper para crear subtítulos rápidamente.
    
    Args:
        text: Texto a subtitular
        duration: Duración en segundos
        output_path: Ruta de salida
        style: Estilo (default, bold_center, minimal, neon)
        
    Returns:
        Ruta al archivo generado
    """
    gen = SubtitleGenerator(style=style)
    return gen.from_text(text, duration, output_path)


if __name__ == "__main__":
    # Test
    test_text = """
    ¿Sabías que hay más estrellas en el universo 
    que granos de arena en todas las playas de la Tierra?
    Los científicos estiman que existen alrededor de 
    200 mil trillones de estrellas.
    ¡Es casi imposible de imaginar!
    """
    
    output = create_subtitles(
        text=test_text,
        duration=30.0,
        output_path="/tmp/test_subs.ass",
        style="default"
    )
    
    print(f"✅ Subtítulos generados: {output}")
    
    with open(output) as f:
        print("\n📄 Contenido:")
        print(f.read())
