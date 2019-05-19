angular.module('frontendApp')
  .controller('BehaviorSheetEditCtrl', function (
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
  var behavior_sheet_edit_ctrl = this;
  behavior_sheet_edit_ctrl.url = 'api/behavior_sheets/';
  console.log('stateParams');
  console.log($stateParams);
  behavior_sheet_edit_ctrl.behavior_sheet = {};
  
  behavior_sheet_edit_ctrl.today = function() {
    behavior_sheet_edit_ctrl.behavior_sheet.date = new Date();
  };
  behavior_sheet_edit_ctrl.today();

  behavior_sheet_edit_ctrl.clear = function() {
    behavior_sheet_edit_ctrl.behavior_sheet.date = null;
  };
  behavior_sheet_edit_ctrl.popup1 = {
    opened: false
  };

  $http.get('/api/employees').then(function(data){
    console.log(data);
    behavior_sheet_edit_ctrl.sellers = data.data.results;
  });
  
  behavior_sheet_edit_ctrl.inlineOptions = {
    customClass: getDayClass,
    minDate: new Date(),
    showWeeks: true
  };

  behavior_sheet_edit_ctrl.dateOptions = {
    dateDisabled: disabled,
    formatYear: 'yy',
    maxDate: new Date(2020, 5, 22),
    minDate: new Date(),
    startingDay: 1
  };
  
  behavior_sheet_edit_ctrl.toggleMin = function() {
    behavior_sheet_edit_ctrl.inlineOptions.minDate = behavior_sheet_edit_ctrl.inlineOptions.minDate ? null : new Date();
    behavior_sheet_edit_ctrl.dateOptions.minDate = behavior_sheet_edit_ctrl.inlineOptions.minDate;
  };

  behavior_sheet_edit_ctrl.toggleMin();

  behavior_sheet_edit_ctrl.open1 = function() {
    behavior_sheet_edit_ctrl.popup1.opened = true;
  };
  
  behavior_sheet_edit_ctrl.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  behavior_sheet_edit_ctrl.format = behavior_sheet_edit_ctrl.formats[0];
  behavior_sheet_edit_ctrl.altInputFormats = ['M!/d!/yyyy'];

  behavior_sheet_edit_ctrl.setDate = function(year, month, day) {
    behavior_sheet_edit_ctrl.behavior_sheet.date = new Date(year, month, day);
  };
  
  if ($stateParams.behaviorSheetId){
    console.log('behavior_sheet id ', $stateParams.behaviorSheetId);
     
    $http.get(behavior_sheet_edit_ctrl.url  + $stateParams.behaviorSheetId).then(function(data){
      console.log(data);
      behavior_sheet_edit_ctrl.behavior_sheet = data.data;
    });
  }
  
  behavior_sheet_edit_ctrl.submit = function(){
    if(typeof behavior_sheet_edit_ctrl.behavior_sheet.date === "object"){
      
      behavior_sheet_edit_ctrl.behavior_sheet.date = 
        behavior_sheet_edit_ctrl.behavior_sheet.date.toLocaleDateString('pt-br')
        .split('/')
        .reverse()
        .join('-')
    }

    
    result = formService.saveFormData(behavior_sheet_edit_ctrl.behavior_sheet, behavior_sheet_edit_ctrl.url);
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^', {},  {reload: true});
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  } 
  
  
  var tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  var afterTomorrow = new Date();
  afterTomorrow.setDate(tomorrow.getDate() + 1);
  behavior_sheet_edit_ctrl.events = [
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

      for (var i = 0; i < behavior_sheet_edit_ctrl.events.length; i++) {
        var currentDay = new Date(behavior_sheet_edit_ctrl.events[i].date).setHours(0,0,0,0);

        if (dayToCheck === currentDay) {
          return behavior_sheet_edit_ctrl.events[i].status;
        }
      }
    }

    return '';
  }
});



