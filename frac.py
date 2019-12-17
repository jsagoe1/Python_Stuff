def factors(n):
    """Returns a list of the factors of n"""
    if(n < 0):  # Handling negative numbers
        n /= -1
    return [i for i in range(1, n + 1) if n % i == 0]


class Frac:
    """Fraction class to represent fractions"""

    def __init__(self, x, y=1):

        # Simplify fraction on initialization
        num_factors = factors(x)
        denom_factors = factors(y)
        hcf = max(set(num_factors) & set(denom_factors))
        self.num, self.denom = int(x/hcf), int(y/hcf)

        if self.denom < 0:
            self.denom = abs(self.denom)
            self.num = -1 * self.num

        elif self.denom == 0:
            raise ZeroDivisionError

    def __repr__(self):
        return "{}/{}".format(self.num, self.denom)

    def __str__(self):
        return self.__repr__()

    def simplify(self):
        """Returns a simplified fraction with num and denom reduced"""

        if self.num % self.denom == 0:
            return int(self.num / self.denom)

        else:
            num_factors = factors(self.num)
            denom_factors = factors(self.denom)
            hcf = max(set(num_factors) & set(denom_factors))
            return Frac(int(self.num / hcf), int(self.denom / hcf))

    def __add__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        top = (self.num * other.denom) + (other.num * self.denom)
        bottom = self.denom * other.denom
        return Frac(top, bottom).simplify()

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        top = (self.num * other.denom) - (other.num * self.denom)
        bottom = self.denom * other.denom
        return Frac(top, bottom).simplify()

    def __rsub__(self, other):
        return Frac(other) - self

    def __mul__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return Frac((self.num * other.num), (self.denom * other.denom)).simplify()

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return Frac((self.num * other.denom), (self.denom * other.num)).simplify()

    def __rtruediv__(self, other):
        return Frac(other) / self

    def __float__(self):
        return float(self.num / self.denom)

    def __int__(self):
        return int(self.num / self.denom)

    def __gt__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) > 0

    def __ge__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) >= 0

    def __lt__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) < 0

    def __le__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) <= 0

    def __eq__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) == 0

    def __ne__(self, other):
        if not isinstance(other, Frac):
            other = Frac(other)
        return int(self-other) != 0

    def __bool__(self):
        return self.num != 0


frac1 = Frac(4, 3)
frac2 = Frac(3, 4)
frac3 = Frac(18, 15)
print(1 / frac3)
print(frac3.simplify())
print(frac1 / frac2)
print(float(frac1 / frac2))
print(int(frac1 / frac2))
