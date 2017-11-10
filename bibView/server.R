
# This is the server logic for a Shiny web application.
# You can find out more about building applications with Shiny here:
#
# http://shiny.rstudio.com
#
options(shiny.maxRequestSize=30*1024^2) 

library(shiny)
library(bibliometrix)
library(markdown)
library(knitr)

#reportFile <- paste0('analysis','_',format(Sys.time(), '%s'),'_',runif(1, 0, 88888888),'.doc')

function(input, output) {
  
    output$analysis <- renderUI({
      HTML("<h1>BibView - An&aacute;lise Bibliom&eacute;trica</h1>
            <hr/>
           <p>O BibView é uma ferramenta online que permite realizar análise bibliométrica dos dados de publicações científicas obtidas na base de dados <a href='http://www.scopus.com' target='_blank'>Scopus</a> utilizando o R e o pacote Bibliometrix.</p>
           
           <p>Este sistema foi desenvolvido baseado na aula 'Análise Bibliométrica com R', apresentada por <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>Diego Cavalca</a> para a turma do Mestrado em Engenharia Urbana, UFSCar/São Carlos. Mais informações podem ser obtidas <a href='https://github.com/diegocavalca/data-science/tree/master/bibliometric-analysis' target='_blank'>aqui</a>.</p>
           
           <p>O pipeline do BibView foi desenvolvido com base no <a href='http://htmlpreview.github.io/?https://github.com/massimoaria/bibliometrix/master/vignettes/bibliometrix-vignette.html' target='_blank'>material oficial do Bibliometrix</a>.</p>
           
           <p>Para começar, no menu ao lado:
           <ul><li>Selecione o arquivo .bib referente ao seu levantamento;</li>
           <li>Ajuste o número K de resultados por indicador;</li>
           <li>Após concluído o upload, clique no botão 'Analisar dados e Gerar relatório'.</li></ul></p>
           
           <h2>Créditos</h2>
           <hr/>
           <p>Desenvolvido e mantido por <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>Diego Cavalca</a>.</p>
           <p><u>AVISO IMPORTANTE:</u> Se você for utilizar os resultados gerados pelo BibView em seu trabalho, por favor considere entrar em contato através do email <a href='mailto:diego.cavalca@dc.ufscar.br' target='_blank'>diego.cavalca@dc.ufscar.br</a> ou através do <a href='https://www.linkedin.com/in/diegocavalca/' target='_blank'>LinkedIn</a>.</p>
           ")    
      })  
  
    observeEvent(input$do, {
      
      output$home <- renderUI({
        HTML("content")
      })
      
      # Make sure requirements are met
      req(input$fileBib)
      
      showModal(modalDialog(
        title = "AGUARDE",
        "Processando dados e gerando relatório...",
        easyClose = FALSE,
        footer = NULL
      ))#, session = getDefaultReactiveDomain())
      
      output$analysis<- renderUI({
        HTML("<h1>BibView - An&aacute;lise Bibliom&eacute;trica</h1>
             <hr/>
             <p>Aguarde, processando dados e gerando relatório...</p>")
        })
      
      # Copy the report file to a temporary directory before processing it, in
      # case we don't have write permissions to the current working dir (which
      # can happen when deployed).
      template <- "biblioAnalysis.Rmd" 
      tempReport <- file.path(tempdir(), template)
      file.copy(template, tempReport, overwrite = TRUE)
      
      params <- list(dataPath = input$fileBib$datapath,
                     kValue = input$k)
      
      # Knit the document, passing in the `params` list, and eval it in a
      # child of the global environment (this isolates the code in the document
      # from the code in this app).
      content <- rmarkdown::render(tempReport, 
                                   params = params,
                                   #output_format = 'word_document',
                                   envir = new.env(parent = globalenv()) )
      
      output$analysis <- renderUI({
        includeHTML(content)
      })
      
      #tags$head(tags$link(rel = "stylesheet", type = "text/css", 
      #                    href = "https://bootswatch.com/4/cerulean/bootstrap.min.css"))
      
      removeModal()
    })

}