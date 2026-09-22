def process(input_string: str) -> str:
    A = 0
    B = 0
    C = 0

    for input_text in input_string.split():
        if int(input_text) > 0:
            A += 1
        elif int(input_text) == 0:
            C += 1
        elif int(input_text) < 0:
            B += 1

    return f"выше нуля: {A}, ниже нуля: {B}, равна нулю: {C}"

input_string = input()
output_string = process(input_string)
print(output_string)