from PIL import Image
import io
import urllib.request
import click

ASCII_CHARS = [ '     ', '?????', '%%%%%', '.....', 'SSSSS', '+++++', '.....', '*****', ':::::', ',,,,,', '@@@@@']

colorMap = {}
#colorMap['\u001b[0m'] = (196,196,196) #reset
colorMap['\u001b[30m'] = (0,0,0) #black
colorMap['\u001b[31m'] = (208,28,7) #red
colorMap['\u001b[32m'] = (168,197,16) #green
colorMap['\u001b[33m'] = (190,196,45) #yellow
colorMap['\u001b[34m'] = (1,46,201) #blue
colorMap['\u001b[35m'] = (202,58,190) #magenta
colorMap['\u001b[36m'] = (3,199,194) #cyan
#colorMap['\u001b[37m'] = (197,197,197) #white
colorMap['\u001b[30;1m'] = (104,104,104) #bright black
colorMap['\u001b[31;1m'] = (253,111,109) #bright red
colorMap['\u001b[32;1m'] = (105,247,106) #bright green
colorMap['\u001b[33;1m'] = (254,249,116) #bright yellow
colorMap['\u001b[34;1m'] = (106,120,250) #bright blue
colorMap['\u001b[35;1m'] = (255,123,255) #bright magenta
colorMap['\u001b[36;1m'] = (105,247,254) #bright cyan
colorMap['\u001b[37;1m'] = (255,255,255) #bright white

colorMap256 =  { # color look-up table
#    8-bit, RGB hex

# Primary 3-bit (8 colors). Unique representation!
'00': '000000',
'01': '800000',
'02': '008000',
'03': '808000',
'04': '000080',
'05': '800080',
'06': '008080',
'07': 'c0c0c0',

# Equivalent "bright" versions of original 8 colors.
'08': '808080',
'09': 'ff0000',
'10': '00ff00',
'11': 'ffff00',
'12': '0000ff',
'13': 'ff00ff',
'14': '00ffff',
'15': 'ffffff',

# Strictly ascending.
'16': '000000',
'17': '00005f',
'18': '000087',
'19': '0000af',
'20': '0000d7',
'21': '0000ff',
'22': '005f00',
'23': '005f5f',
'24': '005f87',
'25': '005faf',
'26': '005fd7',
'27': '005fff',
'28': '008700',
'29': '00875f',
'30': '008787',
'31': '0087af',
'32': '0087d7',
'33': '0087ff',
'34': '00af00',
'35': '00af5f',
'36': '00af87',
'37': '00afaf',
'38': '00afd7',
'39': '00afff',
'40': '00d700',
'41': '00d75f',
'42': '00d787',
'43': '00d7af',
'44': '00d7d7',
'45': '00d7ff',
'46': '00ff00',
'47': '00ff5f',
'48': '00ff87',
'49': '00ffaf',
'50': '00ffd7',
'51': '00ffff',
'52': '5f0000',
'53': '5f005f',
'54': '5f0087',
'55': '5f00af',
'56': '5f00d7',
'57': '5f00ff',
'58': '5f5f00',
'59': '5f5f5f',
'60': '5f5f87',
'61': '5f5faf',
'62': '5f5fd7',
'63': '5f5fff',
'64': '5f8700',
'65': '5f875f',
'66': '5f8787',
'67': '5f87af',
'68': '5f87d7',
'69': '5f87ff',
'70': '5faf00',
'71': '5faf5f',
'72': '5faf87',
'73': '5fafaf',
'74': '5fafd7',
'75': '5fafff',
'76': '5fd700',
'77': '5fd75f',
'78': '5fd787',
'79': '5fd7af',
'80': '5fd7d7',
'81': '5fd7ff',
'82': '5fff00',
'83': '5fff5f',
'84': '5fff87',
'85': '5fffaf',
'86': '5fffd7',
'87': '5fffff',
'88': '870000',
'89': '87005f',
'90': '870087',
'91': '8700af',
'92': '8700d7',
'93': '8700ff',
'94': '875f00',
'95': '875f5f',
'96': '875f87',
'97': '875faf',
'98': '875fd7',
'99': '875fff',
'100': '878700',
'101': '87875f',
'102': '878787',
'103': '8787af',
'104': '8787d7',
'105': '8787ff',
'106': '87af00',
'107': '87af5f',
'108': '87af87',
'109': '87afaf',
'110': '87afd7',
'111': '87afff',
'112': '87d700',
'113': '87d75f',
'114': '87d787',
'115': '87d7af',
'116': '87d7d7',
'117': '87d7ff',
'118': '87ff00',
'119': '87ff5f',
'120': '87ff87',
'121': '87ffaf',
'122': '87ffd7',
'123': '87ffff',
'124': 'af0000',
'125': 'af005f',
'126': 'af0087',
'127': 'af00af',
'128': 'af00d7',
'129': 'af00ff',
'130': 'af5f00',
'131': 'af5f5f',
'132': 'af5f87',
'133': 'af5faf',
'134': 'af5fd7',
'135': 'af5fff',
'136': 'af8700',
'137': 'af875f',
'138': 'af8787',
'139': 'af87af',
'140': 'af87d7',
'141': 'af87ff',
'142': 'afaf00',
'143': 'afaf5f',
'144': 'afaf87',
'145': 'afafaf',
'146': 'afafd7',
'147': 'afafff',
'148': 'afd700',
'149': 'afd75f',
'150': 'afd787',
'151': 'afd7af',
'152': 'afd7d7',
'153': 'afd7ff',
'154': 'afff00',
'155': 'afff5f',
'156': 'afff87',
'157': 'afffaf',
'158': 'afffd7',
'159': 'afffff',
'160': 'd70000',
'161': 'd7005f',
'162': 'd70087',
'163': 'd700af',
'164': 'd700d7',
'165': 'd700ff',
'166': 'd75f00',
'167': 'd75f5f',
'168': 'd75f87',
'169': 'd75faf',
'170': 'd75fd7',
'171': 'd75fff',
'172': 'd78700',
'173': 'd7875f',
'174': 'd78787',
'175': 'd787af',
'176': 'd787d7',
'177': 'd787ff',
'178': 'd7af00',
'179': 'd7af5f',
'180': 'd7af87',
'181': 'd7afaf',
'182': 'd7afd7',
'183': 'd7afff',
'184': 'd7d700',
'185': 'd7d75f',
'186': 'd7d787',
'187': 'd7d7af',
'188': 'd7d7d7',
'189': 'd7d7ff',
'190': 'd7ff00',
'191': 'd7ff5f',
'192': 'd7ff87',
'193': 'd7ffaf',
'194': 'd7ffd7',
'195': 'd7ffff',
'196': 'ff0000',
'197': 'ff005f',
'198': 'ff0087',
'199': 'ff00af',
'200': 'ff00d7',
'201': 'ff00ff',
'202': 'ff5f00',
'203': 'ff5f5f',
'204': 'ff5f87',
'205': 'ff5faf',
'206': 'ff5fd7',
'207': 'ff5fff',
'208': 'ff8700',
'209': 'ff875f',
'210': 'ff8787',
'211': 'ff87af',
'212': 'ff87d7',
'213': 'ff87ff',
'214': 'ffaf00',
'215': 'ffaf5f',
'216': 'ffaf87',
'217': 'ffafaf',
'218': 'ffafd7',
'219': 'ffafff',
'220': 'ffd700',
'221': 'ffd75f',
'222': 'ffd787',
'223': 'ffd7af',
'224': 'ffd7d7',
'225': 'ffd7ff',
'226': 'ffff00',
'227': 'ffff5f',
'228': 'ffff87',
'229': 'ffffaf',
'230': 'ffffd7',
'231': 'ffffff',

# Gray-scale range.
'232': '080808',
'233': '121212',
'234': '1c1c1c',
'235': '262626',
'236': '303030',
'237': '3a3a3a',
'238': '444444',
'239': '4e4e4e',
'240': '585858',
'241': '626262',
'242': '6c6c6c',
'243': '767676',
'244': '808080',
'245': '8a8a8a',
'246': '949494',
'247': '9e9e9e',
'248': 'a8a8a8',
'249': 'b2b2b2',
'250': 'bcbcbc',
'251': 'c6c6c6',
'252': 'd0d0d0',
'253': 'dadada',
'254': 'e4e4e4',
'255': 'eeeeee'
}

