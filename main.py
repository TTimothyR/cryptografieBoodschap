from PIL import Image
import cv2
import numpy as np
import sys
import pygame

def main():
    # Foto omzetten naar binaire tabel, en opslaan voor later, indien er al een andere tabel in staat, zal die overschreven worden.
    tabel = fotoNaarBinair('Foto.png')
    np.savetxt('binaireTabel.txt', tabel, fmt='%d')

    # Random tabel van nullen en eentjes genereren met de zelfde grootte als onze foto, en opslaan voor later gebruik.
    sleutel = np.random.randint(2, size=(150, 150))
    np.savetxt('sleutel.txt', sleutel, fmt='%d')

    # Voor de boodschap beginnen we met een tabel van nullen, we zullen die later bewerken
    boodschap = np.zeros((150, 150), dtype=int)

    for i in range(150):
        for j in range(150):
            # Als 1 van de tabellen een zwart vakje heeft maar niet beide, dan krijg je een zwart vakje
            if tabel[i, j] == 1 and sleutel[i, j] == 0:
                boodschap[i, j] = 0
            elif tabel[i, j] == 0 and sleutel[i, j] == 1:
                boodschap[i, j] = 0

            # Als beide tabellen dezelfde waarden hebben, dan krijg je een wit vakje
            elif tabel[i, j] == 1 and sleutel[i, j] == 1:
                boodschap[i, j] = 1
            elif tabel[i, j] == 0 and sleutel[i, j] == 0:
                boodschap[i, j] = 1
    np.savetxt('boodschap.txt', boodschap, fmt='%d')

    # Sleutel omzetten naar een foto
    sleutel = binairNaarFoto('sleutel.txt', 'Sleutel.png')
    witTransparentMaken("Sleutel.png")
    # Boodschap omzetten naar een foto
    boodschap = binairNaarFoto('boodschap.txt', 'Boodschap.png')
    witTransparentMaken("Boodschap.png")

    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('Cryptografie')
    clock = pygame.time.Clock()

    sleutelLaden = pygame.image.load("Sleutel.png")
    boodschapLaden = pygame.image.load("Boodschap.png")

    boodschapX = 150
    boodschapY = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    boodschapY -= 5
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    boodschapY += 5
        
        screen.fill((255,255,255))
        screen.blit(sleutelLaden, (150, 150))
        screen.blit(boodschapLaden, (boodschapX, boodschapY))

        pygame.display.flip()
        clock.tick(60)




def fotoNaarBinair(imageData, threshold = 128, grootte = (150, 150)):
    img = cv2.imread(imageData, cv2.IMREAD_GRAYSCALE)
    imgVerkleint = cv2.resize(img, grootte)
    _, binaireFoto = cv2.threshold(imgVerkleint, threshold, 255, cv2.THRESH_BINARY)
    binaireTabel = (binaireFoto > 0).astype(int)
    return(binaireTabel)

def binairNaarFoto(bestandNaam, outputNaam):
    # Bestand lezen
    with open(bestandNaam, 'r') as f:
        lines = f.readlines()

    # Lijnen omzetten naar numpy tabel
    data = []
    for line in lines:
        line = line.strip()
        row = []
        for char in line:
            if char == "0":
                row.append(0)
            elif char == "1":
                row.append(255)
        data.append(row)
    data = np.array(data, dtype=np.uint8)

    foto = Image.fromarray(data, mode='L')

    foto.save(outputNaam)

def witTransparentMaken(bestandNaam):
    img = Image.open(bestandNaam)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = list()
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255,255,255,0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save(bestandNaam)

if __name__ == "__main__":
    main()