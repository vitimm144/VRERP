angular.module('frontendApp').service(
  'alertService',['$rootScope', function($rootScope){

  // expose a saveRecipe function from your service
  // that takes a recipe object
            console.log('chamou alertservice');
  var type_dict = {
    
    danger:'alert alert-danger alert-dismissable',
    info:'alert alert-info alert-dismissable',
    success:'alert alert-success alert-dismissable',
    warning:'alert alert-warning alert-dismissable'
    
  };
  this.message = function(message, type){
            console.log('chamou alertservice message');
    $rootScope.message = message;
    $rootScope.type = type_dict[type];
    $rootScope.alertMessage = true;
    
  }
  
}]);


