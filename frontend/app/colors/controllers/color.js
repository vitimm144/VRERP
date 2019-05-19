angular.module('frontendApp')
  .controller('ColorCtrl', function (
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
  var color_ctrl = this;
  var url = '/api/colors';
  color_ctrl.gridOptions = {};
  console.log('colors_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        color_ctrl.colors = response.data.results;
        console.log(color_ctrl.colors);
      }, function(){
        console.log('erro ao pegar colors');
      });
  } 
    
  update_grid();
  color_ctrl.edit = function(id){
    $state.go('colors.edit', {"colorId":id});
  }
  
  color_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar colors');
    }); 
  }
    
});

