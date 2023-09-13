import animedetails


# custom-made html and css for phones and big screen
# func takes the given params and returns html str with
# the data in the params
def anime_html_gene(link, epi_no, img_src="None", info="None"):
    data = animedetails.anime_epi_link(link)
    epi_no = epi_no
    disqs = data[2]
    video_link = data[0]
    img_src = img_src
    info = info
    downloadlink = data[1]
    b = '''

    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />

    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:wght@500&display=swap" rel="stylesheet">   
      <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Dosis:wght@200&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Belanosima:wght@600&display=swap" rel="stylesheet">
      <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
      <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
      <title>Anime Viewer</title>
    </head>
    <body>
      <div class="top">
        <h1 class="heading">   ANIBO  </h1>
        <ul class="info-head" style="margin: 0;">
          <li> 
            <a href="https://instagram.com/jidukrishnapj" alt="instagram" target="_blank"><img src="https://jiduk.me/images/instagram.png"></a>
          </li>
          <li><a href="https://github.com/jidukrishna" alt="github" target="_blank"><img src="https://jiduk.me/images/github.png"></a></li>
        <li><a href="mailto:jidukrishnapj@gmail.com" alt="gmail" target="_blank"><img src="https://jiduk.me/images/gmail.png"></a></li>
      <li><a style="text-decoration: none;" href="https://jiduk.me" target="_blank"><h2 class="dev">Jiduk.me</h2></a>
      </li>  
      </ul>
      </div>
    <div class="info">

    <h2>EPI NO:''' + epi_no + '''</h2>

    </div>
    <div class="anime-video">
      <img class ="anime-img" src="''' + img_src + '''" alt="">
    <div class ="anime">
      <video id="player" controls ></video>

    </div>

    </div>
    <div class="download"><a  href="''' + downloadlink + ''''" target="_blank">

      <ul class="donw_adjust">
    <li>    
      <h3 class="down">Download</h3>
    </li>

    <li>
      <span class="material-symbols-outlined" style="color: rgb(230, 222, 222);">
     download
     </span>
    </li>
   </ul>

    </a>
    </div>

    <p>
    ''' + info + '''
    </p>

    ''' + disqs + '''

    <style>
    body{
      background-color: #080b1f;
      font-family: 'Roboto', sans-serif;
      font-size: 16px;
      font-weight: 400;
      line-height: 1.5;
      color: #212529;
      background-color: #131415;
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }


    html {
    overflow: scroll;
    overflow-x: hidden;
    }
    ::-webkit-scrollbar {
        width: 0;  /* Remove scrollbar space */
        background: transparent;  /* Optional: just make scrollbar invisible */
    }
    /* Optional: show position indicator in red */
    ::-webkit-scrollbar-thumb {
        background: #FF0000;
    }


    @media(min-width: 801px) {


    .anime{
      max-width: 750px;
    }


    .heading {
      font-size: 3rem;
      padding-top: 20px;
      margin: 0;
      font-family: 'Belanosima', sans-serif;
      font-weight: 700;
      color: #52d559;
      text-align: center;
    }


    .top {
      overflow: hidden;
      background-color: #3333334e;
      margin-bottom: 2rem;
    }

    .info-head li img{
      width: 40px;
      height: 40px;
      padding-top: 15px;
    }

    .info-head li{
      margin-top: 0px;
      margin-right: 1rem;
      margin-left: 1rem;
      float: right;
      list-style-type: none;
      margin-bottom: 10;
    }


    .dev{
    float: right; 
    font-size: 1.5rem;
    font-family: Georgia, 'Times New Roman', Times, serif;
    text-decoration: none;
    color: #b9b9b9;
    margin-bottom: 0;

    }

    .anime-video{
      display: flex;
      justify-content: center;
      align-items: center;
      padding-inline: 10px;
      margin: 10px;
    }

    div#disqus_thread iframe[sandbox] {
      max-height: 0px !important;
    }

    .info-picture{
      display: flex;
      justify-content: left;
      align-items: center;
    }

    p{
      margin-top: 0px;
      margin-left: 100px;
      margin-right: 100px;
      font-size: 1.5rem;
      font-family: 'Dosis', sans-serif;       
      text-decoration: none;
      color: #edecec;
      font-weight: 500;
      text-align: center;
      border: #b9b9b9;
    }

    .anime-img{
      margin-right: 10%;
      width: 300px;
    }


    #divComments{
      margin:150px;
      color: aliceblue;
    }

    .publisher-anchor-color a {
      color: rgb(197, 192, 184) !important;
    }

    .info h2{
      display: flex;
      padding-left: 450px;
      font-size: 1.2rem;
      font-family: 'Source Code Pro', monospace;
      justify-content: center;
      text-decoration: underline;
      align-items: center;
      color: rgba(232, 236, 240, 0.9);
    }


    .down{
      text-decoration: none;
      color: #edecec;
      font-size: 1.3rem;
      font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    }


    span{
    padding-top: 24px;
    }

    .donw_adjust{
        list-style-type: none;
        display: flex;
    }


    }


    .download{
      display: flex;
      justify-content: center;
      align-items: center;

     }


    a {
      color: rgb(205, 207, 210) !important;
    }


    @media(max-width: 800px) {
      .anime{
          max-width:700px;
      }

      .down{
          margin: 0px;
          text-decoration: none;
          color: #edececdb;
          font-size: 1.3rem;
          font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;

      }

      #divComments{
          margin:15px;
      }


      .anime-img{
          width: 200px;
          padding-top: 15px;

      }
      .info-picture{
          display: flex;
          justify-content: center;
          align-items: center;
      }


      p{
          margin: 10px;
          font-size: 1rem;
          font-family: 'Dosis', sans-serif;       
          text-decoration: none;
          font-weight: 500;
          color: #edecec;
          text-align: center;
          border: #b9b9b9;
      }
      div#disqus_thread iframe[sandbox] {
          max-height: 0px !important;
    }


      .anime-video{
          display: flex;
          justify-content: center;
          align-items: center;
          padding-inline: 0px;
          margin: 0px;  
      flex-direction: column-reverse; }


    .heading {
      font-size: 1.5rem;
      padding-top: 15px;
      font-weight: 700;
      color: #52d559;
      text-align: center;
      margin: 0;
      font-family: 'Belanosima', sans-serif;
    }

    .dev{
      font-size: 1.2rem;
      font-family: Georgia, 'Times New Roman', Times, serif;
      text-decoration: none;
      color: #b9b9b9;
    }

    .top {
      overflow: hidden;
      background-color: #3333334e;
      margin-bottom: 1rem;
    }

    .info-head li img{
      width: 40px;
      height: 40px;
      padding-top: 10px;

    }

    .info-head li{
      margin-right: 1rem;
      margin-left: 1rem;
      float: right;
      list-style-type: none;
    }

    .info h2{
      display: flex;
      font-size: 1.2rem;
      font-family: 'Source Code Pro', monospace;
      justify-content: center;
      text-decoration: underline;
      align-items: center;
      color: rgba(232, 236, 240, 0.9);
    }

    span{
    padding-top: 2px;
    }
    .donw_adjust{
        list-style-type: none;
        display: flex;
    }

    }</style>

    <!-- script from github for player-->

    <script src="https://cdn.rawgit.com/video-dev/hls.js/18bb552/dist/hls.min.js"></script>

    <script type="text/javascript">
    document.addEventListener("DOMContentLoaded", () => {
     var video=document.getElementById("player");
     var source ="''' + video_link + '''"
     const defaultOptions={};
     if (Hls.isSupported()) {
      const hls = new Hls();
      hls.loadSource(source);
      hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
        const availq=hls.levels.map((l)=>l.height)
        defaultOptions.controls=
        [

      'play-large', // The large play button in the center
      'rewind', // Rewind by the seek time (default 10 seconds)
      'play', // Play/pause playback
      'fast-forward', // Fast forward by the seek time (default 10 seconds)
      'progress', // The progress bar and scrubber for playback and buffering
      'current-time', // The current time of playback
      'duration', // The full duration of the media
      'mute', // Toggle mute
      'captions', // Toggle captions
      'settings', // Settings menu
      'pip', // Picture-in-picture (currently Safari only)
      'airplay', // Airplay (currently Safari only)
      'fullscreen', // Toggle fullscreen
    ];

        defaultOptions.quality={
          default:availq[0],
          options:availq,
          forced:true,
          onChange:(e)=> updateQuality(e)
        }
        new Plyr(video,defaultOptions);

      });
        hls.attachMedia(video);
        window.hls=hls;
     }
    function updateQuality(newQuality){
      window.hls.levels.forEach((level,levelIndex)=>{
        if(level.height===newQuality){
          window.hls.currentLevel=levelIndex
        }
      })
    }

    })

    </script>

    </body>
    </html>
    '''
    return b