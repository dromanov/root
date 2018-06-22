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
      { data: { id: 'Easy_level' }, classes: 'easy' },
      { data: { id: 'Medium_level' }, classes: 'medium' }, 
	  { data: { id: 'Hard_level' }, classes: 'hard' },
	  { data: { id: 'Fine_level' }, classes: 'fine' },
      { data: { id: 'Organizational_stage' } },
	  { data: { id: 'By_corret_answer' } },
      { data: { id: 'By_false_answer' } }, 
	  { data: { id: 'Answer_do_not_matter' }  }
      
    ],
    edges: [
      { data: { source: 'Organizational_stage', target: 'By_corret_answer' }, classes: 'true'  },
      { data: { source: 'Organizational_stage', target: 'By_false_answer' }, classes: 'false'  },     
      { data: { source: 'Organizational_stage', target: 'Answer_do_not_matter' },  },	  
    ]
  },
});