"""
 @file
 @brief This file has code to generate thumbnail images

 """


import openshot


def GenerateThumbnail(file_path, thumb_path, thumbnail_frame, width, height, mask, overlay):
    """Create thumbnail image, and check for rotate metadata (if any)"""

    # Create a clip object and get the reader
    clip = openshot.Clip(file_path)
    reader = clip.Reader()

    # Open reader
    reader.Open()

    # Get the 'rotate' metadata (if any)
    rotate = 0.0
    try:
        if reader.info.metadata.count("rotate"):
            rotate = float(reader.info.metadata.find("rotate").value()[1])
    except:
        pass

    # Save thumbnail image and close readers
    reader.GetFrame(thumbnail_frame).Thumbnail(thumb_path, width, height, mask, overlay, "#000", False, "png", 100, rotate)
    reader.Close()
    clip.Close()
