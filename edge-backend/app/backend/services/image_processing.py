from typing import Any, Callable, Dict, Tuple

import cv2
import numpy as np

from app.backend.models.ImageFilter import FilterType


def resize_image(
    img: np.ndarray, max_width: int = 400, max_height: int = 400
) -> np.ndarray:
    """
    Redimensiona a imagem para que caiba dentro das dimensões especificadas, mantendo a proporção.

    Args:
        img (np.ndarray): Imagem de entrada.
        max_width (int, optional): Largura máxima da imagem redimensionada. Default é 300.
        max_height (int, optional): Altura máxima da imagem redimensionada. Default é 300.

    Returns:
        np.ndarray: Imagem redimensionada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> resized_img = resize_image(img, max_width=500, max_height=500)
    """
    height, width = img.shape[:2]

    # Calcula a proporção mantendo a aspect ratio
    scale = min(max_width / width, max_height / height)

    # Calcula as novas dimensões
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Redimensiona a imagem
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_img


def apply_crop(
    img: np.ndarray,
    crop_coords: Tuple[int, int, int, int] = (0, 0, 100, 100),
    **kwargs: Any
) -> np.ndarray:
    """
    Recorta a imagem de acordo com as coordenadas especificadas. Se as coordenadas ultrapassarem os limites da imagem,
    preenche com preto a região excedente.

    Args:
        img (np.ndarray): Imagem de entrada.
        crop_coords (Tuple[int, int, int, int], optional): Tupla especificando as coordenadas do recorte
            (x, y, largura, altura). Default é (0, 0, 100, 100).
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem recortada ou imagem preenchida com preto onde exceder os limites da imagem original.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> cropped_img = apply_crop(img, crop_coords=(50, 50, 200, 200))
    """
    x, y, w, h = crop_coords
    img_h, img_w = img.shape[:2]

    # Cria uma nova imagem preta do tamanho desejado
    new_img = np.zeros((h, w, 3), dtype=np.uint8)

    # Calcula a região a ser copiada da imagem original
    copy_x1 = max(x, 0)
    copy_y1 = max(y, 0)
    copy_x2 = min(x + w, img_w)
    copy_y2 = min(y + h, img_h)

    # Calcula a região a ser copiada para a nova imagem
    new_x1 = max(0, -x)
    new_y1 = max(0, -y)
    new_x2 = new_x1 + (copy_x2 - copy_x1)
    new_y2 = new_y1 + (copy_y2 - copy_y1)

    # Copia a região válida da imagem original para a nova imagem
    new_img[new_y1:new_y2, new_x1:new_x2] = img[copy_y1:copy_y2, copy_x1:copy_x2]

    return new_img


def apply_blur(img: np.ndarray, ksize: int = 3, **kwargs: Any) -> np.ndarray:
    """
    Aplica um filtro de desfoque Gaussiano à imagem.

    Args:
        img (np.ndarray): Imagem de entrada.
        ksize (int, optional): Tamanho do kernel usado no desfoque, que deve ser ímpar. Default é 3.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem desfocada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> blurred_img = apply_blur(img, ksize=5)
    """
    if ksize % 2 == 0:
        ksize += 1
    return cv2.GaussianBlur(img, (ksize, ksize), 0)


def apply_sharpening(img: np.ndarray, **kwargs: Any) -> np.ndarray:
    """
    Aplica um filtro de sharpening à imagem.

    Args:
        img (np.ndarray): Imagem de entrada.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com sharpening aplicado.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> sharpened_img = apply_sharpening(img)
    """
    # Define o kernel de sharpening
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)

    # Aplica o kernel à imagem
    sharpened_img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
    return sharpened_img


def apply_brightness(
    img: np.ndarray, adjustment: float = 0.0, **kwargs: Any
) -> np.ndarray:
    """
    Ajusta o brilho da imagem.

    Args:
        img (np.ndarray): Imagem de entrada.
        adjustment (float, optional): Valor de ajuste do brilho, positivo para aumentar e negativo para diminuir.
            Default é 0.0.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com brilho ajustado.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> brightened_img = apply_brightness(img, adjustment=50)
    """
    return cv2.convertScaleAbs(img, alpha=1, beta=adjustment)


def apply_contrast(img: np.ndarray, **kwargs: Any) -> np.ndarray:
    """
    Melhora o contraste da imagem usando CLAHE (Contrast Limited Adaptive Histogram Equalization).

    Args:
        img (np.ndarray): Imagem de entrada.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com contraste melhorado.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> contrasted_img = apply_contrast(img)
    """
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_img)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    new_l = clahe.apply(l)
    return cv2.cvtColor(cv2.merge((new_l, a, b)), cv2.COLOR_LAB2BGR)


def apply_exposure(
    img: np.ndarray, adjustment: float = 1.0, **kwargs: Any
) -> np.ndarray:
    """
    Ajusta a exposição da imagem, modificando a escala dos valores de pixel.

    Args:
        img (np.ndarray): Imagem de entrada.
        adjustment (float, optional): Fator de ajuste da exposição. Default é 1.0.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com exposição ajustada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> exposed_img = apply_exposure(img, adjustment=1.5)
    """
    # Aplicando a exposição usando cv2.convertScaleAbs
    img_exposed = cv2.convertScaleAbs(img, alpha=adjustment, beta=0)

    return img_exposed


