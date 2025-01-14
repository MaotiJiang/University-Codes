library(dplyr)
library(readxl)

data = read_xlsx('C:/Users/任自芃/Desktop/EVA_Co.xlsx')
data = data[-1:-2,]
data2 = data %>% filter(!is.na(data$DelistedDate)) %>%
  arrange(DelistedDate)

data_M = data %>% filter(substr(data$Symbol,1,2)=='60'|substr(data$Symbol,1,3)=='000'|
                            substr(data$Symbol,1,3)=='001'|substr(data$Symbol,1,3)=='003') %>%
  arrange(IPODate) %>% 
  mutate(IPOyear = substr(IPODate,1,4))
data_M2 = data2 %>% filter(substr(data2$Symbol,1,2)=='60'|substr(data2$Symbol,1,3)=='000'|
                             substr(data2$Symbol,1,3)=='001'|substr(data2$Symbol,1,3)=='003') %>%
  arrange(DelistedDate) %>% 
  mutate(Dyear = substr(DelistedDate,1,4))
num_M = data_M %>% group_by(IPOyear) %>%
  summarize(new = n())
colnames(num_M) = c('year','new')
num_M2 = data_M2 %>% group_by(Dyear) %>%
  summarize(Delist = n())
colnames(num_M2) = c('year','delist')
num1 = left_join(num_M,num_M2,by='year') %>% 
  mutate(delist = ifelse(is.na(delist),0,delist),
         total = new-delist,
         cum.m = cumsum(total)) %>%
  na.omit()

data_SME = data %>% filter(substr(data$Symbol,1,3)=='002') %>%
  arrange(IPODate) %>% 
  mutate(IPOyear = substr(IPODate,1,4))
data_SME2 = data2 %>% filter(substr(data2$Symbol,1,3)=='002') %>%
  arrange(DelistedDate) %>% 
  mutate(Dyear = substr(DelistedDate,1,4))
num_SME = data_SME %>% group_by(IPOyear) %>%
  summarize(new = n())
colnames(num_SME) = c('year','new')
num_SME2 = data_SME2 %>% group_by(Dyear) %>%
  summarize(Delist = n())
colnames(num_SME2) = c('year','delist')
num2 = left_join(num_SME,num_SME2,by='year') %>% 
  mutate(delist = ifelse(is.na(delist),0,delist),
         total = new-delist,
         cum.sme = cumsum(total)) %>%
  na.omit()

data_GEM = data %>% filter(substr(data$Symbol,1,3)=='300') %>%
  arrange(IPODate) %>% 
  mutate(IPOyear = substr(IPODate,1,4))
data_GEM2 = data2 %>% filter(substr(data2$Symbol,1,3)=='300') %>%
  arrange(DelistedDate) %>% 
  mutate(Dyear = substr(DelistedDate,1,4))
num_GEM = data_GEM %>% group_by(IPOyear) %>%
  summarize(new = n())
colnames(num_GEM) = c('year','new')
num_GEM2 = data_GEM2 %>% group_by(Dyear) %>%
  summarize(Delist = n())
colnames(num_GEM2) = c('year','delist')
num3 = left_join(num_GEM,num_GEM2,by='year') %>% 
  mutate(delist = ifelse(is.na(delist),0,delist),
         total = new-delist,
         cum.g = cumsum(total)) %>%
  na.omit()

num = left_join(num1,num2,by='year') %>%
  select(year,cum.m,cum.sme) %>%
  mutate(cum.sme = ifelse(is.na(cum.sme),lag(cum.sme),cum.sme),
         cum.sme = ifelse(is.na(cum.sme),0,cum.sme))

num = left_join(num,num3,by='year')%>%
  select(year,cum.m,cum.sme,cum.g) %>%
  mutate(cum.g = ifelse(is.na(cum.g),lag(cum.g),cum.g),
         cum.g = ifelse(is.na(cum.g),0,cum.g))

num = num %>%
  mutate(cum.m = ifelse(year=='2021',cum.m+cum.sme,cum.m),
         cum.sme = ifelse(year=='2021',0,cum.sme)) %>%
  filter(year <= 2021) %>%
  mutate(total = cum.g+cum.m+cum.sme)



plot(num$cum.m~num$year,type='l',
     ylab = '主板公司数',
     xlab = '年份')
plot(num$cum.sme~num$year,type='l',
     ylab = '中小板公司数',
     xlab = '年份')
plot(num$cum.g~num$year,type='l',
     ylab = '创业板公司数',
     xlab = '年份')
plot(num$total~num$year,type='l',
     ylab = '三大板块公司数',
     xlab = '年份')
