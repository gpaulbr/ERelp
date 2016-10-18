# README #
### What is this repository for? ###

* Extração de Relações entre Entidades Nomeadas
* v1.0
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

Parâmetros de entrada: 
      
      DIRETORIO TREINO - deve conter os textos separados em arquivos .txt - entrada
      DIRETORIO DE TESTE - deve conter os textos separados em arquivos .txt - entrada 
      DIREOTORIO DO MODELO - diretorio apontando para o modelo utilizado, caso o arquivo não exista será criado um novo, caso exista será utilizado o que já está salvo
      DIRETORIO DE TRABALHO - será criado na execução - saida
      CROSS VALIDATION - se deseja ou não utilizar a técnica de validação cruzada (true ou false)
      QUANTIDADE DE FOLDS - número de folds utilizadas no processo de cross validation (valor ignorado se QUANTIDADE DE FOLDS for falso)
      DIRETORIO MALLET - diretorio que contem a biblioteca MALLET
      CATEGORIAS A UTILIZAR (2) - opcional, mas se for informado devem ser exatamente duas (vírgula) - obritagorio para extração dos parâmetros
      DICIONARIOS - dicionarios a serem utilizados como features

Rodando o Script:

     <interpretador_python_alternativo> ./treinamento/RRcrf.py DIRETORIO_TREINO DIRETORIO_DE_TRABALHO QUANTIDADE_DE_FOLDS DIRETORIO_MALLET <CATEGORIA_A_UTILIZAR_1 CATEGORIA_A_UTILIZAR_2> , DICIONARIOS...<opcional>

Exemplo de linha de execução:

      python ./treinamento/RRcrf.py ./textos/ORG_PES_modificado_rev ./textos/ORG_PES_modificado_rev ./modelos/modelo saida_ORG_PES_Gabriel true 5 ./bibliotecas/Mallet/mallet-0.4 PES ORG , ./Dicionarios/Profissao_Titulo.txt

Bibliotecas utilizadas:

     -feedpaser 5.1.1
     -NLTK 2.0b9
     -scipy 0.10.1
     -PyAML 3.10 linux i686-2.6
     -numpy 1.6.1 -> instalação obrigatória

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###


### Who do I talk to? ###

* gabriel.paul@acad.pucrs.br