
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(shinythemes)

shinyUI(
  
  navbarPage(
    #theme = shinytheme("cerulean"),  # <--- To use a theme, uncomment this
    "BibView",
    tabPanel("Home",
             sidebarPanel(
               fileInput('fileBib', 'Selecione o arquivo .BIB:', accept=c('.bib')),
               sliderInput('k', "K-valor:", 5, 50, 10),
               tags$hr(),
               
               actionButton("do", "Analisar dados e gerar relatório", icon("magic"), class = "btn-primary", width='100%')
             ),
             mainPanel(
               htmlOutput('analysis', width='100%')
               )
    ),
    tabPanel("Sobre", 
             HTML("<h1>BibView - An&aacute;lise Bibliom&eacute;trica</h1>
                   <hr/>
                   <p>O BibView é uma ferramenta online que permite realizar análise bibliométrica dos dados de publicações científicas obtidas na base de dados <a href='http://www.scopus.com' target='_blank'>Scopus</a> utilizando o R e o pacote Bibliometrix.</p>
                  <p>Este sistema foi desenvolvido baseado na aula 'Análise Bibliométrica com R', apresentada por <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>Diego Cavalca</a> para a turma do Mestrado em Engenharia Urbana, UFSCar/São Carlos. Mais informações podem ser obtidas <a href='https://github.com/diegocavalca/data-science/tree/master/bibliometric-analysis' target='_blank'>aqui</a>.</p>
                  <p>O pipeline do BibView foi desenvolvido com base no <a href='http://htmlpreview.github.io/?https://github.com/massimoaria/bibliometrix/master/vignettes/bibliometrix-vignette.html' target='_blank'>material oficial do Bibliometrix</a>.</p>
                  
                  <h2>Créditos</h2>
                  <hr/>
                  <p>Projeto desenvolvido e mantido por <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>Diego Cavalca</a>, disponível no <a href='https://github.com/diegocavalca/misc/tree/master/bibView' target='_blank'>Github</a>.</p>
                  <p>Caso encontre erros, ou queira contribuir com o projeto, entre em contato através do email <a href='mailto:diego.cavalca@dc.ufscar.br' target='_blank'>diego.cavalca@dc.ufscar.br</a> ou através do <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>LinkedIn</a>.</p>
                  <p><u>AVISO IMPORTANTE:</u> Se você for utilizar os resultados gerados pelo BibView em seu trabalho, por favor considere entrar em contato (informações acima).</p>") )
    #,tags$footer(title="Your footer here", align = "right", style = "position:fixed;bottom:0;right:0;left:0;background:#F5F5F5;padding:25px;box-sizing:border-box;")
  )
)