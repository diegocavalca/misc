---
title: "Analise Bibliometrica com R"
output:
  word_document: default
  pdf_document: default
  html_notebook: default
---

Neste trabalho irei apresentar o workflow básico para a realização de uma análise bibliométrica utilizando o R e o pacote Bibliometrix a partir dos dados de publicações científicas obtidas na base de dados [Scopus](http://www.scopus.com). 

A preparação do ambiente (instalação do R, RStudio e Bibliometrix) e a obtenção dos dados seguirão conforme a aula apresentada anteriormente. Mais informações sobre estas etapas podem ser obtidas [aqui](http://github.com/diegocavalca/data-science).

Este _markdown_ foi desenvolvido baseado no [material oficial](http://htmlpreview.github.io/?https://github.com/massimoaria/bibliometrix/master/vignettes/bibliometrix-vignette.html) do Bibliometrix.

***

Inicialmente, se faz necessário carregar o pacote _Bibliometrix_ no R, que irá ser responsável por todo o processamento e análise de indicadores de nosso trabalho.

```r
library(bibliometrix)
```
***
Com o ambiente preparado, iremos carregar os dados bibliométricos obtidos junto a base de dados Scopus.

```r
D <- readLines(inFile)
```

```
## Error in readLines(inFile): 'con' não é uma conexão
```

```r
M <- convert2df(D, dbsource = "scopus", format = "bibtex")
```

```
## Error in as.character(x): cannot coerce type 'closure' to vector of type 'character'
```
***
Para dar início a análise, é necessário executar o pré-processamento dos dados, preparando-os para posterior análise de indicadores. Além disso, algumas métricas interessantes podem ser extraídas.

```r
### (grafico) Processar resultados bibliometricos
results <- biblioAnalysis(M, sep = ";")
```

```
## Error in biblioAnalysis(M, sep = ";"): objeto 'M' não encontrado
```

```r
plot(x = results, k = 10, pause = FALSE)
```

```
## Error in plot(x = results, k = 10, pause = FALSE): objeto 'results' não encontrado
```
***
Com os dados preparados, o Bibliometrix oferece um resumo completo do conjunto de publicações analisados, incluido:

  * Resumo quantitativo
    + Artigos
    + Periódicos
    + Palavras-chave (Autorais e Indexadas)
    + Citações média por artigo
    + Período contemplado na pesquisa
  * Evolução histórica (p/ ano)
  * Autores mais produtivos
  * Artigos mais citados
  * Produção científica por país
  * etc.

```r
### (console) Resumo dos resultados 
S <- summary(object = results, k = 10, pause = FALSE)
```

```
## Error in summary(object = results, k = 10, pause = FALSE): objeto 'results' não encontrado
```
***

É possível também realizar uma análise cruzada entre os trabalhos do conjunto de dados onde, por exemplo, extrair quais os papers mais citados no conjunto de dados analisado.

```r
### (console/viewer) Referências (Papers) mais citadas, no conjunto de dados
CR_Papers = citations(M, field = "article", sep = ";")
```

```
## Error in strsplit(M$CR, sep): objeto 'M' não encontrado
```

```r
CR_Papers <- as.data.frame(CR_Papers$Cited[1:10])
```

```
## Error in as.data.frame(CR_Papers$Cited[1:10]): objeto 'CR_Papers' não encontrado
```

```r
names(CR_Papers) <- c('Paper', 'Citations')
```

```
## Error in names(CR_Papers) <- c("Paper", "Citations"): objeto 'CR_Papers' não encontrado
```

```r
CR_Papers
```

```
## Error in eval(expr, envir, enclos): objeto 'CR_Papers' não encontrado
```

```r
#View(CR_Papers)
```
***
Ou ainda, é possível obter os autores mais referenciados dentro do conjunto de dados.

```r
CR_Authors = citations(M, field = "author", sep = ";")
```

```
## Error in strsplit(M$CR, sep): objeto 'M' não encontrado
```

```r
CR_Authors <- as.data.frame(CR_Authors$Cited[1:10])
```

```
## Error in as.data.frame(CR_Authors$Cited[1:10]): objeto 'CR_Authors' não encontrado
```

```r
names(CR_Authors) <- c('Author', 'Citations')
```

```
## Error in names(CR_Authors) <- c("Author", "Citations"): objeto 'CR_Authors' não encontrado
```

```r
CR_Authors
```

```
## Error in eval(expr, envir, enclos): objeto 'CR_Authors' não encontrado
```

```r
#View(CR_Authors)
```
***
O Fator de Dominância é um importante indicador que mensura a produtividade de autores, calculando a razão entre o número de trabalhos em que o autor aparece como **Primeiro Autor** e o número total de trabalhos multi-autorais em que este aparece.

```r
# k = 10 registros
DF <- dominance(results, k = 10)
```

```
## Error in dominance(results, k = 10): objeto 'results' não encontrado
```

```r
DF
```

```
## Error in eval(expr, envir, enclos): objeto 'DF' não encontrado
```
***
O índice-H (H-index) é outra métrica importante para avaliar a relevância acadêmica de um autor. Ela leva em consideração o número de artigos com citações maiores ou iguais a esse número.

Por exemplo: um autor com índice-H = 15 indica que este autor possui 15 artigos com pelo menos 15 citações.

```r
authors = gsub(",", " ", names(results$Authors)[1:10])
```

```
## Error in gsub(",", " ", names(results$Authors)[1:10]): objeto 'results' não encontrado
```

```r
indices <- Hindex(M, authors, sep = ";", years=10)
```

```
## Error in Hindex(M, authors, sep = ";", years = 10): objeto 'M' não encontrado
```

```r
HI <- indices$H
```

```
## Error in eval(expr, envir, enclos): objeto 'indices' não encontrado
```

```r
HI
```

```
## Error in eval(expr, envir, enclos): objeto 'HI' não encontrado
```
***
Dentro do conjunto de dados, os atributos dos papers estão conectados entre si através do próprio paper. Assim, por exemplo, Autor(es) estão interconectados com Periódicos, Palavras-chave com Data de publicação, etc.
Essas conexões de diferentes atributos geram redes bipartidas que podem ser representadas como matrizes retangulares (Papers x ATRIBUTO_QUALQUER).

Logo, por exemplo, é possível gerar uma rede que apresenta o comportamento colaborativo entre países dentro da área de pesquisa em questão, ou seja, representa o modo como ocorre a transferência de conhecimento acadêmico.


```r
M <- metaTagExtraction(M, Field = "AU_CO", sep = ";")
```

```
## Error in metaTagExtraction(M, Field = "AU_CO", sep = ";"): objeto 'M' não encontrado
```

```r
NetMatrix <- biblioNetwork(M, analysis = "collaboration", network = "countries", sep = ";")
```

```
## Error in cocMatrix(M, Field = "AU_CO", type = "sparse", sep): objeto 'M' não encontrado
```

```r
networkPlot(NetMatrix, n = 20, Title = "Country Collaboration", type = "circle", size=TRUE, remove.multiple=FALSE)
```

```
## Error in networkPlot(NetMatrix, n = 20, Title = "Country Collaboration", : objeto 'NetMatrix' não encontrado
```
***

Ou também, pode ser gerado uma rede de coocorrências de palavras-chave, permitindo analisar subáreas da área de conhecimento estudada.

```r
# (grafico) Rede de co-ocorrencias de palavras-chave (20 keywords)
NetMatrix <- biblioNetwork(M, analysis = "co-occurrences", network = "keywords", sep = ";")
```

```
## Error in cocMatrix(M, Field = "ID", type = "sparse", sep): objeto 'M' não encontrado
```

```r
networkPlot(NetMatrix, n = 20, Title = "Keyword Co-occurrences", type = "kamada", size=T)
```

```
## Error in networkPlot(NetMatrix, n = 20, Title = "Keyword Co-occurrences", : objeto 'NetMatrix' não encontrado
```
***
## Conclusão

Portanto, a linguagem R juntamente com o pacote Bibliometrix fornecem mecanismos eficientes para realizar a análise bibliométrica em conjuntos de publicações acadêmicas obtidos na Scopus, permitindo extrair conhecimento importante a partir de indicadores relevantes, os quais podem agregar qualidade na produção científica em quaisquer áreas do conhecimento.

***
## Referências

* http://r-project.org/
* http://www.bibliometrix.org/
* https://github.com/diegocavalca/data-science
* http://www.collnet.de/Berlin-2008/KumarWIS2008cir.pdf
* http://htmlpreview.github.io/?https://github.com/massimoaria/bibliometrix/master/vignettes/bibliometrix-vignette.html
