class A:
    a = 7
    b = 3
    @staticmethod
    def seta(a):
        a = a

a = A()
a.seta(78)

print(A.a)