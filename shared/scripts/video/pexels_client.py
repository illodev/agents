#!/usr/bin/env python3
"""
Pexels API Client
Cliente para interactuar con la API gratuita de Pexels.

Límites gratuitos:
- 200 requests/hora
- 20,000 requests/mes
- Sin atribución obligatoria para videos

Documentación: https://www.pexels.com/api/documentation/
"""

import os
import requests
from pathlib import Path
from typing import List, Dict, Optional


class PexelsClient:
    """Cliente para la API de Pexels"""
    
    BASE_URL = "https://api.pexels.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el cliente de Pexels.
        
        Args:
            api_key: API key de Pexels. Si no se proporciona, 
                     busca en variable de entorno PEXELS_API_KEY
        """
        self.api_key = api_key or os.getenv("PEXELS_API_KEY")
        
        if not self.api_key:
            # Intentar leer del archivo de credenciales unificado
            config_path = Path(__file__).parents[3] / "config" / "credentials.env"
            if config_path.exists():
                with open(config_path) as f:
                    for line in f:
                        if line.startswith("PEXELS_API_KEY="):
                            self.api_key = line.split("=", 1)[1].strip()
                            break
        
        if not self.api_key:
            raise ValueError(
                "Se requiere PEXELS_API_KEY. Configúrala en:\n"
                "1. Parámetro api_key\n"
                "2. Variable de entorno PEXELS_API_KEY\n"
                "3. Archivo /config/credentials.env"
            )
        
        self.headers = {"Authorization": self.api_key}
    
    def search_videos(
        self,
        query: str,
        orientation: str = "portrait",
        size: str = "medium",
        count: int = 10,
        page: int = 1
    ) -> List[Dict]:
        """
        Busca videos en Pexels.
        
        Args:
            query: Términos de búsqueda
            orientation: portrait | landscape | square
            size: small | medium | large
            count: Número de resultados (máx 80)
            page: Página de resultados
            
        Returns:
            Lista de diccionarios con info de videos
        """
        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "per_page": min(count, 80),
            "page": page
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/videos/search",
                headers=self.headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for video in data.get("videos", []):
                # Buscar mejor archivo de video
                best_file = self._get_best_video_file(video, orientation)
                if best_file:
                    videos.append({
                        "id": video.get("id"),
                        "url": best_file["link"],
                        "width": best_file.get("width"),
                        "height": best_file.get("height"),
                        "duration": video.get("duration"),
                        "user": video.get("user", {}).get("name"),
                        "user_url": video.get("user", {}).get("url"),
                        "pexels_url": video.get("url")
                    })
            
            return videos
            
        except requests.RequestException as e:
            print(f"Error buscando videos en Pexels: {e}")
            return []
    
    def search_images(
        self,
        query: str,
        orientation: str = "portrait",
        size: str = "large",
        count: int = 10,
        page: int = 1
    ) -> List[Dict]:
        """
        Busca imágenes en Pexels.
        
        Args:
            query: Términos de búsqueda
            orientation: portrait | landscape | square
            size: small | medium | large
            count: Número de resultados (máx 80)
            page: Página de resultados
            
        Returns:
            Lista de diccionarios con info de imágenes
        """
        params = {
            "query": query,
            "orientation": orientation,
            "size": size,
            "per_page": min(count, 80),
            "page": page
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/v1/search",
                headers=self.headers,
                params=params,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            images = []
            for photo in data.get("photos", []):
                src = photo.get("src", {})
                # Elegir tamaño según orientation
                if orientation == "portrait":
                    img_url = src.get("portrait") or src.get("large2x")
                else:
                    img_url = src.get("landscape") or src.get("large2x")
                
                images.append({
                    "id": photo.get("id"),
                    "url": img_url,
                    "original_url": src.get("original"),
                    "width": photo.get("width"),
                    "height": photo.get("height"),
                    "photographer": photo.get("photographer"),
                    "photographer_url": photo.get("photographer_url"),
                    "pexels_url": photo.get("url"),
                    "alt": photo.get("alt", "")
                })
            
            return images
            
        except requests.RequestException as e:
            print(f"Error buscando imágenes en Pexels: {e}")
            return []
    
    def get_curated_videos(self, count: int = 10, page: int = 1) -> List[Dict]:
        """Obtiene videos populares/curados"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/videos/popular",
                headers=self.headers,
                params={"per_page": min(count, 80), "page": page},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            
            videos = []
            for video in data.get("videos", []):
                best_file = self._get_best_video_file(video, "portrait")
                if best_file:
                    videos.append({
                        "id": video.get("id"),
                        "url": best_file["link"],
                        "width": best_file.get("width"),
                        "height": best_file.get("height"),
                        "duration": video.get("duration")
                    })
            
            return videos
            
        except requests.RequestException as e:
            print(f"Error obteniendo videos curados: {e}")
            return []
    
    def download_video(
        self,
        video: Dict,
        output_path: str,
        timeout: int = 120
    ) -> Optional[str]:
        """
        Descarga un video.
        
        Args:
            video: Diccionario con info del video (de search_videos)
            output_path: Ruta donde guardar el video
            timeout: Timeout en segundos
            
        Returns:
            Path al archivo descargado o None si falla
        """
        url = video.get("url")
        if not url:
            return None
        
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_path
            
        except requests.RequestException as e:
            print(f"Error descargando video: {e}")
            return None
    
    def download_image(
        self,
        image: Dict,
        output_path: str,
        timeout: int = 60
    ) -> Optional[str]:
        """
        Descarga una imagen.
        
        Args:
            image: Diccionario con info de imagen (de search_images)
            output_path: Ruta donde guardar
            timeout: Timeout en segundos
            
        Returns:
            Path al archivo descargado o None si falla
        """
        url = image.get("url") or image.get("original_url")
        if not url:
            return None
        
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return output_path
            
        except requests.RequestException as e:
            print(f"Error descargando imagen: {e}")
            return None
    
    def _get_best_video_file(
        self,
        video: Dict,
        orientation: str = "portrait"
    ) -> Optional[Dict]:
        """Encuentra el mejor archivo de video para el formato deseado"""
        video_files = video.get("video_files", [])
        
        best = None
        best_score = 0
        
        for vf in video_files:
            width = vf.get("width", 0)
            height = vf.get("height", 0)
            
            # Preferir vertical para Shorts
            is_vertical = height > width
            is_hd = height >= 720
            
            score = 0
            if orientation == "portrait" and is_vertical:
                score += 100
            elif orientation == "landscape" and not is_vertical:
                score += 100
            
            if is_hd:
                score += height // 10  # Mayor res = mayor score
            
            if score > best_score:
                best_score = score
                best = vf
        
        return best
    
    def test_connection(self) -> bool:
        """Prueba la conexión con la API"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/videos/popular",
                headers=self.headers,
                params={"per_page": 1},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False


# Función helper para uso rápido
def get_pexels_client(api_key: Optional[str] = None) -> PexelsClient:
    """Obtiene un cliente de Pexels configurado"""
    return PexelsClient(api_key)


if __name__ == "__main__":
    # Test
    import sys
    
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
    else:
        api_key = None
    
    try:
        client = PexelsClient(api_key)
        
        print("🔍 Probando búsqueda de videos...")
        videos = client.search_videos("stars space", count=3)
        print(f"✅ Encontrados {len(videos)} videos")
        for v in videos:
            print(f"   - ID: {v['id']}, {v['width']}x{v['height']}, {v['duration']}s")
        
        print("\n🔍 Probando búsqueda de imágenes...")
        images = client.search_images("nature", count=3)
        print(f"✅ Encontradas {len(images)} imágenes")
        for img in images:
            print(f"   - ID: {img['id']}, {img['width']}x{img['height']}")
        
        print("\n✅ Cliente de Pexels funcionando correctamente!")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
