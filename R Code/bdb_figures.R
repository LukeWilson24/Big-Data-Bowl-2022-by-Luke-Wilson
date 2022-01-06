
require(ggplot2)
require(gridExtra)
require(reactable)
require(RColorBrewer)
# return_df <- read.csv('nn_eval.csv')
# classify_df <- read.csv('evaluate_classification_nn.csv')

# return_plot <- ggplot(return_df, aes(x=Predicted, y=Real)) +
#  theme_minimal(base_size=12) +
#  geom_point(col = ifelse(return_df$Real > 25, "gray50", "black")) +
#  geom_abline(intercept = 0, col='steelblue3', size=1) +
#  scale_x_continuous(breaks = seq(0, 16, by=2)) +
#  xlab('\nExpected Return Length') +
#  ylab('Real Return Length\n') +
#  ggtitle("Return Length vs Expected Return Length (2020)")

# reduced_return_df <- return_df[return_df$Real <= 25,]
#  reduced_return_plot <- ggplot(reduced_return_df, aes(x=Predicted, y=Real)) +
#   theme_minimal(base_size=12) +
#   geom_point(col = "black") +
#   geom_abline(intercept = 0, col='blue') +
#   xlab('\nPredicted Return Length') +
#   ylab('Real Return Length\n') +
#   ggtitle("Return Length vs Expected Return Length - Under 25 Yards (2020)")


# return_hist <- ggplot(return_df, aes(x = Real)) + 
#     theme_minimal(base_size=12) +
#     geom_histogram(boundary = 0, binwidth=5, fill = "steelblue3", color="black") +
#     scale_x_continuous(breaks = seq(-20, 100, by=5)) +
#     xlab('\nActual Return Lengths') +
#     ylab('Punt Returns') +
#     ggtitle("Return Length Distribution (2020)")

# rmse <- function(actual_data, predicted_data){
#     residuals <- actual_data - predicted_data
#     return(sqrt(mean((residuals^2))))
# }
# overestimate_returns <- nrow(return_df[return_df$Predicted > return_df$Real,]) / nrow(return_df)
# correct_classification_proportion <- nrow(classify_df[classify_df$pred_result == classify_df$result,]) / nrow(classify_df)



# dfr <- classify_df[classify_df$result == 'Return',]
# dff <- classify_df[classify_df$result == 'Fair Catch',]
# dfl <- classify_df[classify_df$result == 'Land',]

# cuts_r<-cut(classify_df$return_prob, breaks=seq(0,1, by=0.025))
# counts_r <-c(t(table(cuts_r)))
# labs_r <- levels(cuts_r)
# label_matrix_r <- cbind(lower = as.numeric( sub("\\((.+),.*", "\\1", labs_r) ), upper = as.numeric( sub("[^,]*,([^]]*)\\]", "\\1", labs_r) ))
# cut_frame_r <- data.frame(label_matrix_r,counts_r)
# midpoint_frame_r <- 0.5 * (cut_frame_r$lower + cut_frame_r$upper)
# value_r <- midpoint_frame_r * cut_frame_r$counts
# bar_frame_r <- data.frame(midpoint_frame_r, value_r)

# cuts_f<-cut(classify_df$fair_catch_prob, breaks=seq(0,1, by=0.025))
# counts_f <-c(t(table(cuts_f)))
# labs_f <- levels(cuts_f)
# label_matrix_f <- cbind(lower = as.numeric( sub("\\((.+),.*", "\\1", labs_f) ), upper = as.numeric( sub("[^,]*,([^]]*)\\]", "\\1", labs_f) ))
# cut_frame_f <- data.frame(label_matrix_f,counts_f)
# midpoint_frame_f <- 0.5 * (cut_frame_f$lower + cut_frame_f$upper)
# value_f <- midpoint_frame_f * cut_frame_f$counts
# bar_frame_f <- data.frame(midpoint_frame_f, value_f)

