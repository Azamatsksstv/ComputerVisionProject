from PIL import Image, ImageOps


def black_and_white_filter(image_path, output_path):
    # Открываем изображение
    image = Image.open(image_path)

    # Преобразуем в черно-белое
    black_and_white_image = ImageOps.grayscale(image)

    # Сохраняем результат
    black_and_white_image.save(output_path)
