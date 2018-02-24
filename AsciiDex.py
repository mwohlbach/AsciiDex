from PIL import Image
import io
import urllib.request
import click
import util.AnsiColors

ASCII_CHARS = [ '     ', '?????', '%%%%%', '.....', 'SSSSS', '+++++', '.....', '*****', ':::::', ',,,,,', '@@@@@']

@click.command()
@click.option('-s',is_flag=True,help='Use this flag to make it print out the shiny version of the pokemon')
@click.option('-p',type=click.Path(exists=True),help='You can pass the path to an image you want to print')
@click.option('-lowcolors',is_flag=True,default=False,help="Use this flag if the console you are using doesn't support 256 colors")
@click.argument('pokemon')
def cli(pokemon,s,p,lowcolors):
    """I do something"""

    if(p):
        image = Image.open(p)
    else:
        image = openImageForPokemon(pokemon,s)

    #image = Image.open('/Users/mwohlbach/Desktop/monalisa.jpg')

    convertImageToColoredPixels(image,96,lowcolors)
    #asciiPrintImage(image)

def openImageForPokemon(pkmnNo,shiny):
    pokemonSpriteUrl = getPokemonSpriteUrl(shiny)

    request = urllib.request.Request(pokemonSpriteUrl + pkmnNo + '.png')
    request.add_header('User-Agent', 'AsciiDex')
    file = io.BytesIO(urllib.request.urlopen(request).read())

    image = Image.open(file)

    return image

def getPokemonSpriteUrl(shiny):
    pokemonSpriteUrl = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/'

    if (shiny):
        pokemonSpriteUrl += 'shiny/'

    return pokemonSpriteUrl


def scaleImage(image, newWidth):
    """Resizes an image preserving the aspect ratio.
    """

    (originalWidth, originalHeight) = image.size
    aspectRatio = originalHeight/float(originalWidth)
    newHeight = int(aspectRatio * newWidth)

    return image.resize((newWidth, newHeight))

def convertToGrayscale(image):
    return image.convert('L')

def convertToRGB(image):
    return image.convert('RGB')

def asciiPrintImage(image):
    image = scaleImage(image,96)
    rgbImage = convertToRGB(image)
    rgbImage = removeBorders(rgbImage)
    grayImage = convertToGrayscale(rgbImage)

    width, length = rgbImage.size

    for y in range(length):
        print('\n')
        for x in range(width):
            coloredPixel = rgbImage.getpixel((x,y))
            grayPixel = grayImage.getpixel((x,y))

            util.AnsiColors.printAnsiColor(True,*coloredPixel)
            print(ASCII_CHARS[grayPixel//25],end='')

            #print(pixelsToChars[(y*length)+x],end='')
    print('\u001b[0m')

def mapPixelsToAsciiChars(image, rangeWidth=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixelsInImage = list(image.getdata())
    pixelsToChars = [ASCII_CHARS[pixelValue//rangeWidth] for pixelValue in
            pixelsInImage]
    return "".join(pixelsToChars)

def removeBorders(image):
    """
    Removes the white space around any image and returns the new image.
    """

    width, length = image.size

    topEmptyRowsFound = False
    topEmptyRows = 0
    bottomEmptyRows = 0

    for y in range(length):

        emptyRow = True
        for x in range(width):
            pixel = image.getpixel((x, y))
            if (pixel != (0, 0, 0) and emptyRow):
                emptyRow = False

        if (emptyRow and not topEmptyRowsFound):
            topEmptyRows += 1
        elif (not emptyRow):
            topEmptyRowsFound = True
        elif (emptyRow and topEmptyRowsFound):
            bottomEmptyRows += 1

    leftEmptyColsFound = False
    leftEmptyCols = 0
    rightEmptyCols = 0

    for x in range(width):

        emptyCol = True
        for y in range(length):
            pixel = image.getpixel((x, y))
            if (pixel != (0, 0, 0) and emptyCol):
                emptyCol = False

        if (emptyCol and not leftEmptyColsFound):
            leftEmptyCols += 1
        elif (not emptyCol):
            leftEmptyColsFound = True
        elif (emptyCol and leftEmptyColsFound):
            rightEmptyCols += 1

    totalEmptyCols = leftEmptyCols + rightEmptyCols
    newWidth = width - totalEmptyCols

    totalEmptyRows = topEmptyRows + bottomEmptyRows
    newLength = length - totalEmptyRows

    newImage = image.crop((leftEmptyCols, topEmptyRows, newWidth+leftEmptyCols, newLength+topEmptyRows))

    return newImage

def pixelPrintImage(image,lowcolors):
    """
    Prints out an RGB image with pixels.
    """
    width, length = image.size

    for y in range(length):
        print('\n')
        for x in range(width):
            pixel = image.getpixel((x,y))
            if(pixel != (0,0,0)):
                util.AnsiColors.printAnsiColor(lowcolors,*pixel)
                print('██████',end='')
            else:
                print('      ',end='')
    print('\u001b[0m')


def convertImageToColoredPixels(image, newWidth, lowcolors):

    image = scaleImage(image, newWidth)

    image = convertToRGB(image)

    image = removeBorders(image)

    pixelPrintImage(image,lowcolors)


