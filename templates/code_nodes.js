fetch('nodes.json', {mode: 'no-cors'})
  .then(function(res) {
    return res.json()
  })
  .then(function(nodes) {
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

 elements {
	node: nodes.elements
	edge: []
  },
});    
});
