from imagekitio import ImageKit

from ..core.config import settings

imagekit = ImageKit(
  private_key=settings.imagekit_private_key.get_secret_value()
)