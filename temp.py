self.states = {
            # state: [file_name, starting_frame, row, fps, nFrames]
            'idle': Player_State("weaver.png", starting_frame=0, row=0, fps=16, num_frames=48),
            'idle_right': Player_State("weaver.png", 0, 0, 16, 48),
            'idle_left': Player_State("weaver.png", 0, 1, 16, 48),

            'walking_right': Player_State(file_name="weaver_walk.png", starting_frame=0, row=0, fps=walk_fps, num_frames=10),
            'walking_left': Player_State("weaver_walk.png", 0, 0, walk_fps, 10, flip_x=True),

            'running_right': Player_State("weaver_run.png", 0, 0, run_fps, 9, flip_x=False),
            'running_left': Player_State("weaver_run.png", 0, 0, run_fps, 9, flip_x=True),

            'crouching_right': Player_State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, loop_fps = 32, flip_x=False),
            'crouching_left': Player_State("weaver_crouch.png", 0, 0, 32, 11, loop=True, loop_start = 3, loop_end=5, loop_fps = 32, flip_x=True),

            'shooting_right': Player_State("weaver_shot.png", 0, 0, 64, 12, loop = True, loop_start = 3, loop_end = 8, loop_fps= 64, flip_x=False),
            'shooting_left': Player_State("weaver_shot.png", 0, 0, 64, 12, loop=True, loop_start = 3, loop_end = 8, loop_fps = 64, flip_x=True),

            'hovering_right': Player_State("weaver_jump.png", row = 0, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 5, loop_end = 8, loop_fps=12),
            'hovering_left': Player_State("weaver_jump.png", row = 1, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 7, loop_end = 8, loop_fps=12),

            'flying_right': Player_State("weaver_jump.png", row = 2, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 5, loop_end = 8, loop_fps=12),
            'flying_left': Player_State("weaver_jump.png", row = 3, starting_frame = 0, fps = 64, num_frames = 13, loop=True, loop_start = 7, loop_end = 8, loop_fps=12),

            'aerial_shot_right': Player_State("weaver_shot.png", 0, 0, 64, 12, loop = True, loop_start = 3, loop_end = 8, loop_fps= 64, flip_x=False),
            'aerial_shot_left': Player_State("weaver_shot.png", 0, 0, 64, 12, loop=True, loop_start = 3, loop_end = 8, loop_fps = 64, flip_x=True),
        }