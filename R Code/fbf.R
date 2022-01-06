
	animate_field <- function(df){
		require(ggplot2)
		require(gganimate)
	df$x <- df$x - 10
	the_plot <- ggplot(df, aes(x=x, y=y, color = color)) +
	geom_point(aes(size = 3, shape=factor(shape))) +
	xlim(10, 110)+
	ylim(0, 53.3)+
	theme(panel.background = element_rect(fill = "darkseagreen4",
															 colour = "darkseagreen4",
															 size = 0.5,
															 linetype = "solid"),
				panel.grid.major.x = element_line(size = 0.5, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.minor.x= element_line(size = 0.25, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.major.y = element_blank(),
				panel.grid.minor.y = element_blank(),
				axis.line = element_line(colour = "ghostwhite",
														size = 3,
														linetype = "solid"),
				axis.text = element_text(size=10, face = "bold"),
				axis.title = element_text(size = 10, face = "bold"))+
	scale_x_continuous(breaks = seq(0, 100, 10), 
									minor_breaks = seq(0, 100, 5)) +
	transition_time(time)
	return(the_plot)
	}
	
	animate_field2 <- function(df){
	df$x <- df$x - 10
	the_plot <- ggplot(df, aes(x=x, y=y)) +
	geom_point(aes(colour=team, shape=team), size=3)+
	xlim(10, 110)+
	ylim(0, 53.3)+
	theme(panel.background = element_rect(fill = "darkseagreen4",
															 colour = "darkseagreen4",
															 size = 0.5,
															 linetype = "solid"),
				panel.grid.major.x = element_line(size = 0.5, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.minor.x= element_line(size = 0.25, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.major.y = element_blank(),
				panel.grid.minor.y = element_blank(),
				axis.line = element_line(colour = "ghostwhite",
														size = 3,
														linetype = "solid"),
				axis.text = element_text(size=10, face = "bold"),
				axis.title = element_text(size = 10, face = "bold"))+
	scale_x_continuous(breaks = seq(0, 100, 10), 
									minor_breaks = seq(0, 100, 5)) +
	transition_time(time) +
	geom_text(aes(label=square_score))
	return(the_plot)
	}

	animate_field3 <- function(df){
	require(ggplot2)
	require(gganimate)
	df$x <- df$x - 10
	the_plot <- ggplot(df, aes(x=x, y=y)) +
	geom_point(aes(colour=team, shape=team), size=3)+
	scale_shape_manual(values= c(19, 18, 19)) + 
	scale_colour_manual(values = c("royalblue4", "sienna", "aquamarine")) + 
	xlim(10, 110)+
	ylim(0, 53.3)+
	theme(panel.background = element_rect(fill = "darkseagreen4",
															 colour = "darkseagreen4",
															 size = 0.5,
															 linetype = "solid"),
				panel.grid.major.x = element_line(size = 1, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.minor.x= element_line(size = 0.5, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.major.y = element_blank(),
				panel.grid.minor.y = element_blank(),
				axis.line = element_line(colour = "ghostwhite",
														size = 6,
														linetype = "solid"),
				axis.text = element_text(size=10, face = "bold"),
				axis.title = element_text(size = 10, face = "bold"),
				legend.position = "none",
				axis.title.x = element_blank(),
				axis.title.y = element_blank(),
				axis.text.x = element_text(face="bold", size = 30),
				axis.text.y = element_blank()) +
	scale_x_continuous(breaks = seq(0, 100, 10), minor_breaks = seq(0, 100, 5), labels=c(0, 10, 20, 30, 40, 50, 40, 30, 20, 10, 0)) +
	transition_time(time)
	return(the_plot)
	}
	
	still_field <- function(df){
	df$x <- df$x - 10
	my_plot <- ggplot(df, aes(x=x, y=y)) +
	geom_point(aes(col=team), size = 3)+
	xlim(10, 110)+
	ylim(0, 53.3)+
	theme(panel.background = element_rect(fill = "darkseagreen4",
															 colour = "darkseagreen4",
															 size = 0.5,
															 linetype = "solid"),
				panel.grid.major.x = element_line(size = 0.5, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.minor.x= element_line(size = 0.25, 
													linetype = "solid",
													colour = "ghostwhite"),
				panel.grid.major.y = element_blank(),
				panel.grid.minor.y = element_blank(),
				axis.line = element_line(colour = "ghostwhite",
														size = 3,
														linetype = "solid"),
				axis.text = element_text(size=20, face = "bold"),
				axis.title = element_text(size = 20, face = "bold"))+
	scale_x_continuous(breaks = seq(0, 100, 10), 
									minor_breaks = seq(0, 100, 5))					
	return(my_plot)
	}

	import_df <- function(name, return_team){
		df <- read.csv(name)
		df$vector_score2[df$team == 'football'] <- 0
		df$vector_score2 <- as.numeric(df$vector_score2)
		df$vector_score2[df$vector_score2 > 50] <- 50
		df$vector_score2[df$vector_score2 < -50] <- -50
		df$color <- floor((df$vector_score2 + 50) / 5)
		df$color[df$team == return_team] <- 0
		df$color[df$team == 'football'] <- 22
		df$shape = 21
		df$shape[df$team == 'away'] <- 25
		df$shape[df$team == 'home'] <- 22
		return(df)
	}
	
	colormap <- function(num){
	  map <- c("grey5", "grey10", "grey15", "grey20", "grey25", 
	           "grey30", 
	    "grey35", "grey40", "grey45", "grey50", "grey55", "grey60",
	    "grey65", "grey70", "grey75", "grey80", "grey85", "grey90",
	    "grey95", "grey100", "lightsalmon3", "red3")
	  return(map[num])
	}

	