import pygame
import math

#ekran boyutları
screen_width = 700
screen_height = 700

#renkler
black = (0,0,0)
white = (255, 255, 255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#noktalar ve konumları
robot_radius = 15
robot_pose = [50,50]

goal_point_radius = 15
goal_point_pose = [600,600]

obstacle_point_radius = 15
obstacle_point_pose = [(150,160),(550,550),(350,500)]

# 1. dikdörtgen engel
obstacle_rect = pygame.Rect(200, 300, 50, 50)
obstacle_points = [(x, y) for x in range(obstacle_rect.left, obstacle_rect.right) 
                        for y in range(obstacle_rect.top, obstacle_rect.bottom)]
obstacle_point_pose.extend(obstacle_points)

# 2. dikdörtgen engel
obstacle_rect2 = pygame.Rect(450, 300, 50, 70)
obstacle_points2 = [(x, y) for x in range(obstacle_rect2.left, obstacle_rect2.right) 
                        for y in range(obstacle_rect2.top, obstacle_rect2.bottom)]
obstacle_point_pose.extend(obstacle_points2)

#çerçeve
frame_rect = pygame.Rect(20, 20, (screen_width-50), (screen_height-50))
frame_thickness = 5    

#sabitler
k_att = -0.07
k_rep = -300
min_distance_obstacle = 100
min_distance_ = 40

pygame.init()

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Yapay Potansiyel Alan")

clock = pygame.time.Clock()


while True:
    # çıkış yapmak isteyip istemediğinin kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            

    #hedefe doğru olan potansiyel alanın hesaplanması
    def attractive_force(): 
        distance_to_goal = math.sqrt((robot_pose[0]-goal_point_pose[0])**2 + (robot_pose[1]-goal_point_pose[1])**2 )
        if distance_to_goal <= min_distance_:
            #att_force = [0,0]
            att_force = [k_att*(robot_pose[0]-goal_point_pose[0]), k_att*(robot_pose[1]-goal_point_pose[1])]
        else:
            att_force = [min_distance_*k_att*(robot_pose[0]-goal_point_pose[0])/distance_to_goal,min_distance_*k_att*(robot_pose[1]-goal_point_pose[1])/distance_to_goal] 
        return att_force
             
    #engelden itici kuvvet
    def repulsive_force():
        rep_force = [0,0]
        for obstacle in obstacle_point_pose:
            distance_to_obstacle = math.sqrt((robot_pose[0]-obstacle[0])**2 + (robot_pose[1]-obstacle[1])**2)
            if distance_to_obstacle < min_distance_obstacle:
                grad = [(robot_pose[0] - obstacle[0]) / distance_to_obstacle, (robot_pose[1] - obstacle[1]) / distance_to_obstacle]
                rep_force[0] += k_rep * ((1 /min_distance_obstacle) - (1 / distance_to_obstacle)) * (grad[0])
                rep_force[1] += k_rep * ((1 / min_distance_obstacle) - (1 / distance_to_obstacle)) * (grad[1])
        return rep_force


    #robotumun hareketi
    def move_robot():
        att_force = attractive_force()
        rep_force = repulsive_force()
        robot_pose[0] += att_force[0] + rep_force[0]
        robot_pose[1] += att_force[1] + rep_force[1]

   

    screen.fill(white)
    
    # çerçeve çizimi
    pygame.draw.rect(screen, black, frame_rect, frame_thickness)

    #noktalarımın çizimi
    pygame.draw.circle(screen, blue, goal_point_pose, goal_point_radius)
    pygame.draw.circle(screen, green, (int(robot_pose[0]),int(robot_pose[1])), robot_radius)
    for obstacle in obstacle_point_pose:
        pygame.draw.circle(screen, red, obstacle, obstacle_point_radius)
    
    

    move_robot()

    # Çizimleri yavaşlatmak için beklenmesi
    clock.tick(60)
    # Ekranın güncellenmesi
    pygame.display.update()


pygame.quit()
