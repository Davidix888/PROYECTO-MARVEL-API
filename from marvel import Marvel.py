from marvel import Marvel
marvel = Marvel("77cd9227f30d31a1e8a6e54a7d12658b","184b87f35ab3b8d461ef993c5b782d0001237fea")

characters = marvel.characters

my_char = characters.all(nameStartsWith="Black")["data"]["results"]

for char in my_char:
    print(char["id"],char["name"])
    for comic in char["comics"]["items"]:
        print(comic)
    print("-----------------------------------------------------------")
