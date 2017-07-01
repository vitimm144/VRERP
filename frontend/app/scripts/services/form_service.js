angular.module('frontendApp').service(
  'formService',['$http', function($http, $state){

  // expose a saveRecipe function from your service
  // that takes a recipe object
  this.saveFormData = function(formData, url){
      // return a Promise object so that the caller can handle success/failure
    var method = formData.id ? 'PATCH' : 'POST';
    if (formData.id){
      url += formData.id;
    }
    return $http({
      method: method,
      url: url,
      data: formData
    })
  }
}]);


