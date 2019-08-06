def byte_string(byte_data):
    return ' '.join('{:02X}'.format(b) for b in byte_data)
