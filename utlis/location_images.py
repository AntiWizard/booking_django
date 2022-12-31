def get_hotel_images_upload_location(instance, filename):
    name = instance.gallery.name
    return 'hotel/{}/{}'.format(name, filename)
