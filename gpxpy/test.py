import gpxpy
gpx = gpxpy.parse(open('Bloque1.gpx'))

print("{} track(s)".format(len(gpx.tracks)))
track = gpx.tracks[0]

print("{} segment(s)".format(len(track.segments)))
segment = track.segments[0]

print("{} point(s)".format(len(segment.points)))


data = []
segment_length = segment.length_3d()
for point_idx, point in enumerate(segment.points):
    print(point.longitude + "|"+ point.latitude + "|"+
                 point.elevation + "|"+ point.time + "|"+ segment.get_speed(point_idx))
    



