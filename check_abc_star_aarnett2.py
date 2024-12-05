from traceTM_aarnett2 import NTM

ntm = NTM("abc_star.csv", "output_abc_star_aarnett2.txt")

# accept
ntm.run("abc")

# accept
ntm.run("aaaabbbbcccc")

# reject
ntm.run("aabcbcababca")

# reject
ntm.run("cccbbbaaa")