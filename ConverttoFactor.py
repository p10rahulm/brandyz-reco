import numpy as np

def get_encoder_dict(column):
    encodings = {}
    unique_col = np.unique(column)
    code = 0;
    for num in unique_col:
        encodings[num] = code;
        code+=1;
    return (encodings,code)


def encode_column(column,encodings):
    new_column = np.zeros(len(column),dtype=np.int)
    for i in range(len(column)):
        new_column[i] = encodings[column[i]]
    return new_column


def convert_to_factor(column):
    (encoded_dict,num_unique) = get_encoder_dict(column)
    new_column = encode_column(column,encoded_dict)
    return (new_column,encoded_dict,num_unique)


if __name__ == "__main__":
    a = [1,2,3,5,7,8,1]
    (new_col,encoded_dict,num_unique) = convert_to_factor(a)
    print(new_col, " ",num_unique)
    print(encoded_dict)
    a = ["hi", "hello", "my", "name", "is", "Rahul", "hi"]
    (new_col, encoded_dict, num_unique) = convert_to_factor(a)
    print(new_col, " ", num_unique)
    print(encoded_dict)

