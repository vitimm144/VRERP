angular.module('frontendApp').service(
  'gridService',['$http', function($http){

  // expose a saveRecipe function from your service
  // that takes a recipe object
  this.update_grid = function(url){
  // return a Promise object so that the caller can handle success/failure
//    if (formData.id){
//      url += formData.id;
//    }
  
    return $http({
      method: 'GET',
      url: url,
    });
  }
  this.delete_data = function(url){
    return $http({
      method: 'DELETE',
      url: url 
    });
  }
}]);


