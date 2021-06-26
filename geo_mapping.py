import argparse
from db.setting import session
from db.article import *
from lib import genimage, geocording
import folium


def parse_args():
    parser = argparse.ArgumentParser(description='Mapping spot')
    parser.add_argument('spot_name', help='spot name')
    return parser.parse_args()


def calc_min_distance(p0, p1, p2):
    a = p2[0] - p1[0]
    b = p2[1] - p2[1]
    a2 = a * a
    b2 = b * b
    r2 = a2 + b2
    tt = -(a * (p1[0] - p0[0]) + b * (p1[1] - p0[1]))
    if tt < 0:
        return (p1[0] - p0[0]) * (p1[0] - p0[0]) + (p1[1] - p0[1]) * (p1[1] - p0[1])
    if tt > r2:
        return (p2[0] - p0[0]) * (p2[0] - p0[0]) + (p2[1] - p0[1]) * (p2[1] - p0[1])
    f1 = a * (p1[1] - p0[1]) - b * (p1[0] - p0[0])
    return f1 * f1 / r2


DEPARTURE = {'title': "日野キャンパス", 'lat': 35.6613427, 'lng': 139.3667929}


def main():
    args = parse_args()
    destination = session.query(Article).filter(Article.title == args.spot_name).first()
    if destination is None:
        print(args.spot_name + " not exists")
        return
    if destination.latitude == 0 and destination.longitude == 0:
        print("[INFO] getting by google api.")
        destination.latitude, destination.longitude = geocording.get_lat_and_lng(destination.title)
        session.commit()  # update db

    articles = session.query(Article).all()
    nearest_spot = None
    distance = 100000000
    for a in articles:
        d = calc_min_distance([a.latitude, a.longitude], [DEPARTURE['lat'], DEPARTURE['lng']],
                          [destination.latitude, destination.longitude])
        if d != 0 and d < distance:
            nearest_spot = a
            distance = d

    destination_wc = genimage.get_image_by_tfidf(destination.read, [a.read for a in articles])
    destination_file_name = destination.title + '.png'
    destination_wc.to_file('out/' + destination_file_name)
    nearest_wc = genimage.get_image_by_tfidf(nearest_spot.read, [a.read for a in articles])
    nearest_file_name = nearest_spot.title + '.png'
    nearest_wc.to_file('out/' + nearest_file_name)

    folium_map = folium.Map(
        location=[(DEPARTURE['lat'] + destination.latitude) / 2, (DEPARTURE['lng'] + destination.longitude) / 2],
        zoom_start=10
    )
    folium.Marker(location=[DEPARTURE['lat'], DEPARTURE['lng']], popup=DEPARTURE['title']).add_to(folium_map)
    folium.Marker(
        location=[destination.latitude, destination.longitude],
        popup='%s<br><img src="%s">' % (destination.title, destination_file_name)
    ).add_to(folium_map)
    folium.vector_layers.PolyLine(
        locations=[[DEPARTURE['lat'], DEPARTURE['lng']], [destination.latitude, destination.longitude]]
    ).add_to(folium_map)
    folium.Marker(
        location=[nearest_spot.latitude, nearest_spot.longitude],
        popup='%s<br><img src="%s">' % (nearest_spot.title, nearest_file_name),
        icon=folium.Icon(color='red')
    ).add_to(folium_map)
    folium_map.save('out/' + destination.title + '.html')


if __name__ == '__main__':
    main()
