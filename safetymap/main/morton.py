# morton.py

class Morton:
    @staticmethod
    def encode2D(x, y):
        # Implement Morton encoding for 2D coordinates
        x = (x | (x << 16)) & 0x0000FFFF0000FFFF
        x = (x | (x << 8)) & 0x00FF00FF00FF00FF
        x = (x | (x << 4)) & 0x0F0F0F0F0F0F0F0F
        x = (x | (x << 2)) & 0x3333333333333333
        x = (x | (x << 1)) & 0x5555555555555555

        y = (y | (y << 16)) & 0x0000FFFF0000FFFF
        y = (y | (y << 8)) & 0x00FF00FF00FF00FF
        y = (y | (y << 4)) & 0x0F0F0F0F0F0F0F0F
        y = (y | (y << 2)) & 0x3333333333333333
        y = (y | (y << 1)) & 0x5555555555555555

        return x | (y << 1)

    @staticmethod
    def decode2D(code):
        # Implement Morton decoding for 2D coordinates
        x = code & 0x5555555555555555
        x = (x ^ (x >> 1)) & 0x3333333333333333
        x = (x ^ (x >> 2)) & 0x0F0F0F0F0F0F0F0F
        x = (x ^ (x >> 4)) & 0x00FF00FF00FF00FF
        x = (x ^ (x >> 8)) & 0x0000FFFF0000FFFF
        x = (x ^ (x >> 16)) & 0x00000000FFFFFFFF

        y = (code >> 1) & 0x5555555555555555
        y = (y ^ (y >> 1)) & 0x3333333333333333
        y = (y ^ (y >> 2)) & 0x0F0F0F0F0F0F0F0F
        y = (y ^ (y >> 4)) & 0x00FF00FF00FF00FF
        y = (y ^ (y >> 8)) & 0x0000FFFF0000FFFF
        y = (y ^ (y >> 16)) & 0x00000000FFFFFFFF

        return x, y
