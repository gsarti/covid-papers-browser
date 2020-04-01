
const baseurl='http://localhost:5000';
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
    vm.total_count = 0;
    vm.dinamicitemsPerPage=10;
    vm.query="What is the effect od Covid-19 on pregnant women?";
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

    
    vm.getData = function(pageno){ 

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
            "license" : vm.license
          }
        }).then(function successCallback(response) {
             console.log(response);
             vm.articles=response.data;
            



             //simila la restiuzione del numeroo totale degli articoli, utile solo in fase demo
             vm.total_count = vm.articles.length;
             
             //simula la paginazione, utile solo in fase demo
             vm.articles = vm.articles.slice((pageno-1)*vm.dinamicitemsPerPage, ((pageno-1)*vm.dinamicitemsPerPage)+vm.dinamicitemsPerPage);

             console.log("pageno",vm.pageno);
             console.log("dinamicitemsPerPage",vm.dinamicitemsPerPage);
             console.log("query",vm.query);
             console.log("year",vm.year);
             console.log("author",vm.author);
             console.log("journal",vm.journal);
             console.log("license",vm.license);

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
        vm.articleid=articlecode;

        console.log("articleview");
        //cambio modalità grafica
        $(".articleview").show();
        $(".articlelist").hide();

        vm.article = {
          "abstract": "An emerging disease is one infectious epidemic caused by a newly transmissible pathogen, which has either appeared for the first time or already existed in human populations, having the capacity to increase rapidly in incidence as well as geographic range. Adapting to human immune system, emerging diseases may trigger large-scale pandemic spreading, such as the transnational spreading of SARS, the global outbreak of A(H1N1), and the recent potential invasion of avian influenza A(H7N9). To study the dynamics mediating the transmission of emerging diseases, spatial epidemiology of networked metapopulation provides a valuable modeling framework, which takes spatially distributed factors into consideration. This review elaborates the latest progresses on the spatial metapopulation dynamics, discusses empirical and theoretical findings that verify the validity of networked metapopulations, and the application in evaluating the effectiveness of disease intervention strategies as well.", 
          "authors": [
            "Lin WANG", 
            "Xiang Li"
          ], 
          "bibliography": [], 
          "cord_id": "i9tbix2v", 
          "doin": "10.1101/003889", 
          "journal": "", 
          "license": "biorxiv", 
          "microsoft_id": "", 
          "pmc_id": "", 
          "publish_time": "2014-06-04", 
          "pubmed_id": "", 
          "ranked_paragraphs": [
            {
              "score": 0.55, 
              "section": "Figure", 
              "spans": [], 
              "text": "Color online) Illustration of the individual-network frame of the networked metapopulation model. a The model is composed of a network of subpopulations. The disease transmission among subpopulations stems from the mobility of infected individuals. b Each subpopulation refers to a location, in which a population of individuals interplays according to the compartment rule (e.g., SIR) that induces local disease outbreaks. Individuals are transferred among subpopulations via mobility networks."
            }, 
            {
              "score": 0.53, 
              "section": "Two scales of dynamics: Recent progress", 
              "spans": [], 
              "text": "As stated in Section 2, the networked metapopulation model is constructed with the individual-network frame, where the individuals are organized into social units (e.g., villages, towns, cities) defined as subpopulations, which are connected by transportation networks that identify the mobility routes. The disease prevails inside each subpopulation due to interpersonal contacts, and is transmitted among subpopulations through the mobility of infected individuals. Typically, the model is comprised of two scales of dynamics: (i) disease invasion among different subpopulations; (ii) disease reaction within each subpopulation. Recent progresses on these two aspects are specified here."
            }, 
            {
              "score": 0.53, 
              "section": "Networked metapopulation.", 
              "spans": [
                [
                  155, 
                  425
                ], 
                [
                  0, 
                  154
                ]
              ], 
              "text": "Spatial distribution of populations and human mobility among connected locations are the pivotal elements mediating the transmission of pandemic diseases. To introduce spatially distributed factors into modeling substrates, it is intuitive to generalize the network model by defining each node as a subpopulation that has a specific location, in which a population of individuals interplays according to the compartment rule. People are also permitted to transfer among subpopulations through mobility networks. This individualnetwork frame organizes the entire system into networked populations, leading to an important class of model in modern epidemiology, namely, the networked metapopulation. Figure 2 illustrates the basic modeling structure."
            }, 
            {
              "score": 0.49, 
              "section": "Abstract", 
              "spans": [
                [
                  491, 
                  712
                ], 
                [
                  713, 
                  993
                ]
              ], 
              "text": "An emerging disease is one infectious epidemic caused by a newly transmissible pathogen, which has either appeared for the first time or already existed in human populations, having the capacity to increase rapidly in incidence as well as geographic range. Adapting to human immune system, emerging diseases may trigger large-scale pandemic spreading, such as the transnational spreading of SARS, the global outbreak of A(H1N1), and the recent potential invasion of avian influenza A(H7N9). To study the dynamics mediating the transmission of emerging diseases, spatial epidemiology of networked metapopulation provides a valuable modeling framework, which takes spatially distributed factors into consideration. This review elaborates the latest progresses on the spatial metapopulation dynamics, discusses empirical and theoretical findings that verify the validity of networked metapopulations, and the application in evaluating the effectiveness of disease intervention strategies as well."
            }, 
            {
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
            }, 
            {
              "score": 0.48, 
              "section": "Intra-subpopulation contagion.", 
              "spans": [], 
              "text": "Note that the characteristic contact rate might vary evidently in different subpopulations. As illustrated by empirical studies [122, 123] , in reality, location-specific factors are the potential drivers resulting in a substantial variation of disease incidences between populations. Inspired by this finding, Wang et al. [124, 125] introduced two categories of location-specific human contact patterns into a phenomenological reaction-commuting metapopulation model. A simple destination-driven scenario is considered first, where individual contact features are determined by the visited locations. Since the residence and the destination can be distinguished by the commuting mobility, an origin-driven scenario is also introduced, where the contacts of individuals are relevant to their subpopulations of residence. Figures 4(a) -(b) illustrate the modeling structures of these two scenarios."
            }, 
            {
              "score": 0.48, 
              "section": "Conclusions & outlooks", 
              "spans": [
                [
                  78, 
                  261
                ]
              ], 
              "text": "At the end of discussions, some open questions still deserve to be addressed. The development of the sophisticated computational techniques and the consideration of detailed human/population dynamics are quite important for the research of spatial epidemiology. However, it is also crucial to understand the fundamental principals governing the complex contagion phenomena [147] . In this regard, an interesting question poses itself, namely, whether it is possible to author/funder. All rights reserved. No reuse allowed without permission."
            }, 
            {
              "score": 0.46, 
              "section": "Inter-subpopulation invasion.", 
              "spans": [
                [
                  176, 
                  420
                ]
              ], 
              "text": "As illustrated by Fig. 3 a, air traffic network acts as a major channel serving human long-range travels, which mediates the pandemic transmission on a large geographic scale. The epidemic dynamics occurred under this scenario is well characterized by the reaction-diffusion processes [88] , which are also widely applied to model phenomena as diverse as genetic drift, chemical reactions, and population evolution [2] ."
            }, 
            {
              "score": 0.46, 
              "section": "Inter-subpopulation invasion.", 
              "spans": [], 
              "text": "Human beings are intelligent. Their risk perception and adaptive abilities promote the active response to epidemic outbreaks, which might in turn alter the disease propagation [99] [100] [101] . Many works [102] [103] [104] [105] [106] [107] [108] [109] [110] [111] have investigated the effect of disease-behavior mutual feedback on compartment models as well as network epidemiology, and recent research topics also begin the generalization to deal with human behavior of mobility response. For example, [112, 113] analyzed the impact of self-initiated mobility on the invasion threshold, showing a counterintuitive phenomenon that the mobility change of avoiding infected locations with high prevalences enhances the disease spreading to the entire system."
            }, 
            {
              "score": 0.44, 
              "section": "Intra-subpopulation contagion.", 
              "spans": [], 
              "text": "Other types of human behavioral diversity have also been considered recently. Motivated by the evidence that the diversity of travel habits or trip durations might yield heterogeneity in the sojourn time spent at destinations, Poletto et al. [127] studied the impact of large fluctuations of visiting durations on the epidemic threshold, finding that the positively-correlated and the negatively-correlated degreebased staying durations lead to distinct invasion paths to global outbreaks. Based on the observation that the specific curing (recovery) condition depends on the available medical resources supplied by local health sectors, Shen et al. [128] studied the effect of degree-dependent curing rates, which demonstrates that an optimal intervention performance with the largest epidemic threshold is obtained by designing the heterogeneous distribution of curing rates as a superlinear mode. Since the epidemic spreading is also relevant to casual contacts during public gatherings, Cao et al. [129] introduced the rendezvous effect into a bipartite metapopulation network, and showed that the rendezvous-induced transmission accelerates the pandemic outbreaks."
            }
          ], 
          "source": "biorxiv", 
          "title": "Spatial epidemiology of networked metapopulation: An overview", 
          "url": "https://doi.org/10.1101/003889", 
          "who_id": ""
        };


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

        console.log(vm.paragraphs);

      }
    vm.getData(vm.pageno); // Call the function to fetch initial data on page load.
});
