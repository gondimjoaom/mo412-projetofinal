# Análise da Composição das Bancas de Defesas do IC/UNICAMP

Jhéssica Silva e João Gondim  
Instituto de Computação  
Universidade Estadual de Campinas  
MO412, 2s2025 - Prof. João Meidanis

---

### Sobre o trabalho:
Neste projeto foi realizada uma análise da composição das Bancas de Defesas (mestrado e doutorado) do Instituto de Computação da Universidade Estadual de Campinas (IC/UNICAMP), entre os anos de 2006 e 2024, com o objetivo de responder as seguintes perguntas de pesquisa: 

**Colaboração entre professor{a/e}s**
* Quais são as universidades que mais colaboram com o IC?
* Quais professor{a/e}s mais participam de bancas no IC?
* Qual o/a professor{a} que mais convidou pessoas diferentes para as bancas?
* Existe comunidade entre professor{a/e}s do IC?

**Composição das bancas (mulheres x homens)**
* Qual a percentagem de gêneros***** nas bancas do IC?
* Orientadoras mulheres convidam mais avaliadoras mulheres para banca? 
* Como se dá a colaboração entre professores homens e professoras mulheres?

---

### Dados utilizados 

Os dados que foram utilizados neste projeto foram primeiramente os disponibilizados pelo IC/UNICAMP das [defesas ocorridas entre 2006 e 2024](https://docs.google.com/spreadsheets/d/1YomoTYGo-2fRbN8_HvS_WGrwh8ZdZUfzjq9y9ZQGKjM/edit?gid=0#gid=0). Dado que a base de dados não está pronta para ser utilizada para se alcançar o objetivo deste projeto, foi necessário coletar dados adicionais de outras fontes.

Primeiramente, a planilha com informações de defesas disponibilizadas pelo IC/UNICAMP, oferece para cada defesa um *link* para os dados do trabalho (dissertação ou tese) no Repositório da Produção Científica e Intelectual da UNICAMP. Foi coletado neste repositório, para cada defesa, o *link* do ORCID das pessoas avaliadoras daquele trabalho (incluindo a pessoa orientadora). No ORCID da pessoa avaliadora, foram coletados o nome, a filiação atual e os tópicos de interesse de pesquisa da pessoa. Todo esse processo de coleta foi realizado de forma automatizada com a ferramenta extratora de dados Selenium.

Como parte da limpeza dos dados, foi realizado manualmente a padronização das filiações de cada pessoa. Para complementar os dados, foi anotado manualmente o departamento das pessoas orientadoras em: 
* DSC - Departamento de Sistemas de Computação
* DSI - Departamento de Sistemas de Informação
* DTC - Departamento de Teoria da Computação

Além disso, como foi desejado fazer um estudo relacionado com o "gênero" das pessoas que compõem uma banca de defesa, manualmente, também foi feito uma atribuição de "gênero" como 'mulher' ou 'homem' para cada pessoa relacionada a essa defesa com base em seu nome, e em alguns casos, com base em sua foto na plataforma Lattes. Entendemos que é preciso e urgente repensar os binários de gênero e que essa atribuição inseriu no nosso estudo crenças equivocadas de classificação. Mas, neste estudo, decidimos enfrentar o dilema da classificação, binarizando o estudo, mas não omitindo do mesmo os riscos dessa classificação em perpetuar a opressão. 

---

### Propriedades da Rede de Defesas do IC/UNICAMP (2006 a 2024)

  
| | N | L | \<k> | \<k_in> | \<k_out> | C |
|:---: | :---: | :---: | :---: | :---: |:---:| :---: |
| Todos os nós | 514 | 1989 | 7,74±20,01 | 3,87±6,64 | 3,87±14,82 | 0,0132 |
| Apenas mulheres | 114 | - | 6,95±16,27 | 3,85±6,22 | 3,10±12,65 | 0,0141 |
| Apenas homens | 399 | - | 7,98±20,97 | 3,88±6,76 | 4,10±15,47 | 0,0123 |

