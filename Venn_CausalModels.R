############################## Venn Diagrams ############################## 

## the diagrammeR by Rich Iannone provides great functionalities to draw graphs
## check it out: https://rich-iannone.github.io/DiagrammeR/index.html


############### installing & loading packages ############### 

rm(list=ls())
if (!require("pacman")) install.packages("pacman")
p_load(DiagrammeR, DiagrammeRsvg, htmltools)

############### logic model 1 ############### 
LM1 <- grViz("
digraph boxes_and_circles {
      
      # define graph
      graph [overlap = true, fontsize = 10]
      
      # define nodes
      node [shape = box, fixedsize = true,  # initialize box
            height = 0.5, width = 1.5,  # set size
            penwidth = 2, color = darkslategray,  # set line
            fontname = CambriaMath, fontcolor = darkslategray]  # set font
      
      # create box nodes
      'SES'; 'CLASS RANK'; 'PREP'  [penwidth = 3, fontname = bold]
      
      node [shape = circle, width = 1, # initialize circle
            fontname = CambriaMath, fontcolor = darkslategray,
            penwidth = 1, color = darkslategray]
      
      # create circle nodes
      'SAT'
      
      # define edges
      edge [color = darkslategray, fixedsize = true,  # initialize edge
            arrowhead = vee, arrowtail = none,  # set arrows
            width = 1, penwidth = 1,  # set size
            style = dashed, minlen = 2]  # set style
      
      # create edges
      {rank=same; 'SES' -> 'CLASS RANK' 'SES' -> 'PREP' 'SES' -> 'SAT'
        'CLASS RANK' -> 'PREP' 'CLASS RANK' -> 'SAT'
        'PREP' -> 'SAT' [style = solid, penwidth = 2]}
      }")


############### exporting ############### 

# print it to html
# launch the page in your browser
# inspect element and select code defining the .svg file
# copy the code in a .txt document and save to .svg
# the svg file is ready!

LM1_export <- export_svg(LM1)
html_print(HTML(LM1_export))

############### 
############### logic model 2 ############### 
############### 

LM2 <- grViz("
digraph boxes_and_circles {
             
             # define graph
             graph [overlap = true, fontsize = 10]
             
             # define nodes
             node [shape = box, fixedsize = true,  # initialize box
             height = 0.5, width = 1.5,  # set size
             penwidth = 2, color = darkslategray,  # set line
             fontname = CambriaMath, fontcolor = darkslategray]  # set font
             
             # create box nodes
             'SES'; 'CLASS RANK'; 'PREP'  [penwidth = 3, fontname = bold]
             
             node [shape = circle, width = 1, # initialize circle
             fontname = CambriaMath, fontcolor = darkslategray,
             penwidth = 1, color = darkslategray]
             
             # create circle nodes
             'SAT'
             
             # define edges
             edge [color = darkslategray, fixedsize = true,  # initialize edge
             arrowhead = vee, arrowtail = none,  # set arrows
             width = 1, penwidth = 1,  # set size
             style = dashed, minlen = 2]  # set style
             
             # create edges
             {rank=same; 'SES' -> 'PREP' 'SES' -> 'CLASS RANK' 'SES' -> 'SAT'
               'PREP' -> 'CLASS RANK' [style = solid, penwidth = 2]
               'PREP' -> 'SAT' [style = solid, penwidth = 2]
               'CLASS RANK' -> 'SAT' [style = solid, penwidth = 2]}
             }")

############### exporting ############### 
LM2_export <- export_svg(LM2)
html_print(HTML(LM2_export))
