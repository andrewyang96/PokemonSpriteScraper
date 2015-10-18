import glob
import os
import re
from PIL import Image

def getAllSprites(directory):
    if not os.path.exists(directory + "/firstframe"):
        os.mkdir(directory + "/firstframe")
    if not os.path.exists(directory + "/transparent"):
        os.mkdir(directory + "/transparent")
    if not os.path.exists(directory + "/compressed"):
        os.mkdir(directory + "/compressed")
    if not os.path.exists(directory + "/grayscale"):
        os.mkdir(directory + "/grayscale")
    if not os.path.exists(directory + "/bw"):
        os.mkdir(directory + "/bw")
    return glob.glob(os.path.join(directory, "sprites", "*.gif"))

def extractFirstFrame(filename, pokemon, directory):
    im = Image.open(filename)
    im.seek(0)
    im.save(os.path.join(directory, "firstframe", pokemon+".gif"))
    # save as PNG with transparent background
    print "Converting to RGBA with white transparent background"
    im = im.convert("RGBA")
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
    im.save(os.path.join(directory, "transparent", pokemon+".png"), format="PNG")
    im.close()

def extractFirstFrameCompressed(pokemon, directory):
    # extract PNGs from <directory>/transparent
    im = Image.open(os.path.join(directory, "transparent", pokemon+".png"))
    width, height = im.size
    im = im.resize((width/6, height/6), Image.ANTIALIAS)
    im.save(os.path.join(directory, "compressed", pokemon+"-"+directory+".png"), format="PNG")
    # then grayscale it
    print "Converting to grayscale"
    pixdata = im.load()
    for y in xrange(im.size[1]):
        for x in xrange(im.size[0]):
            pixdata[x, y] = RGBA2Grayscale(pixdata[x, y])
    im.save(os.path.join(directory, "grayscale", pokemon+"-"+directory+".png"), format="PNG")
    im.close()
    # finally bw silhouette it
    print "Converting to BW"
    im2 = Image.open(os.path.join(directory, "transparent", pokemon+".png"))
    pixdata = im2.load()
    for y in xrange(im2.size[1]):
        for x in xrange(im2.size[0]):
            if pixdata[x, y][-1] != 0:
                pixdata[x, y] = (0, 0, 0, 255)
    im2 = im2.resize((width/4, height/4), Image.NEAREST)
    im2.save(os.path.join(directory, "bw", pokemon+"-"+directory+".png"), format="PNG")
    im2.close()

def RGBA2Grayscale(rgba):
    r, g, b, a = rgba
    l = int(round(r * 299/1000. + g * 587/1000. + b * 114/1000.))
    return (l, l, l, a)

def compressMain():
    # front
    print "Getting all front sprites"
    sprites = getAllSprites("front")
    pokemons = [re.findall("[\\\/].*[\\\/](.*)\.gif", sprite)[0] for sprite in sprites]
    for sprite, pokemon in zip(sprites, pokemons):
        print "Extracting first frame of", pokemon, "front"
        extractFirstFrame(sprite, pokemon, "front")
    for pokemon in pokemons:
        print "Compressing", pokemon, "front"
        extractFirstFrameCompressed(pokemon, "front")

    # front
    print "Getting all back sprites"
    sprites = getAllSprites("back")
    pokemons = [re.findall("[\\\/].*[\\\/](.*)\.gif", sprite)[0] for sprite in sprites]
    for sprite, pokemon in zip(sprites, pokemons):
        print "Extracting first frame of", pokemon, "back"
        extractFirstFrame(sprite, pokemon, "back")
    for pokemon in pokemons:
        print "Compressing", pokemon, "back"
        extractFirstFrameCompressed(pokemon, "back")
    print "Done!"