# cuts_l<-cut(classify_df$land_prob, breaks=seq(0,1, by=0.025))
# counts_l <-c(t(table(cuts_l)))
# labs_l <- levels(cuts_l)
# label_matrix_l <- cbind(lower = as.numeric( sub("\\((.+),.*", "\\1", labs_l) ), upper = as.numeric( sub("[^,]*,([^]]*)\\]", "\\1", labs_l) ))
# cut_frame_l <- data.frame(label_matrix_l,counts_l)
# midpoint_frame_l <- 0.5 * (cut_frame_l$lower + cut_frame_l$upper)
# value_l <- midpoint_frame_l * cut_frame_l$counts
# bar_frame_l <- data.frame(midpoint_frame_l, value_l)

# classify_plot_r <- ggplot(dfr, aes(x=return_prob)) + 
#     geom_histogram(data = classify_df, binwidth = 0.025, boundary = 0, fill = 'gray50') +
#     geom_histogram(boundary=0, binwidth = 0.025, colour = 'black', fill = 'lightcyan2') + 
#     geom_step(data = bar_frame_r, aes(x=cut_frame_r$lower, y=value_r, col='red')) + 
#     theme_minimal(base_size=12) +
#     guides(color = 'none') +
#     scale_x_continuous(name = 'Return Probability') +
#     scale_y_continuous(name = 'Punts') +
#     ggtitle("Return Probability Distribution (2020)")

# classify_plot_f <- ggplot(dff, aes(x=fair_catch_prob)) + 
#     geom_histogram(data = classify_df, binwidth = 0.025, boundary = 0, fill = 'gray50') +
#     geom_histogram(boundary=0, binwidth = 0.025, colour = 'black', fill = 'bisque') + 
#     geom_step(data = bar_frame_f, aes(x=cut_frame_f$lower, y=value_f, col='red')) + 
#     theme_minimal(base_size=12) +
#     guides(color = 'none')+
#     scale_x_continuous(name = 'Fair Catch Probability') +
#     scale_y_continuous(name = 'Punts') +
#     ggtitle("Fair Catch Probability Distribution (2020)")

# classify_plot_l <- ggplot(dfl, aes(x=land_prob)) + 
#     geom_histogram(data = classify_df, binwidth = 0.025, boundary = 0, fill = 'gray50') +
#     geom_histogram(boundary=0, binwidth = 0.025, colour = 'black', fill = 'plum2') + 
#     geom_step(data = bar_frame_l, aes(x=cut_frame_l$lower, y=value_l, col='red')) + 
#     theme_minimal(base_size = 12) +
#     guides(color = 'none')+
#     scale_x_continuous(name = 'Land Probability') +
#     scale_y_continuous(name = 'Punts') +
#     ggtitle("Land Proability Distribution (2020)")

# c_plot <- grid.arrange(classify_plot_r, classify_plot_f, classify_plot_l, ncol=3)

# roll_df <- read.csv('df_for_nn.csv')
# roll_df <- roll_df[(roll_df$is_returned == '[0, 0, 1]') & (roll_df$is_in_play == '1'),]
# roll_df$roll <- roll_df$kickLength - roll_df$nn_vertical_distance
# roll_df <- roll_df[!is.na(roll_df$roll),]
# roll_mean = mean(roll_df$roll)
# roll_plot <- ggplot(roll_df, aes(x=roll)) +
#      geom_histogram(colour = 'black', fill = 'thistle3', binwidth=1, boundary=0) + 
#      theme_minimal(base_size = 12) + 
#      scale_x_continuous(name = 'Roll Length', breaks=seq(-14, 32, by=2)) + 
#      scale_y_continuous(name = 'Punts') +
#      geom_vline(aes(xintercept = roll_mean), color = 'thistle4', linetype = 'dashed', size = 1) +
#      ggtitle("Roll Length Distribution (2018 - 2020)")

# ny_df <- read.csv('raw_evaluation.csv')
# ny_plot <- ggplot(ny_df, aes(x = Expected.Net.Yards, y = Real.Net.Yards, color = Play.Result)) + 
#     geom_point() +
#     theme_minimal(base_size = 12) + 
#     scale_color_manual(name = "Play Result", values = c("Return" = "forestgreen", "Fair Catch" = "wheat3", "Downed" = "palevioletred1",
#      "Out of Bounds" = "royalblue4", "Touchback" = "skyblue", "Muffed" = "seagreen1",  "Blocked Punt" = "Red")) +
#      scale_x_continuous(name = "Expected Net Yards") + 
#      scale_y_continuous(name = "Actual Net Yards") +
#      geom_abline(intercept = 0, color = "firebrick2", alpha = 0.5) +
#      ggtitle("Net Yards vs Expected Net Yards (2020)")

