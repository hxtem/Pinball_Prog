import pygame
from copy import copy
import math
import numpy as np

colors = {'white': (255, 255, 255),
          'black': (0, 0, 0),
          'red': (255, 0 , 0),
          'green': (0, 255, 0),
          'blue': (0, 0, 255)}

class Vector:
    """
    Eine Klasse, die einen Vektor in 2 Dimensionen repräsentiert.

    Attribute:
        x : float oder int
        y : float oder int

    Methoden:
        __init__(self, x, y)
        __str__(self)
        __add__(self, other)
        __sub__(self, other)
        __mul__(self, other)
        __truediv__(self, scalar)
        abs(self)
        rotate(self, angle)
        int_tuple(self)
        angle(self)
        cross(self, other)
        dot(self, other)
        length(self)
        normalize(self)
    """

    def __init__(self, x, y):
        """
        Initialisiere eine neue Instanz eines Vektors
        """
        self.x = x  # Setze die x-Komponente des Vektors
        self.y = y  # Setze die y-Komponente des Vektors

    def __str__(self):
        """
        Gibt eine Zeichenfolge für den Vektor als "Vector(x,y,z)" zurück
        """
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):
        """
        Überlade den + Operator für die Vector-Klasse
        Implementiert die Addition von zwei Instanzen der Vector-Klasse
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Überlade den - Operator für die Vector-Klasse
        Implementiert die Subtraktion von zwei Instanzen der Vector-Klasse
        """
        if isinstance(other, self.__class__):
            return Vector(self.x - other.x, self.y - other.y)
        return Vector(self.x - other, self.y - other)

    def __mul__(self, other):
        """ 
        Überlade den * Operator für die Vector-Klasse
            - Multiplikation von zwei Instanzen der Vector-Klasse:
              Gibt ein float/int zurück, das das Skalarprodukt darstellt
            - Multiplikation eines Vektor-Objekts und eines Skalars (float oder int):
              Gibt einen Vektor zurück, dessen Komponenten mit dem Wert multipliziert sind
        """
        if isinstance(other, Vector):
            return self.mul_vector(other)
        if isinstance(other, float):
            return self.mul_scalar(other)
        if isinstance(other, int):
            return self.mul_scalar(other)

    def mul_vector(self, other):
        """
        Multipliziert zwei Vektoren und gibt das Skalarprodukt zurück
        """
        return float(self.x * other.x + self.y * other.y)

    def mul_scalar(self, other):
        """
        Multipliziert einen Vektor mit einem Skalar und gibt einen neuen Vektor zurück
        """
        return Vector(self.x * other, self.y * other)

    def __truediv__(self, scalar):
        """
        Überlade den / Operator für die Vector-Klasse
        Führt eine Skalardivision durch
        """
        return Vector(self.x / scalar, self.y / scalar)

    def abs(self):
        """
        Gibt den Betrag des Vektor-Objekts zurück
        """
        return float(np.sqrt((self.x * self.x + self.y * self.y)))

    def rotate(self, angle):
        """
        Dreht den Vektor um einen gegebenen Winkel im Bogenmaß
        """
        angle_radians = math.radians(angle)
        new_x = self.x * math.cos(angle_radians) - self.y * math.sin(angle_radians)
        new_y = self.x * math.sin(angle_radians) + self.y * math.cos(angle_radians)
        return Vector(new_x, new_y)

    def int_tuple(self):
        """
        Gibt die Vektor-Komponenten als Ganzzahlen zurück
        """
        return (int(self.x), int(self.y))

    def dot(self, other):
        """
        Berechnet das Skalarprodukt von zwei Vektoren
        """
        return self.x * other.x + self.y * other.y

    def normalize(self):
        """
        Normalisiert den Vektor
        """
        length = self.abs()
        if length != 0:
            self.x /= length
            self.y /= length
        else:
            return Vector(0,0)
        return Vector(self.x, self.y)
     
