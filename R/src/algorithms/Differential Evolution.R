P <- read.csv("../data.csv", header = FALSE)
P <- as.matrix(dat)
H <- P0
mi <- dim(P0)[1]
t <- 0
f <- 0.5
cr = 0.5


sum_of_squares<-function(point){
  sum <- 0.0
  for(p in point)
  {
    sum <- sum + p^2
  }
  return(sum)
}
  
crossover <- function(x,y){
  z <- vector()
  for (i in 1:dim(x)){
    a <- runif(1, 0, 1)
    if (a < cr) 
      append(z, y[i])
    else 
      append(z, x[i])
  }
  return(z)
}


tournanemt <- function(x,y)
{
  cond <- sum_of_squares(x) > sum_of_squares(y)
  if(cond) 
    return(y)
  else
    return(x)
}


while(t != 100)
{
  next_P <- P
  for (i in 1:mi)
  {
    indexes <- sample(1:mi, 3, replace=F)
    r <- P[indexes[1],]
    d_e <- P[indexes[2:3],]
    
    M <- r + f*(d_e[2] - d_e[1])
    
    O <- crossover(r, M)
    append(H,O)
    
    next_P[i,] <- tournanemt(P[i,], O)
  }
  P <- next_P
  t <- t+1
}

