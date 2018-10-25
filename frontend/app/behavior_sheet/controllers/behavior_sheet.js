angular.module('frontendApp')
  .controller('BehaviorSheetCtrl', function (
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
  var behavior_sheet_ctrl = this;
  var url = '/api/behavior_sheets';
  behavior_sheet_ctrl.gridOptions = {};
  console.log('behavior_sheets_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        behavior_sheet_ctrl.behavior_sheets = response.data.results;
        console.log(behavior_sheet_ctrl.behavior_sheets);
      }, function(){
        console.log('erro ao pegar behavior_sheets');
      });
  } 
  behavior_sheet_ctrl.behavior_types = {
    "A": 'Advertência',
    "P": 'Prêmio'
  }
    
  update_grid();
  behavior_sheet_ctrl.edit = function(id){
    $state.go('behavior_sheets.edit', {"behaviorSheetId": id})
  }
  behavior_sheet_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar behavior_sheets');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

