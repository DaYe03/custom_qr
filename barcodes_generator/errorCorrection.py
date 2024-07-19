class ErrorCorrection:
    def __init__(self, ):
        self.prim = 2
        self.exp = 8
        self.irreducible_poly=285
        self.size = self.prim ** self.exp
        self.LOG = bytearray(self.size)
        self.EXP = bytearray(self.size)
        self._generate_tables()  # TODO: precompute all the tables (cache)
    
    def _generate_tables(self):
        value = 1
        for i in range(self.size - 1):  # Iterate over the range of the field size
            self.EXP[i] = value
            self.LOG[value] = i

            # Multiply `value` by 2 in GF(2^exp) field
            value <<= 1
            # Reduce `value` modulo irreducible polynomial if necessary
            if value >= self.size:
                value ^= self.irreducible_poly

        # Special case for `value = 0`
        self.LOG[0] = 0
        self.EXP[self.size - 1] = 1  # EXP[255] = 1 for GF(2^8)

    # in GF(2^n) the addition/sottraction is the XOR operation -> a = -a
    def add(self, a, b):
        if a > self.size or b > self.size:
            raise ValueError("The value is out of the field")
        return a ^ b
    
    def mul(self,a,b):
        if a == 0 or b == 0:
            return 0
        return self.EXP[(self.LOG[a] + self.LOG[b]) % 255]
    
    def div(self,a,b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        if a == 0:
            return 0
        return self.EXP[(self.LOG[a] + (255 - self.LOG[b])) % 255]
    
    def poly_mul(self, poly1, poly2):
        len1 = len(poly1)
        len2 = len(poly2)
        coeffs = [0] * (len1 + len2 - 1)
        
        for i in range(len1):
            for j in range(len2):
                coeffs[i + j] ^= self.mul(poly1[i], poly2[j])

        return coeffs
    
    def poly_rest(self, dividend, divisor):
        rest = list(dividend)
        while len(rest) >= len(divisor):
            if rest[0] != 0:
                factor = self.div(rest[0], divisor[0])
                subtr = self.poly_mul([factor] + [0] * (len(rest) - len(divisor)), divisor)
                rest = [rest[i] ^ subtr[i] for i in range(len(rest))]
            rest.pop(0)
        return rest
    
    # TODO: precompute all the generator polynomials (cache)
    def get_generator_poly(self, degree):
        last_poly = [1]

        for _ in range(degree):
            last_poly = self.poly_mul(last_poly, [1, self.EXP[_]])

        return last_poly
    
    def getEDC(self, data, codewords):
        degree = codewords - len(data)
        messagePoly = bytearray(codewords)
        messagePoly[:len(data)] = data
        generatorPoly = self.get_generator_poly(degree)
        remainder = self.poly_rest(messagePoly, generatorPoly)
        return list(remainder)

