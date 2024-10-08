# This script uses player data as input for two functions: shotContact() and side().
# The shotContact() function outputs a list of coordinates and stroke information based on the selected frames.
# The side() function outputs a list of what side of the court the player is on based on the selected frames.
# Generated by: Vivian Yee
# Date [2024-08-20]

import pandas as pd

# read all player data files
top_player_df = pd.read_csv('top_player_data.csv')
bottom_player_df = pd.read_csv('bottom_player_data.csv')
stroke_detection_df = pd.read_csv('strokeprediction.csv')

def shotContact(top_player, bottom_player, stroke_detection):
    # extract x and y coordinates from top player
    top_player_x = top_player.iloc[:, 0]
    top_player_y = top_player.iloc[:, 1]
    # extract x and y coordinates from bottom player
    bottom_player_x = bottom_player.iloc[:, 0]
    bottom_player_y = bottom_player.iloc[:, 1]
    # extract video frames and stroke information 
    video_frame = stroke_detection.iloc[:, 0]
    stroke = stroke_detection.iloc[:, 4]
    
    coord_list = []
    count = 0
    player_indicator = 0 # set player indicator (1 for top player, 0 for bottom player)
    
    for frame in video_frame:
        coord = []
        if player_indicator == 1: 
            # append top player coordinates
            coord.append(top_player_x.iloc[frame - 1])
            coord.append(top_player_y.iloc[frame - 1])
        elif player_indicator == 0:
            # append bottom player coordinates
            coord.append(bottom_player_x.iloc[frame - 1])
            coord.append(bottom_player_y.iloc[frame - 1])
        coord.append(stroke[count]) # append stroke information for current frame
        coord_list.append(coord)
        count += 1
    # return list of coordinates and stoke information
    return coord_list
    
print(shotContact(top_player_df, bottom_player_df, stroke_detection_df))

def side(top_player, bottom_player, stroke_detection):
    # extract x coordinates for top and bottom player
    top_player_x = top_player.iloc[:, 0]
    bottom_player_x = bottom_player.iloc[:, 0]
    # extract the video frames from the stroke detection
    video_frame = stroke_detection.iloc[:, 0]
    # center the x coordinates around the mean to determine positions relative to the center 
    top_player_x_centered = top_player_x - top_player_x.mean()
    bottom_player_x_centered = bottom_player_x - bottom_player_x.mean()
    
    top_player_side = []
    bottom_player_side = []
    player_indicator = 0 # set player indicator to bottom player
    
    for frame in video_frame:
        # determine the side for the top player based on their centered x coordinate
        if player_indicator == 1 and top_player_x_centered.iloc[frame - 1] < 0:
            top_player_side.append('Deuce')
        elif player_indicator == 1 and top_player_x_centered.iloc[frame - 1] > 0:
            top_player_side.append('Ad')
        # determine the side for the bottom player based on their centered x coordinate
        if player_indicator == 0 and bottom_player_x_centered.iloc[frame - 1] < 0:
            bottom_player_side.append('Ad')
        elif player_indicator == 0 and bottom_player_x_centered.iloc[frame - 1] > 0: 
            bottom_player_side.append('Deuce')
    # return lists of sides for both players
    return top_player_side, bottom_player_side
    
top_player_side, bottom_player_side = side(top_player_df, bottom_player_df, stroke_detection_df)

print(top_player_side)
print(bottom_player_side)