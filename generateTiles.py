from PIL import Image


class __SpriteSheetAbstract(object):
    def __init__(self, tileSize, margin=1):
        self.tileSize = tileSize
        self.margin = margin

    def __pos(self, index):
        return (self.tileSize * index) + (self.margin * (index + 1))


class SpriteSheetWriter(__SpriteSheetAbstract):
    def __init__(self, tileSize, spriteSheetSize, margin=1):
        super(SpriteSheetWriter, self).__init__(tileSize, margin=margin)
        self.spriteSheetSize = spriteSheetSize
        self.spritesheet = Image.new("RGBA", (self.spriteSheetSize, self.spriteSheetSize), (0, 0, 0, 0))
        self.tileX = 0
        self.tileY = 0

    def getCurPos(self):
        posX = self.__pos(self.tileX)
        posY = self.__pos(self.tileY)
        if (posX + self.tileSize > self.spriteSheetSize):
            self.tileX = 0
            self.tileY = self.tileY + 1
            self.getCurPos()
        if (posY + self.tileSize > self.spriteSheetSize):
            raise Exception('Image does not fit within spritesheet!')

    def addImage(self, image, tileX, tileY):
        posX = self.__pos(self.tileX)
        posY = self.__pos(self.tileY)
        destBox = (posX, posY, posX + image.size[0], posY + image.size[1])
        self.spritesheet.paste(image, destBox)
        self.tileX = self.tileX + 1

    def show(self):
        self.spritesheet.show()


class SpriteSheetReader(__SpriteSheetAbstract):
    def __init__(self, imageName, tileSize, margin=1):
        super(SpriteSheetReader, self).__init__(tileSize, margin=margin)
        self.spritesheet = Image.open(imageName)

    def getTile(self, tileX, tileY):
        posX = self.__pos(tileX)
        posY = self.__pos(tileY)
        box = (posX, posY, posX + self.tileSize, posY + self.tileSize)
        return self.spritesheet.crop(box)


reader = SpriteSheetReader("DesertWall.jpg", 32)
writer = SpriteSheetWriter(32, 256)
tile1 = reader.getTile(0, 0)
writer.addImage(tile1, 0, 0)
writer.addImage(tile1, 0, 1)
writer.show()
