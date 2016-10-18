#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
from datetime import datetime


UI_FILE = 'ERelP.ui'

class Programa(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file(UI_FILE)#Carrega o arquivo do programa Glade
	#Instancia todas as janelas, seletores de arquivos e botões de escolha
        self.window = builder.get_object('window1')
        self.about = builder.get_object('about_dialog')
        self.window2 = builder.get_object('window2')
        self.window3 = builder.get_object('window3')
        self.window4 = builder.get_object('window4')
        self.txt_cross = builder.get_object('filechooserbutton1')
        self.nfolds = builder.get_object('spinbutton1')
        self.window5 = builder.get_object('window5')
        self.window6 = builder.get_object('window6')
        self.dicionario1 = builder.get_object('filechooserbutton2')
        self.dicionario2 = builder.get_object('filechooserbutton3')
        self.window7 = builder.get_object('window7')
        self.window8 = builder.get_object('window8')
        self.txt_treino = builder.get_object('filechooserbutton4')
        self.window9 = builder.get_object('window9')
        self.txt_teste = builder.get_object('filechooserbutton5')
        self.window10 = builder.get_object('window10')
        self.window11 = builder.get_object('window11')
        self.nfolds2 = builder.get_object('spinbutton2')
        self.window12 = builder.get_object('window12')
        self.dicionario3 = builder.get_object('filechooserbutton6')
        self.dicionario4 = builder.get_object('filechooserbutton7')
        self.window13 = builder.get_object('window13')
        self.txt_teste2 = builder.get_object('filechooserbutton8')
        self.window14 = builder.get_object('window14')
        self.model = builder.get_object('filechooserbutton9')
        self.window15 = builder.get_object('window15')
        self.nfolds3 = builder.get_object('spinbutton3')
        self.window16 = builder.get_object('window16')
        self.window17 = builder.get_object('window17')
	self.window18 = builder.get_object('window18')
        self.dicionario5 = builder.get_object('filechooserbutton10')
        self.dicionario6 = builder.get_object('filechooserbutton11')
	self.txt_treino2 = builder.get_object('filechooserbutton12')
        self.window.show()#Carrega a primeira janela
	#Variáveis que serão utilizadas para guardar os parametros de entrada do programa
        self.escolha = 1
        self.num_folds = 1
        self.num_folds2 = 1
        self.num_folds3 = 1
        self.pasta_cross = ''
        self.pasta_treino = ''
	self.pasta_treino2 = ''
        self.pasta_teste = ''
        self.pasta_teste2 = ''
        self.modelo = ''
        self.categoria = 'LOCAL ORG'
        self.categoria2 = 'LOCAL ORG'
        self.categoria3 = 'LOCAL ORG'
        self.dic1 = ''
        self.dic2 = ''
        self.dic3 = ''
        self.dic4 = ''
        self.dic5 = ''
        self.dic6 = ''
	#Conecta os sinais com as suas respectivas ações. Ex: Quando o botao1 for clicado, vai acionar o sinal on_button1_clicked, e suas ações estarão na função button
        builder.connect_signals({'on_button1_clicked':self.button,
                                 'on_Sobre_activate': self.sobre,
                                 'on_button2_clicked': self.button2,
                                 'on_button3_clicked': self.button3,
                                 'on_radiobutton1_toggled': self.cross,
                                 'on_radiobutton2_toggled': self.treinoteste,
                                 'on_radiobutton3_toggled': self.teste,
                                 'on_filechooserbutton1_file_set': self.textocross,
                                 'on_button4_clicked': self.button4,
                                 'on_radiobutton4_toggled': self.pes_org,
                                 'on_radiobutton5_toggled': self.local_org,
                                 'on_radiobutton6_toggled': self.org,
                                 'on_radiobutton7_toggled': self.org_local_pes,
                                 'on_button5_clicked': self.button5,
                                 'on_filechooserbutton2_file_set': self.escolher_dic1,
                                 'on_filechooserbutton3_file_set': self.escolher_dic2,
                                 'on_button6_clicked': self.button6,
                                 'on_filechooserbutton4_file_set': self.textotreino,
                                 'on_button7_clicked': self.button7,
                                 'on_filechooserbutton5_file_set': self.textoteste,
                                 'on_button8_clicked': self.button8,
                                 'on_radiobutton8_toggled': self.pes_org2,
                                 'on_radiobutton9_toggled': self.local_org2,
                                 'on_radiobutton10_toggled': self.org2,
                                 'on_radiobutton11_toggled': self.org_local_pes2,
                                 'on_button9_clicked': self.button9,
                                 'on_button10_clicked': self.button10,
                                 'on_filechooserbutton6_file_set': self.escolher_dic3,
                                 'on_filechooserbutton7_file_set': self.escolher_dic4,
                                 'on_button11_clicked': self.button11,
                                 'on_filechooserbutton8_file_set': self.textoteste2,
                                 'on_button12_clicked': self.button12,
                                 'on_filechooserbutton9_file_set': self.escolher_modelo,
                                 'on_button13_clicked': self.button13,
                                 'on_button14_clicked': self.button14,
                                 'on_radiobutton12_toogled': self.pes_org3,
                                 'on_radiobutton13_toogled': self.local_org3,
                                 'on_radiobutton14_toogled': self.org3,
                                 'on_radiobutton15_toogled': self.org_local_pes3,
                                 'on_button15_clicked': self.button15,
                                 'on_filechooserbutton10_file_set': self.escolher_dic5,
                                 'on_filechooserbutton11_file_set': self.escolher_dic6,
                                 'on_button16_clicked': self.button16,
				 'on_button17_clicked': self.button17,
				 'on_filechooserbutton12_file_set': self.textotreino2})

	
    def button(self, widget):#Primeiro botão, fecha a janela do titulo a abre a segunda janela
        self.window.destroy()
        self.window2.show()
	
    def button2(self,widget):#Segundo botao, salva a escolha de qual execução o usuário quer fazer e fecha a janela 2 e abre a janela3.
        self.window2.destroy()
        if self.escolha == 1:
            self.window3.show()#se for cross, abre a janela 3(botao 3)
        elif self.escolha == 2:
            self.window8.show()#se for treino e teste, abre a janela 8(botao7)
        elif self.escolha == 3:
            self.window18.show()#se for teste, abre a janela 18(botao17)
	
    def button3(self, widget):#Terceiro botão, avança
        self.window3.destroy()
        self.window4.show()
        
    def button4(self, widget):#Quarto botão, salva o numero de folds selecionado e avança
        self.num_folds = self.nfolds.get_value_as_int()
        print self.num_folds
        self.window4.destroy()
        self.window5.show()

    def button5(self, widget):#Quinto botão, salva quais as categorias a avança
        print self.categoria
        self.window5.destroy()
        self.window6.show()

    def button6(self, widget):#Sexto botão, pega todos os dados salvos para cross e faz a execução
        self.window6.destroy()
        self.window7.show()
        time = datetime.now()
        dia = str(time.day)
        mes = str(time.month)
        ano = str(time.year)
        hora = str(time.hour)
        minuto = str(time.minute)
        segundo = str(time.second)
        pasta_cross = self.pasta_cross.replace(' ','\ ')
        saida = self.categoria.replace(' ', '_')
        dic1 = self.dic1.replace(' ','\ ')
        dic2 = self.dic2.replace(' ','\ ')
        num_folds = str(self.num_folds)
        temp = 'python treinamento/RRcrf.py '+pasta_cross+' '+pasta_cross+' modelos/modelo-'+dia+'.'+mes+'.'+ano+'-'+hora+':'+minuto+':'+segundo+saida+' saida-'+saida+' true '+num_folds+' bibliotecas/Mallet/mallet-0.4 '+self.categoria+' , '+dic1+' '+dic2
        print temp
        utf8 = temp.encode('utf-8')
        os.system(utf8)#execução
        self.window7.destroy()
        gtk.main_quit()
        
    def button7(self, widget):#botao de seleção dos textos de treino para a execução e avança
        self.window8.destroy()
        self.window9.show()

    def button8(self, widget):#botao de seleção dos textos de teste para a execução e avança
        self.window9.destroy()
        self.window10.show()

    def button9(self, widget):#botao que salva a categoria e avança
        print self.categoria2
        self.window10.destroy()
        self.window11.show()

    def button10(self, widget):#botao que salva a quantidade de folds e avança
        self.num_folds2 = self.nfolds2.get_value_as_int()
        print self.num_folds2
        self.window11.destroy()
        self.window12.show()

    def button11(self, widget):#botao da execução do treino e teste
        self.window12.destroy()
	self.window7.show()
        time = datetime.now()
        dia = str(time.day)
        mes = str(time.month)
        ano = str(time.year)
        hora = str(time.hour)
        minuto = str(time.minute)
        segundo = str(time.second)
        pasta_treino = self.pasta_treino.replace(' ','\ ')
        pasta_teste = self.pasta_teste.replace(' ','\ ')
        saida = self.categoria2.replace(' ', '_')
        dic3 = self.dic3.replace(' ','\ ')
        dic4 = self.dic4.replace(' ','\ ')
        num_folds2 = str(self.num_folds2)
        temp = 'python treinamento/RRcrf.py '+pasta_treino+' '+pasta_teste+' modelos/modelo-'+dia+'.'+mes+'.'+ano+'-'+hora+':'+minuto+':'+segundo+saida+' saida-'+saida+' false '+num_folds2+' bibliotecas/Mallet/mallet-0.4 '+self.categoria2+' , '+dic3+' '+dic4
        print temp
        utf8 = temp.encode('utf-8')
        os.system(utf8)#execução
	self.window7.destroy()
	gtk.main_quit()

    def button12(self, widget):#segunda janela da execução de teste, salva os textos e avança
        self.window13.destroy()
        self.window14.show()

    def button13(self, widget):#terceira janela da execução de teste, salva os textos e avança
        self.window14.destroy()
        self.window15.show()

    def button14(self, widget):#quarta janela da execução de teste, salva o numero de folds e avança
        self.num_folds3 = self.nfolds3.get_value_as_int()
        print self.num_folds3
        self.window15.destroy()
        self.window16.show()

    def button15(self, widget):#quinta janela da execução de teste, salva as categorias e avança
        print self.categoria3
        self.window16.destroy()
        self.window17.show()

    def button16(self, widget):#janela da execução, salva todos os dados e executa no terminal
        self.window17.destroy()
        pasta_teste2 = self.pasta_teste2.replace(' ','\ ')
	pasta_treino2 = self.pasta_treino2.replace(' ','\ ')
	modelo = self.modelo.replace(' ','\ ')
        saida = self.categoria3.replace(' ', '_')
        dic5 = self.dic5.replace(' ','\ ')
        dic6 = self.dic6.replace(' ','\ ')
        num_folds3 = str(self.num_folds3)
        temp = 'python treinamento/RRcrf.py '+pasta_treino2+' '+pasta_teste2+' '+modelo+' '+'saida-'+saida+' false '+num_folds3+' bibliotecas/Mallet/mallet-0.4 '+self.categoria3+' , '+dic5+' '+dic6
        print temp
        utf8 = temp.encode('utf-8')
        os.system(utf8)#execução
	gtk.main_quit()

    def button17(self, widget):#Está invertido o numero, mas esse é o botao da primeira janela da execução do teste
	self.window18.destroy()
	self.window13.show()
    #a partir daqui são todos os widgets, que pegam os textos, numero de folds, categorias, dicionarios
    def textocross(self, widget):
        self.pasta_cross = self.txt_cross.get_current_folder()
        print self.pasta_cross

    def textotreino(self, widget):
        self.pasta_treino = self.txt_treino.get_current_folder()
        print self.pasta_treino

    def textoteste(self, widget):
        self.pasta_teste = self.txt_teste.get_current_folder()
        print self.pasta_teste

    def textotreino2(self, widget):
	self.pasta_treino2 = self.txt_treino2.get_current_folder()
	print self.pasta_treino2 

    def textoteste2(self, widget):
        self.pasta_teste2 = self.txt_teste2.get_current_folder()
        print self.pasta_teste2

    def escolher_modelo(self, widget):
        self.modelo = self.model.get_filename()
        print self.modelo

    def escolher_dic1(self, widget):
        self.dic1 = self.dicionario1.get_filename()
        print self.dic1

    def escolher_dic2(self, widget):
        self.dic2 = self.dicionario2.get_filename()
        print self.dic2

    def escolher_dic3(self, widget):
        self.dic3 = self.dicionario3.get_filename()
        print self.dic3

    def escolher_dic4(self, widget):
        self.dic4 = self.dicionario4.get_filename()
        print self.dic4

    def escolher_dic5(self, widget):
        self.dic5 = self.dicionario5.get_filename()
        print self.dic5

    def escolher_dic6(self, widget):
        self.dic6 = self.dicionario6.get_filename()
        print self.dic6

    def pes_org(self, widget):
        self.categoria = 'ORG PES'

    def local_org(self, widget):
        self.categoria = 'LOCAL ORG'

    def org(self, widget):
        self.categoria = 'ORG'

    def org_local_pes(self, widget):
        self.categoria = ' '

    def pes_org2(self, widget):
        self.categoria2 = 'ORG PES'

    def local_org2(self, widget):
        self.categoria2 = 'LOCAL ORG'

    def org2(self, widget):
        self.categoria2 = 'ORG'

    def org_local_pes2(self, widget):
        self.categoria3 = ' '

    def pes_org3(self, widget):
        self.categoria3 = 'ORG PES'

    def local_org3(self, widget):
        self.categoria3 = 'LOCAL ORG'

    def org3(self, widget):
        self.categoria3 = 'ORG'

    def org_local_pes3(self, widget):
        self.categoria3 = ' '
        
    def sobre(self, widget):
        self.about.run()
        self.about.hide()

    def cross(self, widget):
        self.escolha = 1
        print self.escolha

    def treinoteste(self, widget):
        self.escolha = 2
        print self.escolha

    def teste(self, widget):
        self.escolha = 3
        print self.escolha
        
            
        
#execução do programa
if __name__ == '__main__':
    Programa()
    gtk.main()
