angular.module('frontendApp')
  .controller('CareerCtrl', function (
  $rootScope,
  $scope,
  $state,
  $http,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  $rootScope.alertMessage = true;
  var career_ctrl = this;
  var url = '/api/careers';
  career_ctrl.gridOptions = {};
  console.log('careers_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        career_ctrl.careers = response.data.results;
        console.log(career_ctrl.careers);
      }, function(){
        console.log('erro ao pegar careers');
      });
  } 
    
  update_grid();
  career_ctrl.edit = function(id){
    $state.go('careers.edit', {"careerId":id});
  }
  
  career_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar careers');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

