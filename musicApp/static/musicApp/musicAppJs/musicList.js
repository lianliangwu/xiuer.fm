$(document).ready(function(){

    /**
    * Created by 23rd and Walnut
    * www.23andwalnut.com
    * User: Saleem El-Amin
    * Date: 6/8/11
    * Time: 9:39 AM
    */


    // example music list
/*    var myPlaylist2 = [

        {
            mp3:"{% static 'musicApp/plugin/musicplayer/demo/mix/1.mp3' %}",
            oga:"{% static 'musicApp/plugin/musicplayer/demo/mix/1.ogg' %}",
            title:'Sample',
            artist:'Sample',
            rating:4,
            buy:'#',
            price:'0.99',
            duration:'0:30',
            cover:"{% static 'musicApp/plugin/musicplayer/demo/mix/1.png' %}"
        },{
            mp3:"{% static 'musicApp/plugin/musicplayer/demo/mix/2.mp3' %}",
        }
    ]*/

    var myPlaylist = document.getElementById("myPlaylist_input").value
    var myPlaylist3 = JSON.parse(myPlaylist)

    // alert(myPlaylist3[0]["cover"])

    var description = '';

    $('body').ttwMusicPlayer(myPlaylist3, {
        autoplay:true, 
        description:description,
        jPlayer:{
            swfPath:'musicApp/plugin/musicplayer/plugin/jquery-jplayer' 
        }
    });
});