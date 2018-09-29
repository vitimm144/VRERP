angular.module('frontendApp')
  .controller('SaleEditCtrl', function (
//  $rootScope,
  $scope,
  $stateParams,
  $state,
  Upload,
  $http,
  AuthService,
  formService,
  alertService,
  AUTH_TOKEN_PATH,
  AUTH_LOGOUT_PATH
){
  var sale_edit_ctrl = this;
  sale_edit_ctrl.base_url = 'api/sales/';
  sale_edit_ctrl.url = 'api/sales/';
  sale_edit_ctrl.file = null;
  console.log('stateParams');
  console.log($stateParams);
  
  sale_edit_ctrl.sale = {};
  
  $http.get('/api/users').then(function(data){
    console.log(data);
    sale_edit_ctrl.users = data.data.results;
  });
  $http.get('/api/employees').then(function(data){
    console.log(data);
    sale_edit_ctrl.sellers = data.data.results;
  });
  
  $http.get('/api/clients').then(function(data){
    console.log(data);
    sale_edit_ctrl.clients = data.data.results;
  });
  $http.get('/api/products').then(function(data){
    console.log(data);
    sale_edit_ctrl.products = data.data.results;
  });
  
  
  sale_edit_ctrl.select_config = {
    'options': sale_edit_ctrl.products,
    'placeholder': 'Digite um código ou um produto',
    'show_fields': [ 'description', 'code' ],
    'filter_fields': [ 'description', 'code' ],
    'out_fields': [ 'id' ],
    'min_checkbox': 0,
    'multiple': true,
    'filter_mode': 'contains'
  };
  
  sale_edit_ctrl.paymentModes = [
    {
      'mode': 'D',
      'description': 'Débito'
    }, {
      'mode': 'CA',
      'description': 'Crédito à Vista'
    }, {
      'mode': 'CP',
      'description': 'Crédito Parcelado'
    }, {
      'mode': 'A',
      'description': 'À Vista'
    }, {
      'mode': 'CHA',
      'description': 'Cheque à Vista'
    }, {
      'mode': 'CHP',
      'description': 'Cheque Parcelado'
    }, {
      'mode': 'VP',
      'description': 'Vale Parcelado'
    }, {
      'mode': 'V',
      'description': 'Vale'
    }
  ];

  if ($stateParams.saleId){
            console.log('stateParams ID');
    sale_edit_ctrl.url += $stateParams.saleId + '/';
    console.log('sale id ', $stateParams.saleId);
    $http.get(sale_edit_ctrl.url).then(function(data){
      console.log('Getting Sale');
      console.log(data);
      sale_edit_ctrl.sale = data.data;
    });
  }else{
    sale_edit_ctrl.sale = {
      'id': null,
      'products': [],
      'payments': [],
      'status': 0,
      'saleswoman': null,
      'client': null,
      'deduction': 0
    };
  }
  sale_edit_ctrl.addProduct = function(){
            console.log(sale_edit_ctrl.newProduct);
    sale_edit_ctrl.sale.products.push({
      'id': sale_edit_ctrl.sale.products.length+1,
      'product': sale_edit_ctrl.newProduct.product.id,
      'amount': sale_edit_ctrl.newProduct.amount,
      'price': sale_edit_ctrl.newProduct.product.products[0].id
    });
    sale_edit_ctrl.newProduct = null;
  }
  sale_edit_ctrl.addPayment = function(){
    sale_edit_ctrl.sale.payments.push({
      'id': sale_edit_ctrl.sale.payments.length+1,
      'mode': sale_edit_ctrl.newPayment.mode,
      'plots_amount': 1,
      'value': sale_edit_ctrl.newPayment.value
    });
    sale_edit_ctrl.newPayment = null;
  }

  sale_edit_ctrl.submit = function(){
    //Tratamento para salvar o produto na forma de product sale.
//    sale_edit_ctrl.sale.products.forEach(function(product){
//      
//      if (product.products){
//        product['price'] = product.products[0].id;
//      }
//              
//    });
            console.log('SALE');
    console.log(sale_edit_ctrl.sale);
       
    
    
    console.log('submit');
    console.log(sale_edit_ctrl.url);
    result = formService.saveFormData(
      sale_edit_ctrl.sale,
      sale_edit_ctrl.base_url
    );
    result.then(
    function (response) {
//      window.alert('ok');
      var message = 'Operação realizada com sucesso';
      alertService.message(message, 'success');
      $state.go( '^' );
    }, function (response) {
      var message = 'Erro na operação'
      alertService.message(message, 'danger');
    });
  } 
  
});



