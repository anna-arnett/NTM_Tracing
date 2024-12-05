from traceTM_aarnett2 import NTM

ntm = NTM("data_abc_star_aarnett2.csv", "output_abc_star_aarnett2.txt")

# accept
ntm.run("abc")

# accept
ntm.run("aaaabbbbcccc")

# reject
ntm.run("aabcbcababca")

# reject
ntm.run("cccbbbaaa")
