var canvas;
var context;
var clickX=new Array();
var clickY=new Array();
var clickDrag=new Array();
var paint=false;
var curColor="#FF5733"
var cleared=false;
function drawCanvas()
{
    canvas=document.getElementById('canvas')
    context=document.getElementById('canvas').getContext('2d')

    $('#canvas').mousedown(function(e){
        
        var mouseX=e.pageX - this.offsetLeft
        var mouseY=e.pageY - this.offsetTop
        paint=true
        addClick(mouseX,mouseY,true)
        redraw()
    })
    $('#canvas').mousemove(function(e){
        
        if(paint)
        {
            addClick(e.pageX - this.offsetLeft,e.pageY - this.offsetTop,true)
            redraw()
        }
    })
    $('#canvas').mouseup(function(e){
        paint=false;
    })
}


    function addClick(x,y,draggin)
    {
        clickX.push(x)
        clickY.push(y)
        clickDrag.push(draggin)
    }

    function redraw()
    {
        context.clearRect(0,0,context.canvas.width,context.canvas.height)
        // context.beginPath();
        context.strokeStyle=curColor
        context.lineJoin="round"
        context.lineWidth=20
        if(!cleared)
        {for( var i=0;i<clickX.length;i++)
            {
                context.beginPath();
                if(clickDrag[i]&&i)
                {
                    context.moveTo(clickX[i-1],clickY[i-1])
                }
                else{
                    context.moveTo(clickX[i]-1,clickY[i])
                }
                context.lineTo(clickX[i],clickY[i])
                context.closePath();
                context.stroke();
            }
        }
        else
        {
            clickX=[]
            clickY=[]
            clickDrag=[]
            cleared=false
        }

    }
    // function remove()
    // {
    //     context=document.getElementById('canvas').getContext('2d')
    //     context.clearRect(0,0,context.canvas.width,context.canvas.height)
    //     context.beginPath();
    //     context.fillRect(0, 0, 300, 150);
       
    // }
    // function check()
    // {
    //     console.log("checking")
    // }
    function clear_canvas()
    {
        console.log("indide clear");
        context=document.getElementById('canvas').getContext('2d');
        context.clearRect(0,0,context.canvas.width,context.canvas.height);
        context.beginPath();
        cleared=true;
    }
    function save()
    {
        var img=new Image()
        var url=document.getElementById('url')
        img.id="pic";
        img.src=canvas.toDataURL();
        url.value=img.src;

    }
