from PIL import Image
import io


def compress_image_v1(image, quality=50):
    image = Image.open(image)
    output_io = io.BytesIO()
    image = image.convert("RGB")
    image.save(output_io, format="JPEG", quality=quality)

    return io.BytesIO(output_io.getvalue())


def compress_image_v2(image, dim=(1000, 1000), quality=50):
    image = Image.open(image)

    resized_img = image.resize(dim, Image.Resampling.LANCZOS)
    output_io = io.BytesIO()
    resized_img = resized_img.convert("RGB")
    resized_img.save(output_io, format="JPEG", quality=quality)

    return io.BytesIO(output_io.getvalue())
