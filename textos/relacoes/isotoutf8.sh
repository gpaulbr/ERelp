#!/bin/bash

# 04/07/2007
# por Marcelo Oliveira - www.iboletim.com.br
# Licença de uso: GPL

# uso:
# utf2iso.sh diretorio-a-ser-convertido

# fecha se nao for fornecido nenhum argumento
if [ $# -eq 0 ]
then
echo "ERRO: especifique o nome da pasta com os arquivos a serem convertidos!"
echo "Uso: ./utf2iso.sh diretorio-a-ser-convertido"
exit 1

fi

# cria diretorio para armazenar arquivos convertidos
cp -R $1 utf8

# acessa diretorio com os arquivos a serem convertidos
cd $1

# cria lista de todos os arquivos que serao convertidos (estou excluindo .gif e .jpg)
lista=`find -type f | grep -v gif | grep -v jpg`

# executa conversao
for i in $lista
do
echo "convertendo... $i"
iconv -f iso-8859-15 -t utf-8 $i > ../utf8/$i;
#read; # para verificar as mensagens de erro
done

if [ $? == 0 ]
then
echo -e "\nConversao terminada com sucesso!\n"
fi
