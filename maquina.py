# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as pl
import os

# variaveis globais
tipo_img = ['jpg','jpeg', 'png']
tipo_video = ['mp4','avi']
resultado = []
dir_path = 'arquivos'
arquivos = os.listdir(dir_path)
methods = ['cv2.TM_CCOEFF_NORMED']
query = cv2.imread('query/query_2.jpg',0)
query_2 = query.copy()

# inicio funcao que realiza busca em video -----------------
def busca_video(arquivo, similaridade_minima):
  print('Busca iniciada no video ' + arquivo + ', aguarde...')
  captura = cv2.VideoCapture('arquivos/' + arquivo)
  similaridade_maxima = 0

  while(captura.isOpened()):
    ret, frame = captura.read()
    if ret == True:
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      base = gray.copy()
      w, h = base.shape[::-1]

      for meth in methods:
        method = eval(meth)
        # Aplicando o template Matching
        res = cv2.matchTemplate(base,query_2,method)
        #Recupera a similaridade entre o template e o conteúdo da Imagem de busca
        min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)
        parametro = round(similaridade*100,2)
        if (parametro > similaridade_minima) and (parametro > similaridade_maxima):
          similaridade_maxima = round(similaridade*100,2)
    else: 
      break
  
  return [similaridade_maxima, arquivo]
# fim funcao que realiza busca em video -------------------

# inicio funcao que realiza busca em imagens --------------
def busca_img(arquivo, similaridade_minima):
  print('Busca iniciada na imagem ' + arquivo + ', aguarde...')
  base = cv2.imread(('arquivos/' + arquivo),0)
  base_2 = base.copy()
  similaridade_maxima = 0

  for meth in methods:
    method = eval(meth)
    # Aplicando o template Matching
    res = cv2.matchTemplate(base_2,query_2,method)

    #Recupera a similaridade entre o template e o conteúdo da Imagem de busca
    min_val, similaridade, min_loc, max_loc = cv2.minMaxLoc(res)
    parametro = round(similaridade*100,2)
    if (parametro > similaridade_minima) and (parametro > similaridade_maxima):
      similaridade_maxima = round(similaridade*100,2)
  
  return [similaridade_maxima, arquivo]
# fim funcao que realiza busca em imagens -----------------

# inicio funcao que de inicializacao da maquina de busca --
def maquina_busca(similaridade_minima, qtd_obj):
  for arquivo in arquivos:
    extensao = arquivo.split('.')
    if len(extensao) > 1:
      if extensao[1] in tipo_img:
        aux = busca_img(arquivo, similaridade_minima)
        if aux[0] > 0:
          resultado.append(aux)
      if extensao[1] in tipo_video:
        aux = busca_video(arquivo, similaridade_minima)
        if aux[0] > 0:
          resultado.append(aux)
  
  resultado_ordenado = sorted(resultado, key = lambda x: x[0], reverse=True)

  i = 0
  while(i < qtd_obj):
    if i < len(resultado_ordenado):
      print(str(i+1) + 'º - arquivo: ' + resultado_ordenado[i][1] + ' | Similaridade = ' +  str(resultado_ordenado[i][0]) + '%')
    i+=1
# fim funcao que de inicializacao da maquina de busca --

sim_minima = float(input('Informe a similaridade minima: '))
qt_obj = int(input('Informe a quantidade máxima de objetos a serem retornados: '))

maquina_busca(sim_minima,qt_obj)  






