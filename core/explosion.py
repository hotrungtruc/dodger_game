import pygame
import random
import math

class Explosion:
    """Represents an explosion with multiple distinct styles."""

    def __init__(self, position, sound_effect=None):
        """Initialize the explosion with random style."""
        self.position = position
        self.particles = []
        self.finished = False
        self.sound_effect = sound_effect
        self.style = random.choice(["starburst", "shockwave", "fireworks", "smoke"])
        self.create_effect()
        self.play_sound()

    def create_effect(self):
        """Create effect based on the explosion style."""
        if self.style == "starburst":
            for _ in range(12):  # Create 12 rays
                angle = random.uniform(0, 2 * math.pi)
                self.particles.append({"angle": angle, "length": 0, "speed": random.uniform(2, 5), "max_length": random.randint(30, 60), "color": (255, 255, 0)})

        elif self.style == "shockwave":
            self.radius = 0
            self.max_radius = 60  # Shorter radius for quicker effect
            self.line_width = 3

        elif self.style == "fireworks":
            for _ in range(30):  # Create colorful particles
                direction = [random.uniform(-2, 2), random.uniform(-2, 2)]
                speed = random.uniform(3, 6)
                color = (255, 0, 0)  # Start with red
                self.particles.append({"pos": list(self.position), "dir": direction, "speed": speed, "color": color, "time": random.randint(15, 30)})

        elif self.style == "smoke":
            for _ in range(15):  # Create smoky particles
                direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                speed = random.uniform(0.5, 1.5)
                size = random.randint(10, 20)
                self.particles.append({"pos": list(self.position), "dir": direction, "speed": speed, "size": size, "alpha": 255})

    def play_sound(self):
        """Play the explosion sound effect."""
        if self.sound_effect:
            self.sound_effect.play()

    def draw(self, surface):
        """Update and draw the explosion based on its style."""
        if self.style == "starburst":
            for particle in self.particles[:]:
                particle["length"] += particle["speed"]
                if particle["length"] > particle["max_length"]:
                    self.particles.remove(particle)
                else:
                    end_x = self.position[0] + math.cos(particle["angle"]) * particle["length"]
                    end_y = self.position[1] + math.sin(particle["angle"]) * particle["length"]
                    pygame.draw.line(surface, particle["color"], self.position, (end_x, end_y), 2)

        elif self.style == "shockwave":
            self.radius += 3
            if self.radius > self.max_radius:
                self.finished = True
            else:
                pygame.draw.circle(surface, (255, 255, 255), self.position, self.radius, self.line_width)

        elif self.style == "fireworks":
            for particle in self.particles[:]:
                particle["pos"][0] += particle["dir"][0] * particle["speed"]
                particle["pos"][1] += particle["dir"][1] * particle["speed"]
                particle["time"] -= 1

                # Change color as the particle fades
                if particle["time"] > 15:
                    particle["color"] = (255, 165, 0)  # Orange
                elif particle["time"] > 5:
                    particle["color"] = (255, 255, 0)  # Yellow

                pygame.draw.circle(surface, particle["color"], (int(particle["pos"][0]), int(particle["pos"][1])), 3)

                if particle["time"] <= 0:
                    self.particles.remove(particle)

        elif self.style == "smoke":
            for particle in self.particles[:]:
                particle["pos"][0] += particle["dir"][0] * particle["speed"]
                particle["pos"][1] += particle["dir"][1] * particle["speed"]
                particle["alpha"] -= 15  # Faster fade-out
                if particle["alpha"] <= 0:
                    self.particles.remove(particle)
                else:
                    smoke_surface = pygame.Surface((particle["size"], particle["size"]), pygame.SRCALPHA)
                    pygame.draw.circle(smoke_surface, (128, 128, 128, particle["alpha"]), (particle["size"] // 2, particle["size"] // 2), particle["size"] // 2)
                    surface.blit(smoke_surface, (int(particle["pos"][0] - particle["size"] // 2), int(particle["pos"][1] - particle["size"] // 2)))

        if not self.particles and self.style != "shockwave":
            self.finished = True
