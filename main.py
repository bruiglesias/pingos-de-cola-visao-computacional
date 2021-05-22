# -*- coding: UTF-8 -*-
import cv2
import glob

class Pingos: 

    def __init__(self):
        self.processadas = 0

    # função para exibir texto na imagem
    def put_text(self, image, text, position_x, position_y, color=(0, 255, 0)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, (position_x, position_y), font, 0.5, color, 0, cv2.LINE_AA)

    def posicao_pingos(self, contorno, imagem_colorida, cont):
        # Acha o menor retangulo envolvente do contornos
        x, y, w, h = cv2.boundingRect(contorno)
        # Acha o menor circulo envolvente do contorno
        (position_x, position_y), radius = cv2.minEnclosingCircle(contorno)
        center = (int(position_x),int(position_y))
        radius = int(radius)

        numero = str(cont)
        # Aplica o recorte do contorno
        recorte = imagem_colorida[y - 15:y + h + 15, x - 15:x + w + 15]
        # Exibe o recorte do contorno atual
        #cv2.imshow(numero, recorte)
        
        # Identifica o contorno
        self.put_text(imagem_colorida, "Pingo " + numero, int(x), int(y) - 60)
        self.put_text(imagem_colorida, "Coord. centro: ", int(x), int(y) - 40)
        self.put_text(imagem_colorida, "    X: " + str(int(position_x)), int(x), int(y) - 20)
        self.put_text(imagem_colorida, "    Y: " + str(int(position_y)), int(x), int(y) - 5)
        self.put_text(imagem_colorida, "    Raio: " + str(int(radius)), int(x), int(y) + 20)
        cv2.circle(imagem_colorida, center, radius,(0,255,0) , 1)
        cv2.circle(imagem_colorida, center, 2,(0,255,0) , -1)

        
   
    def tratamento(self, imagem):
        # Altera as dimensões da imagem
        height, width = imagem.shape[:2]
        imagem = cv2.resize(imagem, (int(width / 2), int(height/2)))
        # Converte a imagem de RGB  para HLS
        imagem_hls = cv2.cvtColor(imagem, cv2.COLOR_RGB2HLS)
        # Separa os canais da imagem
        canal_h, canal_l, canal_s = cv2.split(imagem_hls)
        canal_selecionado = canal_l

        # Aplicação da binarização pelo método de Otsu
        limiar, binarizacao_algoritmo_3 = cv2.threshold(canal_selecionado, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #cv2.imshow("HLS", imagem_hls)
        #cv2.imshow("Canal L", canal_selecionado)
        #cv2.imshow("Binarizacao", binarizacao_algoritmo_3)

        return binarizacao_algoritmo_3, imagem

    def contorno(self, imagem_bin, imagem_colorida, nome):
        # Obtém todos os contornos dos objetos segmentados na imagem
        _ , contornos, hierarquia = cv2.findContours(imagem_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cont = 0  # Variável contadora
        # Percorre por todos os contornos da imagem
        self.processadas = self.processadas + 1
        for contorno in contornos:
            cont += 1
            self.posicao_pingos(contorno, imagem_colorida, cont)
            # Exibe a placa atual'''
            #cv2.imshow("Placa atual", imagem_colorida)

        cv2.imwrite("processadas/"+nome+".png", imagem_colorida)
        cv2.imwrite("processadas/"+nome+"_binarizada.png", imagem_bin)
        return imagem_bin, imagem_colorida

    def main(self):
        
        base_de_imagens = "tratadas/*.png"

        for imagem_base in glob.glob(base_de_imagens):
            nome = imagem_base.split("\\")
            nome = nome[1]
            imagem_sem_adesivo = cv2.imread("tratadas_sem_adesivo/"+nome, 1)
            print(nome)
            imagem = cv2.imread(imagem_base, 1) 
            subtracao = cv2.subtract(imagem, imagem_sem_adesivo)
            imagem_bin_atual, imagem_base_colorida = self.tratamento(subtracao)
            self.contorno(imagem_bin_atual, imagem_base_colorida, nome)

        print("Processamento Concluido.")  
       


pingos = Pingos()
pingos.main()