@click.command()
@click.option('-s',is_flag=True,help='Use this flag to make it print out the shiny version of the pokemon')
@click.argument('pokemon')
def cli(pokemon,s):
    """I do something"""

    image = openImageForPokemon(pokemon,s)

    #image = Image.open('/Users/mwohlbach/Desktop/monalisa.jpg')

    convertImageToColoredPixels(image,96)
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

            setAnsiColor256(*coloredPixel)
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

def pixelPrintImage(image):
    """
    Prints out an RGB image with pixels.
    """
    width, length = image.size

    for y in range(length):
        print('\n')
        for x in range(width):
            pixel = image.getpixel((x,y))
            if(pixel != (0,0,0)):
                setAnsiColor256(*pixel)
                print('██████',end='')
            else:
                print('      ',end='')
    print('\u001b[0m')


def convertImageToColoredPixels(image, newWidth):

    image = scaleImage(image, newWidth)

    image = convertToRGB(image)

    image = removeBorders(image)

    pixelPrintImage(image)

def setAnsiColor(R, G, B):
    mindiff = None
    for d in colorMap:
        r, g, b = (colorMap[d])
        diff = abs(R - r) * 256 + abs(G - g) * 256 + abs(B - b) * 256
        if mindiff is None or diff < mindiff:
            mindiff = diff
            mincolorname = d
    print('\u001b[0m',mincolorname,end='')

def setAnsiColor256(R, G, B):
    mindiff = None
    for d in colorMap256:
        r, g, b = hexToRGB(colorMap256[d])
        diff = abs(R - r) * 256 + abs(G - g) * 256 + abs(B - b) * 256
        if mindiff is None or diff < mindiff:
            mindiff = diff
            mincolorname = d
    print('\u001b[0m'  +  '\u001b[38;5;' + mincolorname + 'm', end='')

def hexToRGB(hex):
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))






