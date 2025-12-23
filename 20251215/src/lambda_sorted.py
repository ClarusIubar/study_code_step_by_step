students = [
    ('Alice', 88),
    ('Bob', 95),
    ('Charlie', 75),
]

sorted_by_score = sorted(students,
                         key = lambda x: x[1],
                         reverse = True 
                         )

print(sorted_by_score)