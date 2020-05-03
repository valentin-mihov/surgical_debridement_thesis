from typing import List
from pyrep.objects.shape import Shape
from pyrep.objects.proximity_sensor import ProximitySensor
from rlbench.backend.task import Task
from rlbench.backend.conditions import DetectedCondition, ConditionSet, \
    GraspedCondition
from rlbench.backend.spawn_boundary import SpawnBoundary
from rlbench.const import colors


class MyPickAndLift(Task):

    def init_task(self) -> None:
        self.target_blocks = [Shape('pick_and_lift_target_cube'), Shape('pick_and_lift_target_cuboid'),
                              Shape('pick_and_lift_target_disk')]

        self.distractors = [
            Shape('distractor%d' % i)
            for i in range(7)]
        self.register_graspable_objects(self.target_blocks)
        self.spawn_boundary = SpawnBoundary([Shape('pick_and_lift_boundary')])
        self.success_detector = ProximitySensor('pick_and_lift_success')

        cond_set = ConditionSet([
            DetectedCondition(self.target_blocks[0], self.success_detector),
            DetectedCondition(self.target_blocks[1], self.success_detector),
            DetectedCondition(self.target_blocks[2], self.success_detector)
        ])
        self.register_success_conditions([cond_set])

    def init_episode(self, index: int) -> List[str]:
        self.spawn_boundary.clear()
        for block in self.target_blocks + self.distractors:
            self.spawn_boundary.sample(block, min_distance=0.1)


        return ['pick up the %s block and lift it up to the target' % 'red',
                'grasp the %s block to the target' % 'red',
                'lift the %s block up to the target' % 'red']

    def variation_count(self) -> int:
        return len(colors)

    def is_static_workspace(self) -> bool:
        return True
