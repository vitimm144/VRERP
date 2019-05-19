angular.module('frontendApp')
  .controller('WorkScheduleEditCtrl', function (
//  $rootScope,
//  $scope,
  $stateParams,
  $state,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  function initialize_timer(hour, minutes, seconds){
    var initialized_data = new Date();
    initialized_data.setHours(hour);
    initialized_data.setMinutes(minutes);
    initialized_data.setSeconds(seconds);
    return initialized_data; 
  }
  var work_schedule_edit_ctrl = this;
  work_schedule_edit_ctrl.url = 'api/work_schedules/';
  console.log('stateParams');
  console.log($stateParams);
  
  work_schedule_edit_ctrl.work_schedule = {
    "shift_start": initialize_timer(8, 0, 0),
    "shift_end": initialize_timer(18, 0, 0)
  };
  

  work_schedule_edit_ctrl.clear = function() {
    work_schedule_edit_ctrl.work_schedule.date = null;
  };

  $http.get('/api/employees').then(function(data){
    console.log(data);
    work_schedule_edit_ctrl.sellers = data.data.results;
  });
  work_schedule_edit_ctrl.months ={
    "JAN": "Janeiro",
    "FEV": "Feveireiro",
    "MAR": "Março",
    "ABR": "Abril",
    "MAI": "Maio",
    "JUN": "Junho",
    "JUL": "Julho",
    "AGO": "Agosto",
    "SET": "Setembro",
    "OUT": "Outubro",
    "NOV": "Novembro",
    "DEZ": "Dezembro"
  };
  
  
  work_schedule_edit_ctrl.years = [];
  for(var i = 1990; i <= 2040; i++){
      work_schedule_edit_ctrl.years.push(i.toString());

  }

  if ($stateParams.workScheduleId){
    console.log('work_schedule id ', $stateParams.workScheduleId);
     
    $http.get(work_schedule_edit_ctrl.url  + $stateParams.workScheduleId).then(function(data){
      console.log(data);
      work_schedule_edit_ctrl.work_schedule = data.data;
      shitf_start = data.data.shift_start;
      shitf_end = data.data.shift_end;
      shitf_start = shitf_start.split(':');
      work_schedule_edit_ctrl.work_schedule.shift_start = initialize_timer(
        parseInt(shitf_start[0]), 
        parseInt(shitf_start[1]),
        parseInt(shitf_start[2])
      );
      shitf_end = shitf_end.split(':');
      work_schedule_edit_ctrl.work_schedule.shift_end = initialize_timer(
        parseInt(shitf_end[0]), 
        parseInt(shitf_end[1]),
        parseInt(shitf_end[2])
      );
    });
  }else{
    var d = new Date();
    var n = d.getFullYear();

    work_schedule_edit_ctrl.work_schedule['year'] = n.toString();
    console.log(n);
    
  }
  
  work_schedule_edit_ctrl.submit = function(){
    work_schedule_edit_ctrl.work_schedule.shift_start = work_schedule_edit_ctrl.work_schedule.shift_start.toLocaleTimeString('pt-br') 
    work_schedule_edit_ctrl.work_schedule.shift_end = work_schedule_edit_ctrl.work_schedule.shift_end.toLocaleTimeString('pt-br') 
            console.log(work_schedule_edit_ctrl.work_schedule);
    result = formService.saveFormData(work_schedule_edit_ctrl.work_schedule, work_schedule_edit_ctrl.url);
    result.then(
    function (response) {
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^', {},  {reload: true});
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  }; 
  
});



