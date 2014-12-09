import json
import gpxpy
import gpxpy.gpx
from dateutil.parser import parse
import datetime

data = None
with open('out.txt', "rb") as f:
  body = f.read().split("\n")
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


with open('acc.gpx', "wb") as f:
  f.write(gpx.to_xml())
