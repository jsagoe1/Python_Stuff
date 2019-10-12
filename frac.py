
def factors(n):
    return [i for i in range(1,n+1) if n % i == 0] 

class frac:
    def __init__(self, x, y):
        self.num = x
        self.denom  = y

    def __repr__(self):
        return "{}/{}".format(self.num, self.denom)

    def __str__(self):
        return self.__repr__()

    def simplify(self):
        if self.num % self.denom == 0:
            return int(self.num / self.denom)
        
        else:
            num_factors = factors(self.num)
            denom_factors = factors(self.denom)
            highest_fact = max(set(num_factors) & set(denom_factors))
            return frac(self.num / highest_fact, self.denom / highest_fact)
    
    def __add__(self, other):
        top     = (self.num*other.denom) + (other.num*self.denom)
        bottom  = self.denom*other.denom
        return frac(top, bottom).simplify()
        
    def __mul__(self, other):
        return frac((self.num*other.num) , (self.denom * other.denom)).simplify()
    
    def __div__(self, other):
        return frac((self.num*other.denom) , (self.denom * other.num)).simplify()
    
    def to_float(self):
        return float(self.num) / float(self.denom)


frac1 = frac(4,3)
frac2 = frac(3,4)
frac3 = frac(18,15)
print(frac3)
print(frac3.simplify())
print(frac1/frac2)
print((frac1/frac2).to_float())


