import os
import requests
import re

def downloadSprites():
    if not os.path.exists("front"):
        os.makedirs("front/sprites/")
    if not os.path.exists("back"):
        os.makedirs("back/sprites/")

    # front sprites
    print "Getting front sprites page"
    page = requests.get("http://play.pokemonshowdown.com/sprites/xyani/")
    print "Parsing available sprites"
    pokemons = re.findall(r'<a href=".*">(.*)\.gif</a>', page.text)
    for pokemon in pokemons:
        print "Downloading", pokemon, "front"
        imgurl = "http://play.pokemonshowdown.com/sprites/xyani/{0}.gif".format(pokemon)
        downloadPokemon(pokemon, "front", imgurl)

    # back sprites
    print "Getting back sprites page"
    page = requests.get("http://play.pokemonshowdown.com/sprites/xyani-back/")
    print "Parsing available sprites"
    pokemons = re.findall(r'<a href=".*">(.*)\.gif</a>', page.text)
    for pokemon in pokemons:
        print "Downloading", pokemon, "back"
        imgurl = "http://play.pokemonshowdown.com/sprites/xyani-back/{0}.gif".format(pokemon)
        downloadPokemon(pokemon, "back", imgurl)

def downloadPokemon(pokemon, directory, imgurl):
    img = requests.get(imgurl)
    with open(os.path.join(directory, "sprites", pokemon+".gif"), "wb") as f:
        f.write(img.content)

if __name__ == "__main__":
    downloadSprites()
    print "Done!"