# # Line of code for displaying animation in kaggle notebook
# #<!-- <div style="width:100%;text-align: center;"> <img align=middle src="attachment:0908dab1-bf94-4559-b627-5f1bc5694265.gif" alt="2D Punt Animation" style="height:512px;margin-top:3rem;"> </div> -->

# make_color_pal <- function(colors, bias = 1) {
#   get_color <- colorRamp(colors, bias = bias)
#   function(x) rgb(get_color(x), maxColorValue = 255)
# }

# green_color <- make_color_pal(c("gray90", "mediumseagreen"), bias = 1)
# gray_color <- make_color_pal(c("white", "gray25"), bias = 2)
# inv_gray_color <- make_color_pal(c("lavenderblush3", "lavenderblush"), bias = 1)
# red_green_color <- make_color_pal(c("mediumseagreen", "gray80", "indianred1"), bias = 1)
# green_red_color <- make_color_pal(c("indianred1", "gray80", "mediumseagreen"), bias = 1)
# green_scale <- make_color_pal(c("white", "mintcream"), bias = 1)
# red_scale <- make_color_pal(c("white", "indianred1"), bias = 1)


punter_df <- read.csv('evaluated_punters.csv')
punter_df <- punter_df[punter_df$Punts >= 25,]
punter_df  <- subset(punter_df, select = - c(NFL.Id.Number, Median.ENY, SD.ENY, Q1.ENY,
                                             Q3.ENY, Adjusted.Average.ENY, Punt.Yards, Net.Yards))
punter_df$Return.. <- 100 * punter_df$Return..
punter_df$Fair.Catch.. <- 100 * punter_df$Fair.Catch..
punter_df$Downed.. <- 100 * punter_df$Downed..

punters_tab <- reactable(punter_df, 
    columns = list( Name = colDef(name = "Player", align = "left", minWidth = 100, style = list(fontWeight = "bold")),
                    Average.ENY = colDef(name = 'Avg ENY',
                                            style = function(value){
                                                value
                                                normalized <- (value - min(punter_df$Average.ENY)) / (max(punter_df$Average.ENY) - min(punter_df$Average.ENY))
                                                color <- green_color(normalized)
                                                list(background = color)
                                            }),  
                    Punts = colDef(name = "Punts", minWidth = 50), 
                    Avg.Punt.Yards = colDef(name = 'Avg Punt Yards'), 
                    Average.Net.Yards = colDef(name = "Avg Net Yards"), 
                    Return.. = colDef(name = "Return %",
                                            style = function(value){
                                                value
                                                color <- gray_color(value / 100)
                                                list(background = color)
                                            }), 
                    Fair.Catch.. = colDef(name = "Fair Catch %",
                                            style = function(value){
                                                value
                                                color <- gray_color(value / 100)
                                                list(background = color)
                                            }), 
                    Downed.. = colDef(name = "Land %",
                                            style = function(value){
                                                value
                                                color <- gray_color(value / 100)
                                                list(background = color)
                                            })
                    ),
    bordered = TRUE,
    highlight = TRUE,
    defaultSortOrder = "desc",
    defaultSorted = c("Average.ENY"),
    searchable = FALSE,
    outlined = TRUE,
    defaultPageSize = 100,
    defaultColDef = colDef(align = "center", headerStyle = list(background = "gray50"), minWidth = 75)
    )

returners_df <- read.csv('evaluated_returners.csv')
returners_df <- returners_df[returners_df$Returns >= 10,]
returners_df <- subset(returners_df, select = -c(NFL.Id.Number, Q1.RYOE, Q3.RYOE,
                                                 SD.RYOE, Return.Yards, Adjusted.Average.RYOE,  Returns.Over.Expected))

