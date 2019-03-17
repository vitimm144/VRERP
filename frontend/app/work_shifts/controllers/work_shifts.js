angular.module('frontendApp')
  .controller('WorkShiftCtrl', function (
  $rootScope,
  $scope,
  $state,
  $http,
  $transitions,
  $stateParams,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
) {
  
  var work_shift_ctrl = this;
  
  var url = '/api/work_shifts';
  work_shift_ctrl.work_schedule_id = $stateParams.workScheduleId;
  var filtered_url = '/api/work_shifts/?work_schedule=' + work_shift_ctrl.work_schedule_id;
  work_shift_ctrl.gridOptions = {};
  work_shift_ctrl.employees = {};
  console.log('work_shifts_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(filtered_url)
    result.then(
      function(response){
        work_shift_ctrl.work_shifts = response.data.results;
        console.log(work_shift_ctrl.work_shifts);
      }, function(){
        console.log('erro ao pegar work_shifts');
      });
  } 
  $http.get('/api/employees').then(function(data){
    console.log(data);
    angular.forEach(data.data.results, function(result){
      work_shift_ctrl.employees[result.id] = result.name
    });
    console.log(work_shift_ctrl.employees);
    
  });
  work_shift_ctrl.behavior_types = {
    "A": 'Advertência',
    "P": 'Prêmio'
  }
    
  update_grid();
  work_shift_ctrl.edit = function(id){
    $state.go(
      'work_schedules.work_shift_edit',
       {
         "workShiftId": id,
         "workScheduleId": work_shift_ctrl.work_schedule_id
       }
    )
  }
  work_shift_ctrl.excluir = function(url){
   gridService.delete_data().then(
    function(){
      update_grid();
    }, function(){
      console.log('erro ao pegar work_shifts');
    }); 
  }
  $transitions.onSuccess({}, function() {
    console.log('Transition on success');
    update_grid();
    
  });
    
});

