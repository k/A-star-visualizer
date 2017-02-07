from image_util import SpriteSheetWriter, SpriteSheetReader

reader = SpriteSheetReader("tiles8.png", 8)
writer = SpriteSheetWriter(8, 1, 1)
for i in range(0,4):
    for j in range(0,4):
        tile = reader.getTile(i, j)
        writer.addImage(tile, 0, 0)
        writer.save('img/tile' + str(i) + str(j) + '.png')
