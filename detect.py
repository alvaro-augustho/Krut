import cv2
import math
import numpy
import collections
import urllib
import tempfile

Point = collections.namedtuple("Point", "x y")

def find_chessboard(edges, min_square_dim = 15):
    """
    Finds the chessboard in an image given its edge matrix.

    Accepts an optional parameter, min_square_dim, specifying the minimum
    expected dimension of the chessboard squares.
    """

    def is_in_chessboard(row_or_col):
        """
        Given a row or column, returns whether it is considered
        in or out of the chessboard using a naive algorithm.
        """

        nonzero, = row_or_col.nonzero()

        # compute the approximate number of crossed squares
        squares = 0
        for i, j in zip(nonzero, nonzero[1:]):
            if j - i >= min_square_dim:
                squares += 1

        return squares >= 8

    # build corner candidates in each dimension by iterating over
    # lines and columns and finding which are inside the chessboard
    y_cc = [y for y, line in enumerate(edges) if is_in_chessboard(line)]
    x_cc = [x for x, col in enumerate(edges.T) if is_in_chessboard(col)]

    if not x_cc or not y_cc:
        return None, None

    # return the extreme points
    return (Point(x_cc[0], y_cc[0]), Point(x_cc[-1], y_cc[-1]))

def find_chessboard_squares(image, min_square_dim):
    """
    Convenience wrapper to find chessboard squares directly.
    """

    return compute_chessboard_squares(find_chessboard(image, min_square_dim))

def compute_chessboard_squares(e1, e2):
    """
    Given the extreme points for a chessboard, returns a list
    of tuples of points, where each tuple contains the extreme points
    of a square in the chessboard.
    """

    squares = []

    # equal in an ideal world
    square_dim_x = int(math.ceil((e2.x - e1.x)/8.0))
    square_dim_y = int(math.ceil((e2.y - e1.y)/8.0))

    y = e1.y
    while y < e2.y - square_dim_y/2:
        x = e1.x
        while x < e2.x - square_dim_x/2:
            extr_x = min(x + square_dim_x, e2.x)
            extr_y = min(y + square_dim_y, e2.y)

            sq = (Point(x, y), Point(extr_x, extr_y))
            squares.append(sq)

            x += square_dim_x

        y += square_dim_y

    return squares

def recognize_pieces(edges, v, squares):
    """
    Given the edge matrix and V component in the HSV space of the chessboard
    image, as well as the list of chessboard squares, returns a list whose
    elements are either "W", when the corresponding square contains a white
    piece, "B", when the piece is black, or None, when it contains no pieces.
    """

    pieces = []

    v = cv2.equalizeHist(v)
    for p1, p2 in squares:
        # count the number of slightly centered edges
        occupancy = sum(edges[y][x]
                        for x in range(p1.x + 5, p2.x - 5)
                        for y in range(p1.y + 5, p2.y - 5))

        if occupancy > 70*255:
            corners = (v[p1.y][p1.x], v[p1.y][p2.x],
                       v[p2.y][p1.x], v[p2.y][p2.x])

            # average v-component of the corners
            avg = sum(map(float, corners)) / len(corners)

            # black pixels should be relatively black
            # when compared to the corner average
            black = sum(v[y][x] / avg < 0.2
                        for x in range(p1.x, p2.x + 1)
                        for y in range(p1.y, p2.y + 1))

            if black >= 1000 and black != 1049:
                color = "B"
            else:
                color = "W"

            pieces.append(color)
        else:
            pieces.append(None)

    return pieces

# Funcao que eu usei para fazer a comunicacao entre as partes. 
# Recebe uma imagem e devolve o vetor
# Ainda nao coloquei protecao contra erros como
# pecas trocando de cor, pecas a menos, ou a mais, ainda vou fazer isso
def gerar_vetor(path):
    
    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    image = cv2.imread(path)

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv)

    edges = cv2.Canny(v, 70, 100)
    e1, e2 = find_chessboard(edges)
    if (e1, e2) == (None, None):
        print >>sys.stderr, "No chessboard found."

    cv2.rectangle(image, e1, e2, BLUE)

    squares = compute_chessboard_squares(e1, e2)
    pieces = recognize_pieces(edges, v, squares)

    vetor = []
    for (p1, p2), color in zip(squares, pieces):
        if color == "B":
            vetor.append('1')
        elif color == "W":
            vetor.append('2')
        else:
            vetor.append('0')
            
    return vetor


"""

if __name__ == "__main__":
    import sys
    import urllib
    import tempfile

    BLUE = (255, 0, 0)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    if len(sys.argv) > 1 and sys.argv[1].startswith("http://"):
        def url_iter():
            tmpfile = tempfile.mktemp()

            while True:
                response = urllib.urlopen(sys.argv[1])
                with open(tmpfile, "wb") as tmp:
                    tmp.write(response.read())

                yield cv2.imread(tmpfile)

        images = url_iter()
    else:
        try:
            cam_id = int(sys.argv[1] if len(sys.argv) > 1 else 0)
            vc = cv2.VideoCapture(cam_id)
            assert(vc.isOpened())

            def cam_iter():
                for i in range(5):
                    success, image = vc.read()
                    assert success
                while True:
                    success, image = vc.read()
                    assert success
                    yield image

            images = cam_iter()
        except ValueError:
            images = map(cv2.imread, sys.argv[1:])

    for image in images:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        _, _, v = cv2.split(hsv)

        edges = cv2.Canny(v, 70, 100)
        e1, e2 = find_chessboard(edges)
        if (e1, e2) == (None, None):
            print >>sys.stderr, "No chessboard found."
            continue

        cv2.rectangle(image, e1, e2, BLUE)

        squares = compute_chessboard_squares(e1, e2)
        pieces = recognize_pieces(edges, v, squares)

        for (p1, p2), color in zip(squares, pieces):
            if color == "B":
                cv2.rectangle(image, p1, p2, BLACK)
            elif color == "W":
                cv2.rectangle(image, p1, p2, WHITE)

        cv2.imshow("chessboard", image)
        cv2.waitKey(0)
"""
