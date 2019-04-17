library('lme4')
library('car')
library('dplyr')

df <- read.csv('~/Desktop/hackdartmouth-v/results/1000_logs.tsv', sep = '\t', header = TRUE)

m_f <- df %>% 
      group_by(Label) %>%
      summarise(total_count=n())
x<-chisq.test(select(m_f,total_count))

m_f_by_sub <- df %>%
              group_by(Label, Subject) %>%
              summarise(values=n())

m_f_by_sub$Label <- as.factor(m_f_by_sub$Label)
m_f_by_sub$Subject <- as.factor(m_f_by_sub$Subject)
model <- glm(values ~ Subject * Label, family = "poisson", data=m_f_by_sub)
Anova(model, type=2)