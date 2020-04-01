

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


    vm.years=[
      [
        "2020", 
        3578
      ], 
      [
        "2019", 
        3154
      ], 
      [
        "2018", 
        3106
      ], 
      [
        "2016", 
        2981
      ], 
      [
        "2017", 
        2921
      ], 
      [
        "2015", 
        2854
      ], 
      [
        "2014", 
        2622
      ], 
      [
        "2013", 
        2403
      ], 
      [
        "2012", 
        2114
      ], 
      [
        "2011", 
        2021
      ], 
      [
        "2009", 
        1858
      ], 
      [
        "2010", 
        1839
      ], 
      [
        "2008", 
        1639
      ], 
      [
        "2006", 
        1562
      ], 
      [
        "2007", 
        1480
      ], 
      [
        "2004", 
        1477
      ], 
      [
        "2005", 
        1355
      ], 
      [
        "2003", 
        972
      ], 
      [
        "1992", 
        328
      ], 
      [
        "1991", 
        309
      ]
    ];
    vm.year=[];


    vm.authors=[[
      "Perlman, Stanley", 
      154
    ], 
    [
      "Drosten, Christian", 
      144
    ], 
    [
      "Yuen, Kwok-Yung", 
      144
    ], 
    [
      "Baric, Ralph S.", 
      139
    ], 
    [
      "Jiang, Shibo", 
      139
    ], 
    [
      "Enjuanes, Luis", 
      125
    ], 
    [
      "Snijder, Eric J.", 
      110
    ], 
    [
      "Weiss, Susan R.", 
      97
    ], 
    [
      "Wang, Lin-Fa", 
      93
    ], 
    [
      "Du, Lanying", 
      89
    ], 
    [
      "Gao, George F.", 
      86
    ], 
    [
      "Li, Yan", 
      83
    ], 
    [
      "Saif, Linda J.", 
      81
    ], 
    [
      "Memish, Ziad A.", 
      76
    ], 
    [
      "Buonavoglia, Canio", 
      71
    ], 
    [
      "Feldmann, Heinz", 
      70
    ], 
    [
      "Decaro, Nicola", 
      70
    ], 
    [
      "P\u00f6hlmann, Stefan", 
      70
    ], 
    [
      "Wang, Wei", 
      69
    ], 
    [
      "Woo, Patrick C. Y.", 
      69
    ]];
    vm.author=[]

  

  vm.journals=[[
    "", 
    4050
  ], 
  [
    "Journal of Virology", 
    1736
  ], 
  [
    "PLoS One", 
    1567
  ], 
  [
    "Virology", 
    864
  ], 
  [
    "Emerg Infect Dis", 
    749
  ], 
  [
    "The Lancet", 
    587
  ], 
  [
    "Viruses", 
    569
  ], 
  [
    "Arch Virol", 
    504
  ], 
  [
    "Virus Research", 
    494
  ], 
  [
    "Sci Rep", 
    491
  ], 
  [
    "Vaccine", 
    484
  ], 
  [
    "Veterinary Microbiology", 
    440
  ], 
  [
    "Journal of Virological Methods", 
    392
  ], 
  [
    "Journal of Clinical Virology", 
    378
  ], 
  [
    "PLoS Pathog", 
    361
  ], 
  [
    "Virol J", 
    357
  ], 
  [
    "Antiviral Research", 
    346
  ], 
  [
    "Proceedings of the National Academy of Sciences", 
    341
  ], 
  [
    "The Lancet Infectious Diseases", 
    339
  ], 
  [
    "Journal of Clinical Microbiology", 
    335
  ]];
  vm.journal=[];

  vm.licenses=[
    [
      "els-covid", 
      18397
    ], 
    [
      "unk", 
      10774
    ], 
    [
      "cc-by", 
      8858
    ], 
    [
      "no-cc", 
      3630
    ], 
    [
      "cc-by-nc", 
      1159
    ], 
    [
      "cc-by-nc-nd", 
      668
    ], 
    [
      "biorxiv", 
      631
    ], 
    [
      "medrvix", 
      587
    ], 
    [
      "cc-by-nc-sa", 
      471
    ], 
    [
      "cc0", 
      260
    ], 
    [
      "cc-by-nd", 
      4
    ], 
    [
      "pd", 
      3
    ], 
    [
      "cc-by-sa", 
      2
    ]
  ];

  vm.license=[];



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


              if(pageno==1) //per risolvere bug di paginationjs che non setta a 1 la paginazione quando pageno ritorna a 1
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
        vm.articles = [
                        {
                          "abstract": "", 
                          "authors": "Kupferschmidt, K., Cohen, J.", 
                          "cord_id": "ujoil8pq", 
                          "journal": "Science", 
                          "title": "Can China's COVID-19 strategy work elsewhere?"
                        }, 
                        {
                          "abstract": "A key component of the response to emerging infections is consideration of special populations, including pregnant women. Successful pregnancy depends on adaptation of the woman's immune system to tolerate a genetically foreign fetus. Although the immune system changes are not well understood, a shift from cell-mediated immunity toward humoral immunity is believed to occur. These immunologic changes may alter susceptibility to and severity of infectious diseases in pregnant women. For example, pregnancy may increase susceptibility to toxoplasmosis and listeriosis and may increase severity of illness and increase mortality rates from influenza and varicella. Compared with information about more conventional disease threats, information about emerging infectious diseases is quite limited. Pregnant women's altered response to infectious diseases should be considered when planning a response to emerging infectious disease threats.", 
                          "authors": "Jamieson, Denise J., Theiler, Regan N., Rasmussen, Sonja A.", 
                          "cord_id": "ytzglkgk", 
                          "journal": "Emerg Infect Dis", 
                          "title": "Emerging Infections and Pregnancy"
                        }, 
                        {
                          "abstract": "", 
                          "authors": "Cowper, A.", 
                          "cord_id": "3ztfw8lj", 
                          "journal": "BMJ", 
                          "title": "Covid-19: are we getting the communications right?"
                        }, 
                        {
                          "abstract": "", 
                          "authors": "Anker, Martha", 
                          "cord_id": "3gnfbgeo", 
                          "journal": "Emerg Infect Dis", 
                          "title": "Pregnancy and Emerging Diseases"
                        }, 
                        {
                          "abstract": "", 
                          "authors": "Lipsitch, Marc, Swerdlow, David L., Finelli, Lyn", 
                          "cord_id": "qmyb365g", 
                          "journal": "New England Journal of Medicine", 
                          "title": "Defining the Epidemiology of Covid-19 \u2014 Studies Needed"
                        }, 
                        {
                          "abstract": "Objective: To investigate the clinical characteristics and placental pathology of 2019-nCoV infection in pregnancy, and to evaluate intrauterine vertical transmission potential of 2019-nCoV infection. Methods: The placentas delivered from pregnant women with confirmed 2019-nCoV infection which were received in the Department of Pathology, Union Hospital, Tongji Medical College, Huazhong University of Science and Technology collected by February 4th, 2020 and retrospectively studied. Their clinical material including placental tissue and lung CT, and laboratory results were collected, meanwhile, nucleic acid detection of 2019-nCoV of the placentas were performed by RT-PCR. Results: Three placentas delivered from pregnant women with confirmed 2019-nCoV infection, who were all in their third trimester with emergency caesarean section. All of the three patients presented with fever (one before caesarean and two in postpartum), and had no significant leukopenia and lymphopenia. Neonatal throat swabs from three newborns were tested for 2019-nCoV, and all samples were negative for the nucleic acid of 2019-nCoV. One premature infant was transferred to Department of Neonatology due to low birth weight. By the end of February 25, 2020, none of the three patients developed severe 2019-nCoV pneumonia or died(two patients had been cured and discharged, while another one had been transferred to a square cabin hospital for isolation treatment). There were various degrees of fibrin deposition inside and around the villi with local syncytial nodule increases in all three placentas. One case of placenta showed the concomitant morphology of chorionic hemangioma and another one with massive placental infarction. No pathological change of villitis and chorioamnionitis was observed in our observation of three cases. All samples from three placentas were negative for the nucleic acid of 2019-nCoV. Conclusions: The clinical characteristics of pregnant women with 2019-nCoV infection in late pregnancy are similar to those of non-pregnant patients, and no severe adverse pregnancy outcome is found in the 3 cases of our observation. Pathological study suggests that there are no morphological changes related to infection in the three placentas. Currently no evidence for intrauterine vertical transmission of 2019-nCoV is found in the three women infected by 2019-nCoV in their late pregnancy.", 
                          "authors": "Chen, S., Huang, B., Luo, D. J., Li, X., Yang, F., Zhao, Y., Nie, X., Huang, B. X.", 
                          "cord_id": "gsc0ukst", 
                          "journal": "Zhonghua Bing Li Xue Za Zhi", 
                          "title": "Pregnant women with new coronavirus infection: a clinical characteristics and placental pathological analysis of three cases"
                        }, 
                        {
                          "abstract": "", 
                          "authors": "Stockman, Lauren J., Lowther, Sara A., Coy, Karen, Saw, Jenny, Parashar, Umesh D.", 
                          "cord_id": "ke1r2e1b", 
                          "journal": "Emerg Infect Dis", 
                          "title": "SARS during Pregnancy, United States"
                        }
                      ];//response.data;  



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
