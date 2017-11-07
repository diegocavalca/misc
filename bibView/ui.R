
# This is the user-interface definition of a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#

library(shiny)
library(shinythemes)

shinyUI(
  
  navbarPage(
    theme = shinytheme("cerulean"),  # <--- To use a theme, uncomment this
    "BibView",
    tabPanel("Home",
             sidebarPanel(
               fileInput('fileBib', 'Selecione o arquivo .BIB:', accept=c('.bib')),
               sliderInput('k', "K-valor:", 5, 50, 10),
               tags$hr(),
               
               actionButton("do", "Analisar dados e gerar relatório", icon("magic"), class = "btn-primary", width='100%')
             ),
             mainPanel(htmlOutput('analysis', width='100%'))
    ),
    tabPanel("Sobre", 
             HTML("<h1>BibView - An&aacute;lise Bibliom&eacute;trica</h1>
                   <hr/>
                   <p>Desenvolvido e mantido por <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>Diego Cavalca</a>.</p>
                  
                   <h2>Referências</h2>
                   <hr/>
                   <p>Se você for utilizar os dados gerados pelo BibView em sua pesquisa, por favor entre em contato através do email <a href='mailto:diego.cavalca@dc.ufscar.br' target='_blank'>diego.cavalca@dc.ufscar.br</a>.</p>
                  ") )
    #,tags$footer(title="Your footer here", align = "right", style = "position:fixed;bottom:0;right:0;left:0;background:#F5F5F5;padding:25px;box-sizing:border-box;")
  )
)