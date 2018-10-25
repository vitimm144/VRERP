angular.module('frontendApp')
  .controller('WorkShiftEditCtrl', function (
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
  function initialize_time_picker(hour, minutes, seconds){
    var initialized_data = new Date();
    initialized_data.setHours(hour);
    initialized_data.setMinutes(minutes);
    initialized_data.setSeconds(seconds);
    return initialized_data 
  }
  function handle_time_value(date_time){
    return date_time.toLocaleTimeString('pt-br');
  }
  
  var work_shift_edit_ctrl = this;
  work_shift_edit_ctrl.url = 'api/work_shifts/';
  console.log('stateParams');
  console.log($stateParams);
  work_shift_edit_ctrl.work_shift = {
    "m_start": initialize_time_picker(8, 0, 0),
    "m_end": initialize_time_picker(12, 0, 0),
    "a_start": initialize_time_picker(13, 0, 0),
    "a_end": initialize_time_picker(18, 0, 0),
    "e_start": initialize_time_picker(0, 0, 0),
    "e_end": initialize_time_picker(0, 0, 0)
  };
  
  work_shift_edit_ctrl.allowances ={
    "FO": "Folga",
    "AT": "Atestado",
    "DE": "Declaração",
    "DR": "Descaso Remunerado"
  };
  
  work_shift_edit_ctrl.work_schedule_id = $stateParams.workScheduleId;
  $http.get('api/work_schedules/'  + work_shift_edit_ctrl.work_schedule_id).then(function(data){
    console.log(data);
    work_shift_edit_ctrl.work_schedule = data.data;
  });
  
  work_shift_edit_ctrl.today = function() {
    work_shift_edit_ctrl.work_shift.date = new Date();
  };
  work_shift_edit_ctrl.today();

  work_shift_edit_ctrl.clear = function() {
    work_shift_edit_ctrl.work_shift.date = null;
  };
  work_shift_edit_ctrl.popup1 = {
    opened: false
  };

  $http.get('/api/employees').then(function(data){
    console.log(data);
    work_shift_edit_ctrl.sellers = data.data.results;
  });
  
  work_shift_edit_ctrl.inlineOptions = {
    customClass: getDayClass,
    minDate: new Date(),
    showWeeks: true
  };

  work_shift_edit_ctrl.dateOptions = {
    dateDisabled: disabled,
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };
  
  work_shift_edit_ctrl.toggleMin = function() {
    work_shift_edit_ctrl.inlineOptions.minDate = work_shift_edit_ctrl.inlineOptions.minDate ? null : new Date();
    work_shift_edit_ctrl.dateOptions.minDate = work_shift_edit_ctrl.inlineOptions.minDate;
  };

  work_shift_edit_ctrl.toggleMin();

  work_shift_edit_ctrl.open1 = function() {
    work_shift_edit_ctrl.popup1.opened = true;
  };
  
  work_shift_edit_ctrl.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  work_shift_edit_ctrl.format = work_shift_edit_ctrl.formats[0];
  work_shift_edit_ctrl.altInputFormats = ['M!/d!/yyyy'];

  work_shift_edit_ctrl.setDate = function(year, month, day) {
    work_shift_edit_ctrl.work_shift.date = new Date(year, month, day);
  };
  
  work_shift_edit_ctrl.years = [{value: 'Year', disabled: true}];
  for(var i = 1990; i <= 2040; i++){
      work_shift_edit_ctrl.years.push({value: i});

  }

  var d = new Date();
  var n = d.getFullYear();

  work_shift_edit_ctrl.work_shift.year = n;
  console.log(n);
  
  
  if ($stateParams.workShiftId){
    console.log('work_shift id ', $stateParams.workShiftId);
     
    $http.get(work_shift_edit_ctrl.url  + $stateParams.workShiftId).then(function(data){
      console.log(data);
      work_shift_edit_ctrl.work_shift = data.data;
      
      m_start = data.data.m_start;
      m_start = m_start.split(':');
      work_shift_edit_ctrl.work_shift.m_start = initialize_time_picker(
        parseInt(m_start[0]), 
        parseInt(m_start[1]),
        parseInt(m_start[2])
      )

      m_end = data.data.m_end;
      m_end = m_end.split(':');
      work_shift_edit_ctrl.work_shift.m_end = initialize_time_picker(
        parseInt(m_end[0]), 
        parseInt(m_end[1]),
        parseInt(m_end[2])
      )
      
      a_start = data.data.a_start;
      a_start = a_start.split(':');
      work_shift_edit_ctrl.work_shift.a_start = initialize_time_picker(
        parseInt(a_start[0]), 
        parseInt(a_start[1]),
        parseInt(a_start[2])
      )

      a_end = data.data.a_end;
      a_end = a_end.split(':');
      work_shift_edit_ctrl.work_shift.a_end = initialize_time_picker(
        parseInt(a_end[0]), 
        parseInt(a_end[1]),
        parseInt(a_end[2])
      )
      
      e_start = data.data.e_start;
      e_start = e_start.split(':');
      work_shift_edit_ctrl.work_shift.e_start = initialize_time_picker(
        parseInt(e_start[0]), 
        parseInt(e_start[1]),
        parseInt(e_start[2])
      )

      e_end = data.data.e_end;
      e_end = e_end.split(':');
      work_shift_edit_ctrl.work_shift.e_end = initialize_time_picker(
        parseInt(e_end[0]), 
        parseInt(e_end[1]),
        parseInt(e_end[2])
      )
      
      work_shift_edit_ctrl.work_shift.date = new Date(work_shift_edit_ctrl.work_shift.date);
      
    });
  }
  
  work_shift_edit_ctrl.submit = function(){
    if(typeof work_shift_edit_ctrl.work_shift.date === "object"){
      
      work_shift_edit_ctrl.work_shift.date = 
        work_shift_edit_ctrl.work_shift.date.toLocaleDateString('pt-br')
        .split('/')
        .reverse()
        .join('-')
    }
    
    work_shift_edit_ctrl.work_shift.a_start = handle_time_value(work_shift_edit_ctrl.work_shift.a_start);
    work_shift_edit_ctrl.work_shift.a_end = handle_time_value(work_shift_edit_ctrl.work_shift.a_end);
    work_shift_edit_ctrl.work_shift.m_start = handle_time_value(work_shift_edit_ctrl.work_shift.m_start);
    work_shift_edit_ctrl.work_shift.m_end = handle_time_value(work_shift_edit_ctrl.work_shift.m_end);
    work_shift_edit_ctrl.work_shift.e_start = handle_time_value(work_shift_edit_ctrl.work_shift.e_start);
    work_shift_edit_ctrl.work_shift.e_end = handle_time_value(work_shift_edit_ctrl.work_shift.e_end);
    
    work_shift_edit_ctrl.work_shift.work_schedule = work_shift_edit_ctrl.work_schedule_id;
    
    result = formService.saveFormData(work_shift_edit_ctrl.work_shift, work_shift_edit_ctrl.url);
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
                      console.log('success');
      $state.go('^');
//      $state.go( 
//        'workschedule.work_shifts',
//        {workScheduleId: work_shift_edit_ctrl.work_schedule_id } 
//      );
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  } 
  
  work_shift_edit_ctrl.update = function() {
    var d = new Date();
    d.setHours( 14 );
    d.setMinutes( 0 );
    work_shift_edit_ctrl.mytime = d;
  };
  
  
  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  
  work_shift_edit_ctrl.events = [
    {
      date: tomorrow,
      status: 'full'
    },
    {
      date: afterTomorrow,
      status: 'partially'
    }
  ];
  
  // Disable weekend selection
  function disabled(data) {
    var date = data.date,
      mode = data.mode;
    return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
  }
  
  function getDayClass(data) {
    var date = data.date,
      mode = data.mode;
    if (mode === 'day') {
      var dayToCheck = new Date(date).setHours(0,0,0,0);

      for (var i = 0; i < work_shift_edit_ctrl.events.length; i++) {
        var currentDay = new Date(work_shift_edit_ctrl.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return work_shift_edit_ctrl.events[i].status;
        }
      }
    }

    return '';
  }
});



