from PIL import Image


class __SpriteSheetAbstract(object):
    def __init__(self, tileSize, margin=1):
        self.tileSize = tileSize
        self.margin = margin

    def pos(self, index):
        return (self.tileSize * index) + (self.margin * (index + 1))


class SpriteSheetWriter(__SpriteSheetAbstract):
    def __init__(self, tileSize, sizex, sizey,  margin=1):
        super(SpriteSheetWriter, self).__init__(tileSize, margin=margin)
        self.spriteSheetSize = (sizex*tileSize + sizex*margin, sizey*tileSize + sizey*margin)
        self.spritesheet = Image.new("RGBA", (self.spriteSheetSize[0], self.spriteSheetSize[1]), (0, 0, 0, 0))
        self.tileX = 0
        self.tileY = 0

    def getCurPos(self):
        posX = self.pos(self.tileX)
        posY = self.pos(self.tileY)
        if (posX + self.tileSize > self.spriteSheetSize[0]):
            self.tileX = 0
            self.tileY = self.tileY + 1
            self.getCurPos()
        if (posY + self.tileSize > self.spriteSheetSize[1]):
            raise Exception('Image does not fit within spritesheet!')

    def addImage(self, image, tileX, tileY):
        posX = self.pos(tileX)
        posY = self.pos(tileY)
        destBox = (posX, posY, posX + image.size[0], posY + image.size[1])
        self.spritesheet.paste(image, destBox)

    def show(self):
        self.spritesheet.show()

    def save(self, fname):
        self.spritesheet.save(fname, format="png")


class SpriteSheetReader(__SpriteSheetAbstract):
    def __init__(self, imageName, tileSize, margin=1):
        super(SpriteSheetReader, self).__init__(tileSize, margin=margin)
        self.spritesheet = Image.open(imageName)

    def getTile(self, tileX, tileY):
        posX = self.pos(tileX)
        posY = self.pos(tileY)
        box = (posX, posY, posX + self.tileSize, posY + self.tileSize)
        return self.spritesheet.crop(box)


def split_up_into_tiles():
    for i in range(0, 4):
        for j in range(0, 4):
            reader = SpriteSheetReader("tiles.png", 32)
            writer = SpriteSheetWriter(32, 1, 1)
            image = reader.getTile(i, j)
            writer.addImage(image, 0, 0)
            writer.save('img/tile' + str(i) + str(j) + '.png')
