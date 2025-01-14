library(openxlsx)
library(dplyr)
library(imputeTS)
library(zoo)

#数据的导入与清洗
stock = read.xlsx('D:/z桌面/新建文件夹/FIN3080/HW4/Weekly Stock Price  Returns000511835/TRD_Week.xlsx')
stock = stock[-1:-2,]
stock$str=substr(stock$Trdwnt,start = 1,stop = 4)
stock=stock[stock$str!='2016',-c(3,5)]

market=read.xlsx('D:/z桌面/新建文件夹/FIN3080/HW4/Aggregated Weekly Market Returns135943323/TRD_Weekcm.xlsx')
market = market[-1:-2,]
market=market[market$Markettype=='5.0',]#选取沪深A股的市场回报率
n=count(market) #计算有效周数
market = market %>%
  mutate(flag = c(1:308))

#选取000001股票进行预处理以观察可能存在的问题
test = stock[1:308,]
test = test %>% select(Trdwnt) %>%
  mutate(flag = c(1:308))

market = market %>% left_join(test,by = c('flag','Trdwnt'))
market = market %>% select(Trdwnt,Cwretwdeq,flag)
stock = stock %>% left_join(market, by='Trdwnt')
colnames(stock) = c('id','date','ret','mktret','flag')

#导入risk free rate
rf=read.xlsx('D:/z桌面/新建文件夹/FIN3080/HW4/Risk-Free Rate221700199/TRD_Nrrate.xlsx')
rf = rf[-1:-2,-1]
colnames(rf) = c('date','risk-free rate')
rf$date=substr(rf$date,start=1,stop=7)
stock$rf=0.000286  #基于每日均相同的risk free rate直接构建周risk free rate


#开始进行数据处理
data = stock %>% na.omit() %>% 
  mutate(ret.rf = as.numeric(ret)-rf,
         mkt.rf = as.numeric(mktret) - rf)
#挑出三期数据
data1 = data[data$flag<=102,]
data2 = data %>% filter(flag>102&flag<=205)%>%
  na.omit()
data3 = data %>% filter(flag>205)%>%
  na.omit()
 

library(tidyr)
library(purrr)
library(broom)

#进行与个股相关的回归
model1 = data1 %>%
  group_by(id) %>% 
  summarise(model= list(lm(ret.rf~mkt.rf)), rsq = map_dbl(model, ~ summary(.x)$r.squared)) %>% ungroup() %>% #使用减去rf进行回归更为可靠
  mutate(model = map(model,tidy)) %>%
  unnest(model) %>% ungroup()
#挑选出beta
beta1 = model1 %>% filter(term=='mkt.rf')
head(beta1,20)


#进行step2 开始构建portfolio
p = c(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)
bp = beta1 %>% 
  summarise(qt = list(paste0(p*100,"%")),
            break.point = list(quantile(estimate, p, type=3)))%>% 
  unnest(cols=c(qt,break.point)) %>% ungroup()
bp = spread(bp,"qt","break.point")
port = beta1 %>%
  mutate(group= 
           cut(estimate,breaks=c(min(estimate),
                                 quantile(estimate,p,type=3),
                                 max(estimate)),
               include.lowest = T,
               order_result = T,
               labels=seq(1,10))) %>% ungroup()
port = port %>% select(id,group)
data2 = data2 %>% left_join(port,by='id')
data2=data2[complete.cases(data2$group),]#删去不存在分组的公司（该部分公司在第102周以后上市）

data.2 = data2 %>% group_by(date,group) %>% #进行周以及组别内的回报率计算
  summarise(ret.rf = mean(ret.rf),
            mkt.rf = mean(mkt.rf)) %>%
  ungroup()
model2 = data.2 %>%  #对数据表进行整合 融入R^2 p-value等
  group_by(group) %>% 
  summarise(model= list(lm(ret.rf~mkt.rf)),rsq = map_dbl(model, ~ summary(.x)$r.squared)) %>% ungroup() %>%
  mutate(model = map(model,tidy)) %>%
  unnest(model) %>% ungroup()
beta2 = model2 %>% filter(term=='mkt.rf') %>% na.omit()
alpha2 = model2 %>% filter(term=='(Intercept)') %>% na.omit()



data3 = data3 %>% left_join(port,by='id')
data3=data3[complete.cases(data3$group),]#删去不存在分组的公司（该部分公司在第205周以后上市）
data.3 = data3 %>% group_by(group) %>%
  summarise(ret.rf = mean(ret.rf),
            mkt.rf = mean(mkt.rf)) %>%ungroup()
b = beta2 %>% select(group,estimate)  #将beta与第三组数据进行合并
data.3 = data.3 %>% left_join(b,by='group')
model3 = data.3 %>%
  summarise(model= list(lm(ret.rf~estimate)),rsq = map_dbl(model, ~ summary(.x)$r.squared)) %>% ungroup() %>%
  mutate(model = map(model,tidy)) %>%
  unnest(model) %>% ungroup()
plot(data.3$ret.rf~data.3$estimate,type = 'p',
     xlab = 'Beta',
     ylab = 'Rp')
abline(lm(data.3$ret.rf~data.3$estimate),lwd=1,lty=1)
model31 = lm(data.3$ret.rf~data.3$estimate)
summary(model31)
