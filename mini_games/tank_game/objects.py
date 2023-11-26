import pygame
import pymunk
from pygame.math import Vector2 as Vec2d

class Projectile():
    def __init__(self,owner):
        self.dir = owner.dir#-owner.img_angle
        self.pos = owner.pos+owner.cannon_offset.rotate(owner.img_angle-self.dir+180)
        self.vel = Vec2d(owner.projectile_velocity,0).rotate(owner.img_angle-self.dir+180)
        self.surface = owner.projectile_texture
        self.owner = owner

        self.collision_type = 6
        self.size = Vec2d(15,8)
        self.mass = 10

        self.body = pymunk.Body()
        self.body.angle = -self.dir*0.017
        self.body.position = self.pos[0],self.pos[1]
        self.body.owner = self
        self.shape = pymunk.Poly.create_box(self.body,self.size,0)
        self.shape.collision_type = self.collision_type
        self.shape.mass = self.mass
        self.shape.owner = self
        self.owner.Game.space.add(self.body,self.shape)

    def update(self):
        self.pos = self.body.position + self.vel
        self.body.position = self.pos[0],self.pos[1]

    def on_hit(self,arbiter,space,data):            
        for shape in arbiter.shapes:
            if not shape.body is self.owner.body:
                print("Hit my own tank.")
                self.remove()
                #return False
        print("Target hit!")
        return True

    def blitRotate(self,display):
        rotated_image = pygame.transform.rotate(self.surface, self.dir)
        rotated_image_rect = rotated_image.get_rect(center = self.pos)
        display.blit(rotated_image, rotated_image_rect)
        # draw rectangle around the image
        #pygame.draw.rect(display, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)


class MapObject:
    def __init__(self,obj_data,Game):
        self.Game = Game
        self.texture  = obj_data["texture"]
        self.pos      = Vec2d(obj_data["position"])
        self.dir      = obj_data["direction"]
        self.mass     = obj_data["mass"]
        self.color    = obj_data["color"]
        self.anchored = obj_data["anchored"]
        self.collision_type = obj_data["collision_type"]
        if self.texture in self.Game.TexturePacks: #Texture pack detected
            self.texture_set = self.Game.TexturePacks[self.texture]
            self.surface = self.texture_set[0]
        else:
            self.surface  = self.Game.textures[self.texture]

        if self.anchored:return #Don't proceed further if static object

        #Physics Stuff
        shape =  obj_data["shape"]
        m_shape = shape["shape"]
        if m_shape == "rectangle":
            print(shape)
            size,friction = shape["size"],shape["friction"]
            self.body = pymunk.Body()
            self.Game.space.add(self.body)
            _shape = pymunk.Poly.create_box(self.body, size, 0.0)
            _shape.mass = self.mass
            _shape.friction = friction
            self.Game.space.add(_shape)
            self.body.position = self.pos[0],self.pos[1]
            _shape.collision_type = self.collision_type
        elif m_shape == "circle":
            print("Player #{}".format(obj_data["ID"]))
            radius = shape["radius"]
            inertia = pymunk.moment_for_circle(self.mass, 0, radius, (0, 0))
            self.body = pymunk.Body(self.mass,inertia)
            self.body.position = self.pos[0],self.pos[1]
            _shape = pymunk.Circle(self.body,radius,(.0,.0))
            _shape.collision_type = self.collision_type
            self.Game.space.add(self.body,_shape)
        self.body.owner = self
        _shape.owner = self
        constraints = obj_data["constraints"]
        for c in constraints:
            TYPE = c["type"]
            if TYPE == "PivotJoint":
                pivot = pymunk.PivotJoint(self.Game.space.static_body, self.body, (0, 0), (0, 0))
                self.Game.space.add(pivot)
                pivot.max_bias = 0  # disable joint correction
                pivot.max_force = 1000  # emulate linear friction
            elif TYPE == "GearJoint":
                gear = pymunk.GearJoint(self.Game.space.static_body, self.body, 0.0, 1.0)
                self.Game.space.add(gear)
                gear.max_bias = 0  # disable joint correction
                gear.max_force = 5000  # emulate angular friction
    def hit(self):
        return False
    def blitRotate(self,display):
        #rect_vec2d = Vec2d(self.surface.get_size())/2
        rotated_image = pygame.transform.rotate(self.surface, self.dir)
        rotated_image_rect = rotated_image.get_rect(center = self.pos)
        display.blit(rotated_image, rotated_image_rect)
        # draw rectangle around the image
        #pygame.draw.rect(display, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)
    def render(self,display):
        self.blitRotate(display)
        #display.blit(self.render_surface,self.pos)


class Player(MapObject):
    def __init__(self,obj_data,Game):
        super().__init__(obj_data,Game)
        self.ID = obj_data["ID"]
        self.spawn_pos = self.pos
        self.kill_counter  = 0
        self.death_counter = 0
        self.is_alive = True
        self.img_angle = -90
        self.vel = 2
        self.dir_vel = 4
        self.pressed = False
        self.surface = self.Game.TexturePacks["Tanks"][self.ID]
        self.death_texture = self.Game.TexturePacks["Tanks"][8]
        self.projectile_texture = self.Game.TexturePacks["Projectiles"][self.ID]
        self.projectiles = []
        self.projectile_velocity = 8
        self.cannon_offset = Vec2d(17,0)

    def render(self,display):
        self.blitRotate(display)
        for p in self.projectiles:
            p.blitRotate(display)
    def run_update(self,inputs):
        #self.body.activate()
        #print(self.body.is_sleeping,self.ID)
        u,d,l,r,mono = inputs[(self.ID-1)*5:self.ID*5] #Extract this player's input
        if mono:
            if not self.pressed:
                self.fire_projectile()
                self.pressed = True
            rotated_velocity = Vec2d(self.vel,0).rotate(-self.img_angle-self.dir)
            self.pos = self.body.position + rotated_velocity
        else:
            if self.pressed:
                self.dir_vel*=-1
                self.pressed = False
                
            self.dir = (self.dir+self.dir_vel)%360
        self.body.position = self.pos[0],self.pos[1]

    def update(self,inputs):
        self.update_projectiles()
        if self.is_alive:
            self.run_update(inputs)
        else:
            self.pos = self.body.position
            pass #Death code
    def hit(self):
        self.kill()
        return True
    def kill(self):
        self.death_counter+=1
        print(self.death_counter)
        if self.Game.GameMode == 1:
            self.surface = self.death_texture
            self.is_alive = False
    def spawn(self):
        self.pos = self.spawn_pos
        self.dir = 0

    def update_projectiles(self):
        for p in self.projectiles:
            p.update()

    def remove_projectile(self,p):
        if p in self.projectiles:
            self.projectiles.remove(p)
            self.Game.space.remove(p.body,p.shape)
            del(p)

    def fire_projectile(self):
        self.projectiles.append(Projectile(self))



class DynamicObject(MapObject):
    def __init__(self,obj_data,Game):
        super().__init__(obj_data,Game)
        self.body.angle = self.dir*(1/57.29)

    def update(self):
        self.pos = self.body.position
        self.dir = -self.body.angle*57.29


class StaticObject(MapObject):
    def __init__(self,obj_data,Game):
        super().__init__(obj_data,Game)



        
