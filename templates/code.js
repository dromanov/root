var cy = window.cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,
  autounselectify: true,

  layout: {
    name: 'dagre'
  },

  style: [
    {
      selector: 'node',
      style: {
        'content': 'data(id)',
        'text-opacity': 1,
        'text-valign': 'center',
        'text-halign': 'right',
		'fontSize': '20',
        'background-color': '#11479e'
      }
    },
	
	 {
      selector: 'node.easy',
      style: {
        'background-color': '#A8E4A0'
      }
    },
	
	{
      selector: 'node.medium',
      style: {
        'background-color': '#FBEC5D'
      }
    },
	
	 {
      selector: 'node.hard',
      style: {
        'background-color': '#FD7C6E'
      }
    },
	
	{
      selector: 'node.fine',
      style: {
        'background-color': '#DE5D83'
      }
    },

    {
      selector: 'edge',
      style: {
        'curve-style': 'bezier',
        'width': 4,
        'target-arrow-shape': 'triangle',
        'line-color': '#9dbaea',
        'target-arrow-color': '#9dbaea'
      }
    },
	
	{
      selector: 'edge.true',
      style: {
        'line-color': '#34C924',
        'target-arrow-color': '#34C924'
      }
    }, 
	
	{
      selector: 'edge.false',
      style: {
        'line-color': '#E34234',
        'target-arrow-color': '#E34234'
      }
    }
  ],

  elements: {
    nodes: [
      { data: { id: '1_path' }, classes: 'easy' },
      { data: { id: '1_market_1' }, classes: 'easy'  },
      { data: { id: '1_market_2' }, classes: 'hard'  },
      { data: { id: '1_market_3' }, classes: 'medium'   },
      { data: { id: '1_time' }, classes: 'easy'  },
      { data: { id: '1_market_4' }, classes: 'medium'    },
      { data: { id: '1_speed' }, classes: 'medium'    },
      { data: { id: '1_goal' }, classes: 'hard'   },
      { data: { id: '2_jornal' }, classes: 'easy'  },
      { data: { id: '2_vitaminC' }, classes: 'medium'    },
      { data: { id: '2_record' }, classes: 'hard'   },	  
      { data: { id: '3_supplies' }, classes: 'hard'   },
      { data: { id: '3_sleep' }, classes: 'hard'   },
      { data: { id: '3_sugar' }, classes: 'medium'    },
      { data: { id: '3_path_1' }, classes: 'easy'  },
      { data: { id: '3_path_2' }, classes: 'easy'  },
      { data: { id: '4_proportion_1' }, classes: 'hard'   },
      { data: { id: '4_map' }, classes: 'hard'   },
      { data: { id: '4_proportion_2' }, classes: 'hard'   },	
	  { data: { id: '4_basket' }, classes: 'medium'    },
      { data: { id: '4_progression' }, classes: 'medium'    },
      { data: { id: '4_path_1' }, classes: 'easy'  },
      { data: { id: '4_proportion_3' }, classes: 'easy'  },
      { data: { id: '4_nuts' }, classes: 'medium'    },	
	  { data: { id: '4_path_2' }, classes: 'medium'    },
      { data: { id: '4_rock' }, classes: 'medium'    },
      { data: { id: '4_flood' }, classes: 'hard'   },
      { data: { id: '4_jar' }, classes: 'easy'  },
      { data: { id: '4_square_1' }, classes: 'easy'  },	
	  { data: { id: '4_grape' }, classes: 'medium'    },
      { data: { id: '4_active' }, classes: 'medium'    },
      { data: { id: '4_path_3' }, classes: 'medium'    },
      { data: { id: '4_bags' }, classes: 'easy'  },
      { data: { id: '4_path_4' }, classes: 'medium'    },	
	  { data: { id: '4_animal_1' }, classes: 'easy'  },
      { data: { id: '4_square_2' }, classes: 'medium'    },
      { data: { id: '4_animal_2' }, classes: 'easy'  },
      { data: { id: '4_proportion_4' }, classes: 'hard'   },
      { data: { id: '5_fish' }, classes: 'easy'  },	
	  { data: { id: '5_month' }, classes: 'medium'    },
      { data: { id: '5_speed' }, classes: 'hard'   },
      { data: { id: '6_treasure' }, classes: 'easy'  },
      { data: { id: '6_path' }, classes: 'medium'    },
      { data: { id: '6_code' }, classes: 'hard'   },	    
      { data: { id: '7_human' }, classes: 'hard'   },
      { data: { id: '7_rus' }, classes: 'medium'    },
      { data: { id: '7_zero' }, classes: 'easy'  },
      { data: { id: '7_king' }, classes: 'medium'    },	
	  { data: { id: '7_1001' }, classes: 'medium'    },
      { data: { id: '7_duck' }, classes: 'hard'   },
      { data: { id: '7_sleep' }, classes: 'easy'  },
      { data: { id: '7_birds' }, classes: 'medium'    },
      { data: { id: '7_circle' }, classes: 'hard'   },	
	  { data: { id: '7_budget' }, classes: 'hard'   },
      { data: { id: '7_rim' }, classes: 'medium'    },
      { data: { id: '8_1' }, classes: 'fine'    },
      { data: { id: '8_2' }, classes: 'fine'    },
      { data: { id: '8_3' }, classes: 'fine'    },	
	  { data: { id: '0_plan' } },
      { data: { id: '0_balloon' } },
      { data: { id: '0_crash' } },
      { data: { id: '0_island' } },
      { data: { id: '0_airton' } },	
	  { data: { id: '0_rescue' } },
      { data: { id: '0_balloon_1' } },
      { data: { id: '0_island_1' } },
      { data: { id: '0_island_2' } },
      { data: { id: '0_island_3' } },	    
      { data: { id: '0_final' } }
      
    ],
    edges: [
      { data: { source: '1_path', target: '1_speed' }, classes: 'true'  },
      { data: { source: '1_path', target: '1_market_1' }, classes: 'false' },
      { data: { source: '1_market_1', target: '1_time' }, classes: 'false' },
      { data: { source: '1_market_1', target: '1_speed' }, classes: 'true' },
      { data: { source: '1_market_2', target: '0_balloon' } },
      { data: { source: '1_market_3', target: '0_balloon' }, classes: 'false' },
      { data: { source: '1_market_3', target: '1_market_2' }, classes: 'true' },
      { data: { source: '1_time', target: '8_1' }, classes: 'false' },	 
      { data: { source: '1_time', target: '0_balloon' }, classes: 'true' },
      { data: { source: '1_market_4', target: '1_speed' }, classes: 'true' },
      { data: { source: '1_market_4', target: '1_market_3' }, classes: 'false' },
      { data: { source: '1_speed', target: '1_time' }, classes: 'false'  },
      { data: { source: '1_speed', target: '1_market_3' }, classes: 'true' },
      { data: { source: '1_goal', target: '1_market_3' }, classes: 'false' },
      { data: { source: '1_goal', target: '1_market_2' }, classes: 'true' },
      { data: { source: '2_jornal', target: '2_vitaminC' }, classes: 'true' },		 
      { data: { source: '2_jornal', target: '0_balloon_1' }, classes: 'false' },
      { data: { source: '2_vitaminC', target: '2_record' }, classes: 'true' },
	  { data: { source: '2_vitaminC', target: '0_balloon_1' }, classes: 'false' },
      { data: { source: '2_record', target: '0_balloon_1' } },
      { data: { source: '3_supplies', target: '7_birds' }, classes: 'true' },
      { data: { source: '3_supplies', target: '7_sleep' }, classes: 'false' },
      { data: { source: '3_sleep', target: '3_supplies' }, classes: 'true' },
      { data: { source: '3_sleep', target: '0_island' }, classes: 'false' },	 
      { data: { source: '3_sugar', target: '3_sleep' }, classes: 'true' },
      { data: { source: '3_sugar', target: '3_path_1' }, classes: 'false' },
      { data: { source: '3_path_1', target: '3_sleep' }, classes: 'true' },
      { data: { source: '3_path_1', target: '0_island' }, classes: 'false' },
      { data: { source: '3_path_2', target: '3_sugar' }, classes: 'true' },
      { data: { source: '3_path_2', target: '0_island' }, classes: 'false' },
      { data: { source: '4_proportion_1', target: '4_progression' }, classes: 'false' },
      { data: { source: '4_proportion_1', target: '4_proportion_2' }, classes: 'true' },	
      { data: { source: '4_map', target: '4_path_4' } },
      { data: { source: '4_proportion_2', target: '8_3' }, classes: 'true' },
	  { data: { source: '4_proportion_2', target: '8_2' }, classes: 'false' },
      { data: { source: '4_basket', target: '0_airton' } },
      { data: { source: '4_progression', target: '8_3' }, classes: 'true' },
      { data: { source: '4_progression', target: '8_2' }, classes: 'false' },
      { data: { source: '4_path_1', target: '4_proportion_3' } },
      { data: { source: '4_proportion_3', target: '4_nuts' } },
      { data: { source: '4_nuts', target: '4_basket' } },	 
      { data: { source: '4_path_2', target: '0_island_1' } },
      { data: { source: '4_rock', target: '4_nuts' }, classes: 'true' },
      { data: { source: '4_rock', target: '4_flood' }, classes: 'false' },
      { data: { source: '4_flood', target: '4_basket' }, classes: 'true' },
      { data: { source: '4_flood', target: '4_nuts' }, classes: 'false' },
      { data: { source: '4_jar', target: '4_square_1' }, classes: 'true' },
      { data: { source: '4_jar', target: '4_bags' }, classes: 'false' },
      { data: { source: '4_square_1', target: '4_square_2' } },	
      { data: { source: '4_grape', target: '4_active' }, classes: 'true' },
      { data: { source: '4_grape', target: '4_bags' }, classes: 'false' },
      { data: { source: '4_active', target: '4_proportion_4' }, classes: 'true' },
      { data: { source: '4_active', target: '4_bags' }, classes: 'false' },
      { data: { source: '4_path_3', target: '0_island_1' } },
      { data: { source: '4_bags', target: '4_animal_1' } },
      { data: { source: '4_path_4', target: '4_square_2' }, classes: 'true' },
      { data: { source: '4_path_4', target: '4_jar' }, classes: 'false' },	 
      { data: { source: '4_animal_1', target: '4_animal_2' } },
      { data: { source: '4_square_2', target: '0_island_3' } },
      { data: { source: '4_animal_2', target: '7_rim' }, classes: 'true' },
      { data: { source: '4_animal_2', target: '0_rescue' }, classes: 'false' },
      { data: { source: '4_proportion_4', target: '7_budget' }, classes: 'true' },
      { data: { source: '4_proportion_4', target: '7_rim' }, classes: 'false' },
      { data: { source: '5_fish', target: '5_speed' } },
      { data: { source: '5_month', target: '0_island_2' } },	      
      { data: { source: '5_speed', target: '5_month' } },
      { data: { source: '6_treasure', target: '6_path' } },
      { data: { source: '6_path', target: '6_code' } },
      { data: { source: '6_code', target: '0_final' } },
      { data: { source: '7_human', target: '4_path_4' } },
      { data: { source: '7_rus', target: '0_crash' }, classes: 'true' },
      { data: { source: '7_rus', target: '7_zero' }, classes: 'false' },	 
      { data: { source: '7_zero', target: '0_crash' } },
      { data: { source: '7_king', target: '4_grape' }, classes: 'true' },
      { data: { source: '7_king', target: '4_bags' }, classes: 'false' },
      { data: { source: '7_1001', target: '4_grape' }, classes: 'true' },
      { data: { source: '7_1001', target: '4_bags' }, classes: 'false' },
      { data: { source: '7_duck', target: '0_crash' }, classes: 'true' },
      { data: { source: '7_duck', target: '7_zero' }, classes: 'false' },
      { data: { source: '7_sleep', target: '0_island' } },	
      { data: { source: '7_birds', target: '0_island' } },
      { data: { source: '7_circle', target: '4_proportion_1' }, classes: 'true' },
      { data: { source: '7_circle', target: '4_grape' }, classes: 'false' },
      { data: { source: '7_budget', target: '0_rescue' } },
      { data: { source: '7_rim', target: '7_budget' }, classes: 'true' },
      { data: { source: '7_rim', target: '0_rescue' }, classes: 'false' },
      { data: { source: '8_1', target: '0_balloon' } },
      { data: { source: '8_2', target: '0_rescue' } },	 
      { data: { source: '8_3', target: '0_rescue' } },
      { data: { source: '0_plan', target: '1_path' } },
      { data: { source: '0_plan', target: '1_market_4' } },
      { data: { source: '0_plan', target: '1_goal' } },
      { data: { source: '0_balloon', target: '2_jornal' } },
      { data: { source: '0_balloon', target: '2_vitaminC' } },
      { data: { source: '0_balloon', target: '2_record' } },
      { data: { source: '0_crash', target: '3_path_1' } },	
      { data: { source: '0_crash', target: '3_path_2' } },
      { data: { source: '0_crash', target: '3_sugar' } },
      { data: { source: '0_island', target: '4_path_3' } },
      { data: { source: '0_island', target: '4_path_2' } },
      { data: { source: '0_airton', target: '5_fish' } },
      { data: { source: '0_rescue', target: '6_treasure' } },
      { data: { source: '0_balloon_1', target: '7_zero' } },
      { data: { source: '0_balloon_1', target: '7_rus' } },	 
      { data: { source: '0_balloon_1', target: '7_duck' } },
      { data: { source: '0_island_1', target: '4_path_1' } },
      { data: { source: '0_island_1', target: '4_rock' } },
      { data: { source: '0_island_1', target: '4_flood' } },
      { data: { source: '0_island_2', target: '7_human' } },
      { data: { source: '0_island_2', target: '4_map' } },
      { data: { source: '0_island_3', target: '7_1001' } },
      { data: { source: '0_island_3', target: '7_king' } },	 
      { data: { source: '0_island_3', target: '7_circle' } },

 	  
    ]
  },
});
