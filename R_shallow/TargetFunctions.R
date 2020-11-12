sum_of_squares<-function(point){
   sum <- 0.0        
   for(p in point)
   {
     sum <- sum + p^2
   }
   return(sum)
}