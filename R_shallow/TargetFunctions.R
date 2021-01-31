sphere<-function(point){
   sum <- 0.0        
   for(p in point)
   { 
     sum <- sum + p^2
   }
   return(sum)
}

rosenbrock<-function(point){
  sum <- 0.0
  for(i in 1:length(point))
  {
    if(i == length(point)) break
    sum <- sum + 100*(point[i]^2 - point[i+1])^2 + (point[i] - 1)^2 
  }
  return(sum)
}

rastrigin<-function(point){
  sum <- 0.0
  for(p in point){
    if(is.nan(cos(2*pi*p))){
      print(p)
    }
    sum <- sum + p^2 - 10*cos(2*pi*p) + 10
  }
  return(sum)
}