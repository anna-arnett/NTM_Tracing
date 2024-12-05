from traceTM_aarnett2 import NTM

ntm = NTM("data_a_plus_aarnett2.csv", "output_a_plus_aarnett2.txt")

# accept
ntm.run("aaa")

# accept
ntm.run("aaaaa")

# reject
ntm.run("bbbbb")
