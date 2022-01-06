# This script assesses the aggregate semantic valence
# at every time point during Debate Night
#
# Special thanks to Dr. Billy Brady for his help with this code
# Ian Richard Ferguson


# ---- Imports
library(tidyverse)
library(maps)
library(tidytext)
library(lubridate)

path <- "."
setwd(path)

data <- read.csv("./Debate-output.csv")


# ---- Text cleaning

# Strip extra characters
data$Tweet <- gsub("https\\S*", "", data$Tweet)
data$Tweet <- gsub("@\\w+", "", data$Tweet) 

# Isolate variables of interest
reduced <- data %>% 
        dplyr::select(Created, User.Name, Tweet, TARGET)


# Create new time variable columns based on Created variable
reduced <- reduced %>% 
        mutate(date = ymd_hms(Created)) %>% 
        mutate(minute = with_tz(floor_date(date, unit = "minute")), tzone="America/Los Angeles") %>% 
        mutate(idx = row_number())


#  Isolate each word stem per Tweet
td.data <- reduced %>% 
        unnest_tokens(word, Tweet, token = "tweets") %>% 
        filter(!str_detect(word, "^[0-9]*$")) %>% 
        anti_join(stop_words) %>%
        mutate(word = SnowballC::wordStem(word))


# Assess AFINN polarity value and group by tweet (such that every tweet has len(tweet) polarity values)
td.data <- td.data %>% 
        left_join(get_sentiments("afinn")) %>% 
        group_by(idx)


# Average polarity scores by tweet index
td.data_non <- td.data %>% 
        summarise(target=first(TARGET),
                  value=mean(value, na.rm=T),
                  minute=first(minute)) %>% na.omit()
