Algorithm <- setClass(

  "Algorithm",
  
  slots = c(
    objective_fun = "closure",
    P = "numeric"
  ),
  
  prototype=list(),
  
  
  sel_best<-function(){
    val_array <- c()
    for(p in 1:mi){
      val_array<-append(val_array, sum_of_squares(population[p,]))
    }
    min_index <- which.min(val_array) 
    return(population[min_index,])
  }
  
)