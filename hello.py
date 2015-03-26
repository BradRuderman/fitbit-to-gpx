from flask import Flask, request, make_response
import json
import gpxpy
import gpxpy.gpx
from dateutil.parser import parse
import datetime,sys,traceback
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    try:
      if request.method == 'POST':
        body = request.files['file']
        tzoffset = int(request.form['tzoffset'])
        data = None
        for r in body:
          if "trackpoints" in r:
            data = "{" + r.strip().strip(",").replace("trackpoints","\"trackpoints\"") + "}"
        jdata = json.loads(data)

        gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        for p in jdata["trackpoints"]:
          lng = p["longitude"]
          lat = p["latitude"]
          elevation = p["elevation"]
          dt = parse(p["date"])
          speed = p["speed"]
          vertical_acc = p["verticalAccuracy"]
          horizontal_acc = p["horizontalAccuracy"]
          pnt = gpxpy.gpx.GPXTrackPoint(lat, lng, elevation=elevation, time=dt, speed=speed, horizontal_dilution=horizontal_acc, vertical_dilution=vertical_acc)
          pnt.adjust_time(datetime.timedelta(hours=tzoffset))
          gpx_segment.points.append(pnt)

        response = make_response(gpx.to_xml())
        response.headers['Content-Description'] = 'File Transfer'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = 'attachment; filename=fitbit.gpx'
        return response

      return '''
      <!doctype html>
      <head>
      </head>
      <body>
      <!-- Google Tag Manager -->
<noscript><iframe src="//www.googletagmanager.com/ns.html?id=GTM-TSXJPC"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TSXJPC');</script>
<!-- End Google Tag Manager -->
      <div>
      you can use this utility to convert your fitbit gps data to gpx. In order to use, you must download the source of the html page with your exercise data on it. somewhere in it, it should have a line (in the head) that starts with "trackpoints". This is part of a json object, that contains your gps data.
      <title>Upload new File</title>
      <h1>Upload new File</h1>
      <form action="" method="post" enctype="multipart/form-data">
        <p>
          <input type="file" name="file" >
        </p>
        <p>
          adjustment needed to make recorded time into utc ex. Location where run was (pst=8,pdt=7,est=5, gmt=0, aest=-10)
          <input type="number" name="tzoffset" >
        </p>
        <input type="submit" value="Upload">
      </form>
      <br />
      <div>
      brought to you by <a href="https://twitter.com/chapello" target="_blank">@chapello</a> and <a href="https://twitter.com/bradruderman" target="_blank">@bradruderman</a>
      <br />
      send us the file if you get an error
      <div>
      <div>
      <script src='//redditjs.com/post.js' data-url='http://www.reddit.com/r/fitbit/comments/30bdnn/export_your_fitbit_surge_gps_data_to_other_apps/'></script>
      </div>
      </body>
      </html>
      '''
    except:
      print(traceback.format_exc())
      response = make_response(traceback.format_exc())
      return response


if __name__ == "__main__":
  app.run()

