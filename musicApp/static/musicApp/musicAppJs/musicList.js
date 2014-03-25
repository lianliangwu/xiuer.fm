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
        "mp3": "/static/musicApp/mr3.douban.com/201403101213/b7e77522608c4969a598c4b84c082926/view/song/small/p2037305.mp3",
        "title": " 여전히 (With Rhyme-A-) ",
        "artist": "Soriheda"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101218/8160dfae38b9c5668b8f498af8be0fb1/view/song/small/p2037546.mp3",
        "title": "Lovesick Synthetic",
        "artist": "Baths"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101220/dfd5924e5577dc85898b70b6b70f59ff/view/song/small/p2037660.mp3",
        "title": " 悪霊降臨",
        "artist": "梅林茂"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101228/37ce9cbe8e64dbce14e604fcff8bd100/view/song/small/p2037537.mp3",
        "title": "Sound of the Boot",
        "artist": "蜜三刀"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101232/6013c5855ea3f3b46f8afcb49517fb29/view/song/small/p2037399.mp3",
        "title": "Holding Onto Heaven",
        "artist": "Foxes"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101232/9d8c3bfc0c8199ef272595dfea5134c6/view/song/small/p2037599.mp3",
        "title": "Leaving",
        "artist": "满人"
    },
    {
        "mp3": "/static/musicApp/mr4.douban.com/201403101232/cc519e831b081e55f6202b3ddd94373b/view/song/small/p2037581.mp3",
        "title": "夜魔之路",
        "artist": "冥界"
    },
    {
        "mp3": "/static/musicApp/mr4.douban.com/201403101232/cad2639d211e9e0ad71f5e7bc6d3bc3a/view/song/small/p2037303.mp3",
        "title": "자리 (Position) (With Jolly V, Soulman) ",
        "artist": "Soriheda"
    },
    {
        "mp3": "/static/musicApp/mr4.douban.com/201403101232/dd05d1336901bec7d98031226d4ad529/view/song/small/p2037461.mp3",
        "title": "七三年的姑姑",
        "artist": "秘密后院"
    },
    {
        "mp3": "/static/musicApp/mr3.douban.com/201403101232/e091b672dd926dda82ba0398d6f54432/view/song/small/p2037555.mp3",
        "title": "The Vapors",
        "artist": "Baths"
    }
]*/

    /*show music player plugin*/
    var myPlaylist = document.getElementById("myPlaylist_input").value
    var myPlaylist3 = JSON.parse(myPlaylist)
    var description = '';
    $('body').ttwMusicPlayer(myPlaylist3, {
        autoplay:true, 
        description:description,
        jPlayer:{
            swfPath:"http://www.jplayer.org/latest/js/Jplayer.swf"
        }
    });

    /*show error_message modal*/
    var error_message = document.getElementById("error_message_input");
    if(error_message != null && error_message.value.length !=0){
        $('.error-modal').modal();
    }
});