class Bat:
    
    def __init__(self, screen, color, points, angle=0, direction=1, count=0, active=1, right=False, anschlag = 50):
        '''
        Constructor for the Bat class. 
        
        Parameters:
            points (list of Vector): The corner points of the bat.
            direction (int): The rotation direction of the bat.
            count (int): The number of flips the bat has made.
            active (int): Whether the bat is moving or not.
            right (bool): For right swinging bats.
            points_vec: Only for calculation
            points_tuple: Only for drawing
        '''
        # Initialize instance variables
        self.screen = screen
        self.color = color
        self.points_vec = points
        self.points_tuple = [_.int_tuple() for _ in points]  # Convert vectors to tuples for drawing
        self.width = points[1] - points[0]
        self.height = points[3] - points[0]
        self.center = (self.points_vec[0] - self.points_vec[2]) / 2 + self.points_vec[2]  # Compute the center of the bat
        self.angle = angle
        self.direction = direction
        self.count = count
        self.active = active
        self.anschlag = anschlag
        
        # Determine rotation direction
        if right:
            self.right = -1
        else:
            self.right = 1

    def update(self):
        '''
        Update method to redraw the bat on the screen after rotation.
        '''
        pygame.draw.polygon(self.screen, self.color, self.flip())

    def flip(self):
        '''
        Method to rotate the bat and return the rotated points.

        Returns:
            rotated_points_tuple (list of tuples): Rotated corner points of the bat.
        '''

        # Change rotation direction at specific angles
        if self.angle == -self.anschlag * self.right or self.angle == 20 * self.right:
            self.direction *= -1
            if self.angle == 20 * self.right:
                self.count += 1

        # Update the rotation angle
        self.angle -= 1 * self.direction * self.active

        # Rotate the corner points of the bat
        rotated_points_vec = []
        rotated_points_tuple = []

        pivot_point = self.points_vec[0]
        for point in self.points_vec:
            point = point - pivot_point 
            point = point.rotate(self.angle) + pivot_point
            rotated_points_tuple.append(point.int_tuple())
            rotated_points_vec.append(point)
  
        # Update activity based on count
        if self.count >= 1:
            self.active = 0
        else:
            self.active = 1
        
        # Update instance variables
        self.points_tuple = rotated_points_tuple
        self.center = (Vector(self.points_tuple[0][0], self.points_tuple[0][1]) - Vector(self.points_tuple[2][0], self.points_tuple[2][1]))/2 + Vector(self.points_tuple[2][0], self.points_tuple[2][1])
        
        return rotated_points_tuple

