from pydaisi import Daisi
import time

# start = time.time()
# md = Daisi("GoogleNews")
# print(md.get_news(query="Apple").value)
# print(time.time() - start)


start = time.time()
with Daisi("GoogleNews") as my_daisi:
    calls = [my_daisi.get_news_(query="Apple") for _ in range(100)]

    print(Daisi.run_parallel(*calls))

print(time.time() - start)