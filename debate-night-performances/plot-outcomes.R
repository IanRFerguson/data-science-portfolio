# This script plots the outcome of the operations performed in semantic-valence.R
#
# Ian Richard Ferguson

path <- "~/Box Sync/JOB-CITY-USA/data-science-portfolio/debate-night-performances/"
setwd(path)

source("./semantic-valence.R")


# Lollipop plot
td.data_non %>% 
        ggplot(aes(x = minute, y = value, color = target)) +
        stat_summary() +
        geom_hline(yintercept = 0, linetype = "dashed", alpha=0.75, color="grey") +
        scale_color_brewer(palette = "Set1", direction = -1) +
        theme_minimal() +
        labs(x = "",
             y = "AFINN Polarity Value",
             color = "Candidate",
             title = "Presidential Debate: Twitter Reactions",
             subtitle = "September 29, 2020",
             caption = "All times in PST | Scraped by Ian Ferguson") +
        theme(plot.title = element_text(face = "bold", hjust = 0.5),
              plot.subtitle = element_text(hjust = 0.5),
              axis.title.x = element_text(vjust=2),
              plot.caption = element_text(hjust = 0.5, face="bold"))


# Negative valence barplot
td.data %>% 
        na.omit() %>% dplyr::filter(value < 0) %>%
        group_by(TARGET) %>% count(word) %>%
        arrange(desc(n)) %>% head(20) %>% 
        ggplot(aes(x = reorder(word, +n), y = n, fill = TARGET)) +
        geom_col(position="dodge", color="darkgrey") +
        scale_fill_brewer(palette = "Set1", direction = -1) +
        labs(x = "",
             y = "Word Frequency",
             fill = "Candidate",
             title = "Presidential Debate: Twitter Reactions",
             subtitle = "Negative Valence | September 29, 2020",
             caption = "All times in PST | Scraped by Ian Ferguson") +
        theme_minimal() +
        theme(plot.title = element_text(hjust = 0.5, face="bold"),
              plot.subtitle = element_text(hjust = 0.5 ),
              plot.caption = element_text(hjust = 0.5, face = "bold"))


# Positive valence barplot
td.data %>% 
        na.omit() %>% dplyr::filter(value > 0) %>%
        group_by(TARGET) %>% count(word) %>%
        arrange(desc(n)) %>% head(20) %>% 
        ggplot(aes(x = reorder(word, +n), y = n, fill = TARGET)) +
        geom_col(position="dodge", color="darkgrey") +
        scale_fill_brewer(palette = "Set1", direction = -1) +
        labs(x = "",
             y = "Word Frequency",
             fill = "Candidate",
             title = "Presidential Debate: Twitter Reactions",
             subtitle = "Positive Valence | September 29, 2020",
             caption = "All times in PST | Scraped by Ian Ferguson") +
        theme_minimal() +
        theme(plot.title = element_text(hjust = 0.5, face="bold"),
              plot.subtitle = element_text(hjust = 0.5 ),
              plot.caption = element_text(hjust = 0.5, face = "bold"))


# Smoothed time series plot
td.data_non %>% 
        ggplot(aes(x = minute, y = value, fill = target, color = target)) +
        stat_summary(fun.y = mean, geom="line") +
        stat_summary(geom = "ribbon", alpha = 0.15) +
        scale_fill_brewer(palette = "Set1", direction = -1) +
        scale_color_brewer(palette = "Set1", direction = -1) +
        theme_minimal() +
        coord_cartesian(ylim=c(-2,2)) +
        labs(x = "",
             y = "AFINN Valence Score",
             title = "Time Series of Twitter Responses",
             color = "Candidate",
             caption = "All times in PST | Scraped by Ian Richard Ferguson") +
        theme(plot.title = element_text(hjust = 0.5, face="bold"),
              legend.position = "none",
              plot.caption = element_text(hjust = 0.5, face='bold'))
