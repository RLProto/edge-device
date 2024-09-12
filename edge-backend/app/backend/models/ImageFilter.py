from enum import Enum
from typing import Tuple

from pydantic import BaseModel, Field


class FilterType(str, Enum):
    """
    Enumerador que define os tipos de filtros de imagem suportados. Cada membro do enum representa um tipo específico
    de filtro que pode ser aplicado a uma imagem.

    Membros:<br>
    - crop: Recorta a imagem com base em coordenadas especificadas.<br>
    - blur: Aplica um filtro de desfoque (Gaussian blur).<br>
    - sharpening: Aplica um filtro de realce (Sharpening).<br>
    - brightness: Ajusta o brilho da imagem.<br>
    - contrast: Aumenta o contraste da imagem usando técnicas como CLAHE (Contrast Limited Adaptive Histogram Equalization).<br>
    - exposure: Ajusta a exposição da imagem.<br>
    - grayscale: Converte a imagem para escala de cinza.<br>
    - advanced_grayscale: Converte a imagem para escala de cinza usando pesos personalizados para os canais de cor.<br>
    - edge_detection: Aplica detecção de bordas na imagem (usando o algoritmo Canny, por exemplo).<br>
    - histogram_equalization: Aplica a equalização de histograma para melhorar o contraste da imagem.<br>
    - normalization: Normaliza os valores de pixel da imagem para um intervalo específico.<br>
    - color_segmentation: Segmenta a imagem com base em limites de cor definidos.<br>
    - rotation: Rotaciona a imagem em um ângulo especificado.<br>
    - perspective_distortion: Aplica uma distorção de perspectiva à imagem com base em presets especificados.<br>
    """

    crop = "crop"
    blur = "blur"
    sharpening = "sharpening"
    brightness = "brightness"
    contrast = "contrast"
    exposure = "exposure"
    grayscale = "grayscale"
    advanced_grayscale = "advanced_grayscale"
    edge_detection = "edge_detection"
    histogram_equalization = "histogram_equalization"
    normalization = "normalization"
    color_segmentation = "color_segmentation"
    rotation = "rotation"
    perspective_distortion = "perspective_distortion"


class FilterSpec(BaseModel):
    """
    Especificação de um filtro de imagem, definindo o tipo de filtro e os parâmetros necessários para sua aplicação.

    Atributos:<br>
    - filter_type (FilterType): Tipo do filtro a ser aplicado, conforme definido pelo enumerador FilterType.<br>
    - ksize (int): Tamanho do kernel usado para filtros que envolvem operações de convolução, como o desfoque. O valor deve ser ímpar.<br>
    - intensity (float): Intensidade aplicada em filtros como distorção de perspectiva e outros.<br>
    - adjustment (float): Ajuste geral para filtros que modificam propriedades como brilho ou exposição.<br>
    - lowerBound (Tuple[int, int, int]): Limite inferior para a binarização de cor.<br>
    - upperBound (Tuple[int, int, int]): Limite superior para a binarização de cor.<br>
    - crop_coords (Tuple[int, int, int, int]): Coordenadas para a operação de corte, definidas como (x, y, largura, altura).<br>
    - levels_input (Tuple[int, int]): Níveis de entrada para o ajuste de níveis, especificando mínimo e máximo.<br>
    - levels_output (Tuple[int, int]): Níveis de saída para o ajuste de níveis, especificando mínimo e máximo.<br>
    - gamma (float): Coeficiente para correção gamma no ajuste de níveis.<br>
    - weights (Tuple[float, float, float]): Pesos para conversão em escala de cinza avançada, aplicando pesos diferentes para os canais de cor.
    - rWeight (float): Peso aplicado ao canal vermelho na conversão para escala de cinza avançada.<br>
    - gWeight (float): Peso aplicado ao canal verde na conversão para escala de cinza avançada.<br>
    - bWeight (float): Peso aplicado ao canal azul na conversão para escala de cinza avançada.<br>

    Exemplos:<br>
    Para criar uma especificação de filtro de desfoque:
    ```python
    blur_filter = FilterSpec(filter_type=FilterType.blur, ksize=5)
    ```

    Para definir uma especificação de ajuste de brilho:
    ```python
    brightness_filter = FilterSpec(filter_type=FilterType.brightness, adjustment=20.0)
    ```

    Para criar uma especificação de Advanced Grayscale:
    ```python
    advanced_grayscale_filter = FilterSpec(filter_type=FilterType.advanced_grayscale, weights=(0.3, 0.59, 0.11))
    ```
    """

    filter_type: FilterType
    ksize: int = Field(default=3, ge=1)
    intensity: float = Field(default=1.0)
    adjustment: float = Field(default=0.0)
    lowerBound: Tuple[int, int, int] = Field(default=(0, 0, 0))
    upperBound: Tuple[int, int, int] = Field(default=(255, 255, 255))
    crop_coords: Tuple[int, int, int, int] = Field(default=(0, 0, 100, 100))
    levels_input: Tuple[int, int] = Field(default=(0, 255))
    levels_output: Tuple[int, int] = Field(default=(0, 255))
    gamma: float = Field(default=1.0)
    weights: Tuple[float, float, float] = Field(default=(0.299, 0.587, 0.114))
    rWeight: float = Field(default=0.3)
    gWeight: float = Field(default=0.59)
    bWeight: float = Field(default=0.11)
    alpha: int = Field(default=0)
    beta: int = Field(default=255)
    clipLimit: float = Field(default=2.0)
    angle: int = Field(default=0)
    preset: str = Field(default="none")
