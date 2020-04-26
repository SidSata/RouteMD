
$(document).ready(function(){
    
    //Since adding another room requires a previously created panel, I'm hardcoding the first room as NonCritical. 
    //In the final version, this hardcoded Non-critical room will be replaced by each room of the current hospital from the hospital database using a for loo
    var testroom=["Non-Critical-1","images/placeholder.png","images/bar_graph.svg",20,80,"active"];
    createRoom(testroom);
    
    function createRoom(details){
        //details- [0]-roomName, [1]-imageUrl, [2]-chartUrl, [3]-No. patients, [4]- Capacity, [5]- Active or not- first page has "active", following pages have blank

        //creates the tab panel on the top
        $('.tabs').append(
            $('<li/>')
            .attr('rel',details[0])
            .addClass('tab-panel '+details[5]+" ")
            .text(details[0])
        )

        //creates the dynamic view 
        $('.tab-panels').append(
            $('<div/>')
            .attr('id',details[0])
            .addClass('panel '+details[5]+ ' roompanel')
            .append(
                $('<div/>')
                .addClass('row')
                .append(
                    $('<div/>')
                    .addClass('card flew-row flex-wrap')
                    .css('display','flex')
                    .css('justify-content','left')
                    //placeholder image
                    .append(
                        $('<img/>')
                        .addClass('card-img-top data-image')
                        .attr('id','main-image')
                        .attr('src',details[1])
                        .attr('alt','Placeholder')
                    )
                    //chart image
                    .append(
                        $('<img/>')
                        .addClass('card-img-top data-image')
                        .attr('id','main-chart')
                        .attr('src',details[2])
                        .attr('alt','Placeholder')
                    )
                    //room details
                    .append(
                        $('<h3/>')
                        .addClass('text-primary text-center')
                        .text(details[0]+"\nOccupancy:"+details[3]+'/'+details[4])
                    )
                )
            )
        ) 
   }
    //when the tab of a given room is clicked, the dynamic view switches to that room
    $('.tab-panels .tabs').on('click', 'li', function() {
        var $panel = $(this).closest('.tab-panels');

        $panel.find('.tabs li.active').removeClass('active');
        $(this).addClass('active');

        //figure out which panel to show
        var panelToShow = $(this).attr('rel');

        //hide current panel
        $panel.find('.panel.active').slideUp(100, showNextPanel);

        //show next panel
        function showNextPanel() {
            $(this).removeClass('active');

            $('#'+panelToShow).slideDown(0, function() {
                $(this).addClass('active');
            });
        }
    });

    //when the user enters values into the add room modal, creates a new room by retrieving user input and calling createRoom() 
    //MODAL VALIDATION PENDING: STILL CAN PASS EMPTY VALUES THROUGH MODAL FIELDS
    $('#addRoomModalButton').on('click',createRoomWrapper);
    function createRoomWrapper(){
        var inputName=document.querySelector('input[name="critical-check"]:checked').value;
        var inputCapacity=document.getElementById('roomCapacity').value;
        inputName=inputName.split(' ').join('_');
        var roomName=countExistingRooms(inputName);
        var isActive=(document.querySelector('.roompanel')==null)?"active":"";
        createRoom([roomName,"images/placeholder.png","images/bar_graph.svg",0,inputCapacity,isActive]);
        document.getElementById('roomName').value="";
        document.getElementById('roomCapacity').value="";
    }
    function countExistingRooms(roomType){
        var countNC=0;
        var countC=0;
        var rooms=document.querySelectorAll('.roompanel');
        for (var i=0;i<rooms.length;i++){
            if (rooms[i].id.indexOf('Non-Critical')!=-1){
                countNC+=1;
            }
            else{
                countC+=1;
            }
        }
        if (roomType=="Non-Critical"){
            return ("Non-Critical-"+(countNC+1+""));
        }
        else{
            return ("Critical-"+(countC+1+""));
        }
    }

    //when the user clicks the remove room button, shows a list of rooms that can be removed
    $('#remove-room-button').on('click',removeRoom);
    function removeRoom(){
        $('.roomidwrapper').remove();
        $('.roompanel').each(function(){
            $('#roomlist').append('<label class="roomidwrapper"><input type="checkbox" class="roomid" name="room" value="'+$(this).attr('id')+'">'+$(this).attr('id')+"</label>")
        })
    }

    //when the user selects a room to be removed in the remove room modal, removes the tab and panel of that room
    $('#removeRoomModalButton').on('click',function(){
        var checks=document.getElementsByClassName('roomid');
        for (var i=0;i<checks.length;i+=1){
            if (checks[i].checked===true){
                var removalId=checks[i].value;
                $('.tab-panel').each(function(){
                    if ($(this).attr('rel')===removalId){
                        $(this).remove();
                    }
                })
                $('.roompanel').each(function(){
                    if ($(this).attr('id')===removalId){
                        $(this).remove();
                    }
                })
            }
        }
        checkActive();
    })
    function checkActive(){
        if (document.querySelectorAll('.tab-panel').length==1 && !document.querySelector('.tab-panel').classList.contains('active')){
            document.querySelector('.tab-panel').classList.add('active');
        }
        if (document.querySelectorAll('.roompanel').length==1 && !document.querySelector('.roompanel').classList.contains('active')){
            document.querySelector('.roompanel').classList.add('active');
        }
    }
});

