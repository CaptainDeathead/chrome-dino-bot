import neat
import os
import pickle
import pyautogui as pag
import pygame as pg

from time import sleep, time

from cactus import CactiManager

class AI:
    def __init__(self, cacti_manager: CactiManager, dino_rect: pg.Rect) -> None:
        self.cacti_manager = cacti_manager
        self.dino_rect = dino_rect

        print("Running in...")
        for i in range(5, -1, -1):
            print(i)
            sleep(1)

        self.run()

    def eval_genomes(self, genomes, config):
        nets = []

        i = 1
        best_genome = None
        for genome_id, genome in genomes:
            print(f"Genome {i} / 100 playing...")
            start_time = time()

            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)

            self.cacti_manager.dino.jump()

            while 1:
                if self.cacti_manager.game_over:
                    self.cacti_manager.reset()
                    self.cacti_manager.bot_playing = False
                    self.cacti_manager.dino.jump()
                    break

                screenshot = pag.screenshot(None, region=self.dino_rect)
                self.cacti_manager.grab_and_update(screenshot)

                action = self.choose_action(net, self.cacti_manager.cacti, self.cacti_manager.dino_speed)
                if action == 1:
                    genome.fitness -= 0.05
                    self.cacti_manager.dino.jump()

            genome.fitness += time() - start_time

            if best_genome == None or genome.fitness > best_genome.fitness:
                best_genome = genome

            print(f"Genome scored: {genome.fitness}")
            i += 1

        with open("ai.pickle", "wb") as f:
            pickle.dump(best_genome, f)

    def choose_action(self, net: any, cacti: list, dino_speed: int) -> int:
        cacti_len = len(cacti)

        obstical_1 = 0
        obstical_2 = 0
        obstical_3 = 0
        
        obstical_types = [0, 0, 0]

        if cacti_len > 0: obstical_1 = cacti[0].rect.x
        if cacti_len > 1: obstical_2 = cacti[1].rect.x
        if cacti_len > 2: obstical_3 = cacti[2].rect.x

        for i, cactus in enumerate(cacti[:3]):
            if cactus.rect.y < self.cacti_manager.TOP_BIRD_HEAD_Y:
                #print(cactus.rect.x)
                obstical_types[i] = 1
                #break

        output = net.activate((dino_speed, obstical_1, obstical_types[0], obstical_2, obstical_types[1], obstical_3, obstical_types[2]))

        #print(output)

        if output[0] > 0.5: return 1 # jump
        else: return 0

    def run(self) -> None:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config.txt")

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)

        p = neat.Population(config)
        #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-17')

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        p.add_reporter(neat.Checkpointer(generation_interval=5))

        winner = p.run(self.eval_genomes, 50)