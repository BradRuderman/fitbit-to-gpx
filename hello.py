from flask import Flask, request, Response
import json
import gpxpy
import gpxpy.gpx
from dateutil.parser import parse
import datetime
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      body = request.files['file']
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
        pnt.adjust_time(datetime.timedelta(hours=8))
        gpx_segment.points.append(pnt)

      return Response(gpx.to_xml(), mimetype='text/xml')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
  app.run()

