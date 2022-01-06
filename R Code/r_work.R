
source('fbf.R')

df <- read.csv('graph_me.csv')

the_plot <- animate_field3(df)
animate(the_plot, height = 1028, width = 2056)
save_anim('Play Animation.gif')