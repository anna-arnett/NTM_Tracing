from traceTM_aarnett2 import NTM

ntm = NTM("data_equal_abcs_aarnett2.csv", "output_equal_abcs_aarnett2.txt")

# accept
ntm.run("abc")

# accept
ntm.run("abcabcabc")

# reject
ntm.run("aaabbbcc")

# reject
ntm.run("aaaaabbbbbbcccc")