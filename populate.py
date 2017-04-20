from nested_tree_app.tasks import *

urls = [
    'https://yandex.ru/referats/?t=gyroscope&s=',
    'https://yandex.ru/referats/?t=astronomy&s=',
    'https://yandex.ru/referats/?t=geology&s=',
    'https://yandex.ru/referats/?t=mathematics&s=',
    'https://yandex.ru/referats/?t=physics&s=',
    'https://yandex.ru/referats/?t=chemistry&s='
]

t1 = time.time()

urls3 = grouper(urls, 3)
for chunk in urls3:

    responses = make_request.map(chunk).apply_async().get()
    texts = group(parse_response.s(i) for i in responses)().get()

    job = group(
        ps120.s(texts[0]),
        ps336.s(texts[1]),
        ps336.s(texts[2])
        )
    result = job.apply_async()
    ps = result.get()

    populate_1_2_3_4.delay(ps[0], ps[1], ps[2])

print ("Population script took ", time.time() - t1, " seconds to execute")