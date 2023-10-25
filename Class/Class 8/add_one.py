def add_one(obj: int | list) -> None:
    if not isinstance(obj, int):
        for i, j in enumerate(obj):
            if isinstance(j, int):
                obj[i] += 1
            else:
                add_one(obj[i])


a = [[1, 2], 5, 7]
add_one(a)
print(a)