def apply_grayscale(img: np.ndarray, **kwargs: Any) -> np.ndarray:
    """
    Converte uma imagem colorida para escala de cinza.

    Args:
        img (np.ndarray): Imagem de entrada.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem em escala de cinza.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> gray_img = apply_grayscale(img)
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    colored_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return colored_img


def apply_advanced_grayscale(
    img: np.ndarray,
    rWeight: float = 0.3,
    gWeight: float = 0.59,
    bWeight: float = 0.11,
    **kwargs: Any
) -> np.ndarray:
    """
    Converte a imagem para escala de cinza usando pesos personalizados para os canais de cor.

    Args:
        img (np.ndarray): Imagem de entrada.
        rWeight (float, optional): Peso aplicado ao canal vermelho. Default é 0.3.
        gWeight (float, optional): Peso aplicado ao canal verde. Default é 0.59.
        bWeight (float, optional): Peso aplicado ao canal azul. Default é 0.11.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem convertida para escala de cinza avançada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> adv_gray_img = apply_advanced_grayscale(img, rWeight=0.5, gWeight=0.4, bWeight=0.1)
    """
    # Converter de BGR para RGB, pois OpenCV usa BGR por padrão
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Separar os canais de cores (agora no formato RGB)
    r, g, b = cv2.split(img_rgb)

    # Converter os canais para float32 para operações precisas
    r = r.astype(np.float32)
    g = g.astype(np.float32)
    b = b.astype(np.float32)

    # Aplicar os pesos
    weighted_sum = r * rWeight + g * gWeight + b * bWeight

    # Normalizar os valores para o intervalo 0-255
    normalized_img = cv2.normalize(weighted_sum, None, 0, 255, cv2.NORM_MINMAX)

    # Converter de volta para uint8
    gray = normalized_img.astype(np.uint8)
    colored_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    return colored_img


def apply_edge_detection(img: np.ndarray, **kwargs: Any) -> np.ndarray:
    """
    Detecta as bordas na imagem usando o algoritmo de Canny.

    Args:
        img (np.ndarray): Imagem de entrada em escala de cinza.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com bordas detectadas.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> edges = apply_edge_detection(img)
    """
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.Canny(gray_img, 50, 150)
    colored_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return colored_img


def apply_histogram_equalization(
    img: np.ndarray, clipLimit: float = 2.0, **kwargs: Any
) -> np.ndarray:
    """
    Aplica a equalização do histograma com o uso de CLAHE.

    Args:
        img (np.ndarray): Imagem de entrada.
        clipLimit (float, optional): Limite de corte para o CLAHE. Default é 2.0.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com equalização de histograma aplicada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> equalized_img = apply_histogram_equalization(img, clipLimit=2.0)
    """
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_img)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(8, 8))
    new_l = clahe.apply(l)
    return cv2.cvtColor(cv2.merge((new_l, a, b)), cv2.COLOR_LAB2BGR)


def apply_normalization(
    img: np.ndarray, alpha: int = 0, beta: int = 255, **kwargs: Any
) -> np.ndarray:
    """
    Normaliza a imagem para os valores de pixel entre alpha e beta.

    Args:
        img (np.ndarray): Imagem de entrada.
        alpha (int, optional): Valor mínimo do intervalo de normalização. Default é 0.
        beta (int, optional): Valor máximo do intervalo de normalização. Default é 255.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem normalizada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> normalized_img = apply_normalization(img, alpha=0, beta=255)
    """
    return cv2.normalize(img, None, alpha, beta, cv2.NORM_MINMAX)


def apply_color_segmentation(
    img: np.ndarray,
    lowerBound: Tuple[int, int, int] = (0, 0, 0),
    upperBound: Tuple[int, int, int] = (255, 255, 255),
    **kwargs: Any
) -> np.ndarray:
    """
    Aplica a segmentação de cores com base nos limites especificados.

    Args:
        img (np.ndarray): Imagem de entrada.
        lowerBound (Tuple[int, int, int], optional): Limite inferior da segmentação de cores. Default é (0, 0, 0).
        upperBound (Tuple[int, int, int], optional): Limite superior da segmentação de cores. Default é (255, 255, 255).
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem segmentada com as cores dentro dos limites especificados.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> segmented_img = apply_color_segmentation(img, lowerBound=(50, 50, 50), upperBound=(200, 200, 200))
    """
    # Converter a imagem de BGR para HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Criação das máscaras de limite
    lower = np.array(lowerBound, dtype=np.uint8)
    upper = np.array(upperBound, dtype=np.uint8)

    # Aplicação da máscara para segmentação de cor
    mask = cv2.inRange(hsv, lower, upper)

    # Aplicar a máscara à imagem original
    result = cv2.bitwise_and(img, img, mask=mask)

    return result


def apply_rotation(img: np.ndarray, angle: float = 0, **kwargs: Any) -> np.ndarray:
    """
    Rotaciona a imagem com base no ângulo fornecido.

    Args:
        img (np.ndarray): Imagem de entrada.
        angle (float, optional): Ângulo de rotação em graus. Default é 0.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem rotacionada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> rotated_img = apply_rotation(img, angle=90)
    """
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(img, rotation_matrix, (w, h))


def apply_perspective_distortion(
    img: np.ndarray, preset: str = "none", intensity: float = 0, **kwargs: Any
) -> np.ndarray:
    """
    Aplica distorção de perspectiva com base no preset e intensidade fornecidos.

    Args:
        img (np.ndarray): Imagem de entrada.
        preset (str, optional): Tipo de distorção a ser aplicada. Default é "none".
        intensity (float, optional): Intensidade da distorção. Default é 0.
        **kwargs: Argumentos adicionais (não utilizados aqui).

    Returns:
        np.ndarray: Imagem com distorção de perspectiva aplicada.

    Examples:
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> distorted_img = apply_perspective_distortion(img, preset='expandTopLeft', intensity=10)
    """
    h, w = img.shape[:2]
    basePoints = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

    if preset == "expandTopLeft":
        dstPoints = np.float32([[-intensity, -intensity], [w, 0], [0, h], [w, h]])
    elif preset == "expandTopRight":
        dstPoints = np.float32([[0, 0], [w + intensity, -intensity], [0, h], [w, h]])
    elif preset == "expandBottomLeft":
        dstPoints = np.float32([[0, 0], [w, 0], [-intensity, h + intensity], [w, h]])
    elif preset == "expandBottomRight":
        dstPoints = np.float32([[0, 0], [w, 0], [0, h], [w + intensity, h + intensity]])
    elif preset == "compressTopLeft":
        dstPoints = np.float32([[intensity, intensity], [w, 0], [0, h], [w, h]])
    elif preset == "compressTopRight":
        dstPoints = np.float32([[0, 0], [w - intensity, intensity], [0, h], [w, h]])
    elif preset == "compressBottomLeft":
        dstPoints = np.float32([[0, 0], [w, 0], [intensity, h - intensity], [w, h]])
    elif preset == "compressBottomRight":
        dstPoints = np.float32([[0, 0], [w, 0], [0, h], [w - intensity, h - intensity]])
    elif preset == "expandHorizontally":
        dstPoints = np.float32(
            [[-intensity, 0], [w + intensity, 0], [-intensity, h], [w + intensity, h]]
        )
    elif preset == "compressHorizontally":
        dstPoints = np.float32(
            [[intensity, 0], [w - intensity, 0], [intensity, h], [w - intensity, h]]
        )
    elif preset == "expandVertically":
        dstPoints = np.float32(
            [[0, -intensity], [w, -intensity], [0, h + intensity], [w, h + intensity]]
        )
    elif preset == "compressVertically":
        dstPoints = np.float32(
            [[0, intensity], [w, intensity], [0, h - intensity], [w, h - intensity]]
        )
    else:
        dstPoints = basePoints

    perspective_matrix = cv2.getPerspectiveTransform(basePoints, dstPoints)
    return cv2.warpPerspective(img, perspective_matrix, (w, h))


filter_functions: Dict[FilterType, Callable[[np.ndarray, Any], np.ndarray]] = {
    FilterType.crop: apply_crop,
    FilterType.blur: apply_blur,
    FilterType.sharpening: apply_sharpening,
    FilterType.brightness: apply_brightness,
    FilterType.contrast: apply_contrast,
    FilterType.exposure: apply_exposure,
    FilterType.grayscale: apply_grayscale,
    FilterType.advanced_grayscale: apply_advanced_grayscale,
    FilterType.edge_detection: apply_edge_detection,
    FilterType.histogram_equalization: apply_histogram_equalization,
    FilterType.normalization: apply_normalization,
    FilterType.color_segmentation: apply_color_segmentation,
    FilterType.rotation: apply_rotation,
    FilterType.perspective_distortion: apply_perspective_distortion,
}


def process_image_with_filters(img: np.ndarray, filter_specs: Any) -> np.ndarray:
    """
    Processa uma imagem aplicando uma série de filtros especificados.

    Args:
        img (np.ndarray): Imagem de entrada.
        filter_specs (Any): Especificações dos filtros a serem aplicados.

    Returns:
        np.ndarray: Imagem processada com os filtros aplicados.

    Examples:
        >>> from app.backend.models.ImageFilter import FilterType, FilterSpec  # Import necessário
        >>> img = cv2.imread('app/tests/resources/images/sample.jpg')
        >>> filters = [FilterSpec(filter_type=FilterType.blur, ksize=5)]
        >>> processed_img = process_image_with_filters(img, filters)
    """
    img = resize_image(img)

    for filter_spec in filter_specs:
        func = filter_functions.get(
            filter_spec.filter_type
        )  # Usando a notação de atributo
        if func:
            # Usando model_dump para obter os atributos como dicionário, excluindo filter_type
            img = func(img, **filter_spec.model_dump(exclude={"filter_type"}))

    return img
