angular.module('frontendApp')
  .controller('WorkScheduleCtrl', function (
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
  var work_schedule_ctrl = this;
  var url = '/api/work_schedules';
  work_schedule_ctrl.gridOptions = {};
  work_schedule_ctrl.employees = {};
  console.log('work_schedules_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        work_schedule_ctrl.work_schedules = response.data.results;
        console.log(work_schedule_ctrl.work_schedules);
      }, function(){
        console.log('erro ao pegar work_schedules');
      });
  } 
  $http.get('/api/employees').then(function(data){
    console.log(data);
    angular.forEach(data.data.results, function(result){
      work_schedule_ctrl.employees[result.id] = result.name
    });
            console.log(work_schedule_ctrl.employees);
    
  });
  work_schedule_ctrl.behavior_types = {
    "A": 'Advertência',
    "P": 'Prêmio'
  }
    
  update_grid();
  work_schedule_ctrl.edit = function(id){
    $state.go('work_schedules.edit', {"workScheduleId": id})
  }
  work_schedule_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar work_schedules');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

