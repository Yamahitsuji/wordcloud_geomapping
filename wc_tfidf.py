import argparse
from db.setting import session
from db.article import *
from lib import genimage
from matplotlib import pyplot as plt


def parse_args():
    parser = argparse.ArgumentParser(description='Mapping spot')
    parser.add_argument('spot_name', help='spot name')
    return parser.parse_args()


def main():
    args = parse_args()
    article = session.query(Article).filter(Article.title == args.spot_name).first()
    if article is None:
        print(args.spot_name + " not exists")
        return
    articles = session.query(Article).all()
    img = genimage.get_image_by_tfidf(article.read, [a.read for a in articles])
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