returners_tab <- reactable(returners_df, 
    columns = list( Name = colDef(name = "Player", align = "left", minWidth = 100, style = list(fontWeight = "bold", borderRight = "1px solid rgba(0, 0, 0, 0.2)")),
                    Returns = colDef(name = "Punt Returns", minWidth = 50), 
                    Average.RYOE = colDef(name = 'Average RYOE',
                                            style = function(value){
                                                value
                                                if (value > 0){
                                                    normalized <- 0.5 * (value / max(returners_df$Average.RYOE)) + 0.5
                                                }
                                                else{
                                                    normalized <- 0.5 - 0.5 * (value / min(returners_df$Average.RYOE))
                                                }
                                                color <- green_red_color(normalized)
                                                list(background = color)
                                            }),
                    Return.Proportion.Over.Expected = colDef(name = "Return % Over Expected", 
                    style = function(value){
                                            color <- green_red_color(value)
                                            list(fontWeight = 600, color = color)
                                            }) ,
                    Median.RYOE = colDef(name = "Median RYOE", 
                    style = function(value){
                                            if (value > 0){
                                                    normalized <- 0.5 * (value / max(returners_df$Median.RYOE)) + 0.5
                                                }
                                            else{
                                                    normalized <- 0.5 - 0.5 * (value / min(returners_df$Median.RYOE))
                                                }
                                            color <- green_red_color(normalized)
                                            list(fontWeight = 600, color = color)
                                            }),          
                    Average.Return.Yards = colDef(name = "Avg Return Length")
                    ),
    bordered = TRUE,
    highlight = TRUE,
    defaultSortOrder = "desc",
    defaultSorted = c("Average.RYOE"),
    searchable = FALSE,
    defaultPageSize = 100,
    defaultColDef = colDef(align = "center", headerStyle = list(background = "gray50"), minWidth = 75))

teams_df <- read.csv('evaluated_teams.csv')
teams_df <- teams_df[teams_df$Returns.Against >= 25,]
teams_df[teams_df$Team == 'Oakland Raiders', 1] = "Las Vegas Raiders"
teams_df <- subset(teams_df, select = -c(Abbreviation, SD.RYOE, Q1.RYOE, Q3.RYOE, Return.Yards.Against, Adjusted.Average.RYOE, Returns.Under.Expected))

teams_tab <- reactable(teams_df, 
    columns = list( Team = colDef(name = "Team", align = "left", minWidth = 150, style = list(fontWeight = "bold", borderRight = "1px solid rgba(0, 0, 0, 0.2)")),
                    Returns.Against = colDef(name = "Returns Against", minWidth = 50), 
                    Average.RYOE = colDef(name = 'Average RYOE',
                                            style = function(value){
                                                value
                                                if (value > 0){
                                                    normalized <- 0.5 * (value / max(teams_df$Average.RYOE)) + 0.5
                                                }
                                                else{
                                                    normalized <- 0.5 - 0.5 * (value / min(teams_df$Average.RYOE))
                                                }
                                                
                                                color <- red_green_color(normalized)
                                                list(background = color)
                                            }), 
                    Median.RYOE = colDef(name = "Median RYOE", 
                    style = function(value){
                                            if (value > 0){
                                                    normalized <- 0.5 * (value / max(teams_df$Median.RYOE)) + 0.5
                                                }
                                            else{
                                                    normalized <- 0.5 - 0.5 * (value / min(teams_df$Median.RYOE))
                                                }
                                            color <- red_green_color(normalized)
                                            list(fontWeight = 600, color = color)
                                            }),
                    Return.Proportion.Under.Expected = colDef(name = "Return % Under Expected", 
                    style = function(value){
                                            color <- red_green_color(1 - value)
                                            list(fontWeight = 600, color = color)
                                            }) ,
                    Avg.Return.Yards.Against = colDef(name = "Avg Return Length Against")
                    ),
    bordered = TRUE,
    highlight = TRUE,
    defaultSortOrder = "asc",
    defaultSorted = c("Average.RYOE"),
    searchable = FALSE,
    defaultPageSize = 100,
    defaultColDef = colDef(align = "center", headerStyle = list(background = "gray50")))

# ery_df <- read.csv('evaluate_ery.csv')
# ery_over_expected <- nrow(ery_df[ery_df$ry > ery_df$ery,]) / nrow(ery_df)