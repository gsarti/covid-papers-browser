
const baseurl='http://0.0.0.0:5000';
//**gli articoli con più di 150 caratteri vengono troncati, la scritta scchow more sostituisce il testo eliminato*/
const show_text = function(){ /* to make sure the script runs after page load */

console.log("show_text");

$('.item').each(function(event){ /* select all divs with the item class */

    var max_length = 600; /* set the max content length before a read more link will be added */

    if($(this).html().length > max_length){ /* check for content length */


    var short_content = $(this).html().substr(0,max_length); /* split the content in two parts */
    var long_content  = $(this).html().substr(max_length);


    if($(this).find('a.read_more').length==0)
        $(this).html(short_content+'<a href="#" class="read_more"> ...Show More</a>'+
                '<span class="more_text" style="display:none;">'+long_content+'</span>'); /* Alter the html to allow the read more functionality */

    $(this).find('a.read_more').click(function(event){ /* find the a.read_more element within the new html and bind the following code to it */

        event.preventDefault(); /* prevent the a from changing the url */

        $(this).parents('.item').find('.more_text').show(); /* show the .more_text span */
        $(this).hide(); /* hide the read more button */

    });



    }

});


};


var app = angular.module('angularTable', ['angularUtils.directives.dirPagination']);



app.controller('listdata',function($http,$scope,$timeout){



    var vm = this;

    // Simple GET request example:
    $http({
      method: 'GET',
      url: baseurl+'/years',
      data:{}
    }).then(function successCallback(response) {
        vm.years=response.data;

        setTimeout(function(){
            /**
             * i selectpicker devono settarsi quando i dati vengono aggiornati
             * 
             */
            $('#year-selectpicker').selectpicker("refresh");
      
      
          },1000);
      
      }, function errorCallback(response) {
        vm.years=[];
      });
    
   
    vm.year=[];


    $http({
      method: 'GET',
      url: baseurl+'/authors',
      data:{}
    }).then(function successCallback(response) {
        console.log(response);
        vm.authors=response.data;
        setTimeout(function(){
          /**
           * i selectpicker devono settarsi quando i dati vengono aggiornati
           * 
           */
          $('#author-selectpicker').selectpicker("refresh");
    
    
        },1000);
      }, function errorCallback(response) {
        vm.authors=[];
      });
    

    $http({
      method: 'GET',
      url: baseurl+'/journals',
      data:{}
    }).then(function successCallback(response) {
        vm.journals=response.data;
        setTimeout(function(){
          /**
           * i selectpicker devono settarsi quando i dati vengono aggiornati
           * 
           */
          $('#journal-selectpicker').selectpicker("refresh");
    
    
        },1000);
      }, function errorCallback(response) {
        vm.journals=[];
      });

    $http({
      method: 'GET',
      url: baseurl+'/licenses',
      data:{}
    }).then(function successCallback(response) {
        vm.licenses=response.data;
        setTimeout(function(){
            /**
             * i selectpicker devono settarsi quando i dati vengono aggiornati
             * 
             */
            $('#license-selectpicker').selectpicker("refresh");
      
      
          },1000);
      }, function errorCallback(response) {
        vm.licenses=[];
      });

 


    //article view

    vm.articles = []; //declare an empty array
    vm.pageno = 1; // initialize page no to 1
    vm.total_count = 1;
    vm.dinamicitemsPerPage=10;
    vm.query="";
    //vm.itemsPerPage = $scope.dinamicitemsPerPage; //this could be a dynamic value from a drop down


    vm.article={};
    vm.articleid=0;
    vm.paragraphs=[];




    vm.delete_filters = function(){
        console.log("delete filters");
        vm.year=[];
        vm.author=[];
        vm.journal=[];
        vm.license=[];

        $('#year-selectpicker').val('default').selectpicker("refresh");
        $('#author-selectpicker').val('default').selectpicker("refresh");
        $('#journal-selectpicker').val('default').selectpicker("refresh");
        $('#license-selectpicker').val('default').selectpicker("refresh");


        vm.getData(1);
    }


    vm.update_button = function(){
      console.log("update button");
  
      $("#submit-update").show();

  
   };

    vm.exampleSearch = function(){
      $("#search").val("Is chloroquine effective against SARS-CoV-2?")
      vm.query="Is chloroquine effective against SARS-CoV-2?"
      vm.getData(1)
    };

    var input_bar = document.getElementById("search");

    input_bar.addEventListener("keyup", function(event) {
      // Number 13 is the "Enter" key on the keyboard
      if (event.keyCode === 13) {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        vm.getData(1);
      }
    }); 

    
    vm.getData = function(pageno){ 
      vm.article={}
      console.log(vm.authors);
      /**
       * Modalità lista di articoli
       * 
       * 
       */

          console.log("getData");
          $(document).ready(function(){

            setTimeout(function(){
              /**
               * i selectpicker devono settarsi quando i dati vengono aggiornati
               * 
               */
              $('#year-selectpicker').selectpicker();
              $('#author-selectpicker').selectpicker();
              $('#journal-selectpicker').selectpicker();
              $('#license-selectpicker').selectpicker();

              $("#submit-update").hide(); //nascondo il tasto di update perché la ricerca è sincronizzata con il filtro


              if(pageno==1 && vm.total_count>0) //per risolvere bug di paginationjs che non setta a 1 la paginazione quando pageno ritorna a 1
                $('.pagination.ng-scope').find("a")[0].click();
        
        
            },1);
        
        });


        console.log("articlelist");
        //cambio modalità 
        $(".articleview").hide();
        $(".articlelist").show();
        $("#description").show();

        //non c'è alcun articolo selezionato
        vm.articleid=0;
        
        vm.pageno=pageno;


        
        //**recupero le info dell'articolo */
        $http({
          method: 'POST',
          url: baseurl+'/paper',
          data:{ 
            "query": vm.query,
            "year" : vm.year,
            "author" : vm.author,
            "journal" : vm.journal,
            "license" : vm.license,
            "count" : vm.dinamicitemsPerPage,
            "page": vm.pageno
           }
        }).then(function successCallback(response) {
             console.log(response);
             vm.articles=response.data.data;
            

             //simila la restiuzione del numeroo totale degli articoli, utile solo in fase demo
             vm.total_count = response.data.total;

             if (typeof vm.total_count == "undefined") {
               $(".articlelist-body").hide()
             } else {
              $(".articlelist-body").show()
             }
             
             //simula la paginazione, utile solo in fase demo
             //vm.articles = vm.articles.slice((pageno-1)*vm.dinamicitemsPerPage, ((pageno-1)*vm.dinamicitemsPerPage)+vm.dinamicitemsPerPage);

             console.log("pageno",vm.pageno);
             console.log("dinamicitemsPerPage",vm.dinamicitemsPerPage);
             console.log("query",vm.query);
             console.log("year",vm.year);
             console.log("author",vm.author);
             console.log("journal",vm.journal);
             console.log("license",vm.license);
             console.log("len", vm.total_count);

             //dopo aver renderizzato gli articoli chiamo la funzione showtext che mostra il tasto show more per testi più lunghi di 150 caratteri
             $timeout(function() {
                show_text();
             },2);  


          }, function errorCallback(response) {
            vm.articles=[];
          });







    };

    vm.getarticleData = function(articlecode){ 


      /**
       * Modalità articolo singolo il cui codice è articlecode
       * 
       * 
       */

        event.preventDefault(); 
        vm.cord_id=articlecode;

        console.log("articleview");
        //cambio modalità grafica
        $(".articleview").show();
        $(".articlelist").hide();
        $("#description").hide();

        $http({
          method: 'POST',
          url: baseurl+'/singlearticle',
          data:{ 
            "query": vm.query,
            "cord_id":vm.cord_id,
            "count":10
           }
        }).then(function successCallback(response) {
             console.log(response);
             vm.article=response.data;

             vm.paragraphs=[];

             vm.article.ranked_paragraphs.forEach( function(paragraph){
     
               var start = 0;
               var tokens=[];
     
               paragraph.spans.sort(function(a, b) {
                 
                 if (a[0] < b[0]) return -1;
                 if (a[0] > b[0]) return 1;
                 return 0;
               }).forEach( function(span){
     
                
                 if(start!=span[0]){
                   var token={};
                   token.text=paragraph.text.slice(start, span[0]);
                   token.class="";
                   tokens.push(token);
                 }
                 var token={};
                 token.text=paragraph.text.slice(span[0], span[1]);
                 token.class="paragraph";
                 tokens.push(token);
                 start=span[1]+1;
     
               });
               var token={};
               token.text=paragraph.text.slice(start,paragraph.text.length);
               token.class="";
               tokens.push(token);
     
               vm.paragraphs.push(tokens);
     
             });


          }, function errorCallback(response) {
            vm.article=[];
          });


        console.log("getarticleData");

        /**
         *  analizzo la lista dei paragrafi con gli spam da evidenzare.
         *  restituisco una lista di token specificando quali sono da evidenziare (classe paragraph)
         * {
              "score": 0.49, 
              "section": "Networked metapopulation.", 
              "spans": [
                [
                  286, 
                  564
                ], 
                [
                  0, 
                  285
                ]
              ], 
              "text": "It is not convincing to describe the large-scale spatial pandemic spreading by directly following the routine of network epidemiology, since the network perspective still concerns the epidemic outbreak in a single population, despite considering the connectivity structure among hosts. This can hardly capture the key features of spatial transmission of infectious diseases: epidemics prevails inside separate locations such as cities, each of which can be regarded as a pop-ulation, and is transmitted among populations through the travel of infected individuals."
            }


[{text: "Color online) Illustration of the individual-network frame of the networked metapopulation model. a The model is composed of a network of subpopulations. The disease transmission among subpopulations stems from the mobility of infected individuals. b Each subpopulation refers to a location, in which a population of individuals interplays according to the compartment rule (e.g., SIR) that induces local disease outbreaks. Individuals are transferred among subpopulations via mobility networks."
class: "",
$$hashKey: "object:139",
__proto__: Object,
$$hashKey: "object:119"},
{text: "As stated in Section 2, the networked metapopulati…ogresses on these two aspects are specified here.", class: "", $$hashKey: "object:141"}]         * 
         

*/
        

      }
    vm.getData(vm.pageno); // Call the function to fetch initial data on page load.
});
