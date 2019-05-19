angular.module('frontendApp').service(
  'alertService',['$rootScope', '$timeout', function($rootScope, $timeout){

  // expose a saveRecipe function from your service
  // that takes a recipe object
  $rootScope.alertMessage = false;
  var type_dict = {
    
    danger:'alert alert-danger alert-dismissable',
    info:'alert alert-info alert-dismissable',
    success:'alert alert-success alert-dismissable',
    warning:'alert alert-warning alert-dismissable'
    
  };
  this.message = function(message, type){
    $rootScope.message = message;
    $rootScope.alertMessage = true;
    $rootScope.type = type_dict[type];

    $timeout(function(){
      $rootScope.alertMessage = false;
      $rootScope.message = "";
      
    }, 6000);
    
  }
  
}]);


