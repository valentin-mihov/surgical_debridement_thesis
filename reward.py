import pandas as pd

class Reward():
    
    def __init__(self, pyrep, time_dependant=False, time_penalty=0.05):
        """
        Given the PyRep instance of the current
        scene, return the reward for each timestep.
        The reward function can be configured
        to be time-dependant. This will apply
        a small penalty at each timestep.

        """
        # Save the initialisation parameters
        self.time_dependant = time_dependant
        self.time_penalty = time_penalty
        
        # Generate helper data structure
        self.objects = pyrep.get_objects_in_tree()
        self.objects_df = self.get_objects_df(self.objects)

        # Initialise required object variables
        self.set_targets()
        self.set_distractors()
        self.set_table_objects()
        self.set_goal_area()
        self.set_gripper_collidable_parts()
        
        
    def get_objects_df(self, objects):
        """
        Given an obujects list, generate a helper 
        table with object properties.
        """
        objects_df = pd.DataFrame(objects, columns = ['objects'])
        objects_df['name'] = objects_df['objects'].apply(lambda x: x.get_name())
        objects_df['type'] = objects_df['objects'].apply(lambda x: str(x.get_type()).split('.')[1])
        objects_df['is_collidable'] = objects_df['objects'].apply(lambda x: x.is_collidable())
        return objects_df
    
    def set_targets(self):
        """
        Initialisation of target objects list. The
        list is updated by removing a target object 
        once it is moved to the finish line.
        """
        target_names = ['pick_and_lift_target_cube', 'pick_and_lift_target_disk', 'pick_and_lift_target_cuboid']
        self.targets = list(self.objects_df[self.objects_df['name'].isin(target_names)]['objects'])
        
    def set_distractors(self):
        """
        Initialisation of distractor objects list.
        """
        object_names = ['disc_base','distractor1', 'distractor2', 'distractor3', 'distractor4', 'distractor5', 'distractor6']
        self.distractors = list(self.objects_df[self.objects_df['name'].isin(object_names)]['objects'])
        
    def set_table_objects(self):
        """
        Initialisation of table object list.
        """
        object_names = ['workspace', 'diningTable_visible']
        self.table_objects = list(self.objects_df[self.objects_df['name'].isin(object_names)]['objects'])
        
    def set_goal_area(self):
        """
        Initialisation of Goal Area proximity sensor.
        """
        self.goal_area = list(self.objects_df[self.objects_df['name']=='pick_and_lift_success']['objects'])[0]
    
    def set_gripper_collidable_parts(self):
        """
        Initialisation of gripper and gripper children
        collidable objects, which to use for checking 
        collissions with other objects of the enrivonment.        
        """
        parts_names = ['Panda_gripper_visual', 'Panda_rightfinger_visual', 'Panda_leftfinger_visible']
        self.gripper_collidable_parts = list(self.objects_df[self.objects_df['name'].isin(parts_names)]['objects'])
    
    
    def check_table_collission(self):
        """
        Check whether a collission between the
        table and the gripper ocurrs.        
        """
        for obj in self.table_objects:
            for part in self.gripper_collidable_parts:
                if obj.check_collision(part):
                    return True
        return False
        
    def check_distractor_collission(self):
        """
        Check whether a collission between a
        distractor and the gripper ocurrs.
        """
        for obj in self.distractors:
            for part in self.gripper_collidable_parts:
                if obj.check_collision(part):
                    return True
        return False
    
    def check_goal(self):
        """
        Check whether a target object has reached the goal.
        """
        for target in self.targets:
            if self.goal_area.is_detected(target):
                return True
        return False
    
    def update_goal(self):
        """
        Update the target list by removing all
        targets within the goal area.
        """
        for target in self.targets:
            if self.goal_area.is_detected(target):
                self.targets.remove(target)
    
    def check_finished(self):
        """
        Check whether all targets have been moved
        to the goal area.
        """
        if len(self.targets)==0:
            return True
        else:
            return False
    
    def return_reward(self):
        """
        Function which computes the reward at
        each timestep.
        """
        # Initialise reward
        reward = 0
        
        # Check whether target is at goal
        if self.check_goal():
            reward+=100
            self.update_goal()
        else:
            # Apply time penalty if enabled
            if self.time_dependant:
                reward-=self.time_penalty
        
        # Check whether gripper collides with table
        if self.check_table_collission():
            reward-=20
        
        # Check whether gripper collides with distractor
        if self.check_distractor_collission():
            reward-=5
        
        # Check whether agent has moved all targets to goal
        if self.check_finished():
            reward+=500
        
        return reward