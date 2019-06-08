angular.module('frontendApp')
  .controller('UserCtrl', function (
  $rootScope,
  $scope,
  $http,
  $state,
  $transitions,
  AuthService,
  gridService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH,
  DTOptionsBuilder,
  DTColumnDefBuilder
) {
  $rootScope.alertMessage = false;
  var user_ctrl = this;
  var url = '/api/users';
  user_ctrl.gridOptions = {};
  user_ctrl.dtInstance = {};
  user_ctrl.dtOptions = DTOptionsBuilder.newOptions().withPaginationType(
    'full_numbers'
  ).withDisplayLength( 20 ).withLanguage(
    {
      "sEmptyTable": "Nenhum registro encontrado",
      "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
      "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
      "sInfoFiltered": "(Filtrados de _MAX_ registros)",
      "sInfoPostFix": "",
      "sInfoThousands": ".",
      "sLengthMenu": "_MENU_ resultados por página",
      "sLoadingRecords": "Carregando...",
      "sProcessing": "Processando...",
      "sZeroRecords": "Nenhum registro encontrado",
      "sSearch": "Pesquisar",
      "oPaginate": {
          "sNext": "Próximo",
          "sPrevious": "Anterior",
          "sFirst": "Primeiro",
          "sLast": "Último"
      },
      "oAria": {
          "sSortAscending": ": Ordenar colunas de forma ascendente",
          "sSortDescending": ": Ordenar colunas de forma descendente"
      }
    }
  ).withOption( 'scrollY', '75vh' ).withOption(
    'scrollCollapse',
    true
  ).withOption( 'paging', true );
  console.log('user_ctrl');
  var update_grid = function(){
    var result = gridService.update_grid(url)
    result.then(
      function(response){
        user_ctrl.users = response.data.results;
        console.log(user_ctrl.users);
      }, function(){
        console.log('erro ao pegar users');
      });
  } 
    
  update_grid();
  user_ctrl.excluir = function(url){
   gridService.delete_data(url).then(
    function(){
      $state.transitionTo($state.current, {}, { reload: true });
    }, function(){
      console.log('erro ao pegar users');
    }); 
  }
//  $scope.$on('event:loginConfirmed', function(evt){
//      $scope.loggedIn = true;
//  });
});

