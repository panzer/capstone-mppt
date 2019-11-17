import array


def byte_string(byte_data):
    return ' '.join('{:02X}'.format(b) for b in byte_data)


def bytes_from_list(byte_data):
    return array.array('B', byte_data).tobytes()
