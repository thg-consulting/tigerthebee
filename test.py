class Foo(SomeObjects):
    def bar(self, x=[], y: Union[int, None] = None):
        x.append(1)
        for _ in range(3):
            try:
                super(bla, bla).foo_baz()
            except Exception:
                print("An exception")
            except AttributeError:
                print("An attribute error")
            finally:
                continue

        for a in x:
            yield a

        for a in range(len(x)):
            print(a, "=>", x[a])