class Ball:

    def __init__(self, sc, position: Vector, velocity: Vector, radius: float, grav=Vector(0.0,0.1)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.grav = grav
        self.screen = sc

    def check_screen_collide(self, borders: Vector, damp=0.8,roll=0.995):
        if self.position.y > borders.y - self.radius:
            self.position.y = borders.y - self.radius + 1
            self.velocity.y = self.velocity.y * damp * (-1)
            self.velocity.x = self.velocity.x * roll         # Rollwiderstand
        if self.position.y < self.radius:
            self.position.y += 1
            self.velocity.y = self.velocity.y * damp * (-1)
        if self.position.x > (borders.x - self.radius):
            self.position.x -= 1
            self.velocity.x = self.velocity.x * damp * (-1)
        if self.position.x < self.radius:
            self.position.x += 1
            self.velocity.x = self.velocity.x * damp * (-1)
            

    def check_collision(self, other: object):

        connecting_vec = other.position - self.position
        distance = connecting_vec.abs()
        if distance == 0: distance = 1
        isbigball = False

        if distance <= max(self.radius, other.radius):
            

            if other.radius >= 11: # ie is big ball
                isbigball = True

            self_v_davor = self.velocity
            other_v_davor = other.velocity 
            #Versatz
            self.position = self.position - connecting_vec.normalize()      # Klasse Vector versteht nur + und * deswegen diese komische Schreibweise hier. 
            if not isbigball:
                other.position = other.position + connecting_vec.normalize()     # verschiebt die Bälle nach dem Stoß um 1 Pixel weg voneinander
                other.velocity = self_v_davor * 0.8
                self.velocity = other_v_davor * 0.8

            if isbigball:
                sound = pygame.mixer.Sound("sound.wav")
                pygame.mixer.Sound.play(sound)
                self.velocity = self.velocity * (-1.1)
                if self.velocity.abs() >= 7:
                    return True            

    def gravitate(self,DT=0.7):

        self.velocity = self.velocity + self.grav*DT * 0.5
        self.position = self.position + self.velocity*DT + self.grav*DT**2*0.5  
    
    def is_object_collision(self, i):
        return i.is_collision(self)[0]
    
    def collides_with(self, p_of_obj):

        vec_of_points = []
        for vec in p_of_obj:
            thing = Vector(vec[0],vec[1])
            vec_of_points.append(thing)

        return vec_of_points
    
    def sat_algo(self, points, other):

        vec_points = [Vector(point[0], point[1]) for point in points]

        # SAT Beginn
        vertices = []
        for index in range(len(vec_points)):
            vertice = vec_points[index-1] - vec_points[index]
            vertices.append(vertice)
        normals = []
        overlaps = []
        for vertice in vertices:
            normal = vertice.rotate(90 * other.right).normalize()
            normals.append(normal)

            obj_projections = [p.dot(normal) for p in vec_points]
            ball_projections = [self.position.dot(normal) + 2*self.radius, self.position.dot(normal) - 2*self.radius]

            min_rect = min(obj_projections)
            max_rect = max(obj_projections)
            min_ball = min(ball_projections)  # 20 ist ball radius
            max_ball = max(ball_projections)

            overlap =  min(max_rect, max_ball) - max(min_rect, min_ball)
            overlaps.append(overlap)

            if max_ball < min_rect or min_ball > max_rect:
                # Es gibt eine separierende Achse!
                return False, 0

        # Wenn keine separierende Achse gefunden wurde, gibt es eine Kollision
        min_overlap = np.argmin(overlaps)
        self.collide(normals[min_overlap], other)
    
    def collide(self, n, other):
        '''
        Lets the ball reflect from massive obj
        Input: normal n
        '''
        boost = other.active * 1
        t = n.rotate(-90 * other.right)
        old_velo = self.velocity
        new_velo = n * old_velo.dot(n) * (-1) + t * old_velo.dot(t)
        self.position += new_velo.normalize() * 10
        self.velocity = new_velo * old_velo.abs() * (1+boost)

    def reset(self):
        self.position = Vector(20, 660)
        self.velocity = Vector(0,0)


class Rect:
    def __init__(self, position : Vector, width : float, height: float):
        """
        Initialisiert ein Rechteck mit einer Position, Breite und Höhe.

        Args:
            position (Vector): Die Position des Rechtecks als Vektor.
            width (float or int): Die Breite des Rechtecks.
            height (float or int): Die Höhe des Rechtecks.
        """
        self.position = position  # Die Position des Rechtecks
        self.width = width  # Die Breite des Rechtecks
        self.height = height  # Die Höhe des Rechtecks
        fps_multiplyer = 1

    def calculate_vertices(self):
        """
        Berechnet die Eckpunkte des Rechtecks.

        Returns:
            Eine Liste von Vektoren, die die Eckpunkte des Rechtecks darstellen.
        """
        return [
            Vector(self.position.x, self.position.y),
            Vector(self.position.x + self.width, self.position.y),
            Vector(self.position.x + self.width, self.position.y + self.height),
            Vector(self.position.x, self.position.y + self.height)
        ]

    def is_collision(self, ball):
        rect_vertices = self.calculate_vertices()
        
        # Erstelle ein Rechteck um den Ball
        ball_rect = Rect(Vector(ball.position.x - ball.radius, ball.position.y - ball.radius),
                         ball.radius * 2, ball.radius * 2)

        normals = []
        overlaps = []
        for i in range(len(rect_vertices)):
            edge = rect_vertices[(i + 1) % len(rect_vertices)] - rect_vertices[i]
            normal = Vector(-edge.y,edge.x).normalize()
            normals.append(normal)

            # Berechne Projektionen für das Rechteck und das Ball-Rechteck
            rect_projections = [p.dot(normal) for p in rect_vertices]
            ball_rect_projections = [p.dot(normal) for p in ball_rect.calculate_vertices()]

            min_rect = min(rect_projections)
            max_rect = max(rect_projections)
            min_ball_rect = min(ball_rect_projections * 2)
            max_ball_rect = max(ball_rect_projections * 2)

            overlap =  min(max_rect, max_ball_rect) - max(min_rect, min_ball_rect)
            overlaps.append(overlap)

            # Überprüfe die Kollision zwischen dem Ball-Rechteck und dem Rechteck
            if max_ball_rect < min_rect or min_ball_rect > max_rect:
                # Es gibt eine separierende Achse!
                return False, 0

        # Wenn keine separierende Achse gefunden wurde, gibt es eine Kollision
        min_overlap = (np.argmin(overlaps), np.min(overlaps))
        return True, normals[min_overlap[0]]

class Triangle:
    def __init__(self, point1, point2, point3):
        """
        Initialisiert ein Dreieck mit drei Punkten.

        Args:
            point1 (Vector): Der erste Punkt des Dreiecks als Vektor.
            point2 (Vector): Der zweite Punkt des Dreiecks als Vektor.
            point3 (Vector): Der dritte Punkt des Dreiecks als Vektor.
        """
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def calculate_vertices(self):
        """
        Berechnet die Eckpunkte des Dreiecks.

        Returns:
            Eine Liste von Vektoren, die die Eckpunkte des Dreiecks darstellen.
        """
        return [self.point1, self.point2, self.point3]

    def is_collision(self, ball):
        tri_vertices = self.calculate_vertices()

        # Erstelle ein Rechteck um den Ball
        ball_rect = Rect(Vector(ball.position.x - ball.radius, ball.position.y - ball.radius),
                         ball.radius * 2, ball.radius * 2)

        normals = []
        overlaps = []
        for i in range(len(tri_vertices)):
            edge = tri_vertices[(i + 1) % len(tri_vertices)] - tri_vertices[i]
            normal = Vector(-edge.y, edge.x).normalize()
            normals.append(normal)

            # Berechne Projektionen für das Dreieck und das Ball-Rechteck
            tri_projections = [p.dot(normal) for p in tri_vertices]
            ball_rect_projections = [p.dot(normal) for p in ball_rect.calculate_vertices()]

            min_tri = min(tri_projections)
            max_tri = max(tri_projections)
            min_ball_rect = min(ball_rect_projections)
            max_ball_rect = max(ball_rect_projections)

            overlap = min(max_tri, max_ball_rect) - max(min_tri, min_ball_rect)
            overlaps.append(overlap)

            # Überprüfe die Kollision zwischen dem Ball-Rechteck und dem Dreieck
            if max_ball_rect < min_tri or min_ball_rect > max_tri:
                # Es gibt eine separierende Achse!
                return False, 0

        # Wenn keine separierende Achse gefunden wurde, gibt es eine Kollision
        min_overlap = (np.argmin(overlaps), np.min(overlaps))
        return True, normals[min_overlap[0]]
    
    
    def draw_triangle(self, screen):
        triangle_vertices = self.calculate_vertices()
        pygame.draw.polygon(screen, (255, 0, 0), [(v.x, v.y) for v in triangle_vertices],5)
