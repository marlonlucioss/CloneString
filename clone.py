import sys
import collections
import requests
import json

print ("First File: %s" % str(sys.argv[1]))
print ("Second File: %s" % str(sys.argv[2]))


def _get_character_pairs(text):

    if not hasattr(text, "upper"):
        raise ValueError("Invalid argument")

    results = collections.defaultdict(int)  # default value of 0

    for word in text.upper().split():
        for pair in [word[i]+word[i+1] for i in range(len(word)-1)]:
            results[pair] += 1
    return results

def convertGithubUrl(url):
    convertedUrl = url.replace("/blob", "")
    return convertedUrl.replace("//", "//raw.")

def compare_strings(string1, string2):

    file1 = requests.get(convertGithubUrl(string1))
    file2 = requests.get(convertGithubUrl(string2))

    s1_pairs = _get_character_pairs(file1.text)
    s2_pairs = _get_character_pairs(file2.text)

    s1_size = sum(s1_pairs.values())
    s2_size = sum(s2_pairs.values())

    intersection_count = 0

    # determine the smallest dict to optimise the calculation of the
    # intersection.
    if s1_size < s2_size:
        smaller_dict = s1_pairs
        larger_dict = s2_pairs
    else:
        smaller_dict = s2_pairs
        larger_dict = s1_pairs

    # determine the intersection by counting the subtractions we make from both
    # dicts.
    for pair, smaller_pair_count in smaller_dict.items():
        if pair in larger_dict and larger_dict[pair] > 0:
            if smaller_pair_count < larger_dict[pair]:
                intersection_count += smaller_pair_count
            else:
                intersection_count += larger_dict[pair]
    result = (2.0 * intersection_count) / (s1_size + s2_size)
    
    print result

    return result

compare_strings(sys.argv[1],sys.argv[2])

if __name__ == "__main__":
    import doctest
    doctest.testmod()